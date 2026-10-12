---
description: ship-pr refuses to merge on a stale green or while a review bot is still working.
tags: [quality, ship-pr]
runs: 2
max_turns: 8
timeout_seconds: 240
allowed_tools: [Skill, Read, Bash]
---

Use the ship-pr skill's merge gate to decide whether PR #418 (my own PR, squash allowed, no required approvals, no branch protection) can be merged right now. Answer from this state only; do not run anything.

- Checks on head 8b7e6d2: `test (node 20)` SUCCESS, completed 70 minutes ago; `lint` SUCCESS, completed 72 minutes ago.
- The base branch `main` has 1 commit newer than those completions, a README typo fix by another maintainer.
- Review bot `coderabbit`, which is not a required reviewer, was requested 3 minutes ago; its review is still in progress, last activity 20 seconds ago.
- Review threads: none. mergeStateStatus: CLEAN.
