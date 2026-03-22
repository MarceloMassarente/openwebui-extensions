# 🔧 AI Task Instruction (AI 任务指令生成器)

| 作者: [Fu-Jie](https://github.com/Fu-Jie) · v1.0.0 | [⭐ 给项目点个 Star](https://github.com/Fu-Jie/openwebui-extensions) |
| :--- | ---: |

| ![followers](https://img.shields.io/endpoint?url=https%3A%2F%2Fgist.githubusercontent.com%2FFu-Jie%2Fdb3d95687075a880af6f1fba76d679c6%2Fraw%2Fbadge_followers.json&label=%F0%9F%91%A5&style=flat) | ![points](https://img.shields.io/endpoint?url=https%3A%2F%2Fgist.githubusercontent.com%2FFu-Jie%2Fdb3d95687075a880af6f1fba76d679c6%2Fraw%2Fbadge_points.json&label=%E2%AD%90&style=flat) | ![top](https://img.shields.io/badge/%F0%9F%8F%86-Top%20%3C1%25-10b981?style=flat) | ![contributions](https://img.shields.io/endpoint?url=https%3A%2F%2Fgist.githubusercontent.com%2FFu-Jie%2Fdb3d95687075a880af6f1fba76d679c6%2Fraw%2Fbadge_contributions.json&label=%F0%9F%93%A6&style=flat) | ![downloads](https://img.shields.io/endpoint?url=https%3A%2F%2Fgist.githubusercontent.com%2FFu-Jie%2Fdb3d95687075a880af6f1fba76d679c6%2Fraw%2Fbadge_downloads.json&label=%E2%AC%87%EF%B8%8F&style=flat) | ![saves](https://img.shields.io/endpoint?url=https%3A%2F%2Fgist.githubusercontent.com%2FFu-Jie%2Fdb3d95687075a880af6f1fba76d679c6%2Fraw%2Fbadge_saves.json&label=%F0%9F%92%BE&style=flat) | ![views](https://img.shields.io/endpoint?url=https%3A%2F%2Fgist.githubusercontent.com%2FFu-Jie%2Fdb3d95687075a880af6f1fba76d679c6%2Fraw%2Fbadge_views.json&label=%F0%9F%91%81%EF%B8%8F&style=flat) |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |

将模糊的通用需求或无结构自然语言，转换为精确、结构化且高度优化的 AI 任务指令框架。

## 📋 基础信息

- **触发指令 (Command)**: `/ai-task-instruction`
- **社区链接 (Community Link)**: [OpenWebUI Post](https://openwebui.com/posts/9bab8b37-5c43-48e6-988b-946564510b91)

## 🔥 版本特性 v1.0.0

- ✨ **提示词架构师 Persona**: 将任何形式的语句解构为极其精细的指令模块。
- 🌍 **语言强制对齐**: 新增逻辑自适应模块，根据您的输入语言动态回溯对应语言输出。

## ✨ 核心优势

- 🎯 **精确结构化**: 输出带角色、目标、上下景深、拆解步骤、错误防御与输出规范格式。
- ⚙️ **完美挂载**: 完全利用 OpenWebUI 原生面板支持动态下拉菜单选择。

## 🚀 如何使用

1. 查看提示词文件：[ai-task-instruction.md](./ai-task-instruction.md)
2. **复制** 文件的完整内容。
3. 打开 OpenWebUI，进入 **Workspace** -> **Prompts** 并点击 **Create Prompt**。
4. 填写标题后，将复制的文本粘贴进内容。
5. 在日常会话中，键入 `/` 呼出提示词，选择该模板并填充对应字段后发送即可。

## ⚙️ 动态变量 (Variables)

该模板使用 OpenWebUI 官方原生支持的提示词动态变量规范：

| 变量名 | 类型 | 选项 / 默认值 | 描述说明 |
| :--- | :--- | :--- | :--- |
| **target_role** | `text` | `AI Assistant` | 目标 Agent 应扮演的专家角色。 |
| **complexity** | `select` | `Basic`, **`Intermediate`**, `Advanced` | 输出结果的拆解深度（Basic 等）。 |
| **output_style** | `select` | **`Markdown Template`**, `JSON`, `Step-by-Step`| 提示词的结构化展示样式，如 Json/Md。 |
| **requirements** | `textarea`| 必填 | 用户输入的原始自然语言需求文本。 |

## ⭐ 支持

如果该提示词扩展对您有所帮助，欢迎在 GitHub 给 [OpenWebUI Extensions](https://github.com/Fu-Jie/openwebui-extensions) 点一个 Star，这是我最大的动力！
