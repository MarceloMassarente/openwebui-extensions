---
name: pr-submitter
inclusion: manual
description: Submits a feature branch as a Pull Request with a validated, properly formatted bilingual PR body. Handles shell-escape-safe body writing via temp files. Use after release-prep has committed all changes.
---

# PR Submitter

## Overview

This skill handles the final step of pushing a feature branch and creating a validated Pull Request on GitHub. It avoids shell-escaping pitfalls by always writing the PR body to a **temp file** first.

## Prerequisites

- All changes are committed (use `release-prep` skill first)
- The `gh` CLI is authenticated (`gh auth status`)
- Current branch is NOT `main` or `master`

---

## Workflow

### Step 1 — Pre-Flight Checks

```bash
git branch --show-current
git log origin/$(git branch --show-current)..HEAD --oneline 2>/dev/null || echo "No remote tracking branch yet"
gh auth status
```

### Step 2 — Build PR Body File

Always write to `.temp/pr_body.md`:

```bash
mkdir -p .temp
cat > .temp/pr_body.md << 'HEREDOC'
## Summary
...
## Changes
...
## 变更摘要（中文）
...
HEREDOC
```

### Step 3 — Validate PR Body

```bash
grep -q "## Summary" .temp/pr_body.md && echo "✅ Summary"
grep -q "## Changes" .temp/pr_body.md && echo "✅ Changes"
grep -q "## 变更摘要" .temp/pr_body.md && echo "✅ CN Section"
```

### Step 4 — Push Branch

```bash
git push -u origin $(git branch --show-current)
```

### Step 5 — Create Pull Request

```bash
gh pr create \
  --base main \
  --head $(git branch --show-current) \
  --title "<PR title>" \
  --body-file .temp/pr_body.md
```

Always use `--body-file`, never `--body` with inline markdown.

### Step 6 — Cleanup

```bash
rm -f .temp/pr_body.md
```

## Anti-Patterns to Avoid

- ❌ Never use `--body "..."` with multi-line content
- ❌ Never force-push without explicit user confirmation
- ❌ Never target `main` as the source branch
- ❌ Never skip the body validation step
