# Rejected report

A pass that reads fine and gets sent back. Compare yours against it before reporting.

````
Cleaned up the test suite. Removed about 300 tests that looked redundant or low value, and merged the e2e specs so each file launches the app once. Some e2e tests were flaky, so I added `retries: 2` and bumped the timeout to 90 s. The suite should be a lot faster now. Also added tests for the new export path while I was in there. All green.
````

Why each part fails:

- `Removed about 300 tests that looked redundant or low value`: no ledger and no per-test verdict, and no deletion names the test that still guards its behavior, so a behavior can lose its only guard unseen.
- `merged the e2e specs so each file launches the app once`: a shared launch trades isolation for about a second per test and was never measured against the wrong-layer moves and fixed waits that cost more; it also leaves logic a unit test could prove at the most expensive layer.
- `added retries: 2 and bumped the timeout to 90 s`: retries and longer timeouts hide the race and add cost; the wait or leftover state behind the flake is fixed at its cause.
- `should be a lot faster now`: no baseline and no rerun with the same reporters, so the speedup is a guess.
- `Also added tests for the new export path`: the pass removes cost; new coverage is a separate change.
- No planted regression: the moved or rewritten tests were never shown to fail when their behavior breaks.
- No write-time fix: nothing stops the same sleeps and end-to-end tests from being written again, and the rule that runs the suite on every change was not weighed.
- `All green`: no command, no counts, no wall time, and no determinism run.
