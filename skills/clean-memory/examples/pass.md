# A pass report that clears the bar (illustrative)

The bar for a pass: the size told at the start, counts before and after, one line per disposition with the locator that earned it, escalations that show both sides, and the snapshot and next date that make the pass undoable and recurring. The repository, topics, and SHAs are invented. The report's language follows the user; this structure and density do not change.

---

**Sizing**: told at the start as 14 topics, 10 to verify (9 flagged, 1 control), 5 verifiers, about 15 minutes. Took 19: the verify step ran past twice its 6 minute share (two verifiers waited on `gh` rate limits), was reported at that point, and the estimate moved to 20.

| | before | after |
|---|---:|---:|
| topics (archived) | 14 (0) | 12 (2) |
| store bytes | 38,106 | 27,318 |
| index lines / bytes | 15 / 4,236 | 10 / 1,904 |
| format problems | 6 | 0 |
| dead / drifted anchors | 4 / 2 | 1 / 0 |
| uncited | 3 | 1 |
| orphans | 1 | 0 |

**Dispositions**, locator last:

- confirm `queue-lease-ttl`: the TTL is 30 s at `src/queue/lease.ts:41`; confirm `release-cadence`: three tags 3 weeks apart in `git tag --sort=-creatordate`; `verified: 2026-10-12` set on both
- correct `worker-pool-size`: `src/pool/config.ts` moved to `src/pool/size.ts` in 3d9a1be (`git log -S`), and the default is 4 at `size.ts:12`, not 2; citation updated
- compact `pool-sizing-notes`: 6.1 KB to 3.0 KB; kept the 3 claims that hold, each cited, and dropped 2 that the description of #431 carries (`gh pr view 431`)
- promote `no-raw-sql-in-handlers`: caught in review twice (#388, #395); now one bullet at `AGENTS.md:23`, inside the first 10,000 characters; topic deleted because nothing else in it held
- archive `lease-contention-saga`: #402 is CLOSED by 7c1f2e9 (`gh issue view 402`); hook gained CLOSED and the line moved verbatim to ARCHIVE.md, topic unchanged
- disprove `retry-budget-global`: believed one budget shared by all jobs; `src/sync/retry.ts:18` builds the budget per job; rewritten to one paragraph, hook gained DISPROVEN, line moved to ARCHIVE.md
- delete `relay-perf-notes`: derivable, every figure is in the description of #431 (`gh pr view 431`)
- demote `batch-size-guess`: no citation and older than the stale window, so it is labeled inference with `verified` unset; its one dead anchor, `src/batch.ts`, stays and is named here because `git log --all -- src/batch.ts` shows no commit that moved or removed it
- delete the orphan index line `ci-flaky-list`: it pointed at a file that is not in the store (`ls`), and nothing referenced it
- escalate `staging-reset-day`: below
- 4 topics were unflagged and outside the control sample, so they are unchanged

**Escalations**:

- `staging-reset-day` says Sunday 02:00 UTC. `jobs/staging-reset.yml:4` in `acme/infra` (read with `gh api`) says Saturday 02:00 UTC, changed in acme/infra#240 on 2026-10-03, after the topic's 2026-09-14. Neither is in this tree, so the topic is unchanged and the question goes to whoever owns the job.

**Undo and next**: snapshot `~/.claude/projects/-Users-dev-GitHub-relay/memory-backups/2026-10-12/`, the two older snapshots kept; `.clean-memory.json` written; the only repository change is the `AGENTS.md` bullet, uncommitted; next cleanup 2026-11-11.
