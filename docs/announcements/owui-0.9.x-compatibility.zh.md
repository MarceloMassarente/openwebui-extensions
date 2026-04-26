# OpenWebUI 0.9.x 兼容性更新 — 全部插件已适配

**发布日期：** 2026-04-26  
**作者：** [Fu-Jie](https://github.com/Fu-Jie/openwebui-extensions)

---

好消息！最近三天，我完成了**全系插件的 OpenWebUI 0.9.x 兼容性适配**。无论你使用的是 0.9.x 还是更早版本，所有插件均可无缝运行，**无需你做任何配置修改**。

---

## 🔌 GitHub Copilot SDK — v0.13.1

**OpenWebUI 0.9.x 双兼容层**

SDK 现在自动检测你的 OpenWebUI 实例是 pre-0.9 还是 0.9+ 版本，并将所有数据库模型调用路由到对应路径——0.9.x 上使用 async/await，旧版本使用同步调用。**零配置，即插即用。**

[🔗 在 OpenWebUI 上安装](https://openwebui.com/posts/github_copilot_official_sdk_pipe_ce96f7b4) · [📖 GitHub 文档](https://github.com/Fu-Jie/openwebui-extensions/tree/main/plugins/pipes/github-copilot-sdk)

---

## 🧠 Smart Mind Map — v1.0.1（Action + Tool 双版）

**OpenWebUI 0.9.x 异步数据库兼容性**

Action 版（基于对话生成思维导图）和独立 Tool 版均已适配 OpenWebUI 0.9.x 的异步数据库会话，在旧版本上也有完美回退。

[🔗 安装 Action 版](https://openwebui.com/posts/turn_any_text_into_beautiful_mind_maps_3094c59a) · [🔧 安装 Tool 版](https://openwebui.com/posts/smart_mind_map_tool_auto_generate_interactive_know_d25f4e3d) · [📖 GitHub 文档](https://github.com/Fu-Jie/openwebui-extensions/tree/main/plugins/actions/smart-mind-map)

---

## 📊 Smart Infographic — v1.6.2

**OpenWebUI 0.9.x 异步数据库兼容性**

信息图生成插件的所有数据库操作均已接入异步兼容层，在 OpenWebUI 0.9.x 上稳定运行。

[🔗 在 OpenWebUI 上安装](https://openwebui.com/posts/smart_infographic_ad6f0c7f) · [📖 GitHub 文档](https://github.com/Fu-Jie/openwebui-extensions/tree/main/plugins/actions/smart-infographic)

---

## 📋 Export to Docx — v0.4.5

**OpenWebUI 0.9.x 异步数据库兼容性**

Word 文档导出现已完美支持 OpenWebUI 0.9.x，包含所有现有功能：标题、表格、行内代码、Smart List 格式及公式支持。

[🔗 在 OpenWebUI 上安装](https://openwebui.com/posts/export_to_word_enhanced_formatting_fca6a315) · [📖 GitHub 文档](https://github.com/Fu-Jie/openwebui-extensions/tree/main/plugins/actions/export_to_docx)

---

## 📈 Export to Excel — v0.3.8

**OpenWebUI 0.9.x 异步数据库兼容性**

电子表格导出（`.xlsx` 和带中文支持的旧版 `.xls`）现已支持 OpenWebUI 0.9.x 的异步数据库会话管理。

[🔗 在 OpenWebUI 上安装](https://openwebui.com/posts/export_mulit_table_to_excel_244b8f9d) · [📖 GitHub 文档](https://github.com/Fu-Jie/openwebui-extensions/tree/main/plugins/actions/export_to_excel)

---

## 🗜️ Async Context Compression — v1.6.1

**OpenWebUI 0.9.x 异步数据库兼容性**

上下文压缩引擎现已全面支持 OpenWebUI 0.9.x 的异步数据库模型，对话摘要和压缩在所有支持版本上均可靠运行。

[🔗 在 OpenWebUI 上安装](https://openwebui.com/posts/async_context_compression_b1655bc8) · [📖 GitHub 文档](https://github.com/Fu-Jie/openwebui-extensions/tree/main/plugins/filters/async-context-compression)

---

## 🧰 OpenWebUI Skills 管理工具 — v0.3.2

**OpenWebUI 0.9.x 异步兼容性 + 多行 Frontmatter 修复**

技能管理（列出/查看/安装/创建/更新/删除）现已完全兼容 0.9.x 异步模式。此外，远程 `SKILL.md` 文件中的多行 `description: >` / `description: |` frontmatter 块现在可以正确解析，导入后的技能描述不再被截断。

[🔗 在 OpenWebUI 上安装](https://openwebui.com/posts/openwebui_skills_manager_tool_b4bce8e4) · [📖 GitHub 文档](https://github.com/Fu-Jie/openwebui-extensions/tree/main/plugins/tools/openwebui-skills-manager)

---

## 这对你意味着什么？

| 你的 OpenWebUI 版本 | 需要做什么 |
|---|---|
| **OpenWebUI < 0.9.x** | 一切照旧，无需任何修改。 |
| **OpenWebUI ≥ 0.9.x** | 兼容层自动激活，只需更新插件即可。 |

**无需配置调整，无需迁移步骤。更新插件，然后继续你的工作。** 🚀

---

## 全部插件一览

| 插件 | 类型 | 版本 |
|---|---|---|
| [GitHub Copilot SDK](https://openwebui.com/posts/github_copilot_official_sdk_pipe_ce96f7b4) | Pipe | v0.13.1 |
| [Smart Mind Map](https://openwebui.com/posts/turn_any_text_into_beautiful_mind_maps_3094c59a) | Action | v1.0.1 |
| [Smart Mind Map Tool](https://openwebui.com/posts/smart_mind_map_tool_auto_generate_interactive_know_d25f4e3d) | Tool | v1.0.1 |
| [Smart Infographic](https://openwebui.com/posts/smart_infographic_ad6f0c7f) | Action | v1.6.2 |
| [Export to Word](https://openwebui.com/posts/export_to_word_enhanced_formatting_fca6a315) | Action | v0.4.5 |
| [Export to Excel](https://openwebui.com/posts/export_mulit_table_to_excel_244b8f9d) | Action | v0.3.8 |
| [Async Context Compression](https://openwebui.com/posts/async_context_compression_b1655bc8) | Filter | v1.6.1 |
| [OpenWebUI Skills 管理工具](https://openwebui.com/posts/openwebui_skills_manager_tool_b4bce8e4) | Tool | v0.3.2 |
| [Markdown Normalizer](https://openwebui.com/posts/markdown_normalizer_baaa8732) | Action | v1.2.8 |
| [Batch Install Plugins](https://openwebui.com/posts/batch_install_plugins_install_popular_plugins_in_s_c9fd6e80) | Tool | — |
| [AI Task Instruction Generator](https://openwebui.com/posts/ai_task_instruction_generator_9bab8b37) | Action | — |

---

*插件源码及文档：[Fu-Jie/openwebui-extensions](https://github.com/Fu-Jie/openwebui-extensions)*