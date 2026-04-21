---
name: branch
description: Create a new branch and move all uncommitted changes to it.
argument-hint: "<branch-name> [--base <branch>] [--keep-base]"
---

## Context

Current branch: !`git branch --show-current`

Default base: !`git symbolic-ref --short refs/remotes/origin/HEAD 2>/dev/null | sed 's|^origin/||' || echo main`

Commits ahead of default base on current branch:
!`git log $(git symbolic-ref --short refs/remotes/origin/HEAD 2>/dev/null | sed 's|^origin/||' || echo main)..HEAD --oneline 2>/dev/null || echo "(none or base not found)"`

### Uncommitted changes

!`git status --short`

### Potentially relevant ignored files

!`git ls-files --others --ignored --exclude-standard 2>/dev/null | head -20 || echo "(none)"`

## Instructions

Create a new branch and move all current uncommitted changes to it. Execute immediately without asking for confirmation.

### Base selection (critical)

Default: branch off the **default base** (e.g. `main`), NOT the current HEAD. This keeps unrelated commits (like dependency bumps on `chore/bump-dependencies`) out of the new branch.

- If `--base <branch>` is provided, use it.
- If `--keep-base` is provided, branch off current HEAD (legacy behavior).
- Otherwise, if there are commits ahead of the default base AND those commits look unrelated to the uncommitted diff (different scope/files), branch off the default base.
- If commits ahead look related to the same work (e.g. same files, same feat scope), branch off current HEAD.

When in doubt and the set is small, err on branching off the default base.

### Process

1. If no branch name is provided via `$ARGUMENTS`, infer one from the uncommitted changes using conventional branch naming (`feat/`, `fix/`, `chore/`, `refactor/`).
2. If there are no uncommitted changes AND no ignored candidates, abort with a message.
3. If branching off the default base (not current HEAD):
   - `git stash push -u -m "branch-skill-transfer"` to capture both tracked + untracked
   - `git checkout <base>` then `git checkout -b <branch-name>`
   - `git stash pop`
   - If pop conflicts on files the user did not author, that signals a bad base pick — abort and ask
4. Otherwise (branching off current HEAD):
   - `git checkout -b <branch-name>`
5. **Stage ALL uncommitted changes. NEVER revert, discard, filter, or skip any file — even if it looks like noise, CRLF churn, a dep bump, or seemingly unrelated work.** The user can sort scope later. Destructive ops (`git checkout HEAD -- <file>`, `git restore`, `git clean`) are forbidden in this skill unless the user explicitly asks.
6. Stage all changes: `git add -A`.
7. Check for **gitignored files** that look like they belong to the work (e.g. drizzle migration SQL/snapshot when `drizzle/` is in `.gitignore`):
   - If found, force-add with `git add -f <file>` AND flag to user that the `.gitignore` rule may need fixing.
8. Show `git status --short` and confirm the branch was created. If there are files that might be unrelated noise, **flag them to the user** so they can decide — do NOT revert.
9. Also show `git log <base>..HEAD --oneline` to confirm 0 stray commits.

### Rules

- Branch name must use kebab-case (`feat/discord-bot`, not `feat/Discord Bot`)
- If the branch already exists, abort with a message — do NOT overwrite
- NEVER commit — only create the branch and stage changes
- NEVER modify or delete any existing branches (except the just-created branch on a failed retry)
- NEVER touch `.gitignore` unless asked — flag the issue instead
