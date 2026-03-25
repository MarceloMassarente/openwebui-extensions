# OpenWebUI Skills 管理工具

**Author:** [Fu-Jie](https://github.com/Fu-Jie/openwebui-extensions) | **Version:** 0.3.1 | **Project:** [OpenWebUI Extensions](https://github.com/Fu-Jie/openwebui-extensions)

一个可跨模型使用的 OpenWebUI 原生 Tool 插件，用于管理 Workspace Skills。

## 最新更新

- `install_skill` 现已支持远程 `SKILL.md` 中的多行 `description: >` / `description: |` frontmatter 描述。
- 新增 `title` 作为 `name` 缺失时的元数据回退，并补齐 CRLF 与 YAML 块标量回归测试。

## 核心特性

- 原生技能管理
- 用户范围内的 list/show/install/create/update/delete
- 每步操作提供状态栏反馈

## 方法

- `list_skills`
- `show_skill`
- `install_skill`
- `create_skill`
- `update_skill`
- `delete_skill`

## 安装方式

1. 打开 OpenWebUI → Workspace → Tools
2. 在官方市场安装 **OpenWebUI Skills 管理工具**
3. 保存并在模型/聊天中启用

### 手动安装（备选）

- 新建 Tool 并粘贴：
   - `plugins/tools/openwebui-skills-manager/openwebui_skills_manager.py`
