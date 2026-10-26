---
description: ship-pr refreshes an old green when the base moved under the PR's own files.
tags: [quality, ship-pr]
runs: 2
max_turns: 8
timeout_seconds: 240
allowed_tools: [Skill, Read, Bash]
---

Use the ship-pr skill's merge gate to decide whether PR #418 (my own PR, squash allowed, no required approvals, a ruleset that does not require branches to be up to date) can be merged right now. Answer from this state only; do not run anything.

- PR #418 changes `sync/retry.ts` and `sync/retry.test.ts`.
- Checks on head 8b7e6d2: `test (node 20)` SUCCESS, completed 70 minutes ago; `lint` SUCCESS, completed 72 minutes ago.
- The base branch `main` has 1 commit newer than those completions: another maintainer renamed `maxAttempts` to `attemptLimit` in `sync/retry.ts`.
- verify-pr's Verified head is 8b7e6d2.
- Review bot `coderabbit` reviewed 8b7e6d2 and left no threads. Review threads: none. mergeStateStatus: CLEAN.
