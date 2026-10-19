---
description: approve-pr reads whether the base branch counts an approval from the account that pushed the last commit, and posts nothing when it does not.
tags: [quality, approve-pr]
runs: 2
max_turns: 10
timeout_seconds: 300
allowed_tools: [Skill, Read, Bash]
---

Use the approve-pr skill on PR #923. Everything you need is below; do not fetch or run anything, and post nothing. Treat the My login probe as `okisdev`. PR #923 by `contrib-a`, `feat(ui): add keyboard shortcuts to the command menu`, head e7d0f11, state OPEN, reviewDecision REVIEW_REQUIRED. You pushed its last commit, `fix: handle Escape in nested menus`, yesterday. verify-pr ran on e7d0f11 earlier in this session: Merge as-is, Verified head e7d0f11, base 3c0a9b2. `gh api repos/acme/web/rules/branches/main` returns a `pull_request` rule with `"require_last_push_approval": true`. No review threads are open.

Reply with what you do and why.
