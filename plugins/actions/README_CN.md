# Actions（动作插件）

[English](./README.md) | 中文

动作插件（Actions）允许您定义可以从聊天中触发的自定义功能。此目录包含可用于扩展 OpenWebUI 功能的各种动作插件。

## 📋 动作插件列表

| 插件名称     | 描述                                 | 版本  | 文档                                                                          |
| :----------- | :----------------------------------- | :---- | :---------------------------------------------------------------------------- |
| **思维导图** | 智能分析文本内容，生成交互式思维导图 | 1.0.1 | [中文](./smart-mind-map/README_CN.md) / [English](./smart-mind-map/README.md) |

## 🎯 什么是动作插件？

动作插件通常用于：

- 生成特定格式的输出（如思维导图、图表、表格等）
- 与外部 API 或服务交互
- 执行数据转换和处理
- 保存或导出内容到文件
- 创建交互式可视化
- 自动化复杂工作流程

## 🚀 快速开始

### 安装动作插件

1. 将插件文件（`.py`）下载到本地
2. 在 OpenWebUI 管理员设置中，找到"Plugins"部分
3. 选择"Actions"类型
4. 上传下载的文件
5. 刷新页面并在聊天设置中启用插件
6. 在聊天中从可用动作中选择使用该插件

## 📖 开发指南

### 添加新动作插件

添加新动作插件时，请遵循以下步骤：

1. **创建插件目录**：在 `plugins/actions/` 下创建新文件夹（例如 `my_action/`）
2. **编写插件代码**：创建 `.py` 文件，清晰记录功能说明
3. **编写文档**：
   - 创建 `README.md`（英文版）
   - 创建 `README_CN.md`（中文版）
   - 包含：功能说明、配置方法、使用示例和故障排除
4. **更新此列表**：在上述表格中添加您的插件

### Open WebUI 插件开发通用功能

开发 Action 插件时，可以使用以下 Open WebUI 提供的标准功能：

#### 1. **插件元数据定义**

```python
"""
title: 插件名称
icon_url: data:image/svg+xml;base64,...  # 插件图标（Base64编码的SVG）
version: 1.0.0
description: 插件功能描述
"""
```

#### 2. **Valves 配置系统**

使用 Pydantic 定义可配置参数，用户可在 UI 界面动态调整：

```python
from pydantic import BaseModel, Field

class Valves(BaseModel):
    show_status: bool = Field(
        default=True,
        description="是否显示状态更新"
    )
    api_key: str = Field(
        default="",
        description="API密钥"
    )
```

#### 3. **标准 Action 类结构**

```python
class Action:
    def __init__(self):
        self.valves = self.Valves()
    
    async def action(
        self,
        body: dict,
        __user__: Optional[Dict[str, Any]] = None,
        __event_emitter__: Optional[Any] = None,
        __request__: Optional[Request] = None,
    ) -> Optional[dict]:
        # 插件逻辑
        return body
```

#### 4. **获取用户信息**

```python
# 支持字典和列表两种格式
user_language = __user__.get("language", "en-US")
user_name = __user__.get("name", "User")
user_id = __user__.get("id", "unknown_user")
```

#### 5. **事件发射器 (event_emitter)**

**发送通知消息：**

```python
await __event_emitter__({
    "type": "notification",
    "data": {
        "type": "info",      # info/warning/error/success
        "content": "消息内容"
    }
})
```

**发送状态更新：**

```python
await __event_emitter__({
    "type": "status",
    "data": {
        "description": "状态描述",
        "done": False,       # True表示完成
        "hidden": False      # True表示隐藏
    }
})
```

#### 6. **调用内置 LLM**

```python
from open_webui.utils.chat import generate_chat_completion
from open_webui.models.users import Users

# 获取用户对象
user_obj = Users.get_user_by_id(user_id)

# 构建 LLM 请求
llm_payload = {
    "model": "model-id",
    "messages": [
        {"role": "system", "content": "系统提示词"},
        {"role": "user", "content": "用户输入"}
    ],
    "temperature": 0.7,
    "stream": False
}

# 调用 LLM
llm_response = await generate_chat_completion(
    __request__, llm_payload, user_obj
)
```

#### 7. **处理消息体 (body)**

```python
# 读取消息
messages = body.get("messages")
user_message = messages[-1]["content"]

# 修改消息
body["messages"][-1]["content"] = f"{user_message}\n\n新增内容"

# 返回修改后的body
return body
```

#### 8. **嵌入 HTML 内容**

```python
html_content = "<div>交互式内容</div>"
html_embed_tag = f"```html\n{html_content}\n```"
body["messages"][-1]["content"] = f"{text}\n\n{html_embed_tag}"
```

#### 9. **异步处理**

所有插件方法必须是异步的：

```python
async def action(...):
    await __event_emitter__(...)
    result = await some_async_function()
    return result
```

#### 10. **错误处理和日志**

```python
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

try:
    # 插件逻辑
    pass
except Exception as e:
    logger.error(f"错误: {str(e)}", exc_info=True)
    await __event_emitter__({
        "type": "notification",
        "data": {"type": "error", "content": f"操作失败: {str(e)}"}
    })
```

### 开发最佳实践

1. **使用 Valves 配置**：让用户可以自定义插件行为
2. **提供实时反馈**：使用事件发射器告知用户进度
3. **优雅的错误处理**：捕获异常并给出友好提示
4. **支持多语言**：从 `__user__` 获取语言偏好
5. **日志记录**：记录关键操作和错误，便于调试
6. **验证输入**：检查必需参数和数据格式
7. **返回完整的 body**：确保消息流正确传递

---

> **贡献者注意**：为了确保项目质量，请为每个新增插件提供清晰完整的文档，包括功能说明、配置方法、使用示例和故障排除指南。参考上述通用功能开发您的插件。

## 作者

Fu-Jie
GitHub: [Fu-Jie/openwebui-extensions](https://github.com/Fu-Jie/openwebui-extensions)
