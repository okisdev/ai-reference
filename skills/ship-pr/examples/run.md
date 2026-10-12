# A run that clears the bar (illustrative)

What the user sees from a good run: one status line per tick that names what is pending and whether it is alive, fixes batched until the head settles, `verify-pr` on every head, the gate re-read right before the merge, and the merge confirmed from GitHub. Names, numbers, and SHAs are invented; the shape is the bar.

````
Opened #418 (feat: add retry budget to the sync worker), head 3f2a9c1. Squash is allowed.
Tick 1 (0m): pending `test (node 20)` 1m, `lint` 1m, review bot `coderabbit` 1m; all three show activity. verify-pr: Merge as-is, Verified head 3f2a9c1.
Tick 2 (4m): `lint` failed (unused import in sync/retry.ts:14). `test (node 20)` still running 5m and `coderabbit` reviewing 5m, so the fix is committed locally and held until the head settles.
Tick 3 (7m): `test (node 20)` passed; `coderabbit` posted 2 threads on 3f2a9c1. Pushing the lint fix and the thread fixes together as 8b7e6d2.
Tick 4 (8m): pending `test (node 20)` 0m, `lint` 0m, and `coderabbit` 0m on 8b7e6d2, all started 40s ago. verify-pr --since 3f2a9c1: Merge as-is, Verified head 8b7e6d2.
Tick 5 (12m): all checks passed on 8b7e6d2; `coderabbit` reviewed 8b7e6d2 with no new threads; 2 threads resolved (fixed in 8b7e6d2); 0 required approvals; mergeStateStatus CLEAN.
Gate re-read: head is still 8b7e6d2, newest check completed 1m ago, base has no newer commits. Merging with --squash.
Merged #418 at 14:22 (gh pr view: MERGED, merge commit c41d0e5). Back on main at c41d0e5.
````

Why it clears the bar:

- Every tick names each pending item by its exact check or reviewer name and its age, so the user can pass a name to `--advisory`, and says whether it is still moving.
- The lint fix waits until the in-flight test finishes, because pushing would cancel and restart every run on the head.
- The fix commit gets its own `verify-pr --since` pass; authoring a commit is not judging it.
- The gate is re-read immediately before the merge: same head, fresh checks, no newer base commits.
- The merge is confirmed from `gh pr view`, not from the merge command's exit code.
