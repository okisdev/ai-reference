# A pass that clears the bar (illustrative)

What the user sees from a good pass: the suites timed before and after with the same reporters, every disposition counted, every moved or deleted test paired with what still guards its behavior, each move proven by a planted regression, and the write-time cause turned into a check. Names, paths, and numbers are invented; the shape is the bar.

The invented monorepo `acme-desk` has a Vitest unit suite and a Playwright suite that launches the Electron app. The user said: "the tests take forever, see which ones we don't need."

````
Scope: all tests, 412 files (unit 318 in apps/desktop/src, e2e 94 in apps/desktop/e2e). Estimate 60 to 90 minutes; e2e ledger split across 3 subagents by folder.

Baseline (same reporters before and after)
| Suite | Tests | Wall | Slowest |
|---|---|---|---|
| unit (vitest --reporter=json) | 6,210 | 71 s | phones-service.test.ts 25.4 s |
| e2e (playwright --reporter=json, 4 workers) | 388 | 11.2 min | phones.spec.ts:12 186 s |

After
| Suite | Tests | Wall | Slowest |
|---|---|---|---|
| unit | 3,746 | 44 s | git-status.test.ts 3.1 s |
| e2e | 301 | 6.4 min | terminal-survival.spec.ts:40 21 s |
| make full (nightly, new) | 1 | 3.1 min | phones.spec.ts:12 186 s moved here |

Dispositions (412 files, 6,598 tests): keep 3,890, delete 2,551, rewrite 37, move down 64, fix cost 56.

Deleted, with what still guards each behavior
- i18n/catalog.test.ts: 2,512 generated cases collapsed to 22, one per rule (missing key, plural forms, placeholder parity...); the 22 rules are each asserted once over every locale.
- app.spec.ts:88 "window opens": copy of welcome.spec.ts:10, which asserts the same window and its first screen.
- export.test.ts "legacy exporter is gone": depends on the past; nothing must guard an absence.
- session.test.ts "clears the cache" and the production helpers `_resetCacheForTests`, `_getCacheSize` that existed only for it: it asserted private state; session.test.ts:40 "signing out drops cached profiles" guards what callers see, and failed when the clear call was removed.
- 33 more, each with its guard, in the ledger attached below the report.

Moved down (each lower test failed on the planted regression before the e2e test was deleted)
- help-tags.spec.ts (6 tests) -> help-tags.test.ts: tag text and placement are pure functions of the descriptor; planted: swapped the placement map, 4 of 6 failed, restored.
- window-bounds.spec.ts (5 tests) -> window-bounds.test.ts: clamp logic; planted: dropped the menu bar inset, 3 of 5 failed, restored. One e2e test kept for the debug bridge it crossed.
- 9 more specs, each with its plant, in the ledger.

Cost fixed
- phones-service.test.ts: the fake process never emitted `exit`, so 5 tests each waited out 5 s; the fake now emits it. 25.4 s -> 0.3 s. One test keeps a fake that never exits and advances a fake clock past the grace period, so the fallback stays guarded.
- 41 fixed sleeps in e2e replaced by waits on the condition they stood for (`expect.poll`, the pane's ready event).
- phones.spec.ts drove the iOS simulator through the desktop app for a list layout; the layout moved to a unit test, the one simulator round trip that crosses a real boundary stays, moved to `make full`.
- 35 unit files rebuilt a git repository per test; they now copy the template repository the suite already builds in global setup.

Determinism: every changed spec ran with --repeat-each 5 on an empty data folder, and every changed unit file 5 times shuffled, all green. Full ladder (`set -o pipefail; make check`) passed.

Unguarded behaviors found (not deleted, reported)
- channels.spec.ts took 18 screenshots and compared none; the channel order it seems to protect has no assertion anywhere. Left in place; needs an owner decision on what to assert.

Stop the cause
- Proposed lint: forbid `waitForTimeout` and `setTimeout(…, n>=100)` in e2e and *.test.ts outside tests of time-based behavior (41 sites removed, 0 left).
- Proposed rule for apps/desktop/e2e/AGENTS.md: "Add an end-to-end test only for behavior that crosses a real process, terminal, native UI, or file-watching boundary; prove logic in a unit test."
- Root AGENTS.md orders the full e2e suite before every change is done; measured cost 6.4 min per change after this pass (11.2 before). Proposed: changed specs per change, full suite in `make full`. Owner decides.

Uncommitted. Net: -18,940 lines (git diff --shortstat).
````

Why it clears the bar:

- The same suites ran with the same reporters before and after, so the speedup is measured, not estimated.
- Every deletion names what still guards its behavior, or why nothing must.
- Each move down and cost fix was proven by a planted regression failing the new test before the old one went, and the wiring a move crossed kept one test.
- The test moved out of the default run is reported as its own suite with its time and cadence, not counted as a saving.
- Costs were fixed at their cause (a fake that never signalled, fixed sleeps, a rebuilt fixture), never by retries or longer timeouts.
- A test whose purpose was unclear was reported, not silently deleted.
- The patterns that made the suite slow became a proposed check and an admission rule, and the per-change run rule went to the owner with its measured cost.
