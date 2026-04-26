# OpenWebUI 0.9.x Compatibility — Full Plugin Suite Updated

**Published:** 2026-04-26  
**Author:** [Fu-Jie](https://github.com/Fu-Jie/openwebui-extensions)

---

Great news for the OpenWebUI community! Over the past few days, I've completed **full OpenWebUI 0.9.x compatibility updates** across my entire plugin suite. Whether you're already on 0.9.x or sticking with an earlier version, all plugins now work seamlessly with zero configuration changes on your end.

---

## 🔌 GitHub Copilot SDK — v0.13.1

**OpenWebUI 0.9.x Dual-Compatibility Layer**

The SDK now auto-detects whether your OpenWebUI instance is pre-0.9 or 0.9+ and routes all database model calls through the appropriate path — async/await on 0.9.x, synchronous on older versions. **Zero configuration needed.**

[🔗 Install on OpenWebUI](https://openwebui.com/posts/github_copilot_official_sdk_pipe_ce96f7b4) · [📖 GitHub Docs](https://github.com/Fu-Jie/openwebui-extensions/tree/main/plugins/pipes/github-copilot-sdk)

---

## 🧠 Smart Mind Map — v1.0.1 (Action + Tool)

**OpenWebUI 0.9.x Async Database Compatibility**

Both the Action plugin (chat-based mind map generation) and the standalone Tool now handle async database sessions gracefully on OpenWebUI 0.9.x. Seamless fallback on older versions.

[🔗 Install Action on OpenWebUI](https://openwebui.com/posts/turn_any_text_into_beautiful_mind_maps_3094c59a) · [🔧 Install Tool on OpenWebUI](https://openwebui.com/posts/smart_mind_map_tool_auto_generate_interactive_know_d25f4e3d) · [📖 GitHub Docs](https://github.com/Fu-Jie/openwebui-extensions/tree/main/plugins/actions/smart-mind-map)

---

## 📊 Smart Infographic — v1.6.2

**OpenWebUI 0.9.x Async Database Compatibility**

The async database compatibility layer has been applied to all database operations, ensuring stable performance on OpenWebUI 0.9.x.

[🔗 Install on OpenWebUI](https://openwebui.com/posts/smart_infographic_ad6f0c7f) · [📖 GitHub Docs](https://github.com/Fu-Jie/openwebui-extensions/tree/main/plugins/actions/smart-infographic)

---

## 📋 Export to Docx — v0.4.5

**OpenWebUI 0.9.x Async Database Compatibility**

Word document export now works seamlessly on OpenWebUI 0.9.x with async database session handling. Includes all existing features: headings, tables, inline code, Smart List formatting, and formula support.

[🔗 Install on OpenWebUI](https://openwebui.com/posts/export_to_word_enhanced_formatting_fca6a315) · [📖 GitHub Docs](https://github.com/Fu-Jie/openwebui-extensions/tree/main/plugins/actions/export_to_docx)

---

## 📈 Export to Excel — v0.3.8

**OpenWebUI 0.9.x Async Database Compatibility**

Spreadsheet exports (both `.xlsx` and legacy `.xls` with Chinese character support) now work seamlessly on OpenWebUI 0.9.x with async database session handling built in.

[🔗 Install on OpenWebUI](https://openwebui.com/posts/export_mulit_table_to_excel_244b8f9d) · [📖 GitHub Docs](https://github.com/Fu-Jie/openwebui-extensions/tree/main/plugins/actions/export_to_excel)

---

## 🗜️ Async Context Compression — v1.6.1

**OpenWebUI 0.9.x Async Database Compatibility**

The context compression engine now fully supports OpenWebUI 0.9.x's async database models. Conversation summarization and compression work reliably across all supported versions.

[🔗 Install on OpenWebUI](https://openwebui.com/posts/async_context_compression_b1655bc8) · [📖 GitHub Docs](https://github.com/Fu-Jie/openwebui-extensions/tree/main/plugins/filters/async-context-compression)

---

## 🧰 OpenWebUI Skills Manager — v0.3.2

**OpenWebUI 0.9.x Async Compatibility + Multi-line Frontmatter Fix**

Skill management — list, show, install, create, update, delete — is now fully async-compatible with 0.9.x. Additionally, multi-line `description: >` / `description: |` frontmatter blocks in remote `SKILL.md` files are now correctly parsed, so skill descriptions won't get truncated on import.

[🔗 Install on OpenWebUI](https://openwebui.com/posts/openwebui_skills_manager_tool_b4bce8e4) · [📖 GitHub Docs](https://github.com/Fu-Jie/openwebui-extensions/tree/main/plugins/tools/openwebui-skills-manager)

---

## What Does This Mean for You?

| Your OpenWebUI Version | What to Do |
|---|---|
| **OpenWebUI < 0.9.x** | Everything works exactly as before. No changes needed. |
| **OpenWebUI ≥ 0.9.x** | The compatibility layer activates automatically. Just update the plugins. |

**No configuration tweaks. No migration steps. Just update and carry on.** 🚀

---

## Full Plugin Suite

Want to explore more? Here's the full list of my plugins:

| Plugin | Type | Version |
|---|---|---|
| [GitHub Copilot SDK](https://openwebui.com/posts/github_copilot_official_sdk_pipe_ce96f7b4) | Pipe | v0.13.1 |
| [Smart Mind Map](https://openwebui.com/posts/turn_any_text_into_beautiful_mind_maps_3094c59a) | Action | v1.0.1 |
| [Smart Mind Map Tool](https://openwebui.com/posts/smart_mind_map_tool_auto_generate_interactive_know_d25f4e3d) | Tool | v1.0.1 |
| [Smart Infographic](https://openwebui.com/posts/smart_infographic_ad6f0c7f) | Action | v1.6.2 |
| [Export to Word](https://openwebui.com/posts/export_to_word_enhanced_formatting_fca6a315) | Action | v0.4.5 |
| [Export to Excel](https://openwebui.com/posts/export_mulit_table_to_excel_244b8f9d) | Action | v0.3.8 |
| [Async Context Compression](https://openwebui.com/posts/async_context_compression_b1655bc8) | Filter | v1.6.1 |
| [OpenWebUI Skills Manager](https://openwebui.com/posts/openwebui_skills_manager_tool_b4bce8e4) | Tool | v0.3.2 |
| [Markdown Normalizer](https://openwebui.com/posts/markdown_normalizer_baaa8732) | Action | v1.2.8 |
| [Batch Install Plugins](https://openwebui.com/posts/batch_install_plugins_install_popular_plugins_in_s_c9fd6e80) | Tool | — |
| [AI Task Instruction Generator](https://openwebui.com/posts/ai_task_instruction_generator_9bab8b37) | Action | — |

---

*Plugin source code and documentation: [Fu-Jie/openwebui-extensions](https://github.com/Fu-Jie/openwebui-extensions)*