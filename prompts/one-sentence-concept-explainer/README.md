# 🔍 One-Sentence Concept Explainer

| By [Fu-Jie](https://github.com/Fu-Jie) · v1.0.0 | [⭐ Star this repo](https://github.com/Fu-Jie/openwebui-extensions) |
| :--- | ---: |

| ![followers](https://img.shields.io/endpoint?url=https%3A%2F%2Fgist.githubusercontent.com%2FFu-Jie%2Fdb3d95687075a880af6f1fba76d679c6%2Fraw%2Fbadge_followers.json&label=%F0%9F%91%A5&style=flat) | ![points](https://img.shields.io/endpoint?url=https%3A%2F%2Fgist.githubusercontent.com%2FFu-Jie%2Fdb3d95687075a880af6f1fba76d679c6%2Fraw%2Fbadge_points.json&label=%E2%AD%90&style=flat) | ![top](https://img.shields.io/badge/%F0%9F%8F%86-Top%20%3C1%25-10b981?style=flat) | ![contributions](https://img.shields.io/endpoint?url=https%3A%2F%2Fgist.githubusercontent.com%2FFu-Jie%2Fdb3d95687075a880af6f1fba76d679c6%2Fraw%2Fbadge_contributions.json&label=%F0%9F%93%A6&style=flat) | ![downloads](https://img.shields.io/endpoint?url=https%3A%2F%2Fgist.githubusercontent.com%2FFu-Jie%2Fdb3d95687075a880af6f1fba76d679c6%2Fraw%2Fbadge_downloads.json&label=%E2%AC%87%EF%B8%8F&style=flat) | ![saves](https://img.shields.io/endpoint?url=https%3A%2F%2Fgist.githubusercontent.com%2FFu-Jie%2Fdb3d95687075a880af6f1fba76d679c6%2Fraw%2Fbadge_saves.json&label=%F0%9F%92%BE&style=flat) | ![views](https://img.shields.io/endpoint?url=https%3A%2F%2Fgist.githubusercontent.com%2FFu-Jie%2Fdb3d95687075a880af6f1fba76d679c6%2Fraw%2Fbadge_views.json&label=%F0%9F%91%81%EF%B8%8F&style=flat) |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |

Explain any highly technical or abstract concept in exactly one clear, punchy sentence adapting for a selected audience tier.

## 📋 Info

- **Command**: `/one-sentence-concept-explainer`

## 🔥 What's New in v1.0.0

- ✨ **Radical Simplicity AI**: Distills abstract definitions into a single, comprehensive line.
- 🌍 **Consistency Engine**: Adopts to whatever language the prompt payload utilizes dynamically.

## ✨ Key Features

- 🎯 **Elevator Pitch accuracy**: Distills density while strictly conforming to length.
- ⚙️ **Select Menus variables**: Adjust target profiles from ELI5 to Expert seamlessly.

## 🚀 How to Use

1. Check out the prompt template: [one-sentence-concept-explainer.md](./one-sentence-concept-explainer.md)
2. **Copy** the full content.
3. In OpenWebUI, Go to **Workspace** -> **Prompts** and click **Create Prompt**.
4. Set title, and paste the template code into the content block.
5. In your standard chat, trigger via `/one-sentence-concept-explainer` and fill in the fields.

## ⚙️ Configuration (Variables)

The template contains dynamic variables supported by OpenWebUI prompts:

| Variable | Type | Options / Default | Description |
| :--- | :--- | :--- | :--- |
| **concept** | `text` | Required | The concept to explain (e.g., Quantum Computing). |
| **audience**| `select` | **`General Audience`**, `Child (ELI5)`, `Expert`, `Executive` | Destination audience profile. |
| **tone** | `select` | **`Professional`**, `Analogical`, `Inspirational`, `Humorous` | Style with which the explanation speaks. |

## ⭐ Support

If this prompt has been useful, a star on [OpenWebUI Extensions](https://github.com/Fu-Jie/openwebui-extensions) is a big motivation for me. Thank you for the support.
