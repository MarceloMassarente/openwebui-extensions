# OpenWebUI 0.9.x Async DB Migration

## Summary

Starting from OpenWebUI **v0.9.0**, all Database Abstraction Model methods were migrated to `async def`. Any plugin calling these methods without `await` will receive a `coroutine` object instead of the actual data, causing `'coroutine' object is not iterable` or similar errors at runtime.

**CRITICAL**: Plugins must support BOTH versions (< 0.9.0 where DB methods are sync, and >= 0.9.0 where they are async). Use the `_call_db` version-aware helper pattern below.

## Affected Models

All methods in these models are now `async def`:
- `open_webui.models.chats.Chats`
- `open_webui.models.users.Users`
- `open_webui.models.files.Files`
- `open_webui.models.folders.Folders`
- `open_webui.models.tools.Tools`
- `open_webui.models.models.Models`
- `open_webui.models.skills.Skills`
- (and all other models in `open_webui.models.*`)

## Version-Aware `_call_db` Pattern (REQUIRED)

Every plugin that calls DB model methods MUST include these helpers to ensure backward compatibility with OpenWebUI < 0.9.0. There are **two** helpers — one for async contexts, one for sync contexts:

```python
# ── OpenWebUI version detection for async DB compatibility ──────────
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
    """
    Call an OpenWebUI DB model method with version-aware async handling (for ASYNC contexts).
    - OpenWebUI >= 0.9.0: DB methods are async, so we await them.
    - OpenWebUI <  0.9.0: DB methods are sync, so we call them directly.
    """
    if _owui_version_ge("0.9.0"):
        return await method(*args, **kwargs)
    else:
        return method(*args, **kwargs)


def _call_db_sync(method, *args, **kwargs):
    """
    Call an OpenWebUI DB model method with version-aware async handling (for SYNC contexts).
    - OpenWebUI <  0.9.0: DB methods are sync, call directly.
    - OpenWebUI >= 0.9.0: DB methods are async, run in a separate thread with its own
      event loop (asyncio.run) to avoid "cannot run from running event loop" errors.
    """
    if not _owui_version_ge("0.9.0"):
        return method(*args, **kwargs)
    import concurrent.futures
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
        return pool.submit(asyncio.run, method(*args, **kwargs)).result()
```

### When to use which helper

- **`await _call_db(method, ...)`**: Use inside `async def` functions (async methods, pipe(), inlet(), outlet(), etc.)
- **`_call_db_sync(method, ...)`**: Use inside regular `def` functions (sync methods, @classmethod, __init__, _build_xxx, etc.)

### Common pitfall: `asyncio.to_thread` is NOT sufficient

`asyncio.to_thread(Models.get_model_by_id, model_id)` wraps a **sync** function for async use. But on OpenWebUI >= 0.9.0, the method IS async — calling it through `to_thread` would pass a coroutine object to `to_thread`, which expects a sync callable. This will crash. Use `await _call_db()` instead.

### Usage

```python
# Before (broken in 0.9.x, works in <0.9.x)
user_obj = Users.get_user_by_id(user_id)

# WRONG (breaks in <0.9.x — sync methods can't be awaited)
user_obj = await Users.get_user_by_id(user_id)

# CORRECT (works in both versions)
user_obj = await _call_db(Users.get_user_by_id, user_id)
```

### Multi-arg calls

```python
# Before
chat = await Chats.get_chat_by_id_and_user_id(id=chat_id, user_id=user_id)

# After
chat = await _call_db(Chats.get_chat_by_id_and_user_id, id=chat_id, user_id=user_id)
```

## Official Migration Guide (0.9.0) — Key Findings

Source: https://docs.openwebui.com/features/extensibility/plugin/migration/to-0.9.0

### 1. ALL `open_webui.utils.*` helpers that touch DB are now async too

Not just model classes — **any** helper in `open_webui.utils.*`, `open_webui.retrieval.*`, router helpers, and access-control checks that directly or indirectly touch the DB have been promoted to `async def`. Check every `from open_webui.*` import.

**Specific async utils confirmed (>= 0.9.0)**:
- `open_webui.utils.tools.get_tools` → `async def get_tools(...)`
- `open_webui.utils.tools.get_builtin_tools` → `async def get_builtin_tools(...)`
- `open_webui.utils.chat.generate_chat_completion` → was already async before 0.9.0

**Specific sync utils confirmed (unchanged)**:
- `open_webui.config.get_config` → remains sync
- `open_webui.utils.misc.convert_output_to_messages` → remains sync
- `open_webui.storage.provider.Storage.upload_file` → remains sync

### 2. Sync DB helpers are startup-only — NEVER use at runtime

`SessionLocal`, `get_db`, `get_session`, `get_db_context`, sync `save_config` / `reset_config` — these are **reserved for startup code only** (config loading, Alembic migrations, health checks). Using them from a plugin, route handler, or anything inside the event loop will:
- Block the event loop
- Acquire connections from the sync pool (competing with async pool)
- Can deadlock under concurrent load

**Runtime code must use**: `get_async_db`, `get_async_db_context`, `get_async_session`, `async_save_config`, `async_reset_config`.

### 3. SQLAlchemy 2.0 async query style required

- `db.query(Model)` → no longer supported
- Use `select(Model)` + `await db.execute(...)`
- `.first()` / `.all()` / `.count()` → `.scalars().first()`, `.scalars().all()`, `.scalar_one()`
- Session type: `AsyncSession` (not `Session`)

### 4. Plugin entrypoints unchanged

`pipe`, `inlet`, `outlet`, `stream`, `action`, and Tool methods were already async since 0.5. Only the code inside them needs updates.

### 5. Async propagates upward

If any helper in your call chain becomes `async def`, every caller must also be `async def` — all the way up to the plugin entrypoint. This is why `_save_summary` and `_load_summary_record` in async_context_compression had to be converted from sync to async.

## Custom ORM Tables (async_context_compression pattern)

When a plugin creates its own ORM table (e.g., `ChatSummary`) and uses direct SQLAlchemy queries:

### Before 0.9.0 (sync):
```python
def _db_session(self):
    with get_db_context() as session:
        yield session

def _save_summary(self, ...):
    with self._db_session() as session:
        existing = session.query(ChatSummary).filter_by(chat_id=chat_id).first()
        session.commit()
```

### After 0.9.0 (async, with backward compat):
```python
@contextlib.asynccontextmanager
async def _async_db_session(self):
    if _owui_version_ge("0.9.0"):
        async_ctx = getattr(self._owui_db, "get_async_db_context", None)
        if callable(async_ctx):
            async with async_ctx() as session:
                yield session
                return
    # Fallback: wrap sync session for < 0.9.0
    with self._sync_db_session() as session:
        yield session

async def _save_summary(self, ...):
    async with self._async_db_session() as session:
        if _owui_version_ge("0.9.0"):
            result = await session.execute(select(ChatSummary).filter_by(chat_id=chat_id))
            existing = result.scalars().first()
            # ... modify existing ...
            await session.commit()
        else:
            existing = session.query(ChatSummary).filter_by(chat_id=chat_id).first()
            # ... modify existing ...
            session.commit()
```

**Key**: `session.commit()` → `await session.commit()` in 0.9.0. The `_owui_version_ge` check determines which query style to use.

### Startup-only sync session (for __init__ / table creation):
```python
def _sync_db_session(self):
    """Startup-only sync DB session. Never use from runtime code."""
    with get_db_context() as session:
        yield session
```

## Database Driver Changes

- SQLite: `aiosqlite` required (sync URLs auto-rewritten to `sqlite+aiosqlite://`)
- PostgreSQL: `asyncpg` required (URLs auto-rewritten to `postgresql+asyncpg://`)
- **SQLCipher** (`sqlite+sqlcipher://`) is NOT supported in 0.9.0 — no async driver exists
