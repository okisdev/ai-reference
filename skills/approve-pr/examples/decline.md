# Decline (illustrative)

The bar when the table says do not approve: the same fresh reads, the blocking thread named with its location, verify-pr's rationale passed through verbatim instead of paraphrased, and nothing written to GitHub without an opt-in flag. Names, numbers, and SHAs are invented; the shape is the bar.

---

````
Guard: author mia-dev, me okisdev; #4621 is open, head 3f2a9c1, base e4f5a6b.
Gate: verify-pr from this session says push back with Verified head 3f2a9c1 against base e4f5a6b, equal to the fresh pair, so it is reused.
Threads: 5 total, 2 unresolved, read fresh. verify-pr-comments: 1 Fresh and Confirmed (retry.ts:41), 1 Stale.
Decision: do not approve. Push back posts nothing without --request-changes, and it was not passed. Nothing was written to GitHub.

verify-pr's rationale, verbatim:
Push back. Necessity holds, but the abort path releases a token twice (retry.ts:41 and retry.ts:63), so the budget grows past the cap after any aborted job. Release in `finally` only and make abort reject; extend the exhaustion test to abort mid retry and assert the count never exceeds the cap.

Blocking thread: retry.ts:41, Confirmed and unaddressed.
Next: rerun /approve-pr 4621 after the author pushes; add --request-changes to post this as a review.
````
