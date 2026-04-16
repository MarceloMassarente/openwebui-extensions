# GitHub Copilot Agent Pipe for OpenWebUI

| By [Fu-Jie](https://github.com/Fu-Jie) · v0.13.0 | [⭐ Star this repo](https://github.com/Fu-Jie/openwebui-extensions) |
| :--- | ---: |

| ![followers](https://img.shields.io/endpoint?url=https%3A%2F%2Fgist.githubusercontent.com%2FFu-Jie%2Fdb3d95687075a880af6f1fba76d679c6%2Fraw%2Fbadge_followers.json&label=%F0%9F%91%A5&style=flat) | ![points](https://img.shields.io/endpoint?url=https%3A%2F%2Fgist.githubusercontent.com%2FFu-Jie%2Fdb3d95687075a880af6f1fba76d679c6%2Fraw%2Fbadge_points.json&label=%E2%AD%90&style=flat) | ![top](https://img.shields.io/badge/%F0%9F%8F%86-Top%20%3C1%25-10b981?style=flat) | ![contributions](https://img.shields.io/endpoint?url=https%3A%2F%2Fgist.githubusercontent.com%2FFu-Jie%2Fdb3d95687075a880af6f1fba76d679c6%2Fraw%2Fbadge_contributions.json&label=%F0%9F%93%A6&style=flat) | ![downloads](https://img.shields.io/endpoint?url=https%3A%2F%2Fgist.githubusercontent.com%2FFu-Jie%2Fdb3d95687075a880af6f1fba76d679c6%2Fraw%2Fbadge_downloads.json&label=%E2%AC%87%EF%B8%8F&style=flat) | ![saves](https://img.shields.io/endpoint?url=https%3A%2F%2Fgist.githubusercontent.com%2FFu-Jie%2Fdb3d95687075a880af6f1fba76d679c6%2Fraw%2Fbadge_saves.json&label=%F0%9F%92%BE&style=flat) | ![views](https://img.shields.io/endpoint?url=https%3A%2F%2Fgist.githubusercontent.com%2FFu-Jie%2Fdb3d95687075a880af6f1fba76d679c6%2Fraw%2Fbadge_views.json&label=%F0%9F%91%81%EF%B8%8F&style=flat) |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |

This is a **GitHub Copilot SDK** Pipe for **OpenWebUI** with **Agent Team** coordination, **Session Modes** (`autopilot`/`interactive`/`plan`), autonomous **Web Search**, **Context Compaction**, and reuse of your OpenWebUI **Tools, MCP servers, and Skills**.

> [!IMPORTANT]
> **Essential Companion**
> To unlock file handling and data analysis capabilities, you must install the [GitHub Copilot SDK Files Filter](https://openwebui.com/posts/403a62ee-a596-45e7-be65-fab9cc249dd6).

> [!TIP]
> **No Subscription Required for BYOK**
> If you are using your own API keys (BYOK mode with OpenAI/Anthropic), **you do NOT need a GitHub Copilot subscription.** A subscription is only required to access GitHub's official models.

---

---

## Install with Batch Install Plugins

If you already use [Batch Install Plugins from GitHub](https://openwebui.com/posts/batch_install_plugins_install_popular_plugins_in_s_c9fd6e80) , you can install or update this plugin with:

```text
Install plugin from Fu-Jie/openwebui-extensions
```

When the selection dialog opens, search for this plugin, check it, and continue.

> [!IMPORTANT]
> If the official OpenWebUI Community version is already installed, remove it first. After that, Batch Install Plugins can keep this plugin updated in future runs.

## ✨ v0.13.0: Agent Team + Session Mode Now Work End-to-End

- **🤖 Agent Team** (New): Coordinate multiple OpenWebUI custom models as a sub-agent team within one session. Select by tag (`AGENT_TEAM_TAG`) or model IDs (`AGENT_TEAM_MODEL_IDS`), assign a leader (`AGENT_TEAM_LEADER`) — every agent inherits the same tools (OpenWebUI skills + MCP servers) as the base session.
- **🎯 Active Session Mode Awareness**: The Agent now knows which session mode is active (`autopilot` / `interactive` / `plan`) via an injected `[Active Session Mode]` system prompt directive, aligned with the official Copilot SDK agent-loop docs. Autopilot drives tasks to completion; interactive stops between steps; plan gates execution behind your approval.
- **⚡ Mode-Aware Workstyle**: Each mode now injects its own preamble — autopilot encourages full end-to-end completion, interactive enforces step-by-step pausing, plan requires approval before any action.
- **🔒 SDK Mode Set Hardened**: Both resume and create session paths now call `session.rpc.mode.set()` with `asyncio.wait_for(timeout=5.0)` to prevent hangs, with full debug visibility on failure.
- **🧹 System Prompt Overhaul**: Removed hardcoded Copilot CLI tool names and inapplicable conventions; resolved SQL pattern contradiction; SESSION_MODE now resolves globally as user_valve > global valve > `autopilot`.

> [!IMPORTANT]
> **If the plugin shows errors after an update, restart your OpenWebUI server.** The plugin is cached in memory and old bytecode may cause import errors. Restarting clears the cache and loads the fresh version.

---

## 🚀 Quick Start

1. **Install via Batch Install Plugins** → select this plugin
2. **Configure a credential**: `GH_TOKEN` (GitHub Copilot) **or** `BYOK_API_KEY` (OpenAI/Anthropic)
3. **Start chatting** — select this Pipe's model and ask naturally

> Companion Files Filter is required for the Agent to receive raw uploaded files. Install from [here](https://openwebui.com/posts/403a62ee-a596-45e7-be65-fab9cc249dd6).

## 🧭 How to Use

Just describe what you want. No need to mention tools or internal parameters.

| What you ask | What happens |
| :--- | :--- |
| `Fix the failing tests` | Normal reply |
| `Summarize this Excel file and chart the trend` | Agent processes the file and generates charts |
| `Create an interactive dashboard` | RichUI page rendered in chat |
| `Refactor this plugin` | Agent plans, executes, and tracks TODO automatically |

## ✨ Key Capabilities

| Capability | What it means for you |
| :--- | :--- |
| 🤖 **Agentic AI** | The Agent autonomously plans the path to your goal |
| 👥 **Agent Team** | Coordinate multiple sub-agents within one session — assign a leader, share tools |
| 🔄 **Session Mode** | Choose `autopilot` (autonomous), `interactive` (step-by-step confirm), or `plan` (plan-first) |
| 🛠️ **Built-in Tools** | File system, Git, bash, publish-to-workspace, directory-based skills — all installed in Docker data dir and persist across sessions |
| 🌐 **Web Search** | Triggers searches when your question needs up-to-date info |
| ♾️ **Infinite Sessions** | Weeks-long projects with automatic context compaction |
| 🧩 **Tools & MCP Bridge** | Your OpenWebUI instance's own Tools and MCP servers are automatically available and persist across sessions |
| 🎨 **RichUI / Artifacts** | Interactive dashboards and pages rendered directly in chat |
| 🛡️ **Workspace Isolation** | Each session runs with privacy isolation where possible |

---

## 🧩 Companion Files Filter

Required for the Agent to receive raw uploaded files (Excel, CSV, images) instead of RAG-processed text.

Install: [GitHub Copilot SDK Files Filter](https://openwebui.com/posts/403a62ee-a596-45e7-be65-fab9cc249dd6)

---

## ⚙️ Core Configuration (Valves)

Configure credentials (choose one or both):

| Valve | What to set |
| :--- | :--- |
| `GH_TOKEN` | GitHub Copilot token (see [Get Token](#get-token) below) |
| `BYOK_API_KEY` | OpenAI or Anthropic key |
| `BYOK_TYPE` | BYOK type: `openai` or `anthropic` |
| `BYOK_BASE_URL` | BYOK API endpoint (required when using BYOK), e.g. `https://api.openai.com/v1` (OpenAI) or `https://api.anthropic.com` (Anthropic). Other providers may differ — check vendor docs. |

> 💡 **Both at once**: You can configure both `GH_TOKEN` and `BYOK_API_KEY` — the model list will show models from both.

Other valves are optional. See the full list on [GitHub](https://github.com/Fu-Jie/openwebui-extensions/blob/main/plugins/pipes/github-copilot-sdk/TUTORIAL.md).

### Get Token

1. Visit [github.com/settings/tokens?type=beta](https://github.com/settings/tokens?type=beta)
2. Create a **Fine-grained token** with **Account permissions → Copilot Requests** access
3. Paste the token into the `GH_TOKEN` field

---

## ⭐ Support

If this plugin has been useful, a **Star** on [OpenWebUI Extensions](https://github.com/Fu-Jie/openwebui-extensions) would be a great motivation for me. Thank you!

---

## Troubleshooting

- **Agent ignores uploaded files?** → Install the Files Filter (see above)
- **Errors after update?** → Restart your OpenWebUI server to clear cached bytecode
