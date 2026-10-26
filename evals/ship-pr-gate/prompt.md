---
description: ship-pr waits for a review bot that is still working and keeps an old green whose base moved only elsewhere.
tags: [quality, ship-pr]
runs: 2
max_turns: 8
timeout_seconds: 240
allowed_tools: [Skill, Read, Bash]
---

Use the ship-pr skill's merge gate to decide whether PR #418 (my own PR, squash allowed, no required approvals, no branch protection) can be merged right now. Answer from this state only; do not run anything.

- PR #418 changes `sync/retry.ts` and `sync/retry.test.ts`.
- Checks on head 8b7e6d2: `test (node 20)` SUCCESS, completed 70 minutes ago; `lint` SUCCESS, completed 72 minutes ago.
- The base branch `main` has 1 commit newer than those completions, a typo fix in `README.md` by another maintainer, which changes no other file.
- Review bot `coderabbit`, which is not a required reviewer, was requested 3 minutes ago; its review is still in progress, last activity 20 seconds ago.
- Review threads: none. mergeStateStatus: CLEAN.
