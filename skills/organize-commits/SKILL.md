---
name: organize-commits
description: Organize uncommitted changes or messy commits on the current branch into clean, categorized commits grouped by purpose. Can reset and rewrite already-committed (even pushed) history.
argument-hint: "[base-branch]"
---

## Context

Current branch: !`git symbolic-ref --short HEAD 2>/dev/null || echo "(detached HEAD or no commits yet)"`
Base branch (arg `$1`, falls back to `origin/HEAD` then `main`): !`echo "${1:-$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@refs/remotes/origin/@@' || echo main)}"`
Upstream: !`git rev-parse --abbrev-ref --symbolic-full-name '@{upstream}' 2>/dev/null || echo "(no upstream tracked)"`
Ahead / behind upstream: !`git rev-list --left-right --count '@{upstream}...HEAD' 2>/dev/null | awk '{print "behind "$1", ahead "$2}' || echo "(n/a)"`
Pushed commits in range: !`(BASE="${1:-$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@refs/remotes/origin/@@' || echo main)}"; git rev-list --count "$(git merge-base HEAD "$BASE" 2>/dev/null)..@{upstream}" 2>/dev/null) || echo "(no upstream tracked)"`

### Uncommitted changes

!`git status --short`

### Commits on this branch vs base

!`(BASE="${1:-$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@refs/remotes/origin/@@' || echo main)}"; git log --oneline "$(git merge-base HEAD "$BASE" 2>/dev/null)..HEAD" 2>/dev/null) || echo "(no committed history yet, empty repo or no merge-base with $BASE)"`

### Diff stat: committed vs base

!`(BASE="${1:-$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@refs/remotes/origin/@@' || echo main)}"; git diff --stat "$(git merge-base HEAD "$BASE" 2>/dev/null)..HEAD" 2>/dev/null) || echo "(no committed diff to show)"`

## Instructions

Analyze all changes (committed + uncommitted), group by **purpose**, and create clean commits. **Always print the categorization plan first; pause for confirmation before any destructive operation** (`git reset`, anything that requires force-push to publish).

### Scenarios

1. **Uncommitted only**: stage and commit into categorized groups; existing commits stay as-is.
2. **Existing commits to reorganize, all local**: `git reset --soft $(git merge-base HEAD <base>)` to collapse into the index, then re-commit by category.
3. **Existing commits to reorganize, some already pushed**: same flow as #2, but the branch has a tracked upstream and at least one commit in the reset range is already on the remote (Pushed commits in range above greater than 0), so the rewrite can only be published with force-push. Surface this in the plan and require explicit confirmation. A never-pushed local branch (no upstream, or zero pushed commits in range) is scenario 2, not this case; do not false-warn about force-push there.
4. **Both uncommitted and existing commits**: same flow as #2 or #3.
5. **Edge cases**: empty repo (no HEAD) → stage and commit directly, the first commit becomes the initial commit, do not reset. Detached HEAD → stop, ask the user to check out a branch first (`git switch -c <name>`).

### Process

1. **Plan** ($1 is the optional base branch): read the actual diffs before grouping, not just the stats above (uncommitted via `git diff HEAD`, the committed range via `git diff $(git merge-base HEAD <base>)..HEAD`), then categorize. Print one line per planned commit in the form `<conventional-prefix>(<scope>): <subject> (<file count> file(s))`, then list which files go in each. State the scenario number above.
2. **Confirm (only when destructive)**: for scenarios 2, 3, 4, ask before running `git reset`. For scenario 3 specifically, call out "rewriting N pushed commit(s); publishing requires force-push".
3. **Execute**: before any `git reset`, record a recovery ref: `git branch _backup/<branch>` (or note the current tip with `git rev-parse HEAD`). Then run `git reset --soft $(git merge-base HEAD <base>)` if needed, then `git add <files>` + `git commit` per group. If the regroup goes wrong, restore the original history with `git reset --hard _backup/<branch>` (or `git reset --hard <recorded-sha>`).
4. **Verify**: `git status` is clean, then `git log --oneline -<n>` to show the rewritten tip.
5. **Recommended sanity check**: run the project's `build` / `test` if it's quick.

### Rules

- As many commits as the work has distinct concerns, no more; a single-file polish change is fine as one commit.
- Use conventional commit prefixes: `feat:`, `fix:`, `docs:`, `style:`, `refactor:`, `perf:`, `test:`, `ci:`, `build:`, `chore:`, `revert:`.
- Stage by explicit paths; avoid `git add -A` and `git add .` so sensitive files (`.env`, credentials) don't sneak in.
- Group files by their primary concern. A single file may be split across commits with `git add -p` only when its diff genuinely spans two unrelated concerns; cohesive diffs stay together.
- Order: foundational (config, rename, types) → features → polish (docs, tests, chore).
- If pre-commit hooks fail, fix the issue and re-commit. Never use `--no-verify`.
- Match the repository's existing commit-message style (subject case, scope notation, body wrap, sign-off).
- NEVER force push without explicit user permission, even when the rewrite would otherwise leave the branch unpublishable. State the situation and let the user run the force-push themselves.
