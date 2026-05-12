---
name: test-copilot-pipe
inclusion: manual
description: Automated deployment and testing of GitHub Copilot SDK Pipe plugin for frontend/backend status stability.
---

# Test Copilot Pipe

A universal testing framework for publishing the latest `github_copilot_sdk.py` (Pipe) code to a local OpenWebUI instance and verifying it via automated browser testing.

## Static Environment Info

| Attribute | Fixed Value |
|------|--------|
| **Deployment Script** | `scripts/deploy_pipe.py` |
| **Python Path** | `python3` (use conda ai env) |
| **Test URL** | `http://localhost:3003/?model=github_copilot_official_sdk_pipe.github_copilot_sdk-gpt-4.1` |

## Standard Workflow

### Step 1: Analyze Changes & Plan Test

Define the purpose of this test turn based on code changes.

### Step 2: Deploy Latest Code

```bash
python3 scripts/deploy_pipe.py
```

Look for `✅ Successfully updated... version X.X.X`.

### Step 3: Verify via Browser

Access the test URL, inject a test prompt, wait for response, and verify expected behavior.

### Step 4: Evaluate & Iterate

- **PASS**: Report success.
- **FAIL**: Analyze, modify code, re-run workflow.
