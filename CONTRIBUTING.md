# Contributing Guide

Thank you for your interest in **OpenWebUI Extensions**!

## 🚀 How to Contribute

1. **Fork** this repository.
2. **Add/Modify** the plugin file in the `plugins/` directory.
3. **Prepare release surfaces** for versioned plugin updates.
4. **Submit PR**: We will review and merge it.

## 🤖 Agent-Assisted Release Prep

For plugin releases or versioned updates, contributors may use or reference the repository skill at `.github/skills/release-prep/SKILL.md`.

- Use `release-prep` as the source-of-truth workflow for version sync, bilingual release notes, consistency verification, and Conventional Commit drafting.
- Ask your agent to prepare the plugin release before opening the PR, including the plugin file, bilingual READMEs, mirrored docs pages, docs indexes, and versioned release notes.
- `release-prep` stops before `git push` or PR creation. After prep is complete, continue with the normal PR flow and the documented release workflow.

## 💡 Important

- Ensure your plugin includes complete metadata (title, author, version, description).
- If updating an existing plugin, please **increment the version number** (e.g., `0.1.0` -> `0.1.1`) to trigger the auto-update.
- For plugin updates, include both `README.md` and `README_CN.md`, and keep release notes bilingual.

Thank you! 🚀
