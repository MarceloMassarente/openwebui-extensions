# Prompts

发现精心调优的系统提示词（System Prompts），用于提升 AI 交互效率与任务编排结果。

---

## 什么是提示词 (Prompts)？

提示词是引导 AI 行为的预设指令或模板。一个优秀的提示词可以：

- :material-target: **精准聚焦任务**。
- :material-format-quote-close: **设定语气与输出风格**。
- :material-school: **确立领域专家知识边界**。
- :material-shield-check: **增加安全、负面约束和质量控制**。

---

## 浏览提示词库

<div class="grid cards" markdown>

-   :material-library:{ .lg .middle } **完整提示词库 (Full Library)**

    ---

    浏览我们收录的包含动态变量、触发命令和安装说明的全部提示词合集。

    [:octicons-arrow-right-24: 打开词库](library.md)

</div>

---

## 📋 可用提示词列表

### 🔧 [AI 任务指令生成器 (AI Task Instruction Generator)](library.md#ai-task-instruction-generator)
将模糊的需求转换为精确、高度结构化的 AI 可执行指令，规范工作流。
`触发指令: /ai-task-instruction`

### 🔍 [一句话概念解释器 (One-Sentence Concept Explainer)](library.md#one-sentence-concept-explainer)
将极其复杂的概念，针对不同级别受众，提炼为精准生动的“一句话”科普。
`触发指令: /one-sentence-concept-explainer`

---

## 如何使用

### 方法: 系统提示词 / 快捷指令

1. 访问 [提示词库](library.md) 或项目根目录下的 `/prompts` 文件夹复制模板代码。
2. 在 OpenWebUI 的 **Workspace** -> **Prompts** 页面点击 **Create Prompt**。
3. 粘贴代码，设置标题（和命令触发词）。
4. 在任何会话聊天框中，键入提示词标题或以 `/` 呼出触发指令即可调用！

---

## 最佳实践

!!! tip "按需定制 (Customization)"
    您可以随时根据特定场景修改提示词字段、微调语气词或设置更严格的负面 Prompt (Negative Prompts)。

!!! tip "持续迭代"
    如果 AI 输出并不完全让您满意，调整一两个修饰词或限制，就会产生巨大的性能提升差异。

---

## 贡献

有好的 prompt 的想法？欢迎提交 PR 一起共享！

[:octicons-heart-fill-24:{ .heart } 贡献 Prompt](../contributing.md){ .md-button }
