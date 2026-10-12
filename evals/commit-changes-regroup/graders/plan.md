---
type: llm
weight: 2
---

The block records the staged paths with `git diff --cached --name-only --no-renames` and unstages everything with `git restore --staged :/` before any `git add`. It then makes exactly four commits, one per purpose, each staged by explicit paths: `chore(deps)` for `package.json` and `pnpm-lock.yaml`, before the feature that needs the new release; `feat(sync)` for `retry.ts` and `retry.test.ts`; `fix(sync)` for `cursor.ts`; and `docs` for `README.md`, with lowercase conventional subjects in the repo's style. Before each `git commit` it compares `git diff --cached --name-only --no-renames` with that group's paths. It ends with `git status` and `git log --oneline`, and proves each new commit is signed with `git cat-file commit <sha> | grep -c '^gpgsig'` rather than an improvised check such as `git log --show-signature` or `git verify-commit`.
