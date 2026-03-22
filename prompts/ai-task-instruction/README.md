# 🔧 AI Task Instruction

| By [Fu-Jie](https://github.com/Fu-Jie) · v1.0.0 | [⭐ Star this repo](https://github.com/Fu-Jie/openwebui-extensions) |
| :--- | ---: |

| ![followers](https://img.shields.io/endpoint?url=https%3A%2F%2Fgist.githubusercontent.com%2FFu-Jie%2Fdb3d95687075a880af6f1fba76d679c6%2Fraw%2Fbadge_followers.json&label=%F0%9F%91%A5&style=flat) | ![points](https://img.shields.io/endpoint?url=https%3A%2F%2Fgist.githubusercontent.com%2FFu-Jie%2Fdb3d95687075a880af6f1fba76d679c6%2Fraw%2Fbadge_points.json&label=%E2%AD%90&style=flat) | ![top](https://img.shields.io/badge/%F0%9F%8F%86-Top%20%3C1%25-10b981?style=flat) | ![contributions](https://img.shields.io/endpoint?url=https%3A%2F%2Fgist.githubusercontent.com%2FFu-Jie%2Fdb3d95687075a880af6f1fba76d679c6%2Fraw%2Fbadge_contributions.json&label=%F0%9F%93%A6&style=flat) | ![downloads](https://img.shields.io/endpoint?url=https%3A%2F%2Fgist.githubusercontent.com%2FFu-Jie%2Fdb3d95687075a880af6f1fba76d679c6%2Fraw%2Fbadge_downloads.json&label=%E2%AC%87%EF%B8%8F&style=flat) | ![saves](https://img.shields.io/endpoint?url=https%3A%2F%2Fgist.githubusercontent.com%2FFu-Jie%2Fdb3d95687075a880af6f1fba76d679c6%2Fraw%2Fbadge_saves.json&label=%F0%9F%92%BE&style=flat) | ![views](https://img.shields.io/endpoint?url=https%3A%2F%2Fgist.githubusercontent.com%2FFu-Jie%2Fdb3d95687075a880af6f1fba76d679c6%2Fraw%2Fbadge_views.json&label=%F0%9F%91%81%EF%B8%8F&style=flat) |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |

Convert vague or unstructured requirements into precise, structured instructions optimized for AI agent execution.

## 📋 Info

- **Command**: `/ai-task-instruction`
- **Community Link**: [OpenWebUI Post](https://openwebui.com/posts/9bab8b37-5c43-48e6-988b-946564510b91)

## 🔥 What's New in v1.0.0

- ✨ **Task Architect Persona**: Directly refactors arbitrary description into modular specs.
- 🌍 **Language Consistency**: Automated response adapting based on your dynamic input payload language.

## ✨ Key Features

- 🎯 **Precise Structuring**: Builds distinct modules like context, role, atomic steps, and constraints.
- ⚙️ **Configurable variables**: Operates seamlessly with OpenWebUI dropdown and text areas configurations.

## 🚀 How to Use

1. Check out the prompt template: [ai-task-instruction.md](./ai-task-instruction.md)
2. **Copy** the full content.
3. In OpenWebUI, Go to **Workspace** -> **Prompts** and click **Create Prompt**.
4. Set title, and paste the template code into the content block.
5. In your standard chat, trigger via `/ai-task-instruction` and fill in the fields.

## ⚙️ Configuration (Variables)

The template contains dynamic variables supported by OpenWebUI prompts:

| Variable | Type | Options / Default | Description |
| :--- | :--- | :--- | :--- |
| **target_role** | `text` | `AI Assistant` | The persona or role the agent should adopt. |
| **complexity** | `select` | `Basic`, **`Intermediate`**, `Advanced` | Level of depth the output template should contain. |
| **output_style** | `select` | **`Markdown Template`**, `JSON`, `Step-by-Step` | Structured style for the resulting prompt framework. |
| **requirements** | `textarea`| Required | The unstructured tasks or instructions from the user. |

## ⭐ Support

If this prompt has been useful, a star on [OpenWebUI Extensions](https://github.com/Fu-Jie/openwebui-extensions) is a big motivation for me. Thank you for the support.
