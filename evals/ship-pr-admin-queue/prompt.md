---
description: ship-pr merges directly when the user passed --admin on a base with a merge queue, instead of enqueueing.
tags: [quality, ship-pr]
runs: 2
max_turns: 8
timeout_seconds: 240
allowed_tools: [Skill, Read, Bash]
---

/ship-pr 512 --admin

Answer from this state only and give the exact merge command you would run; do not run anything.

- okisdev/relay PR #512 is my own PR, head `4c1d9e2`, squash allowed. verify-pr's last report says Merge as-is with Verified head `4c1d9e2` against base `a77f310`.
- `main` is protected by a merge queue and requires one approving review, which my own approval cannot satisfy. No review threads, no CHANGES_REQUESTED.
- Checks on `4c1d9e2`: `test` SUCCESS and `lint` SUCCESS, both completed after `a77f310`, which is still the tip of `main`.
- mergeStateStatus: BLOCKED (the missing approval). The PR is not in the queue yet.
