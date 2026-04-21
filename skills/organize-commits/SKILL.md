---
name: organize-commits
description: Organize uncommitted changes or messy commits on the current branch into clean, categorized commits grouped by purpose.
argument-hint: "[base-branch]"
---

## Context

Current branch: !`git branch --show-current`
Base branch: $ARGUMENTS (default to `main` or `master` if not specified)

### Uncommitted changes

!`git status --short`

### Commits on this branch

!`git log --oneline $(git merge-base HEAD ${1:-$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@refs/remotes/origin/@@' || echo main)})..HEAD 2>/dev/null`

### Changed files (committed + uncommitted vs base)

!`git diff --stat $(git merge-base HEAD ${1:-$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@refs/remotes/origin/@@' || echo main)})..HEAD 2>/dev/null`
!`git diff --stat HEAD 2>/dev/null`

## Instructions

Analyze all changes (committed + uncommitted), categorize by purpose, and create clean commits. Execute immediately without asking for confirmation.

### Scenarios

1. **Uncommitted only**: Stage and commit into categorized groups.
2. **Existing commits only**: `git reset --soft <base>`, unstage, re-commit by category.
3. **Both**: `git reset --soft <base>` to merge everything, unstage, re-commit by category.

### Process

1. Read diffs to understand what changed. Group by **purpose** using conventional commits (`feat:`, `fix:`, `chore:`, `refactor:`, `docs:`, `style:`, `test:`).
2. Execute: reset if needed, then `git add` + `git commit` for each group.
3. Verify `git status` is clean, show `git log --oneline` of new commits.

### Rules

- 3-7 commits, each independently meaningful
- Assign each file to its primary category — don't split files across commits
- Foundational changes first (config, rename), then features, then polish
- Fix lint errors if pre-commit hooks fail, then re-commit
- NEVER force push — just show the result and let the user decide
