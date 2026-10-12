---
name: commit-changes
description: Stage and commit only uncommitted file changes into clean, categorized commits; existing commits are left untouched.
argument-hint: "[--cwd <path>]"
---

## Context

Current branch: !`git branch --show-current`

Uncommitted changes: !`git status --short`

Uncommitted diff stat: !`git diff --stat HEAD 2>/dev/null`

## Instructions

Categorize **only the current uncommitted changes** into clean commits. Leave existing commits untouched.

1. `--cwd <path>` in `$ARGUMENTS` names the repository or worktree to act in: rerun the Context probes there with `git -C <path>` and run every git command there. Record the staged paths (`git diff --cached --name-only --no-renames`), then unstage everything with `git restore --staged :/` so no pre-staged file rides into a group's commit. Read diffs (`git diff HEAD`). Untracked/new files don't appear in `git diff HEAD`; read those files directly so they're categorized, not missed. Group by **purpose** using conventional commits (`feat:`, `fix:`, `chore:`, `refactor:`, `docs:`, `style:`, `test:`, `perf:`, `ci:`, `build:`, `revert:`).
2. For each group, stage by explicit paths only: `git add <files>` (`git add -f <file>` only for a recorded path that git ignores), confirm `git diff --cached --name-only --no-renames` equals that group's list, then `git commit`. Never `git add -A` or `git add .`.
3. Verify `git status` is clean, show `git log --oneline` of new commits. When `git config commit.gpgsign` is true, prove each new commit is signed: `git cat-file commit <sha> | grep -c '^gpgsig'` prints 1. A signing failure, at `git commit` or in this check, stops the run and is reported; never bypass it with `--no-gpg-sign` or `commit.gpgsign=false`.

Rules:

- One commit per distinct purpose, each independently meaningful; a single concern is one commit whatever its file count
- Assign each file to its primary category; don't split files across commits
- Dependency order: foundational first (config, types, rename, schema and generated definitions), then core logic, then wiring, then UI, then polish
- Match the repo's existing commit-message style (subject case, scope notation, body)
- If pre-commit hooks fail, fix the failure and re-commit; never bypass with `--no-verify`
- NEVER reset, rebase, modify existing commits, or force push
