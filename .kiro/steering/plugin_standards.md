---
inclusion: fileMatch
fileMatchPattern: "plugins/**"
---
# Plugin Development Standards

## README Documentation

All plugins MUST follow the standard README template.

**Reference Template**: #[[file:docs/PLUGIN_README_TEMPLATE.md]]

### Language Requirements

- **English Version (`README.md`)**: The primary documentation source. Must follow the template strictly.
- **Chinese Version (`README_CN.md`)**: MUST be translated based on the English version (`README.md`) to ensure consistency in structure and content.

### Metadata Requirements

Use this exact header format (copied directly — same for EN and CN):

English:

```markdown
| By [Fu-Jie](https://github.com/Fu-Jie) · vX.Y.Z | [⭐ Star this repo](https://github.com/Fu-Jie/openwebui-extensions) |
| :--- | ---: |

| ![followers](https://img.shields.io/endpoint?url=https%3A%2F%2Fgist.githubusercontent.com%2FFu-Jie%2Fdb3d95687075a880af6f1fba76d679c6%2Fraw%2Fbadge_followers.json&label=%F0%9F%91%A5&style=flat) | ![points](https://img.shields.io/endpoint?url=https%3A%2F%2Fgist.githubusercontent.com%2FFu-Jie%2Fdb3d95687075a880af6f1fba76d679c6%2Fraw%2Fbadge_points.json&label=%E2%AD%90&style=flat) | ![top](https://img.shields.io/badge/%F0%9F%8F%86-Top%20%3C1%25-10b981?style=flat) | ![contributions](https://img.shields.io/endpoint?url=https%3A%2F%2Fgist.githubusercontent.com%2FFu-Jie%2Fdb3d95687075a880af6f1fba76d679c6%2Fraw%2Fbadge_contributions.json&label=%F0%9F%93%A6&style=flat) | ![downloads](https://img.shields.io/endpoint?url=https%3A%2F%2Fgist.githubusercontent.com%2FFu-Jie%2Fdb3d95687075a880af6f1fba76d679c6%2Fraw%2Fbadge_downloads.json&label=%E2%AC%87%EF%B8%8F&style=flat) | ![saves](https://img.shields.io/endpoint?url=https%3A%2F%2Fgist.githubusercontent.com%2FFu-Jie%2Fdb3d95687075a880af6f1fba76d679c6%2Fraw%2Fbadge_saves.json&label=%F0%9F%92%BE&style=flat) | ![views](https://img.shields.io/endpoint?url=https%3A%2F%2Fgist.githubusercontent.com%2FFu-Jie%2Fdb3d95687075a880af6f1fba76d679c6%2Fraw%2Fbadge_views.json&label=%F0%9F%91%81%EF%B8%8F&style=flat) |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
```

Chinese:

```markdown
| 作者：[Fu-Jie](https://github.com/Fu-Jie) · vX.Y.Z | [⭐ 点个 Star 支持项目](https://github.com/Fu-Jie/openwebui-extensions) |
| :--- | ---: |

| ![followers](https://img.shields.io/endpoint?url=https%3A%2F%2Fgist.githubusercontent.com%2FFu-Jie%2Fdb3d95687075a880af6f1fba76d679c6%2Fraw%2Fbadge_followers.json&label=%F0%9F%91%A5&style=flat) | ![points](https://img.shields.io/endpoint?url=https%3A%2F%2Fgist.githubusercontent.com%2FFu-Jie%2Fdb3d95687075a880af6f1fba76d679c6%2Fraw%2Fbadge_points.json&label=%E2%AD%90&style=flat) | ![top](https://img.shields.io/badge/%F0%9F%8F%86-Top%20%3C1%25-10b981?style=flat) | ![contributions](https://img.shields.io/endpoint?url=https%3A%2F%2Fgist.githubusercontent.com%2FFu-Jie%2Fdb3d95687075a880af6f1fba76d679c6%2Fraw%2Fbadge_contributions.json&label=%F0%9F%93%A6&style=flat) | ![downloads](https://img.shields.io/endpoint?url=https%3A%2F%2Fgist.githubusercontent.com%2FFu-Jie%2Fdb3d95687075a880af6f1fba76d679c6%2Fraw%2Fbadge_downloads.json&label=%E2%AC%87%EF%B8%8F&style=flat) | ![saves](https://img.shields.io/endpoint?url=https%3A%2F%2Fgist.githubusercontent.com%2FFu-Jie%2Fdb3d95687075a880af6f1fba76d679c6%2Fraw%2Fbadge_saves.json&label=%F0%9F%92%BE&style=flat) | ![views](https://img.shields.io/endpoint?url=https%3A%2F%2Fgist.githubusercontent.com%2FFu-Jie%2Fdb3d95687075a880af6f1fba76d679c6%2Fraw%2Fbadge_views.json&label=%F0%9F%91%81%EF%B8%8F&style=flat) |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
```

### Structure Checklist

1. **Title & Description** — One sentence, concise. Avoid 5+ bullet point lists here.
2. **Header Metadata Table** (Author, version, repo star link)
3. **Preview** (Screenshot, GIF, or a short note if preview is not ready)
4. **Install with Batch Install Plugins** (Include the fixed prompt block)
   Use the generic prompt `Install plugin from Fu-Jie/openwebui-extensions` instead of hard-coding the plugin name.
5. **What's New** (Keep last 1 version only in README; full changelog on GitHub)
6. **Key Capabilities** — Keep to ~8-9 items. One-line descriptions.
7. **How to Use** — 2-4 representative examples. Keep it short.
8. **Configuration (Valves)**
   - If valves > ~10: show only essential/required parameters here
   - Link to detailed documentation with absolute GitHub URL, e.g.:
     `Full parameter list: https://github.com/Fu-Jie/openwebui-extensions/blob/main/plugins/{type}/{name}/TUTORIAL.md`
9. **Support** — Must appear before Troubleshooting
10. **Troubleshooting** (Must include link to GitHub Issues and mention official-version conflict if relevant)

### Design Principles

- **Scannability first**: Keep README short enough that users can reach the Star button without excessive scrolling. If content grows beyond ~120 lines, extract details to a separate TUTORIAL doc.
- **No `<br>` in tables**: Markdown tables don't render `<br>` consistently. Use commas or semicolons to separate items in a single cell.
- **Concise feature descriptions**: Avoid bullet-point lists in the opening description. One sentence is better.
- **Accurate capability naming**: Don't use vague terms like "sandbox" (say "privacy isolation where possible"). Don't claim "data analysis" for file bypass — say "bypass RAG parsing".
- **Persistence context**: If tools/installations persist (e.g., in Docker data dir), mention it — users care about whether their setup survives restarts.
- **Session Mode / Agent Team**: If the plugin supports these, mention them prominently in both the one-line description and Key Capabilities.
- **Link to detailed docs**: When a plugin has many valves, always provide an absolute GitHub URL to the full documentation. Don't dump all parameters in the README.
