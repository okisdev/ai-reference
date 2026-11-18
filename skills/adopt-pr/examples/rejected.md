# Rejected adoption

An adoption run that compiles into a pushed result and still gets stopped by the user. Compare yours against it before reporting.

````
Checked out #318 in the main checkout and fixed retry.ts.
While in there I also renamed the helpers in utils/num.ts and reformatted the config loader.
Squashed Lena's two commits and mine into one and force-pushed to lena-codes/tidal.
Opened a new PR #322 with the same change, and closed #318.
Done, merged #322.
````

Why each part fails:

- `in the main checkout`: work in a task worktree on the PR's head, because the primary checkout carries the user's own state; confirm `git rev-parse HEAD` equals `headRefOid` first.
- `renamed the helpers ... reformatted the config loader`: the trim covers the PR's own diff only; unrelated files widen a contributor's change into one nobody asked to review.
- `Squashed ... force-pushed`: never force-push or rewrite the contributor's commits; add commits on top.
- `Opened a new PR #322 ... closed #318`: the head was pushable and the approach held, so amend; a duplicate PR throws away the contributor's work and their thread.
- `Done, merged` with no stop: nothing is pushed before the user has seen the change or said ship, and the report was never given.
- `with the same change`: the new PR carries no `Co-authored-by:` trailer and no original commits, so the contributor is no longer credited.
