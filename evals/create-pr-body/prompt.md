---
description: create-pr drafts a title and body in the user's register, with verified claims backed by commands and no tooling trace.
tags: [quality, create-pr]
runs: 2
max_turns: 8
timeout_seconds: 240
allowed_tools: [Skill, Read, Bash]
---

Use the create-pr skill to draft, not create, the PR for this branch. Everything you need is below; do not run commands.

Repository: acme/sync. Branch: feat/retry-budget. Base: main. No linked issue. No repo PR template.
Recent merged PR titles: `fix(sync): drop duplicate cursor writes`, `feat(sync): stream checkpoints to disk`.
Commits:
- feat(sync): cap retries per job with a shared budget
- test(sync): cover budget exhaustion and refill
Diff stat: packages/sync/src/retry.ts | 64 +++, packages/sync/src/retry.test.ts | 88 +++
Verified before the push: `pnpm --filter @acme/sync test` passed 48 of 48; `pnpm lint` reported no problems.
Not verified: behavior under the production worker pool.

Reply with the title on the first line and then the body, nothing else.
