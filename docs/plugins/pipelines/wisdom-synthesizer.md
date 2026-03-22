# Wisdom Synthesizer (Collective Wisdom Synthesizer)

An external pipeline filter (Pipeline/Filter) for **Open WebUI** that intercepts multi-model aggregate requests to leverage collective wisdom, reshaping **basic and linear aggregate outputs** into structured, high-contrast **expert analysis reports**.

![Effect Demonstration](https://raw.githubusercontent.com/Fu-Jie/open-webui-pipeline-wisdom-synthesizer/main/wisdom_synthesizer.gif)

---

## 🚀 Key Features

* **Smart Interception**: Automatically catches Open WebUI's “Summarize various models' responses” requests.
* **Dynamic Parsing**: Strips away generic formatting and precisely extracts the **original user query** and **each model's individual response**.
* **Wisdom Fusion**: Directs the summary model to act as a “Chief Analyst”, enforcing a critical evaluation workflow instead of generic merging.
* **Standardized Output Structure**: Guarantees output layout includes:
  * **【Core Consensus】**: Aggregated common ground across models.
  * **【Key Divergences】**: Comparative breakdown of different perspectives/approaches.
  * **【Unique Insights】**: Spotlighting innovative points found in a single model.
  * **【Synthesis & Recommendation】**: An action-oriented, blended strategy set.

---

## 📦 Installation & Usage (Pipelines Mode)

> [!IMPORTANT]
> **Prerequisite**:
> This plugin relies on the official **[open-webui/pipelines](https://github.com/open-webui/pipelines)** framework. Please ensure your Open WebUI backend is already connected to an active `pipelines` runner environment beforehand.

This plugin runs as a single-file pipeline filter component and supports importing with just a single click:

### 🚀 One-Click Import via URL (Recommended 🌟)

1. Log into your Open WebUI board, go to **Admin settings** -> **Pipelines** tab.
2. Click **“Add Pipeline”** and paste the **GitHub Raw link** of `wisdom_synthesizer.py` into the address bar.
3. Save configurations to load automatically.

Below is the visual operational guide for getting it loaded:

![Installation Guide](https://raw.githubusercontent.com/Fu-Jie/open-webui-pipeline-wisdom-synthesizer/main/install.gif)

---

## ⚙️ Valves Configuration

Configuration items inside safe Valves toggles:

| Parameter | Default | Description |
| :--- | :--- | :--- |
| `pipelines` | `["*"]` | Target model IDs to apply this Filter to *（Keep default for global）* |
| `priority` | `0` | Filter pipeline execution order priority (lower numbers execute first). |
| `model_id` | `None` | (Optional) Force the summarize job to run on a dedicated high-spec summary model. |
| `trigger_prefix` | `You have been provided...` | Pre-set phrase to trigger interception. Usually requires no changes. |
| `query_start_marker` | `'the latest user query: "'` | Anchor used to locate the start of the original query. |
| `query_end_marker` | `'"\n\nYour task is to'` | Anchor used to locate the end of the original query. |
| `response_start_marker` | `"Responses from models: "` | Anchor used to locate where the model responses begin. |

> [!TIP]
> **Configuration Tip**:
> The default `["*"]` allows the filter to securely adapt to any aggregator models chosen on the fly. In most scenarios, **keeping this default configuration** is highly recommended.

---

## 🤝 Related Projects

If you're building inside the Open WebUI ecosystem, you might find my other plugins sets helpful:

*   🚀 **[openwebui-extensions](https://github.com/Fu-Jie/openwebui-extensions)** —— A comprehensive collection of Actions, Pipes, and Tools to supercharge your workspace.
*   🪄 **[open-webui-prompt-plus](https://github.com/Fu-Jie/open-webui-prompt-plus)** —— Enhances Prompt engineering with AI-powered generators, Spotlight-style searches, and interactive forms.

---

## 📄 License

[MIT License](LICENSE)
