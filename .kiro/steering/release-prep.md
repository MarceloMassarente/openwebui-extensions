---
name: release-prep
inclusion: manual
description: Orchestrates the full release preparation flow for a plugin — version sync across 7+ files, bilingual release notes creation, and commit message drafting. Use before submitting a PR.
---

# Release Prep

## Overview

Drives the complete pre-PR release pipeline. Enforces that every release synchronizes the version number and changelog across at least 7 locations before a commit is created.

## Scope

This skill covers:
1. Version sync (delegates detail to `version-bumper` if needed)
2. Bilingual release notes file creation
3. 7-location consistency verification
4. Conventional Commits message drafting
5. `git add -A && git commit` execution

It **stops before** `git push` or `gh pr create`. Use the `pr-submitter` skill for those steps.

---

## Workflow

### Step 1 — Collect Release Info

- **Plugin name** and **type** (actions / filters / pipes / tools)
- **New version number** (e.g., `0.8.0`)
- **Key changes** in English and Chinese

### Step 2 — Sync Version Across 7 Locations

| # | File | Location |
|---|------|----------|
| 1 | `plugins/{type}/{name}/{name}.py` | `version:` in docstring |
| 2 | `plugins/{type}/{name}/README.md` | metadata line |
| 3 | `plugins/{type}/{name}/README_CN.md` | metadata line |
| 4 | `docs/plugins/{type}/{name}.md` | metadata line |
| 5 | `docs/plugins/{type}/{name}.zh.md` | metadata line |
| 6 | `docs/plugins/{type}/index.md` | version badge |
| 7 | `docs/plugins/{type}/index.zh.md` | version badge |

### Step 3 — Update What's New (All 4 Doc Files)

Only the most recent release's changes. Previous entries removed.

### Step 4 — Create Bilingual Release Notes Files

- `plugins/{type}/{name}/v{version}.md`
- `plugins/{type}/{name}/v{version}_CN.md`

### Step 5 — Verify Consistency

```bash
python3 scripts/check_version_consistency.py
```

### Step 6 — Draft Conventional Commits Message

English only. Format: `type(scope): subject`

### Step 7 — Stage and Commit

```bash
git add -A
git commit -m "<approved commit message>"
```

## Anti-Patterns to Avoid

- ❌ Do NOT add extra features during release prep
- ❌ Do NOT push or create PR in this skill — use `pr-submitter`
- ❌ Do NOT leave stale What's New content from prior versions
