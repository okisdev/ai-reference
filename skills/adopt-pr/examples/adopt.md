# Adopt (illustrative)

The bar for an adoption: amend is chosen with a reason, the work happens in a task worktree confirmed against the PR's head SHA, the fixes come from the verify-pr findings and the PR's own diff gets trimmed without widening, and the run stops uncommitted until the user says go. Names, numbers, and SHAs are invented; the shape is the bar.

---

````
Judge: PR #318 by lena-codes, from the fork lena-codes/tidal. verify-pr says merge after small fixes on head 7c2e9d4: Blocking retry.ts:52 swallows a rejected refill and leaves the budget stuck, and a fold-in finding at retry.ts:74 where the PR re-implements `clampInt` that `utils/num.ts` already exports.
Decision: amend. isCrossRepository is true and maintainerCanModify is true, so the fork branch takes a push, and the approach holds, so a replacement PR would only discard Lena's commits.
Worktree: git worktree add --detach .claude/worktrees/adopt-318 origin/main, then gh pr checkout 318 inside it. git rev-parse HEAD is 7c2e9d4, equal to headRefOid.
Fixes: retry.ts:52 now rethrows after releasing the token, and the PR's own test gains the rejected-refill case.
Trim, in the PR's own files only: removed the comment above `take()` that restated its name, and replaced the local `clampInt` with the import from utils/num.ts. No file outside the PR changed.
Checks: pnpm --filter tidal test and pnpm --filter tidal lint, both pass in the worktree.
Stopped: the diff is uncommitted in /repo/.claude/worktrees/adopt-318 for review; nothing was pushed, and --ship was not passed.
````

On the user's go:

````
Committed on top of Lena's two commits as "fix: release the token when a refill rejects" and "refactor: reuse clampInt in the retry budget". Pushed to lena-codes/tidal at the PR's head branch without force. headRefOid moved from 7c2e9d4 to b81f60a, my commit. Approved with approve-pr, then handed to ship-pr, which merges and removes the worktree.
````

Why it clears the bar:

- amend is chosen with both facts that justify it, a pushable head and a sound approach, instead of building beside the PR.
- The worktree is a task worktree under `.claude/worktrees`, and the checked out commit is proved equal to `headRefOid` before any edit.
- Every verify-pr finding is fixed, and the trim stays inside the PR's own diff, with the one added test belonging to the fix.
- The report states the decision, each change with its reason, the checks run, and where the uncommitted diff lives.
- Nothing reached the contributor's branch until the user said go, and then the push was on top of her commits with the head SHA confirmed.
- The contributor stays credited because her commits stay.
