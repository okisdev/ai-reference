---
name: commit-changes
description: Stage and commit only uncommitted file changes into clean, categorized commits — existing commits are left untouched.
---

## Context

Current branch: !`git branch --show-current`

### Uncommitted changes

!`git status --short`

### Uncommitted diff stat

!`git diff --stat HEAD 2>/dev/null`

## Instructions

Categorize **only the current uncommitted changes** into clean commits. Do NOT touch or reset any existing commits.

### Process

1. Read diffs (`git diff HEAD`) to understand what changed. Group by **purpose** using conventional commits (`feat:`, `fix:`, `chore:`, `refactor:`, `docs:`, `style:`, `test:`).
2. For each group: `git add <files>` + `git commit`.
3. Verify `git status` is clean, show `git log --oneline` of new commits.

### Rules

- 3-7 commits max, each independently meaningful
- If only 1-2 files changed, a single commit is fine
- Assign each file to its primary category — don't split files across commits
- Foundational changes first (config, types, rename), then features, then polish
- Fix lint errors if pre-commit hooks fail, then re-commit
- NEVER reset, rebase, or modify existing commits
- NEVER force push — just show the result and let the user decide
