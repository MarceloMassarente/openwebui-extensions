"""
title: 📂 文件夹记忆 (Folder Memory)
author: Fu-Jie
author_url: https://github.com/Fu-Jie/openwebui-extensions
funding_url: https://github.com/open-webui
version: 0.1.0
description: 自动从对话中提取项目规则，并将其注入到文件夹的系统提示词中。
requirements:
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, List
from fastapi import Request
import logging
import json
import re
import asyncio
from datetime import datetime

from open_webui.utils.chat import generate_chat_completion
from open_webui.models.users import Users
from open_webui.models.folders import Folders, FolderUpdateForm
from open_webui.models.chats import Chats

# ── OpenWebUI 版本检测（异步 DB 兼容） ──────────
try:
    from open_webui.env import VERSION as _owui_version
except ImportError:
    _owui_version = "0.0.0"


def _owui_version_ge(threshold: str) -> bool:
    try:
        v = [int(x) for x in _owui_version.split(".")[:3]]
        t = [int(x) for x in threshold.split(".")[:3]]
        return v >= t
    except (ValueError, TypeError):
        return False


async def _call_db(method, *args, **kwargs):
    if _owui_version_ge("0.9.0"):
        return await method(*args, **kwargs)
    else:
        return method(*args, **kwargs)


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# 规则注入标记
RULES_BLOCK_START = "<!-- OWUI_PROJECT_RULES_START -->"
RULES_BLOCK_END = "<!-- OWUI_PROJECT_RULES_END -->"

# 规则生成系统提示词
SYSTEM_PROMPT_RULE_GENERATOR = """
你是一个项目规则提取器。你的任务是从对话中提取“项目规则”，并与现有规则合并。

### 输入
1. **现有规则 (Existing Rules)**：当前文件夹系统提示词中的规则。
2. **对话片段 (Conversation)**：最近的聊天记录。

### 目标
综合生成一份适用于当前项目/文件夹的简洁规则列表。
- **移除** 不再相关或仅是一次性指令的规则。
- **添加** 对话中发现的新的、一致性的要求。
- **合并** 相似的规则。
- **格式**：简洁的 Markdown 项目符号列表。

### 输出格式
仅输出 Markdown 项目符号列表形式的规则。不要包含任何开头或结尾的说明文字。
示例：
- 始终使用 Python 3.11 进行类型提示。
- 文档字符串必须遵循 Google 风格。
- 提交信息必须使用英文。
"""


class Filter:
    class Valves(BaseModel):
        PRIORITY: int = Field(default=20, description="过滤器操作的优先级。")
        SHOW_DEBUG_LOG: bool = Field(
            default=False, description="在控制台显示调试日志。"
        )
        MESSAGE_TRIGGER_COUNT: int = Field(
            default=10, description="每隔 N 条消息分析一次规则。"
        )
        MODEL_ID: str = Field(
            default="", description="用于提取规则的模型 ID。为空则使用当前对话模型。"
        )
        RULES_BLOCK_TITLE: str = Field(
            default="## 📂 项目规则", description="显示在规则块上方的标题。"
        )
        UPDATE_ROOT_FOLDER: bool = Field(
            default=False,
            description="如果启用，将向上查找并更新根文件夹的规则，而不是当前子文件夹。",
        )

    def __init__(self):
        self.valves = self.Valves()

    # ==================== 辅助方法 ====================

    def _get_user_context(self, __user__: Optional[dict]) -> Dict[str, str]:
        """安全提取用户上下文信息。"""
        if isinstance(__user__, (list, tuple)):
            user_data = __user__[0] if __user__ else {}
        elif isinstance(__user__, dict):
            user_data = __user__
        else:
            user_data = {}

        return {
            "user_id": user_data.get("id", ""),
            "user_name": user_data.get("name", "User"),
            "user_language": user_data.get("language", "zh-CN"),
        }

    def _get_chat_context(
        self, body: dict, __metadata__: Optional[dict] = None
    ) -> Dict[str, str]:
        """统一提取聊天上下文信息 (chat_id, message_id)。"""
        chat_id = ""
        message_id = ""

        if isinstance(body, dict):
            chat_id = body.get("chat_id", "")
            message_id = body.get("id", "")

            if not chat_id or not message_id:
                body_metadata = body.get("metadata", {})
                if isinstance(body_metadata, dict):
                    if not chat_id:
                        chat_id = body_metadata.get("chat_id", "")
                    if not message_id:
                        message_id = body_metadata.get("message_id", "")

        if __metadata__ and isinstance(__metadata__, dict):
            if not chat_id:
                chat_id = __metadata__.get("chat_id", "")
            if not message_id:
                message_id = __metadata__.get("message_id", "")

        return {
            "chat_id": str(chat_id).strip(),
            "message_id": str(message_id).strip(),
        }

    async def _emit_debug_log(self, __event_emitter__, title: str, data: dict):
        if self.valves.SHOW_DEBUG_LOG and __event_emitter__:
            try:
                # 按照用户要求的格式输出展平的日志
                js_code = f"""
                    console.log("[Folder Memory] {title}", {json.dumps(data, ensure_ascii=False)});
                """
                await __event_emitter__({"type": "execute", "data": {"code": js_code}})
            except Exception as e:
                logger.error(f"发出日志错误: {e}")

    async def _emit_status(
        self, __event_emitter__, description: str, done: bool = False
    ):
        if __event_emitter__:
            await __event_emitter__(
                {"type": "status", "data": {"description": description, "done": done}}
            )

    async def _get_folder_id(self, body: dict) -> Optional[str]:
        # 1. 尝试从 metadata 获取 folder_id
        if "metadata" in body and isinstance(body["metadata"], dict):
            if "folder_id" in body["metadata"]:
                return body["metadata"]["folder_id"]

        # 2. 检查 chat 对象
        if "chat" in body and isinstance(body["chat"], dict):
            if "folder_id" in body["chat"]:
                return body["chat"]["folder_id"]

        # 3. 尝试通过 Chat ID 查找 (最可靠的方法)
        chat_id = body.get("chat_id")
        if not chat_id:
            if "metadata" in body and isinstance(body["metadata"], dict):
                chat_id = body["metadata"].get("chat_id")

        if chat_id:
            try:
                chat = await _call_db(Chats.get_chat_by_id, chat_id)
                if chat and chat.folder_id:
                    return chat.folder_id
            except Exception as e:
                logger.error(f"获取聊天信息失败 chat_id={chat_id}: {e}")

        return None

    def _extract_existing_rules(self, system_prompt: str) -> str:
        pattern = re.compile(
            re.escape(RULES_BLOCK_START) + r"([\s\S]*?)" + re.escape(RULES_BLOCK_END)
        )
        match = pattern.search(system_prompt)
        if match:
            # 如果标题在块内，将其移除以便纯净合并
            content = match.group(1).strip()
            title_pat = re.compile(r"^#+\s+.*$", re.MULTILINE)
            return title_pat.sub("", content).strip()
        return ""

    def _inject_rules(self, system_prompt: str, new_rules: str, title: str) -> str:
        new_block_content = f"\n{title}\n\n{new_rules}\n"
        new_block = f"{RULES_BLOCK_START}{new_block_content}{RULES_BLOCK_END}"

        system_prompt = system_prompt or ""
        pattern = re.compile(
            re.escape(RULES_BLOCK_START) + r"[\s\S]*?" + re.escape(RULES_BLOCK_END)
        )

        if pattern.search(system_prompt):
            # 替换现有块
            return pattern.sub(new_block, system_prompt).strip()
        else:
            # 追加到末尾
            if system_prompt:
                return f"{system_prompt}\n\n{new_block}"
            else:
                return new_block

    async def _generate_new_rules(
        self,
        current_rules: str,
        messages: List[Dict],
        user_id: str,
        __request__: Request,
    ) -> str:
        # 准备上下文
        conversation_text = "\n".join(
            [
                f"{msg['role'].upper()}: {msg['content']}"
                for msg in messages[-20:]  # 分析最近 20 条消息上下文
            ]
        )

        prompt = f"""
Existing Rules (现有规则):
{current_rules if current_rules else "无"}

Conversation Excerpt (对话片段):
{conversation_text}

Please output the updated Project Rules (请输出更新后的项目规则):
"""

        payload = {
            "model": self.valves.MODEL_ID,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT_RULE_GENERATOR},
                {"role": "user", "content": prompt},
            ],
            "stream": False,
        }

        try:
            # 需要用户对象进行权限检查
            user = await _call_db(Users.get_user_by_id, user_id)
            if not user:
                return current_rules

            completion = await generate_chat_completion(__request__, payload, user)
            if "choices" in completion and len(completion["choices"]) > 0:
                content = completion["choices"][0]["message"]["content"].strip()
                # 简单验证：确保看起来像个列表
                if (
                    content.startswith("-")
                    or content.startswith("*")
                    or content.startswith("1.")
                ):
                    return content
        except Exception as e:
            logger.error(f"规则生成失败: {e}")

        return current_rules

    async def _process_rules_update(
        self,
        folder_id: str,
        body: dict,
        user_id: str,
        __request__: Request,
        __event_emitter__,
    ):
        try:
            await self._emit_debug_log(
                __event_emitter__,
                "开始处理",
                {"step": "start", "initial_folder_id": folder_id, "user_id": user_id},
            )

            # 1. 获取文件夹数据 (ORM)
            initial_folder = await _call_db(
                Folders.get_folder_by_id_and_user_id, folder_id, user_id
            )
            if not initial_folder:
                await self._emit_debug_log(
                    __event_emitter__,
                    "错误：未找到初始文件夹",
                    {
                        "step": "fetch_initial_folder",
                        "initial_folder_id": folder_id,
                        "user_id": user_id,
                    },
                )
                return

            # 处理子文件夹逻辑：决定是更新当前文件夹还是根文件夹
            target_folder = initial_folder
            if self.valves.UPDATE_ROOT_FOLDER:
                # 向上遍历直到找到没有 parent_id 的根文件夹
                while target_folder and getattr(target_folder, "parent_id", None):
                    try:
                        parent = await _call_db(
                            Folders.get_folder_by_id_and_user_id,
                            target_folder.parent_id,
                            user_id,
                        )
                        if parent:
                            target_folder = parent
                        else:
                            break
                    except Exception as e:
                        await self._emit_debug_log(
                            __event_emitter__,
                            "警告：向上查找父文件夹失败",
                            {"step": "traverse_root", "error": str(e)},
                        )
                        break

            target_folder_id = target_folder.id

            await self._emit_debug_log(
                __event_emitter__,
                "定目标文件夹",
                {
                    "step": "target_resolved",
                    "target_folder_id": target_folder_id,
                    "target_folder_name": target_folder.name,
                    "is_root_update": target_folder_id != folder_id,
                },
            )

            existing_data = target_folder.data if target_folder.data else {}
            existing_sys_prompt = existing_data.get("system_prompt", "")

            # 2. 提取现有规则
            current_rules_content = self._extract_existing_rules(existing_sys_prompt)

            # 3. 生成新规则
            await self._emit_status(
                __event_emitter__, "正在分析项目规则...", done=False
            )

            messages = body.get("messages", [])
            new_rules_content = await self._generate_new_rules(
                current_rules_content, messages, user_id, __request__
            )

            rules_changed = new_rules_content != current_rules_content

            # 如果生成结果无变更
            if not rules_changed:
                await self._emit_debug_log(
                    __event_emitter__,
                    "无变更",
                    {
                        "step": "check_changes",
                        "reason": "content_identical_or_generation_failed",
                    },
                )
                await self._emit_status(
                    __event_emitter__, "规则分析完成：无新增内容。", done=True
                )
                return

            # 5. 注入规则到 System Prompt
            updated_sys_prompt = existing_sys_prompt
            if rules_changed:
                updated_sys_prompt = self._inject_rules(
                    updated_sys_prompt,
                    new_rules_content,
                    self.valves.RULES_BLOCK_TITLE,
                )

            await self._emit_debug_log(
                __event_emitter__,
                "准备更新数据库",
                {"step": "pre_db_update", "target_folder_id": target_folder_id},
            )

            # 6. 更新文件夹 (ORM) - 仅更新 'data' 字段
            existing_data["system_prompt"] = updated_sys_prompt

            updated_folder = await _call_db(
                Folders.update_folder_by_id_and_user_id,
                target_folder_id,
                user_id,
                FolderUpdateForm(data=existing_data),
            )

            if not updated_folder:
                raise Exception("Update folder failed (ORM returned None)")

            await self._emit_status(
                __event_emitter__, "规则分析完成：规则已更新。", done=True
            )
            await self._emit_debug_log(
                __event_emitter__,
                "规则生成过程和变更详情",
                {
                    "step": "success",
                    "folder_id": target_folder_id,
                    "target_is_root": target_folder_id != folder_id,
                    "model_used": self.valves.MODEL_ID,
                    "analyzed_messages_count": len(messages),
                    "old_rules_length": len(current_rules_content),
                    "new_rules_length": len(new_rules_content),
                    "changes_digest": {
                        "old_rules_preview": (
                            current_rules_content[:100] + "..."
                            if current_rules_content
                            else "None"
                        ),
                        "new_rules_preview": (
                            new_rules_content[:100] + "..."
                            if new_rules_content
                            else "None"
                        ),
                    },
                    "timestamp": datetime.now().isoformat(),
                },
            )

        except Exception as e:
            logger.error(f"异步规则处理错误: {e}")
            await self._emit_status(__event_emitter__, "更新规则失败。", done=True)
            # 在控制台也输出错误信息，方便调试
            await self._emit_debug_log(
                __event_emitter__, "执行出错", {"error": str(e), "folder_id": folder_id}
            )

    # ==================== Filter Hooks ====================

    async def inlet(
        self, body: dict, __user__: Optional[dict] = None, __event_emitter__=None
    ) -> dict:
        return body

    async def outlet(
        self,
        body: dict,
        __user__: Optional[dict] = None,
        __event_emitter__=None,
        __request__: Optional[Request] = None,
    ) -> dict:
        user_ctx = self._get_user_context(__user__)
        chat_ctx = self._get_chat_context(body)

        messages = body.get("messages", [])
        if not messages:
            return body

        # 触发逻辑：消息计数阈值
        if len(messages) % self.valves.MESSAGE_TRIGGER_COUNT != 0:
            return body

        folder_id = await self._get_folder_id(body)
        if not folder_id:
            await self._emit_debug_log(
                __event_emitter__,
                "跳过分析",
                {"reason": "对话不属于任何文件夹", "chat_id": chat_ctx.get("chat_id")},
            )
            return body

        # 用户信息
        user_id = user_ctx.get("user_id")
        if not user_id:
            return body

        # 异步任务
        if self.valves.MODEL_ID == "":
            self.valves.MODEL_ID = body.get("model", "")

        asyncio.create_task(
            self._process_rules_update(
                folder_id, body, user_id, __request__, __event_emitter__
            )
        )

        return body
