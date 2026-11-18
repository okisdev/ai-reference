---
description: approve-pr reads whether the base branch counts an approval from the account that pushed the last commit, and posts nothing when it does not.
tags: [quality, approve-pr]
runs: 2
max_turns: 10
timeout_seconds: 300
allowed_tools: [Skill, Read, Bash]
---

Use the approve-pr skill on PR #923. Everything you need is below; do not fetch or run anything, and post nothing. Treat the My login probe as `okisdev`. PR #923 by `contrib-a`, `feat(ui): add keyboard shortcuts to the command menu`, head e7d0f11, state OPEN, reviewDecision REVIEW_REQUIRED. verify-pr ran on e7d0f11 earlier in this session: Merge as-is, Verified head e7d0f11, base 3c0a9b2. No review threads are open.

`gh pr view 923 --json commits --jq '.commits[] | {oid: .oid[0:7], headline: .messageHeadline, authors: [.authors[].login]}'` prints:

```
{"oid":"5a1c9d2","headline":"feat(ui): add keyboard shortcuts to the command menu","authors":["contrib-a"]}
{"oid":"b83e04c","headline":"test: cover the shortcut registry","authors":["contrib-a"]}
{"oid":"e7d0f11","headline":"fix: handle Escape in nested menus","authors":["okisdev"]}
```

`gh api repos/acme/web/rules/branches/main` prints:

```
[{"type":"deletion","ruleset_id":4102},{"type":"non_fast_forward","ruleset_id":4102},{"type":"required_status_checks","parameters":{"strict_required_status_checks_policy":false,"required_status_checks":[{"context":"test (node 20)"},{"context":"lint"}]},"ruleset_id":4102},{"type":"pull_request","parameters":{"required_approving_review_count":1,"dismiss_stale_reviews_on_push":false,"require_code_owner_review":false,"require_last_push_approval":true,"required_review_thread_resolution":true},"ruleset_id":4102}]
```

Reply with what you do and why.
