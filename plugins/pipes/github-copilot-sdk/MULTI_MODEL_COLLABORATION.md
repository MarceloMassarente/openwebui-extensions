# Multi-Model Collaboration

> Implementation Reference · GitHub Copilot SDK Pipe

---

## Overview

OpenWebUI allows users to select multiple models simultaneously in a single conversation. When N models are active, OpenWebUI sends **N completely independent requests** to the pipe — each request carries only its own `model` field, with no `selected_models`, no `metadata`, and no indication that other models are involved.

This document describes how the pipe detects multi-model mode, isolates sessions per slot, and enables cross-turn collaboration via a shared workspace.

---

## Key Finding: No Server-Side Multi-Model Signal

Verified by intercepting the outgoing fetch requests from the browser:

```
model (sent to backend) : cfdeepseek-deepseek
models                  : undefined
selected_models         : undefined
metadata                : undefined
```

Two models selected → two independent requests arrive at the pipe, each with only its own `model` field. The pipe cannot distinguish them from two unrelated single-model requests based on request content alone.

---

## FR-1 · Multi-Model Detection

Detection is performed at the start of each request by executing a JavaScript snippet via `__event_call__` to read the model selector buttons directly from the UI DOM.

**JavaScript (executed in browser):**

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

**Python (in pipe `inlet` or `_pipe_impl`):**

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

**Observed return values:**

```
["deepseek-v3"]                                    → single-model
["deepseek-v3", "deepseek-思考"]                   → multi-model (2 different)
["deepseek-v3", "gemini-3-flash", "deepseek-v3"]  → multi-model (same model × 2 + 1)
```

**Rules:**

- If `__event_call__` is unavailable or the call fails → fall back to single-model mode
- `len == 1` → single-model, all existing logic unchanged
- `len > 1` → multi-model mode activated
- Duplicate entries mean the same model is selected more than once; each is a distinct Slot

> **Note:** The returned values are UI display names, not the internal model IDs in `body.model`. They are used only for counting Slots and detecting multi-model mode.

---

## FR-2 · Session ID Resolution

In single-model mode the session ID stays exactly as it is today. In multi-model mode a per-Slot stable anchor is appended.

```python
def _resolve_session_id(
    self,
    chat_id: str,
    messages: Optional[list],
    current_message_id: Optional[str],
    is_multi_model: bool,
) -> str:
    # Single-model: preserve current behavior
    if not is_multi_model:
        return chat_id

    # Multi-model: append the Slot anchor
    anchor = self._resolve_slot_anchor(messages, current_message_id)
    return f"{chat_id}::{anchor}" if anchor else chat_id


def _resolve_slot_anchor(
    self,
    messages: Optional[list],
    current_message_id: Optional[str],
) -> Optional[str]:
    """
    Stable per-Slot identifier derived purely from message history.
    Turn 1 : no prior assistant message → use current message_id (birth ID).
    Turn 2+: first assistant message in history → its id is always this Slot's anchor.
    """
    for msg in (messages or []):
        if msg.get("role") == "assistant":
            anchor = msg.get("id") or msg.get("message_id")
            if anchor:
                return anchor
    return current_message_id
```

**Why this works across turns:**

```
Turn 1  slot A → messages=[], message_id="A1"  → anchor="A1" → session="chat::A1"
Turn 1  slot B → messages=[], message_id="B1"  → anchor="B1" → session="chat::B1"

Turn 2  slot A → messages=[..., {assistant, id="A1"}, ...]   → anchor="A1" → session="chat::A1" ✅
Turn 2  slot B → messages=[..., {assistant, id="B1"}, ...]   → anchor="B1" → session="chat::B1" ✅
```

No shared state, no registry, no locks. The anchor is self-contained in message history.

| Scenario | Session ID |
|----------|-----------|
| Single model | `chat_id` (unchanged) |
| Multi-model | `chat_id::{slot_anchor}` |

---

## FR-3 · Workspace Structure

**Single model (unchanged):**

```
{base}/{user_id}/{chat_id}/
```

**Multi-model:**

```
{base}/{user_id}/{chat_id}/
  ├── shared/                ← Read/write for all Slots (collaborative whiteboard)
  ├── {anchor[:8]}/          ← Slot A private workspace
  ├── {anchor[:8]}/          ← Slot B private workspace
  └── {anchor[:8]}/          ← Slot N private workspace
```

```python
def _get_workspace_dir(self, user_id, chat_id, slot_anchor=None):
    base = os.path.join(root, user_id, chat_id)
    if slot_anchor:
        return os.path.join(base, slot_anchor[:8])
    return base
```

Each Slot's private workspace is passed to its SDK Session as `working_directory`. The `shared/` directory sits at the `chat_id` level and is naturally visible to all Slots.

---

## FR-4 · File Naming Convention in Shared Workspace

To prevent write conflicts when multiple Slots write to `shared/`:

- Every file created inside `shared/` **must be prefixed with the Slot's own anchor** (first 8 characters)
- Any Slot may **read** any file in `shared/`
- No Slot may **overwrite or delete** files belonging to other Slots

```
✅  shared/a1b2c3d4_notes.md        (Slot A writing its own file)
✅  shared/a1b2c3d4_draft.py        (Slot A writing its own file)
❌  shared/result.md                 (no prefix — forbidden)
❌  shared/e5f6g7h8_notes.md        (another Slot's prefix — forbidden)
```

Using the anchor (derived from `message_id`) rather than the model display name as the prefix guarantees uniqueness even when the same model is selected multiple times.

This rule is communicated to models via system prompt injection. It is enforced by instruction, not by the Pipe.

---

## FR-5 · System Prompt Injection

`_build_final_system_message` appends a collaboration block when `is_multi_model` is `True`.

**Static section** (same every turn):

```python
if is_multi_model:
    other_anchors = [a for a in all_slot_anchors if a != slot_anchor]
    shared_dir = os.path.join(chat_workspace, "shared")
    collab_block = f"""
[Multi-Model Session]
You are one of {len(all_slot_anchors)} models working on the same problem in parallel.
You are not divided by role — each works independently, but can see the others' progress.

Your file prefix  : {slot_anchor[:8]}
Your workspace    : {private_workspace}
Shared whiteboard : {shared_dir}

File rule: every file you create inside shared/ MUST start with "{slot_anchor[:8]}_".
You may read any file in shared/ regardless of prefix.

Each turn:
1. Check shared/ for notes left by other models.
2. Write your working thoughts and findings to shared/{slot_anchor[:8]}_notes.md.
3. Your response should reflect what you found — agree, challenge, or build on it.

Turn 1 has no prior history. Begin from your own reasoning.
"""
    system_parts.append(collab_block)
```

**Dynamic section** (scanned fresh each turn):

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
        "[Current shared/ contents]\n" + "\n".join(shared_files)
    )
```

Only filenames and sizes are injected. File contents are not read into the prompt to avoid context bloat.

---

## FR-6 · Collaboration Timeline

```
Turn 1 (cold start):
  selected_models JS → ["model-A", "model-B"]  → is_multi_model = True
  Both Slots start with no shared files.
  Each writes initial reasoning to shared/{anchor}_notes.md.

Turn 2+:
  selected_models JS → same list (user hasn't changed selection)
  Each Slot reads shared/ listing injected into system prompt.
  Each Slot responds with awareness of others' previous-turn notes.
  Each Slot updates its own shared/{anchor}_notes.md.
```

All Slots within a single Turn execute **in parallel**. They cannot read each other's output within the same Turn. Cross-turn file exchange via `shared/` is the only communication channel.

---

## Non-Functional Requirements

| Item | Requirement |
|------|------------|
| Backward compatibility | Single-model behavior is completely unchanged |
| No shared in-memory state | Slot anchor derived purely from message history; no registry or locks |
| N-model scalability | Supports any number of parallel Slots; no hardcoded limit |
| Lightweight injection | Dynamic section lists filenames only; file contents never read into prompt |
| Graceful degradation | If JS call fails, fall back to single-model mode silently |

---

## Constraints

- **No intra-Turn communication**: parallel execution makes same-turn model-to-model messaging impossible
- **Collaboration rules by instruction**: file naming convention is communicated via prompt, not enforced by the Pipe
- **Turn 1 is a cold start**: genuine collaboration begins from Turn 2 onwards
- **Display names ≠ model IDs**: JS returns UI display names; these are sufficient for Slot counting but not for routing

---

## Open Questions

| # | Question |
|---|---------|
| 1 | Should the `shared/` file listing in the prompt be capped (e.g. max 20 files) when the directory grows large? |
| 2 | Is a **synthesis turn** needed — a dedicated mechanism where one Slot summarizes all others' outputs on demand? |
| 3 | Should `shared/` be pre-created at session start, or created lazily on first write? |
| 4 | The JS reads UI display names, not internal model IDs. Is display-name-based Slot counting always sufficient, or do we need a display-name → model-ID mapping for any downstream logic? |