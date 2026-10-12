---
type: llm
weight: 2
---

The report does not treat PR #3322 as covering #3310. It says the issue's own repro prints the same delays on head e1f2a3b as on main (attempt 14 still waits 4096000 ms), so the symptom is still there, and that neither the `Fixes #3310` line, the green checks, nor the PR's own test counts as evidence that it is fixed. It names why: the PR caps the delay only in `pollLoop` (`poller.ts` line 21), while `retryLoop` (`worker.ts` line 44), the path the repro takes, still sleeps for the uncapped `backoff` (`worker.ts` line 12). It keeps #3322 under Prior art, does not recommend running `/verify-pr` on it as the fix, and proposes capping inside `backoff` itself so both callers are covered.
