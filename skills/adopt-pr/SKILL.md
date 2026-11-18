---
name: adopt-pr
description: Take over another author's pull request as a maintainer, fixing and simplifying it on its own branch (or superseding it when it cannot be saved), then hand it to approval and merge, when asked to fix, optimize, or finish a contributor's PR instead of waiting for them.
argument-hint: "<pr-number-or-url> [--ship] [--supersede] [--admin]"
---

## Context

Repository: !`gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null || echo "unknown"`
My login: !`gh api user --jq .login 2>/dev/null || echo "unknown"`
Worktrees: !`out=$(git worktree list 2>/dev/null | head -5); echo "${out:-(none)}"`

## Instructions

**The one rule: the contributor's work lands, improved, under their name, and nothing is pushed to their branch before the user has seen the change or told you to ship it.** A great run decides amend or supersede with a reason, works in its own worktree on the PR's head, fixes every finding and trims the PR's own diff without widening its scope, and either stops with a reviewable uncommitted diff or pushes, approves, and ships in one go when told to. Open [examples/adopt.md](examples/adopt.md) before reporting and check it against [examples/rejected.md](examples/rejected.md).

### Process

1. Parse `$ARGUMENTS`: the PR, `--ship` to push, approve, and merge without stopping (also when the user's ask says to ship), `--supersede` to force a replacement PR, and merge flags such as `--admin` to pass through. Without `--ship`, the run stops at step 6 with the change uncommitted.
2. Judge the PR first (`verify-pr` when installed): a close or redirect verdict ends the run with that verdict and a closing reply drafted (`draft-reply` when installed); otherwise its Blocking and fold-in findings are the work list.
3. Decide amend or supersede and say why: amend when the head can take a push (`isCrossRepository` false, or `maintainerCanModify` true) and the approach holds; supersede when the approach must be rewritten or the head cannot take a push, because building beside a salvageable PR wastes the contributor's work (seen: the user asked whether to fix the existing PR or redo it, and then to close a duplicate and push the fix onto the original).
4. Check out the head in its own task worktree, never in the primary checkout: `git worktree add --detach .claude/worktrees/adopt-<n> origin/<base>`, then `gh pr checkout <n> --detach` inside it, detached so it never collides with the PR's branch checked out elsewhere; confirm `git rev-parse HEAD` equals the PR's `headRefOid`. A superseding PR branches from the fresh base instead and carries the contributor's commits or a `Co-authored-by:` trailer with their name and email.
5. Fix every finding, then simplify the PR's own diff only (`optimize-repo` scoped to the changed files when installed): remove dead code, comments that restate the code, and needless indirection, and reuse existing helpers; touch a file outside the PR only for a test the fix needs. Run the repository's checks for the touched packages.
6. Without `--ship`, stop here: report the amend or supersede decision, each change with its reason, the checks run, and the worktree path, with the diff uncommitted for the user to review (seen: the user repeatedly asked for the optimized PR to be left uncommitted so they could check it before any push).
7. On `--ship` or the user's go: commit by purpose (`commit-changes` when installed) on top of the contributor's commits, push explicitly to the PR's head ref (`git push https://github.com/<headRepositoryOwner>/<headRepository>.git HEAD:<headRefName>`, the three values from `gh pr view <n> --json headRepositoryOwner,headRepository,headRefName`), and confirm the PR's `headRefOid` moved to your commit. A superseding PR is opened, and the original closed with a pointer to it and thanks (`draft-reply` when installed).
8. Hand off: approve (`approve-pr` when installed), then merge (`ship-pr` when installed) with the passed-through flags; the merge step removes the worktree.

### Rules

- Never force-push or rewrite the contributor's commits; add commits on top.
- Never push to the contributor's branch before the user's go or `--ship`.
- The contributor stays credited: their commits stay, or a superseding commit carries their `Co-authored-by:` trailer.
