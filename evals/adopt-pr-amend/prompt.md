---
description: adopt-pr amends a pushable fork PR in a separate worktree and stops uncommitted when the user did not say ship.
tags: [quality, adopt-pr]
runs: 2
max_turns: 8
timeout_seconds: 240
allowed_tools: [Skill, Read, Bash]
---

/adopt-pr 318

Answer from this state only and say what you do next; do not run anything.

- tidal-labs/tidal PR #318 is by an outside contributor from the fork lena-codes/tidal; I am a maintainer. `isCrossRepository` is true and `maintainerCanModify` is true.
- A verify-pr report on the current head `7c2e9d4` (base `4a1b0e3`) says Merge after small fixes, with two items, both in files the PR already touches: `src/retry.ts:52` swallows a rejected refill and leaves the budget stuck, and `src/retry.ts:74` re-implements `clampInt`, which `src/utils/num.ts` already exports. The approach itself holds.
- CI is green on `7c2e9d4`. I did not say to ship; I want to look at the result first.
