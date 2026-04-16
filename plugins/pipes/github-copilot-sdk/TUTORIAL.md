# GitHub Copilot SDK Pipe 详细使用教程

本文档提供 GitHub Copilot SDK Pipe 的完整配置指南和高级用法。

---

## 目录

1. [安装与配置](#1-安装与配置)
2. [凭证配置详解](#2-凭证配置详解)
3. [完整参数配置](#3-完整参数配置)
4. [Companion Files Filter](#4-companion-files-filter)
5. [高级功能](#5-高级功能)
6. [故障排除](#6-故障排除)

---

## 1. 安装与配置

### 1.1 安装 Pipe

推荐使用 **Batch Install Plugins** 安装：

1. 打开 OpenWebUI → **Workspace** → **Batch Install Plugins**
2. 输入：`Install plugin from Fu-Jie/openwebui-extensions`
3. 在弹窗中搜索并选中 **GitHub Copilot SDK Pipe**
4. 完成安装

### 1.2 安装 Companion Files Filter

**强烈推荐安装**，否则上传的文件会被 RAG 处理，Agent 无法获取原始文件。

1. 访问 [GitHub Copilot SDK Files Filter](https://openwebui.com/posts/403a62ee-a596-45e7-be65-fab9cc249dd6)
2. 按提示安装

### 1.3 配置凭证

配置 **至少一个** 凭证，否则模型列表不会显示。

详见 [第2节](#2-凭证配置详解)

---

## 2. 凭证配置详解

### 2.1 GitHub Copilot 凭证

如果你有 GitHub Copilot 订阅，使用此方式。

#### 获取 Token

1. 访问 [github.com/settings/tokens?type=beta](https://github.com/settings/tokens?type=beta)
2. 点击 **Generate new token** → **Generate new fine-grained token**
3. 配置权限：
   - **Account permissions** → **Copilot Requests** → 选择 `Access: Read and write`
4. 设置 Token 名称和过期时间
5. 点击 **Generate token**
6. 复制生成的 Token

#### 配置 Token

1. 打开 OpenWebUI → **Workspace** → **Functions** → **GitHub Copilot SDK Pipe**
2. 在 Valves 中找到 `GH_TOKEN`
3. 粘贴 Token 并保存

> [!IMPORTANT]
> GitHub Copilot Token 需要 'Copilot Requests' 权限。普通 GitHub 账号无法使用官方 Copilot 模型。

### 2.2 BYOK 凭证（推荐无订阅用户）

如果你没有 GitHub Copilot 订阅，使用自己的 API Key。

#### 支持的 Provider

| Provider | Model |
| :--- | :--- |
| OpenAI | GPT-4o, GPT-4o-mini, GPT-4-Turbo, etc. |
| Anthropic | Claude Opus, Claude Sonnet, Claude Haiku, etc. |

#### 获取 API Key

**OpenAI:**

1. 访问 [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. 创建 API Key

**Anthropic:**

1. 访问 [console.anthropic.com/settings/keys](https://console.anthropic.com/settings/keys)
2. 创建 API Key

#### 配置 BYOK

在 Valves 中配置：

| Valve | 值 |
| :--- | :--- |
| `BYOK_TYPE` | `openai` 或 `anthropic` |
| `BYOK_API_KEY` | 你的 API Key |
| `BYOK_BASE_URL` | （可选）自定义 API 端点 |
| `BYOK_MODELS` | （可选）指定模型列表，逗号分隔 |

---

## 3. 完整参数配置

### 3.1 必需/常用设置

| Valve | 默认值 | 说明 |
| :--- | :--- | :--- |
| `GH_TOKEN` | `""` | GitHub Fine-grained Token（需要 'Copilot Requests' 权限） |
| `BYOK_TYPE` | `openai` | BYOK Provider 类型：`openai` 或 `anthropic` |
| `BYOK_BASE_URL` | `""` | BYOK Base URL (`https://api.openai.com/v1` for OpenAI with /v1, `https://api.anthropic.com` for Anthropic without version suffix; other providers may differ — check vendor docs) |
| `BYOK_API_KEY` | `""` | BYOK API Key |

### 3.2 会话模式（适用于所有会话）

| Valve | 默认值 | 说明 |
| :--- | :--- | :--- |
| `SESSION_MODE` | `autopilot` | SDK 会话 Agent 模式：`autopilot`（自主多步执行）、`interactive`（每步确认）、`plan`（先计划） |

### 3.3 Agent Team（可选功能）

| Valve | 默认值 | 说明 |
| :--- | :--- | :--- |
| `AGENT_TEAM_TAG` | `""` | 按标签筛选 Agent 团队。选择标签查看可用模型。 |
| `AGENT_TEAM_LEADER` | `""` | 选择 Agent 团队的 Leader 模型。 |
| `AGENT_TEAM_MODEL_IDS` | `""` | 选择 OpenWebUI 自定义模型作为 Agent 团队（需2+个模型）。示例：`model-id-1,model-id-2` |

### 3.4 功能开关

| Valve | 默认值 | 说明 |
| :--- | :--- | :--- |
| `ENABLE_OPENWEBUI_TOOLS` | `True` | 启用 OpenWebUI Tools（包括定义的 Tools 和内置 Tools） |
| `ENABLE_OPENAPI_SERVER` | `True` | 启用 OpenAPI Tool Server 连接 |
| `ENABLE_MCP_SERVER` | `True` | 启用直接 MCP Client 连接（推荐） |
| `ENABLE_OPENWEBUI_SKILLS` | `True` | 启用将 OpenWebUI 模型附加的 Skills 加载到 SDK skill 目录 |
| `DISABLED_SKILLS` | `""` | 禁用的 Skills 名称列表，逗号分隔（如 `docs-writer,webapp-testing`） |

### 3.5 AI 行为

| Valve | 默认值 | 说明 |
| :--- | :--- | :--- |
| `REASONING_EFFORT` | `medium` | 推理努力级别：`low`, `medium`, `high`, `xhigh`（仅影响标准 Copilot 模型） |
| `SHOW_THINKING` | `True` | 显示模型推理/思考过程 |

### 3.6 运行时行为

| Valve | 默认值 | 说明 |
| :--- | :--- | :--- |
| `INFINITE_SESSION` | `True` | 启用无限会话（自动上下文压缩） |
| `DEBUG` | `False` | 启用技术调试日志（连接信息等） |
| `LOG_LEVEL` | `error` | Copilot CLI 日志级别：`none`, `error`, `warning`, `info`, `debug`, `all` |
| `TIMEOUT` | `86400` | 每个流式响应的超时时间（秒），默认 86400（24小时） |

### 3.7 过滤与限制

| Valve | 默认值 | 说明 |
| :--- | :--- | :--- |
| `EXCLUDE_KEYWORDS` | `""` | 排除包含这些关键词的模型，逗号分隔（如 `codex, haiku`） |
| `MAX_MULTIPLIER` | `3.0` | 标准 Copilot 模型的最大计费倍数。0 表示仅免费模型（0x）。设置为高值（如 100）允许所有模型。 |
| `COMPACTION_THRESHOLD` | `0.8` | 后台压缩阈值（0.0-1.0） |
| `BUFFER_THRESHOLD` | `0.95` | 缓冲区耗尽阈值（0.0-1.0） |

### 3.8 BYOK（高级）

| Valve | 默认值 | 说明 |
| :--- | :--- | :--- |
| `BYOK_BEARER_TOKEN` | `""` | BYOK Bearer Token（全局，优先于 API Key） |
| `BYOK_MODELS` | `""` | BYOK 模型列表，逗号分隔。留空则从 API 获取。 |
| `BYOK_WIRE_API` | `completions` | BYOK Wire API：`completions` 或 `responses` |

### 3.9 目录与缓存（很少更改）

| Valve | 默认值 | 说明 |
| :--- | :--- | :--- |
| `COPILOTSDK_CONFIG_DIR` | `/app/backend/data/.copilot` | Copilot SDK 配置和会话状态的持久化目录 |
| `OPENWEBUI_SKILLS_SHARED_DIR` | `/app/backend/data/cache/copilot-openwebui-skills` | OpenWebUI Skills 转换为 SDK SKILL.md 格式的共享缓存目录 |
| `OPENWEBUI_UPLOAD_PATH` | `/app/backend/data/uploads` | OpenWebUI 上传文件目录（用于文件处理） |
| `MODEL_CACHE_TTL` | `3600` | 模型列表缓存 TTL（秒），设为 0 禁用缓存。默认 3600（1小时） |
| `CUSTOM_ENV_VARS` | `""` | 自定义环境变量（JSON 格式，如 `{"VAR": "value"}`） |

---

## 4. Companion Files Filter

### 4.1 作用

OpenWebUI 默认会对上传的文件进行 RAG 处理（解析、向量化），这会导致 Agent 无法获取原始二进制文件。

Files Filter 将上传的文件移动到 `copilot_files` 目录，使 Agent 能够直接访问原始文件。

### 4.2 安装

从 [openwebui.com/posts/403a62ee-a596-45e7-be65-fab9cc249dd6](https://openwebui.com/posts/403a62ee-a596-45e7-be65-fab9cc249dd6) 安装。

### 4.3 配置

| Valve | 默认值 | 说明 |
| :--- | :--- | :--- |
| `SHOW_DEBUG_LOG` | `False` | 同时输出调试日志到后端日志和浏览器控制台 |

---

## 5. 高级功能

### 5.1 RichUI vs Artifacts

**RichUI**（默认）：生成的 HTML 页面直接渲染在聊天窗口内。

**Artifacts**：使用类似 GitHub Copilot 的 artifacts 风格展示。

Agent 通常会根据上下文自动选择。用户也可以明确要求：

- `Generate this as artifacts` → 使用 Artifacts 模式

### 5.2 发布文件

Agent 可以使用 `publish_file_from_workspace(...)` 工具发布生成的文件（Excel、CSV、文档等），提供永久下载链接。

### 5.3 Skills Bridge

SDK 与 OpenWebUI Workspace > Skills 双向同步：

- **自动同步**：Skills 自动下载到 SDK 缓存
- **`manage_skills` 工具**：Agent 可以管理 Skills
  - `list`：列出所有已安装的 Skills
  - `install`：从 GitHub URL 或 zip 文件安装
  - `create`：从上下文创建新 Skill
  - `edit`：编辑现有 Skill
  - `delete`：删除 Skill

详见 [SKILLS_MANAGER.md](https://github.com/Fu-Jie/openwebui-extensions/blob/main/plugins/pipes/github-copilot-sdk/SKILLS_MANAGER.md)

### 5.4 Web Search

Agent 可以自动触发网络搜索来获取最新信息。确保在 OpenWebUI 中启用 Web Search 功能。

### 5.5 Infinite Sessions

启用后，Agent 会自动管理上下文窗口：

- 当上下文接近限制时，自动压缩（总结 + TODO 持久化）
- 项目状态跨会话保持

---

## 6. 故障排除

### 常见问题

| 问题 | 解决方案 |
| :--- | :--- |
| 模型列表不显示 | 配置 `GH_TOKEN` 或 `BYOK_API_KEY` |
| Agent 忽略上传的文件 | 安装并启用 Files Filter |
| 更新后报错 | 重启 OpenWebUI 服务器清除缓存字节码 |
| 长时间无响应 | 检查 `TIMEOUT` 设置，增加超时时间 |
| 不显示 Thinking 过程 | 将 `SHOW_THINKING` 设置为 `True` |

### 日志调试

1. 将 `DEBUG` 设置为 `True`
2. 打开浏览器开发者工具 → Console
3. 查看详细日志

### 重置会话

如果会话卡住，可以：

1. 开启新对话
2. 或在 OpenWebUI 中删除当前会话

---

## 更多资源

- [publish_file_from_workspace 使用指南](https://github.com/Fu-Jie/openwebui-extensions/blob/main/plugins/pipes/github-copilot-sdk/PUBLISH_FILE_FROM_WORKSPACE.md)
- [manage_skills 工具指南](https://github.com/Fu-Jie/openwebui-extensions/blob/main/plugins/pipes/github-copilot-sdk/SKILLS_MANAGER.md)
- [Skills 最佳实践](https://github.com/Fu-Jie/openwebui-extensions/blob/main/plugins/pipes/github-copilot-sdk/SKILLS_BEST_PRACTICES.md)
- [完整变更日志](https://github.com/Fu-Jie/openwebui-extensions)

---

## 支持

如果这个插件对你有帮助，欢迎到 [OpenWebUI Extensions](https://github.com/Fu-Jie/openwebui-extensions) 点个 Star，这将是我持续改进的动力，感谢支持。
