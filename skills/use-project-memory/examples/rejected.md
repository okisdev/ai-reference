# Rejected topic

A write that passes `check.py --strict` and still fails admission, because it saves a report. It comes from a request to remember a hand-off latency analysis. Compare yours against it before writing.

````md
---
name: handoff-latency-analysis-2026-10
description: "Hand-off latency analysis for relay, October 2026"
metadata:
  type: project
---

# Hand-off latency analysis

Over 14 days p50 hand-off from queue to worker was 240 ms and p95 was 1.9 s. 71 percent of the p95 tail is cold worker starts in `src/pool/spawn.ts`; the rest is lease contention in `src/queue/lease.ts`.

Raising `minWorkers` from 2 to 6 cut p95 to 610 ms in the 2026-09-30 staging run (run 8841).

BUILT: prewarm pool shipped in #431, merged 2026-10-02.

Next: add a lease shard.
````

````md
- [handoff-latency-analysis-2026-10](handoff-latency-analysis-2026-10.md) — BUILT; p50 240 ms, p95 1.9 s, prewarm, lease
````

Why each part fails:

- `handoff-latency-analysis-2026-10`: a topic is named for its subject, never for a report or a date.
- The measurements and the run id: what was measured is carried by the PR or issue that ran it, and a report the user wants kept goes to an issue or a published page.
- `BUILT: prewarm pool shipped in #431, merged 2026-10-02`: what shipped, when, and in which PR is the PR and `git log`; no later decision depends on it (seen: BUILT status saved as topics).
- `Next: add a lease shard`: a plan. A session's progress, plan, analysis, or report goes nowhere in this store.
- Four facts in one topic: a topic holds one fact, and none of these changes a decision the repository cannot already answer.
- The hook summarizes the body; it is meant to be the shortest cue that finds the topic.
- Passing `check.py` proves the format, not the admission (seen: 49 percent of sampled writes failed the admission test, among them analyses, audits, and BUILT status saved as topics).

The right output is no write. Reply with where the content belongs and stop: "Not stored. This is an analysis with measurements and a plan, which the admission test rejects, and the PR for the prewarm change carries what shipped. A report worth keeping goes to an issue or a published page."
