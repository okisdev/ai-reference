# Review with items to act on (illustrative)

The bar when the author has several separable things to do: the verdict says not yet and gives its reason in one sentence, then numbered items so each can be answered on its own, each pinned to `file:line` in the baseline and saying what was run and what it printed. What already works is not narrated. The PR, files, and numbers are invented; the shape is the bar.

---

````
not ready yet: an aborted job still returns its retry token twice, so the budget grows past the cap (item 1). the other two are smaller.

1. `retry.ts:58` releases the token in both the `finally` block and the `abort` handler. i added `retry.abort.test.ts`: on your head it fails with `expected 3, received 4`, and it passes once the release lives only in `finally` (`b5c6d7e`). keep the abort handler to rejecting the promise; releasing there looks harmless and is the bug.
2. the docs say the budget is per job, and the code shares one per worker (`retry.ts:12`). i changed the docs line in `b5c6d7e` to match the code. if per job was the intent, the code is what has to move, and that is your call.
3. `refill()` rounds down (`retry.ts:63`) and loses a token an hour at the default rate. it does not block while the cap is 3, but say so in a comment before someone raises the cap.
````
