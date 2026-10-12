# Approval (illustrative)

The bar for an approval: the gate is read fresh and named, the approval binds to the head that was judged, the body is a note to the author that gives the verdict, the one reason it holds, and what was run against what was only read, and the run ends at the post. Names, numbers, and SHAs are invented; the shape is the bar.

---

````
Guard: author mia-dev, me okisdev; #4621 is open, head 9d1c3f7, base e4f5a6b.
Gate: verify-pr from this session says merge as-is with Verified head 9d1c3f7 against base e4f5a6b, equal to the fresh pair, so it is reused.
Threads: 3 total, 0 unresolved, read fresh.
Head re-read before posting: still 9d1c3f7. My latest review here is COMMENTED, so this is a fresh approval, not an edit.
Posted the approval with the body below; reviewDecision is APPROVED. Stopping here: checks and the merge belong to ship-pr.
````

The body, passed through `gh pr review 4621 --approve --body-file -`:

````
lgtm on 9d1c3f7. the cap holds because `budget.take()` runs once per attempt, not once per job (retry.ts:41), so a job that fails twice spends two tokens.

i ran the 48 sync tests plus your exhaustion test, and forced the refill timer to fire mid attempt with a fake clock; the count stayed at or above zero. i did not run the production worker pool, so the budget shared across processes is a reading, not a check. one thing stands and does not block: `refill()` rounds down (retry.ts:58) and loses a token an hour at the default rate, which only matters if the cap is raised.
````
