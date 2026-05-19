# 贡献指南

感谢你对 **OpenWebUI Extensions** 感兴趣！

## 🚀 贡献流程

1. **Fork** 本仓库。
2. **修改/添加** `plugins/` 目录下的插件文件。
3. **为带版本的插件更新准备发布面**。
4. **提交 PR**: 我们会尽快审核并合并。

## 🤖 Agent 发布准备

对于插件发布或带版本号的更新，贡献者可以直接使用或参考仓库中的 `.github/skills/release-prep/SKILL.md`。

- 将 `release-prep` 视为发布准备的标准流程来源，用它来完成版本同步、双语发布说明、一致性校验和 Conventional Commits 提交信息草拟。
- 可以要求 agent 在创建 PR 之前先完成发布准备，包括插件文件、双语 README、镜像文档页、索引页以及版本发布说明文件。
- `release-prep` 不会执行 `git push` 或创建 PR。准备完成后，再继续正常的 PR 提交流程和仓库既有的发布流程。

## 💡 注意事项

- 请确保插件包含完整的元数据（title, author, version, description）。
- 如果是更新已有插件，请记得**增加版本号**（如 `0.1.0` -> `0.1.1`），这样系统会自动同步更新。
- 对插件更新，请同时提供 `README.md` 和 `README_CN.md`，并保持发布说明双语同步。

再次感谢你的贡献！🚀
