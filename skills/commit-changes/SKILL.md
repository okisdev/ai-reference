---
name: commit-changes
description: Stage and commit only uncommitted file changes into clean, categorized commits; existing commits are left untouched.
---

## Context

Current branch: !`git branch --show-current`

Uncommitted changes: !`git status --short`

Uncommitted diff stat: !`git diff --stat HEAD 2>/dev/null`

## Instructions

Categorize **only the current uncommitted changes** into clean commits. Do NOT touch or reset any existing commits.

1. Read diffs (`git diff HEAD`) to understand what changed. Untracked/new files don't appear in `git diff HEAD`; read those files directly so they're categorized, not missed. Group by **purpose** using conventional commits (`feat:`, `fix:`, `chore:`, `refactor:`, `docs:`, `style:`, `test:`, `perf:`, `ci:`, `build:`, `revert:`).
2. For each group, stage by explicit paths only: `git add <files>` + `git commit`. Never `git add -A` or `git add .`.
3. Verify `git status` is clean, show `git log --oneline` of new commits.

Rules:

- 3 to 7 commits max, each independently meaningful
- If only 1 to 2 files changed, a single commit is fine
- Assign each file to its primary category; don't split files across commits
- Foundational changes first (config, types, rename), then features, then polish
- Match the repo's existing commit-message style (subject case, scope notation, body)
- If pre-commit hooks fail, fix the failure and re-commit; never bypass with `--no-verify`
- NEVER reset, rebase, modify existing commits, or force push
