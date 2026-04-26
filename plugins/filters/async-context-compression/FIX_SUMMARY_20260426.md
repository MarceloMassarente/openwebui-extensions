# 🛠️ Async Context Compression 修复总结 (2026-04-26)

## 1. 已解决的核心问题
### 🚫 异步上下文管理器协议错误
- **报错信息**: `'_GeneratorContextManager' object does not support the asynchronous context manager protocol`
- **原因**: `_async_db_session` 被错误地同时装饰了 `@contextlib.contextmanager` 和 `@contextlib.asynccontextmanager`。这导致 `async with` 调用时拿到的其实是一个同步生成器对象。
- **修复**: 移除了多余的同步装饰器，仅保留 `@contextlib.asynccontextmanager`。

### 🔍 数据库 Session 类型检测不精准
- **原因**: 原代码使用 `hasattr(session, "execute")` 来区分同步/异步 Session。由于 SQLAlchemy 同步 Session 也包含 `execute` 方法，这导致在旧版本 OpenWebUI 下会错误进入异步分支。
- **修复**: 引入 `inspect.iscoroutinefunction`，通过检测 `session.execute` 是否为协程函数来精准识别异步 Session。已覆盖 `_load_summary_record` 和 `_save_summary` 两个关键路径。

### 🐛 `_get_effective_keep_first` 在 `keep_first=0` 时返回 1（**根因**）
- **症状**: 日志停留在 `Middle messages empty (Start: 1, End: 1), skipping`，异步摘要任务永远不执行。
- **原因**: 当 `keep_first=0` 时，循环条件 `non_system_count >= keep_first` (即 `0 >= 0`) 在第一次迭代就为真，但 `target_index` 已经被设为 `i + 1 = 1`。函数错误地返回 1 而不是 0。
- **影响范围**: 该函数被 6 个调用点使用，包括 inlet 的头部消息保护、outlet 的压缩边界计算、以及 `_generate_summary_async` 的压缩范围决定。
- **修复**: 
  1. 新增 short-circuit：`keep_first <= 0` 时直接返回 0
  2. 重构循环逻辑：仅在达到 keep_first 阈值时才返回 `i + 1`，消除先赋值再判断的竞态问题
  3. 增强 "Middle messages empty" 日志：输出完整的诊断上下文（summary_index, base_progress, target_compressed_count, keep_first, keep_last, total_messages）

## 2. 当前状态
- **语法检查**: `ast.parse` 通过。
- **逻辑断言**: 
  - `keep_first=0` → `_get_effective_keep_first` 返回 0 ✅
  - `keep_first=1, [system, user]` → 返回 2 ✅
  - `keep_first=1, [user, assistant]` → 返回 1 ✅
  - `keep_first=2, [sys, user, sys, user, assistant]` → 返回 4 ✅
  - 20条消息 + keep_first=0 + keep_last=6 → start=0, end=14, middle=14条 ✅
- **测试结果**: 仓库通用测试通过。

## 3. 待进一步排查的问题 (Handover for Next AI)
1. **数据库操作的线程安全**: 在 OpenWebUI < 0.9.0 环境下，底层使用的是同步数据库引擎。虽然当前代码在降级路径中使用了 `with self._sync_db_session()`，但由于 `Inlet` 是异步调用的，频繁的数据库读写可能存在潜在的连接池抢占问题。
2. **Commit/Expunge 兼容性**: 在异步模式下使用了 `await session.commit()`，而在同步模式下直接使用 `session.commit()`。需确认在所有可能的降级场景中，`session` 对象状态管理是否完全符合 SQLAlchemy 2.0 的混合模式要求。
3. **Outlet 消息源完整性**: 如果 `_load_full_chat_messages` 从 DB 加载失败（返回空列表），outlet 只能依赖 body 中已被 inlet 压缩过的消息列表。此时消息数量极少，即使修复了 `_get_effective_keep_first`，`target_compressed_count` 仍可能不足以触发摘要生成。建议在这种降级场景中增加额外的日志监控。
