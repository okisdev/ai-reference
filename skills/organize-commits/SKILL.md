---
name: organize-commits
description: Organize uncommitted changes or messy commits on the current branch into clean, categorized commits grouped by purpose, resetting and rewriting already-committed (even pushed) history when needed.
argument-hint: "[base-branch | --base <branch>] [--cwd <path>]"
---

## Context

Current branch: !`git symbolic-ref --short HEAD 2>/dev/null || echo "(detached HEAD or no commits yet)"`
Base branch (the repo default from `origin/HEAD`, then `main`; step 1 replaces it when the arguments name a base): !`out=$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@refs/remotes/origin/@@'); echo "${out:-main}"`
Upstream: !`git rev-parse --abbrev-ref --symbolic-full-name '@{upstream}' 2>/dev/null || echo "(no upstream tracked)"`
Behind / ahead of upstream (first count behind, second count ahead): !`git rev-list --left-right --count '@{upstream}...HEAD' 2>/dev/null || echo "(n/a)"`
Pushed commits in range: !`(BASE=$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@refs/remotes/origin/@@'); BASE=${BASE:-main}; git rev-list --count "$(git merge-base HEAD "$BASE" 2>/dev/null)..@{upstream}" 2>/dev/null) || echo "(no upstream tracked)"`

### Uncommitted changes

!`git status --short`

### Commits on this branch vs base

!`(BASE=$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@refs/remotes/origin/@@'); BASE=${BASE:-main}; git log --oneline "$(git merge-base HEAD "$BASE" 2>/dev/null)..HEAD" 2>/dev/null) || echo "(no committed history yet, empty repo or no merge-base with $BASE)"`

### Diff stat: committed vs base

!`(BASE=$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@refs/remotes/origin/@@'); BASE=${BASE:-main}; git diff --stat "$(git merge-base HEAD "$BASE" 2>/dev/null)..HEAD" 2>/dev/null) || echo "(no committed diff to show)"`

## Instructions

Analyze all changes (committed + uncommitted), group by **purpose**, and create clean commits. **Always print the categorization plan first; pause for confirmation before any destructive operation** (`git reset`, anything that requires force-push to publish).

### Scenarios

1. **Uncommitted only**: hand the grouping to `/commit-changes`; existing commits stay as-is, so no rewrite consent, recovery ref, or tree-identity check applies.
2. **Existing commits to reorganize, all local**: `git reset --soft $(git merge-base HEAD <base>)` to collapse into the index, then re-commit by category.
3. **Existing commits to reorganize, some already pushed**: same flow as #2, but the branch has a tracked upstream and at least one commit in the reset range is already on the remote (Pushed commits in range above greater than 0), so the rewrite can only be published with force-push. A never-pushed local branch (no upstream, or zero pushed commits in range) is scenario 2, not this case; do not false-warn about force-push there.
4. **Both uncommitted and existing commits**: same flow as #2 or #3.
5. **Edge cases**: empty repo (no HEAD) → stage and commit directly, do not reset. Detached HEAD → stop, ask the user to check out a branch first (`git switch -c <name>`).

### Process

1. **Plan** (`--cwd <path>` in `$ARGUMENTS` names the repository or worktree to act in: rerun the Context probes there with `git -C <path>` and run every git command there. The base comes from the arguments: `--base <branch>`, or a leading token that is not a flag and names a branch; when it differs from the `Base branch` probe, rerun the three range probes (Pushed commits in range, Commits on this branch vs base, Diff stat: committed vs base) against it by assigning `BASE=<base>`): state the scenario number above; for scenario 1, run `/commit-changes` (passing `--cwd <path>` when given) and stop. Otherwise read the actual diffs before grouping, not just the stats above (uncommitted via `git diff HEAD`, the committed range via `git diff $(git merge-base HEAD <base>)..HEAD`), then categorize. Print one line per planned commit in the form `<conventional-prefix>(<scope>): <subject> (<file count> file(s))`, then list which files go in each.
2. **Confirm (only when destructive)**: for scenarios 2, 3, 4, ask before running `git reset`. For scenario 3 specifically, call out "rewriting N pushed commit(s); publishing requires force-push".
3. **Execute**: before any `git reset`, record a recovery ref: `git branch _backup/<branch>` (or note the current tip with `git rev-parse HEAD`), and for a committed-only regroup (scenarios 2 and 3, no uncommitted changes joining) also record the content identity: `ORIGINAL_TREE=$(git rev-parse HEAD^{tree})`. Then run `git reset --soft $(git merge-base HEAD <base>)` if needed; that stages the whole range, so record it (`git diff --cached --name-only --no-renames`), unstage it with `git restore --staged :/`, and stage each group by path (`git add -f` for a recorded path git ignores), confirming `git diff --cached --name-only --no-renames` equals that group's list before its `git commit`. If the regroup goes wrong, restore the original history with `git reset --hard _backup/<branch>` (or `git reset --hard <recorded-sha>`).
4. **Verify**: `git status` is clean, then `git log --oneline -<n>` to show the rewritten tip. On a committed-only regroup, compare `git rev-parse HEAD^{tree}` against `ORIGINAL_TREE`; a mismatch means the rewrite changed content, not just history, so stop and reconcile before any publication.
5. **Recommended sanity check**: run the project's `build` / `test` if it's quick.

### Rules

- As many commits as the work has distinct concerns, no more; a single-file polish change is fine as one commit.
- Use conventional commit prefixes: `feat:`, `fix:`, `docs:`, `style:`, `refactor:`, `perf:`, `test:`, `ci:`, `build:`, `chore:`, `revert:`.
- Stage by explicit paths; avoid `git add -A` and `git add .` so sensitive files (`.env`, credentials) don't sneak in.
- Group files by their primary concern. A single file may be split across commits with `git add -p` only when its diff genuinely spans two unrelated concerns; cohesive diffs stay together.
- Order: foundational (config, rename, types, schema and generated definitions) → core logic → wiring and integration → UI or surface behavior → polish (docs, tests, chore).
- If pre-commit hooks fail, fix the issue and re-commit. Never use `--no-verify`.
- Match the repository's existing commit-message style (subject case, scope notation, body wrap, sign-off).
- NEVER force push without explicit user permission, even when the rewrite would otherwise leave the branch unpublishable. State the situation and let the user run the force-push themselves.
