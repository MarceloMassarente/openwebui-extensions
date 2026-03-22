# 🔍 One-Sentence Concept Explainer (一句话概念解释器)

| 作者: [Fu-Jie](https://github.com/Fu-Jie) · v1.0.0 | [⭐ 给项目点个 Star](https://github.com/Fu-Jie/openwebui-extensions) |
| :--- | ---: |

| ![followers](https://img.shields.io/endpoint?url=https%3A%2F%2Fgist.githubusercontent.com%2FFu-Jie%2Fdb3d95687075a880af6f1fba76d679c6%2Fraw%2Fbadge_followers.json&label=%F0%9F%91%A5&style=flat) | ![points](https://img.shields.io/endpoint?url=https%3A%2F%2Fgist.githubusercontent.com%2FFu-Jie%2Fdb3d95687075a880af6f1fba76d679c6%2Fraw%2Fbadge_points.json&label=%E2%AD%90&style=flat) | ![top](https://img.shields.io/badge/%F0%9F%8F%86-Top%20%3C1%25-10b981?style=flat) | ![contributions](https://img.shields.io/endpoint?url=https%3A%2F%2Fgist.githubusercontent.com%2FFu-Jie%2Fdb3d95687075a880af6f1fba76d679c6%2Fraw%2Fbadge_contributions.json&label=%F0%9F%93%A6&style=flat) | ![downloads](https://img.shields.io/endpoint?url=https%3A%2F%2Fgist.githubusercontent.com%2FFu-Jie%2Fdb3d95687075a880af6f1fba76d679c6%2Fraw%2Fbadge_downloads.json&label=%E2%AC%87%EF%B8%8F&style=flat) | ![saves](https://img.shields.io/endpoint?url=https%3A%2F%2Fgist.githubusercontent.com%2FFu-Jie%2Fdb3d95687075a880af6f1fba76d679c6%2Fraw%2Fbadge_saves.json&label=%F0%9F%92%BE&style=flat) | ![views](https://img.shields.io/endpoint?url=https%3A%2F%2Fgist.githubusercontent.com%2FFu-Jie%2Fdb3d95687075a880af6f1fba76d679c6%2Fraw%2Fbadge_views.json&label=%F0%9F%91%81%EF%B8%8F&style=flat) |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |

将任何高级或抽象的概念，针对不同受众，用极其精练、准确且直击本质的**一句话**向特定的目标受众解释清楚。

## 📋 基础信息

- **触发指令 (Command)**: `/one-sentence-concept-explainer`

## 🔥 版本特性 v1.0.0

- ✨ **极致简约 AI**: 将本来具有门槛的名词解构为一针见血的单一句子，极合电梯游说场景。
- 🌍 **规则回溯对齐**: 全自动化兼容处理，无需人工设定目标输出语言。

## ✨ 核心优势

- 🎯 **杜绝啰嗦**: 遵循严格的一句话长度指令执行率。
- ⚙️ **兼容性高**: 下拉菜单一秒在儿童、专家、高管等维度自由切换密度视角。

## 🚀 如何使用

1. 查看提示词文件：[one-sentence-concept-explainer.md](./one-sentence-concept-explainer.md)
2. **复制** 文件的完整内容。
3. 打开 OpenWebUI，进入 **Workspace** -> **Prompts** 并点击 **Create Prompt**。
4. 填写标题后，将复制的文本粘贴进内容。
5. 在日常会话中，键入 `/` 呼出提示词，选择该模板并填充对应字段后发送即可。

## ⚙️ 动态变量 (Variables)

该模板使用 OpenWebUI 官方原生支持的提示词动态变量规范：

| 变量名 | 类型 | 选项 / 默认值 | 描述说明 |
| :--- | :--- | :--- | :--- |
| **concept** | `text` | 必填 | 要解释的概念（例如：量子纠缠）。 |
| **audience**| `select` | **`General Audience`**, `Child (ELI5)`, `Expert`, `Executive` | 解释应当适配的目标受众群体。 |
| **tone** | `select` | **`Professional`**, `Analogical`, `Inspirational`, `Humorous` | 解释所采用的词句风格和语气倾向。 |

## ⭐ 支持

如果该提示词扩展对您有所帮助，欢迎在 GitHub 给 [OpenWebUI Extensions](https://github.com/Fu-Jie/openwebui-extensions) 点一个 Star，这是我最大的动力！
