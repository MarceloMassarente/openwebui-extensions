---
name: pr-reviewer
inclusion: manual
description: Fetches PR review comments, analyzes requested changes, implements fixes, commits and pushes the resolution. Use after a reviewer has left comments on an open PR to close the feedback loop efficiently.
---

# PR Reviewer

## Overview

This skill automates the response cycle for code review. When a reviewer leaves comments on a Pull Request, this skill fetches all pending feedback, categorizes issues by severity, implements fixes, and submits a follow-up commit with appropriate review response comments.

## Prerequisites

- An open PR exists with pending review comments
- The local branch matches the PR's head branch
- `gh` CLI is authenticated

---

## Workflow

### Step 1 — Fetch Review State

Retrieve all review comments and overall review status:

```bash
# Get overall review decisions
PAGER=cat GH_PAGER=cat gh pr view <PR-NUMBER> --json reviews,reviewDecision,headRefName \
  --jq '{decision: .reviewDecision, reviews: [.reviews[] | {author: .author.login, state: .state, body: .body}]}'

# Get inline code comments (specific line comments)
PAGER=cat GH_PAGER=cat gh api repos/Fu-Jie/openwebui-extensions/pulls/<PR-NUMBER>/comments \
  --jq '[.[] | {path: .path, line: .line, body: .body, author: .user.login, id: .id}]'

# Get general issue comments
PAGER=cat GH_PAGER=cat gh issue view <PR-NUMBER> --comments --json comments \
  --jq '[.comments[] | {author: .author.login, body: .body}]'
```

### Step 2 — Categorize Review Feedback

| Category | Examples | Action |
|----------|---------|--------|
| **Code Bug** | Logic error, incorrect variable | Fix code immediately |
| **Style / Formatting** | Indentation, naming convention | Fix code |
| **Documentation** | Missing i18n key, wrong version | Fix docs |
| **Design Question** | Suggestion to restructure | Discuss with user before implementing |
| **Nitpick / Optional** | Minor style preferences | Fix if quick; document if skipped |
| **Blocking** | Reviewer explicitly blocks merge | Must fix before proceeding |

### Step 3 — Implement Fixes

For each accepted fix, apply the change and verify.

### Step 4 — Stage and Commit

```bash
git add -A
git commit -m "fix(scope): address review feedback"
```

### Step 5 — Push

```bash
git push origin $(git branch --show-current)
```

### Step 6 — Respond to Reviewers

```bash
gh api repos/Fu-Jie/openwebui-extensions/pulls/<PR-NUMBER>/comments/<COMMENT-ID>/replies \
  -X POST -f body="Fixed in commit <SHORT-SHA>."
```

## Anti-Patterns to Avoid

- ❌ Do NOT `git commit --amend` on a pushed commit without user approval
- ❌ Do NOT silently skip a reviewer's comment
- ❌ Do NOT use `--force` (only `--force-with-lease` when necessary)
- ❌ Do NOT make unrelated changes in the fixup commit
