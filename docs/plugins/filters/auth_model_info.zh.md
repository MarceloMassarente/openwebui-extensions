# 模型授权信息过滤器 (Auth Model Info Filter)

一个专为 OpenWebUI 设计的过滤器插件，用于显示通过 Antigravity Auth API 管理的模型的实时元数据（显示名称、Token 容量和剩余配额）。

## 使用 Batch Install Plugins 安装

如果你已经安装了 [Batch Install Plugins from GitHub](https://openwebui.com/posts/batch_install_plugins_install_popular_plugins_in_s_c9fd6e80) ，可以用下面这句来安装或更新当前插件：

```text
从 Fu-Jie/openwebui-extensions 安装“模型授权信息过滤器 (Auth Model Info Filter)”
```

当选择弹窗打开后，确认当前插件并继续安装即可。

> [!IMPORTANT]
> 如果你已经安装了 OpenWebUI 官方社区里的同名版本，请先删除旧版本，否则重新安装时可能报错。删除后，Batch Install Plugins 后续就可以继续负责更新这个插件。

## 功能特性

- **自动元数据注入**: 在聊天界面的状态栏显示模型详细信息。
- **配额追踪**: 显示当前模型的剩余配额百分比。
- **动态匹配**: 从 API 获取授权模型列表，并与当前聊天会话匹配。
- **缓存机制**: 高效缓存模型信息，减少 API 请求开销。

## 配置项 (Valves)

- `BASE_URL`: 模型管理服务的 API 地址。
- `TOKEN`: 认证用的 Bearer 令牌。
- `PROJECT_ID`: 管理服务上的项目 ID。
- `AUTH_INDEX`: 服务要求的认证索引。
- `ENABLE_CACHE`: 是否启用模型数据缓存（默认：`True`）。

## 安装与同步

该插件被设计为仅本地使用，默认已在 `.gitignore` 中排除。

1. 确保目录 `plugins/filters/auth_model_info/` 存在。
2. 核心逻辑位于 `auth_model_info.py`。
