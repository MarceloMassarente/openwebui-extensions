# 多模型协作

> 实现参考文档 · GitHub Copilot SDK Pipe

---

## 概述

OpenWebUI 允许用户在同一对话中同时选择多个模型。当 N 个模型同时激活时，OpenWebUI 向 Pipe 发送 **N 个完全独立的请求**——每个请求只携带自身的 `model` 字段，不包含 `selected_models`、不包含 `metadata`、也没有任何表明其他模型同时存在的标记。

本文档描述 Pipe 如何检测多模型模式、为每个 Slot 隔离会话，以及如何通过共享工作区实现跨轮协作。

---

## 关键发现：服务端无多模型信号

通过在浏览器拦截实际发出的 fetch 请求验证：

```
model (sent to backend) : cfdeepseek-deepseek
models                  : undefined
selected_models         : undefined
metadata                : undefined
```

选中 2 个模型 → 2 个独立请求到达 Pipe，每个仅包含自身的 `model` 字段。仅凭请求内容，Pipe 无法将其与两个毫不相关的单模型请求区分开来。

---

## FR-1 · 多模型检测

在每次请求开始时，通过 `__event_call__` 执行一段 JavaScript，直接从 UI 的模型选择器按钮读取当前选中的模型列表。

**JavaScript（在浏览器端执行）：**

```javascript
try {
    return [...document.querySelectorAll('button[id^="model-selector-"]')]
        .map(btn => (btn.getAttribute('aria-label') || '')
            .replace(/^已选择[：:]\s*/, '').trim())
        .filter(Boolean);
} catch (e) {
    return [];
}
```

**Python（在 Pipe `inlet` 或 `_pipe_impl` 中）：**

```python
selected_models = []
if __event_call__:
    try:
        js_code = """
            try {
                return [...document.querySelectorAll('button[id^="model-selector-"]')]
                    .map(btn => (btn.getAttribute('aria-label') || '')
                        .replace(/^已选择[：:]\s*/, '').trim())
                    .filter(Boolean);
            } catch (e) {
                return [];
            }
        """
        selected_models = await asyncio.wait_for(
            __event_call__({"type": "execute", "data": {"code": js_code}}),
            timeout=2.0,
        ) or []
    except Exception:
        selected_models = []

is_multi_model = isinstance(selected_models, list) and len(selected_models) > 1
```

**实测返回值示例：**

```
["deepseek-v3"]                                    → 单模型
["deepseek-v3", "deepseek-思考"]                   → 多模型（2 个不同模型）
["deepseek-v3", "gemini-3-flash", "deepseek-v3"]  → 多模型（同一模型 × 2 + 1）
```

**检测规则：**

- `__event_call__` 不可用或调用失败 → 回退到单模型模式
- 列表长度为 `1` → 单模型，所有现有逻辑保持不变
- 列表长度大于 `1` → 进入多模型模式
- 列表中出现重复条目，表示同一模型被选中多次，每个重复项是一个独立的 Slot

> **注意：** 返回值是 UI 显示名称，不一定等于 `body.model` 中的内部模型 ID。此列表仅用于统计 Slot 数量和判断是否为多模型模式，不用于请求路由。

---

## FR-2 · Session ID 解析

单模型模式下 Session ID 与现在完全相同。多模型模式下追加每个 Slot 的稳定锚点。

```python
def _resolve_session_id(
    self,
    chat_id: str,
    messages: Optional[list],
    current_message_id: Optional[str],
    is_multi_model: bool,
) -> str:
    # 单模型：保持现有行为不变
    if not is_multi_model:
        return chat_id

    # 多模型：追加 Slot anchor
    anchor = self._resolve_slot_anchor(messages, current_message_id)
    return f"{chat_id}::{anchor}" if anchor else chat_id


def _resolve_slot_anchor(
    self,
    messages: Optional[list],
    current_message_id: Optional[str],
) -> Optional[str]:
    """
    从消息历史中自解析的 Slot 稳定标识，不依赖任何共享状态。
    第一轮：无历史 assistant 消息 → 使用当前 message_id（即诞生 ID）。
    第二轮起：历史中第一条 assistant 消息的 id 始终是该 Slot 的 anchor。
    """
    for msg in (messages or []):
        if msg.get("role") == "assistant":
            anchor = msg.get("id") or msg.get("message_id")
            if anchor:
                return anchor
    return current_message_id
```

**为何跨轮保持稳定：**

```
Turn 1  slot A → messages=[], message_id="A1"  → anchor="A1" → session="chat::A1"
Turn 1  slot B → messages=[], message_id="B1"  → anchor="B1" → session="chat::B1"

Turn 2  slot A → messages=[..., {assistant, id="A1"}, ...]   → anchor="A1" → session="chat::A1" ✅
Turn 2  slot B → messages=[..., {assistant, id="B1"}, ...]   → anchor="B1" → session="chat::B1" ✅
```

无共享状态，无注册表，无锁。anchor 完全自包含于消息历史中。

| 场景 | Session ID |
|------|-----------|
| 单模型 | `chat_id`（现有逻辑不变）|
| 多模型 | `chat_id::{slot_anchor}` |

---

## FR-3 · 工作区结构

**单模型（不变）：**

```
{base}/{user_id}/{chat_id}/
```

**多模型：**

```
{base}/{user_id}/{chat_id}/
  ├── shared/                ← 所有 Slot 可读写（协作白板）
  ├── {anchor[:8]}/          ← Slot A 私有工作区
  ├── {anchor[:8]}/          ← Slot B 私有工作区
  └── {anchor[:8]}/          ← Slot N 私有工作区
```

```python
def _get_workspace_dir(self, user_id, chat_id, slot_anchor=None):
    base = os.path.join(root, user_id, chat_id)
    if slot_anchor:
        return os.path.join(base, slot_anchor[:8])
    return base
```

每个 Slot 的私有工作区作为 `working_directory` 传入其 SDK Session。`shared/` 目录位于 `chat_id` 层级，天然对所有 Slot 可见。

---

## FR-4 · 共享工作区文件命名约束

为防止多个 Slot 同时写入 `shared/` 时发生冲突：

- 每个 Slot 在 `shared/` 下创建的所有文件，**必须以自身 anchor 前 8 位作为前缀**
- 任意 Slot 可以**读取** `shared/` 下任意文件
- 任意 Slot **不得覆盖或删除**其他 Slot 前缀的文件

```
✅  shared/a1b2c3d4_notes.md        （Slot A 写入自己的文件）
✅  shared/a1b2c3d4_draft.py        （Slot A 写入自己的文件）
❌  shared/result.md                 （无前缀，禁止）
❌  shared/e5f6g7h8_notes.md        （其他 Slot 的前缀，禁止）
```

使用来自 `message_id` 的 anchor 而非模型显示名称作为前缀，确保同一模型被选中多次时仍能唯一区分。

此规则通过 System Prompt 注入告知模型，由模型自觉遵守，Pipe 层不做强制校验。

---

## FR-5 · System Prompt 动态注入

当 `is_multi_model` 为 `True` 时，`_build_final_system_message` 追加协作上下文块。

**静态部分**（每轮不变）：

```python
if is_multi_model:
    other_anchors = [a for a in all_slot_anchors if a != slot_anchor]
    shared_dir = os.path.join(chat_workspace, "shared")
    collab_block = f"""
[多模型协作会话]
你正在与其他 {len(other_anchors)} 个模型协同解决同一个问题。
你们不分工，各自独立推进，但可以通过共享工作区互相看到对方的进展。

你的文件前缀  : {slot_anchor[:8]}
你的私有工作区 : {private_workspace}
共享白板目录  : {shared_dir}

文件规则：你在 shared/ 下创建的所有文件必须以 "{slot_anchor[:8]}_" 开头。
你可以读取 shared/ 下任意文件，无论其前缀。

每轮建议：
1. 查看 shared/ 下其他模型留下的笔记。
2. 将你的思路和发现写入 shared/{slot_anchor[:8]}_notes.md。
3. 你的回答应体现你是否参考了其他模型的思路——认同、质疑或补充均可。

第一轮无历史可读，直接展开你的初始思路即可。
"""
    system_parts.append(collab_block)
```

**动态部分**（每轮实时扫描）：

```python
shared_files = []
if os.path.isdir(shared_dir):
    for f in sorted(os.listdir(shared_dir)):
        fpath = os.path.join(shared_dir, f)
        if os.path.isfile(fpath):
            size = os.path.getsize(fpath)
            shared_files.append(f"  - {f}  ({size} bytes)")

if shared_files:
    system_parts.append(
        "[当前 shared/ 目录内容]\n" + "\n".join(shared_files)
    )
```

仅注入文件名和大小，不读取文件内容，避免 prompt 膨胀。

---

## FR-6 · 协作时序

```
Turn 1（冷启动）：
  JS 检测 → ["model-A", "model-B"]  → is_multi_model = True
  两个 Slot 均无共享文件可读。
  各自将初始思路写入 shared/{anchor}_notes.md。

Turn 2+：
  JS 检测 → 同一列表（用户未改变选择）
  shared/ 文件列表注入到各自的 system prompt。
  各 Slot 基于其他模型上一轮的笔记做出回应。
  各 Slot 更新自己的 shared/{anchor}_notes.md。
```

同一 Turn 内所有 Slot **并行执行**，无法读取对方当轮的输出。通过 `shared/` 进行的跨轮文件交换是唯一的通信渠道。

---

## 非功能需求

| 项目 | 要求 |
|------|------|
| 向后兼容 | 单模型场景行为完全不变 |
| 无共享内存状态 | Slot anchor 从消息历史自解析，无需注册表或锁 |
| N 模型扩展性 | 支持任意数量的并行 Slot，不硬编码上限 |
| 轻量注入 | 动态部分仅注入文件名，不读取文件内容 |
| 优雅降级 | JS 调用失败时静默回退到单模型模式 |

---

## 约束

- **同轮内无实时通信**：并行执行决定了模型间的交流只能发生在 Turn 之间
- **协作规则靠引导**：文件命名约束通过 prompt 告知模型，Pipe 层不做强制校验
- **第一轮是冷启动**：真正的协作从第二轮开始
- **显示名称 ≠ 内部模型 ID**：JS 返回 UI 显示名称，足够用于 Slot 计数，但不适用于请求路由

---

## 开放问题

| # | 问题 |
|---|------|
| 1 | 当 `shared/` 下文件过多时，注入的文件列表是否需要设上限（如最多 20 条）？|
| 2 | 是否需要**合流轮**机制——一个专用的 Turn，让某个 Slot 汇总所有其他 Slot 的输出？|
| 3 | `shared/` 目录应在 Session 启动时预创建，还是在首次写入时懒创建？|
| 4 | JS 读取的是 UI 显示名称而非内部模型 ID，基于显示名称的 Slot 计数是否始终足够，还是需要建立显示名称到模型 ID 的映射？|