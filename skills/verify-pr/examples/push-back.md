# Push back (illustrative)

The bar for a fix that hides its symptom: the report proves the cause is still reachable by a second path, names the origin by `file:line`, and says what the real fix changes, instead of passing a diff that makes the reported repro go quiet. The PR below is invented; the shape is what matters.

---

**PR summary**: #4512 `fix(runtime): ignore stale messages after thread switch`, head `a1b2c3d`, MERGEABLE / CLEAN, closes #4498. Scope: the whole patch (1 file, +6 / -1).

| Dimension | Verdict | One-line note |
|-----------|---------|---------------|
| Necessity | OK | #4498 is real and reproducible; no other open PR addresses it |
| Correctness | fail | The guard drops the stale message in `onMessage`, but the run that produced it keeps streaming into the old thread's store |
| Test quality | minor | The added test switches threads once; it never switches back, which is where the leak shows |
| Conventions / paradigm | OK | Follows the guard style in `thread-runtime.ts` |
| Side effects | fail | A user who returns to the first thread sees the leaked messages appended out of order |
| CI | green | All checks pass; green proves the tree builds, not that the run stops |

**Correctness.** Claim from #4498: switching threads mid-run must not show the old run's messages. On the base, `pnpm vitest run thread-switch.test.ts` fails: the new thread shows the old run's messages. On the head it passes, so the reported repro goes quiet. Extended to switch back to the first thread, the same test fails on the head with `expected 3 chunks, received 7`: the run that was never cancelled appended its remaining chunks out of order. Origin: `src/runtime/thread-runtime.ts:212`, `switchThread` never calls `run.cancel()`. The guard at `onMessage` patches the symptom one layer down while the cause stays reachable.

**Final recommendation**: Push back. Cancel the active run in `switchThread` (`thread-runtime.ts:212`) and drop the guard; extend the test to switch away and back mid-run and assert the first thread holds only the chunks produced before the switch.

**Merge readiness**: no blockers besides the recommendation; no threads open.

**Verified head**: `a1b2c3d` against base `e4f5a6b`.
