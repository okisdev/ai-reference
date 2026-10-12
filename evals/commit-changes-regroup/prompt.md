---
description: commit-changes unstages a tree that create-branch staged, regroups it by purpose with explicit paths, and proves signing with its one check.
tags: [quality, commit-changes]
runs: 2
max_turns: 8
timeout_seconds: 240
allowed_tools: [Skill, Read, Bash]
---

Use the commit-changes skill to plan the commits for this working tree. Everything you need is below; do not run commands.

Branch: feat/retry-budget, cut a minute ago by create-branch, which ran `git add -A`, so every change is already staged. Nothing is committed yet. `git config commit.gpgsign` prints true.
`git status --short`:
```
M  package.json
M  pnpm-lock.yaml
M  packages/sync/src/cursor.ts
M  packages/sync/src/retry.ts
A  packages/sync/src/retry.test.ts
M  README.md
```
What changed: package.json and pnpm-lock.yaml bump `p-queue`; retry.ts adds a shared retry budget that needs the new `p-queue` release, and retry.test.ts covers it; cursor.ts fixes a crash when a job has no cursor, unrelated to the budget; README.md fixes a broken install link.
Recent subjects in this repo: `feat(sync): stream checkpoints to disk`, `fix(sync): drop duplicate cursor writes`, `chore(deps): bump zod to 3.24`, `docs: fix the contributing link`.

Reply with one fenced block holding the exact git commands you would run, in order, and nothing else.
