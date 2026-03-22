# Pipeline Plugins

Pipelines are complex workflows that combine multiple processing steps for advanced use cases.

## What are Pipelines?

Pipelines extend beyond simple transformations to implement:

- :material-workflow: Multi-step processing workflows
- :material-source-merge: Model orchestration
- :material-robot-industrial: Advanced agent behaviors
- :material-cog-box: Complex business logic

---

## Available Pipeline Plugins

<div class="grid cards" markdown>

-   :material-view-module:{ .lg .middle } **Wisdom Synthesizer**
    [:octicons-tag-24: v0.1.0](https://github.com/Fu-Jie/open-webui-pipeline-wisdom-synthesizer){ .bubble }

    An external pipeline filter that refactors aggregate requests with collective wisdom to output structured expert reports.

    [:octicons-arrow-right-24: Documentation](wisdom-synthesizer.md)

</div>

---

## How Pipelines Differ

| Feature | Filters | Pipes | Pipelines |
|---------|---------|-------|-----------|
| Complexity | Simple | Medium | High |
| Use Case | Message processing | Model integration | Multi-step workflows |
| Execution | Before/after LLM | As LLM | Custom orchestration |
| Dependencies | Minimal | API access | Often multiple services |

---

## Quick Installation

1. Download the pipeline `.py` file
2. Navigate to **Admin Panel** → **Settings** → **Functions**
3. Upload and configure required services
4. Enable the pipeline

---

## Development Considerations

Pipelines often require:

- Multiple API integrations
- State management across steps
- Error handling at each stage
- Performance optimization

See the [Plugin Development Guide](../../development/plugin-guide.md) for detailed guidance.
