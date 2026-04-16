---
name: Plugin Documentation
description: Use when writing or updating plugin README files, mirrored docs pages, bilingual release notes, or other user-facing documentation for plugins.
applyTo: "plugins/**/README*.md"
---
# Plugin Documentation Standards

## Delivery Language

- Plugin directories must keep both `README.md` and `README_CN.md`
- When a task includes docs, guides, announcements, release notes, or development docs, prepare both English and Chinese versions for review unless the user explicitly asks for single-language delivery
- Even if only English is committed, provide a Chinese review draft in the conversation when documentation is part of the work

## README Structure

Use this order for plugin READMEs:

1. Title with icon
2. README header
3. One-sentence description
4. `What's New` with only the latest update
5. `Key Features`
6. `How to Use`
7. Configuration or Valves table
8. Support section
9. Other sections such as examples, template notes, troubleshooting, or changelog link

## README Header

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

Guidelines:
- Keep the author link pointing to `https://github.com/Fu-Jie`
- Keep the star link pointing to the repository root
- Put the version on the left-side author line as plain text (`vx.y.z`), not as a badge
- Keep the `Top` badge compact and use the project standard wording (`Top <1%`)
- Do not add a visible label header row above the badges

## Support Section

Use the repository-standard support wording.

English:
`If this plugin has been useful, a star on [OpenWebUI Extensions](https://github.com/Fu-Jie/openwebui-extensions) is a big motivation for me. Thank you for the support.`

Chinese:
`如果这个插件对你有帮助，欢迎到 [OpenWebUI Extensions](https://github.com/Fu-Jie/openwebui-extensions) 点个 Star，这将是我持续改进的动力，感谢支持。`

## Mirror and Sync Rules

When plugin documentation changes, keep these layers aligned as needed:

- Plugin-local README files under `plugins/`
- Mirrored docs pages under `docs/plugins/`
- Plugin index pages under `docs/plugins/<type>/index.md` and `index.zh.md`
- Root `README.md` and `README_CN.md` date badge when preparing a release

Use the `doc-mirror-sync` skill when the task includes mirroring plugin READMEs into `docs/`.

## Changelog Handling

- Keep detailed changelog history in GitHub release history or dedicated docs
- In README files, keep `What's New` focused on the latest version only

## One-Sentence Description

- One sentence only. No bullet-point lists in the opening description.
- If the plugin supports Agent Team or Session Modes, mention them here — this is the first thing users read.
- Example: `This is a **GitHub Copilot SDK** Pipe for **OpenWebUI** with **Agent Team** coordination, **Session Modes** (`autopilot`/`interactive`/`plan`), autonomous **Web Search**, **Context Compaction**, and reuse of your OpenWebUI **Tools, MCP servers, and Skills**.**

## Key Capabilities

- Keep to ~8-9 items maximum. One-line descriptions.
- Order by importance: Agentic AI → Agent Team → Session Mode → Built-in Tools → Web Search → Infinite Sessions → Tools/MCP Bridge → RichUI → Workspace Isolation.
- If a tool or installation persists (e.g., in Docker data dir), mention it — users care about whether their setup survives restarts.
- Use accurate naming: say "privacy isolation where possible" instead of "sandbox"; say "bypass RAG parsing" instead of "data analysis".

## How to Use

- 2-4 representative examples. Keep it short. Don't use generic examples like "Fix the failing tests".

## Configuration (Valves) —分级展示

- **Always keep** the Configuration section in README.
- If valves > ~10: show only essential/required parameters in README; link to full documentation with absolute GitHub URL.
- Example link format: `Full parameter list: https://github.com/Fu-Jie/openwebui-extensions/blob/main/plugins/{type}/{name}/TUTORIAL.md`
- Do NOT use `<br>` in table cells — Markdown tables don't render it consistently. Use commas or semicolons to separate items within a single cell.

## Design Principles

- **Scannability first**: Keep README short enough that users can reach the Star button without excessive scrolling. If content grows beyond ~120 lines, extract details to a separate TUTORIAL doc.
- **Session Mode / Agent Team prominence**: If the plugin supports these, mention them in both the one-line description and Key Capabilities — they are headline features.
- **Persistence context**: Mention when tools or installations persist across sessions/restarts. Users need to know their setup survives Docker restarts.
- **Accurate capability naming**: Avoid vague terms. Be specific about what each capability actually does.
