---
name: release-finalizer
inclusion: manual
description: Merges a release PR, associates it with resolved issues, replies to issue reporters, and closes issues. Use after PR review is complete and ready for merge.
---

# Release Finalizer

## Overview

Completes the final step of the release cycle: merging the release PR to `main`, replying to all related issues with solutions, and automatically closing them.

## Prerequisites

- The PR is in `OPEN` state and ready to merge
- All status checks have passed
- All review feedback has been addressed

---

## Workflow

### Step 1 — Pre-Merge Verification

```bash
PAGER=cat GH_PAGER=cat gh pr view <PR-NUMBER> --json state,statusCheckRollup,reviewDecision
```

### Step 2 — Identify Related Issues

Look for `Closes #XX`, `Fixes #XX`, `Resolves #XX` in PR description and commits.

### Step 3 — Select Merge Strategy

Default: `--squash` for release PRs.

### Step 4 — Execute Merge

```bash
gh pr merge <PR-NUMBER> \
  --squash \
  --delete-branch \
  -m "type(scope): description" \
  -b "- Bullet 1\n\nCloses #48"
```

### Step 5 — Post Closing Message

```bash
gh issue comment <ISSUE-NUMBER> --body "This has been fixed in PR #<PR-NUMBER>. Thank you for reporting! ⭐"
```

## Anti-Patterns to Avoid

- ❌ Do NOT merge if any status checks are PENDING or FAILED
- ❌ Do NOT merge without `Closes #XX` keywords for related issues
- ❌ Do NOT delete the branch if it might be needed for cherry-pick
