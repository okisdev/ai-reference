---
name: create-branch
description: Create a new branch off the default base (not the current HEAD, so unrelated commits stay behind) and move all uncommitted changes onto it, for when work started on the wrong branch or on main.
argument-hint: "[branch-name] [--base <branch>] [--keep-base] [--cwd <path>]"
---

## Context

Current branch: !`git branch --show-current 2>/dev/null || echo "(not a git repository)"`

Default base: !`out=$(git symbolic-ref --short refs/remotes/origin/HEAD 2>/dev/null | sed 's|^origin/||'); echo "${out:-main}"`

Commits ahead of default base on current branch:
!`b=$(git symbolic-ref --short refs/remotes/origin/HEAD 2>/dev/null | sed 's|^origin/||'); b=${b:-main}; git log "$b"..HEAD --oneline 2>/dev/null || echo "(none or base not found)"`

Uncommitted changes: !`git status --short 2>/dev/null || echo "(not a git repository)"`

Potentially relevant ignored files: !`out=$(git ls-files --others --ignored --exclude-standard 2>/dev/null | head -20); echo "${out:-(none)}"`

## Instructions

**The one rule: no change is lost and no unrelated commit comes along.** A great run ends on a new branch cut from the fresh base (from HEAD only when the commits ahead are the same work), every uncommitted change staged and none committed, reverted, or dropped, `git log <base>..HEAD` showing only commits that belong, reached by the cheapest safe route.

### Base selection

Default: branch off the **default base** (e.g. `main`), NOT the current HEAD.

- If `--base <branch>` is provided, use it.
- If `--keep-base` is provided, branch off current HEAD.
- Otherwise, if there are commits ahead of the default base AND those commits look unrelated to the uncommitted diff (different scope/files), branch off the default base.
- If commits ahead look related to the same work (e.g. same files, same feat scope), branch off current HEAD.

When in doubt and the set is small, err on branching off the default base.

### Process

1. `--cwd <path>` in `$ARGUMENTS` names the repository or worktree to act in: rerun the Context probes there with `git -C <path>` and run every git command there. If there are no uncommitted changes AND no ignored candidates, abort with a message. (If no branch name is provided via `$ARGUMENTS`, infer one from the uncommitted changes using conventional branch naming: `feat/`, `fix/`, `chore/`, `refactor/`.)
2. If branching off the default base (not current HEAD):
   - `git fetch origin` so the base is current, not a stale local ref
   - If `git rev-parse HEAD` equals `git rev-parse origin/<base>`, skip the stash and the rest of this step: run `git checkout -b <branch-name>` directly (uncommitted changes carry over; seen: every run stashed even when HEAD already sat on the base, and 184 of 289 runs needed only `git checkout -b`)
   - Otherwise try `git checkout -b <branch-name> origin/<base>` first (leaves the local base ref untouched); git carries the uncommitted changes across when they do not collide with the base, so no stash is needed
   - Only when git refuses because a change would be overwritten: `git stash push -u -m "create-branch-<branch-name>-<epoch seconds>"`, then `git checkout -b <branch-name> origin/<base>`, then pop that exact entry by its ref (`git stash list --format='%gd %s'`, then `git stash pop <ref>`), never a bare `git stash pop`, because `refs/stash` is shared by every worktree of the repository (seen: a bare pop in a PR worktree applied another session's `stash@{0}`)
   - If the pop conflicts on files the user did not author, that signals a bad base pick; abort and ask
3. Otherwise (branching off current HEAD): `git checkout -b <branch-name>`.
4. **Stage ALL uncommitted changes with `git add -A`. NEVER revert, discard, filter, or skip any file.**
5. Check for **gitignored files** that look like they belong to the work (e.g. drizzle migration SQL/snapshot when `drizzle/` is in `.gitignore`): if found, force-add with `git add -f <file>` AND flag to the user that the `.gitignore` rule may need fixing.
6. Show `git status --short` and confirm the branch was created. If files might be unrelated noise, **flag them to the user**; do NOT revert.
7. Show `git log <base>..HEAD --oneline`: on the default-base path it should be empty (no stray commits); on the `--keep-base` / branch-off-HEAD path, confirm only the intended related commits are ahead.

### Rules

- Stage only, never commit; kebab-case branch names only (`feat/discord-bot`, not `feat/Discord Bot`).
- If the branch already exists, abort with a message; do NOT overwrite. NEVER modify or delete any other branch.
- Destructive ops (`git checkout HEAD -- <file>`, `git restore`, `git clean`) are forbidden unless the user explicitly asks.
- NEVER touch `.gitignore` unless asked; flag the issue instead.
