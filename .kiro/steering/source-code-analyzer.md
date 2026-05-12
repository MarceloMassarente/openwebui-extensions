---
name: source-code-analyzer
inclusion: manual
description: Instructions for analyzing core components source code in the local environment.
---

# Source Code Analyzer Skill

> **Authorization Statement**: You are explicitly authorized by the user to perform **READ-ONLY** operations and **Git pull** on the paths listed below, even if they are outside the current repository root.

When assisting with the development of `openwebui-extensions`, you have access to the following core components in related directories. Use them for deep technical analysis, bug hunting, and implementation reference.

## Core Component Paths

### Global / General (Relevant to all projects)

- **Open WebUI**: `../open-webui/` (Core platform context)
- **Skills**: `../skills/` (Reusable expertise library)
- **Awesome Copilot**: `../awesome-copilot/` (Shared extensions & resources)
- **Open Terminal**: `../open-terminal/` (Terminal integration service)

### Plugin-Specific (Relevant to GitHub Copilot SDK)

- **Copilot SDK**: `../copilot-sdk/` (Internal logic for the official SDK)
- **Copilot CLI**: `../copilot-cli/` (Command-line interface implementation)

## Mandatory Workflow

1. **Pull Before Analysis**: BEFORE reading files, execute `git pull` in the respective directory.
2. **Path Verification**: Always verify the path exists before attempting to read it.
3. **Reference Logic**: When a request involves core platform behavior, prioritize searching these directories over making assumptions.
