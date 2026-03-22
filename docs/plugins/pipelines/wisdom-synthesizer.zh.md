# Wisdom Synthesizer (集体智慧合成器)

专为 **Open WebUI** 设计的外置管道过滤器（Pipeline/Filter），旨在通过智能拦截并重构多模型汇总请求，发挥集体智慧（Collective Wisdom），将原本较为**基础和扁平的常规汇总**熔炼为结构清晰、具备多维对比度的**专家级综合分析报告**。

![效果演示](wisdom_synthesizer.gif)

---

## 🚀 核心功能

* **智能拦截**：自动捕获 Open WebUI 的“汇总多模型响应”请求（通过内置前缀触发）。
* **动态解析**：剥离多余格式，精准提取**原始用户问题**与**各模型的独立回答**。
* **智慧融合**：摒弃基础的模型合并，强制总结模型扮演“首席分析师”，发挥集体智慧审视全局。
* **规范输出**：将汇总响应熔炼为以下结构：
  * **【核心共识】**: 提炼模型间的相同点。
  * **【关键分歧】**: 对比不同视角的碰撞。
  * **【独特洞察】**: 发现单一模型闪光点。
  * **【综合建议】**: 最终形成有弹性的熔铸方案。

---

## 📦 安装与使用 (Pipelines 模式)

> [!IMPORTANT]
> **前提条件**：
> 本插件依赖于 Open WebUI 官方的 **[open-webui/pipelines](https://github.com/open-webui/pipelines)** 框架插件系统。请确保你的 Open WebUI 后端已经架设好或已连接底层的 `pipelines` 服务端环境。

本插件为单文件管道过滤组件，支持在面板中一键拉取安装：

### 🚀 通过 URL 一键导入 (推荐 🌟)

1. 登录你的 Open WebUI 后台，进入 **管理员设置** -> **Pipelines** 选项卡。
2. 点击 **“添加 Pipeline”**，并在地址栏中复制贴入此仓库中 `wisdom_synthesizer.py` 的 **GitHub Raw 链接**。
3. 点击 **保存** 即可成功加载。

以下是操作动态演示：

![安装操作图](install.gif)

---

## ⚙️ Valves 管道配置

进入管道配置项，可动态调整以下参数：

| 参数 | 默认值 | 说明 |
| :--- | :--- | :--- |
| `pipelines` | `["*"]` | 应用此 Filter 的目标模型 ID *（如果要全局生效保持默认）* |
| `priority` | `0` | 过滤器管道执行优先级（数字越小，越优先执行） |
| `model_id` | `None` | (可选) 强制将汇总任务流向你指定的某个专用高性能总结模型 |
| `trigger_prefix` | `You have been provided...` | 用于触发拦截的提示词起始句柄前缀。一般无需修改 |
| `query_start_marker` | `'the latest user query: "'` | 解析原始查询的起始标记锚点 |
| `query_end_marker` | `'"\n\nYour task is to'` | 解析原始查询的结束标记锚点 |
| `response_start_marker` | `"Responses from models: "` | 解析各个模型独立响应的起始锚点标志 |

> [!TIP]
> **配置建议**：
> 默认值 `["*"]` 可在所有选定的汇总模型上自适应生效。在绝大多数情况下，你**仅需保持此默认参数**便可保障全局自适应拦截。

---

## 🤝 友情链接 (Related Projects)

如果你对 Open WebUI 的扩展生态感兴趣，欢迎关注我的其它开源方案：

*   🚀 **[openwebui-extensions](https://github.com/Fu-Jie/openwebui-extensions)** —— 包含各种增强 Actions、Pipes、Tools 等一篮子开源插件合集，助你解锁更多黑魔法。
*   🪄 **[open-webui-prompt-plus](https://github.com/Fu-Jie/open-webui-prompt-plus)** —— 包含 AI 驱动的提示词生成器、Spotlight 搜索框及交互变量表单，极速拉满提示词工程。

---

## 📄 开源许可

[MIT License](LICENSE)
