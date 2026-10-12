# Why (a failure the day before)

The bar for a why: it leads with the answer, tabulates every failure surface in the window, and when the window holds no failure searches one window length to each side, names the nearest failure with its distance, and says when it falls inside the asked span only in UTC. It then gives the timeline, the first failing log line, the last good and first bad version with the changes between them, and a diagnosis that follows `diagnose-root` inside the read-only rule, where an unreproduced mechanism is labeled a hypothesis and the record that would settle it is named. Condensed from a real run: the repository, its tables, and its job names are replaced because the original is private. The report's language follows the user; this structure and density do not change.

---

````
## batch-jobs, why, 2026-10-11 00:00 to 2026-10-11 23:59 (+08:00)

**Answer**: nothing failed on 2026-10-11 (+08:00). The nearest failure is the scheduled `Classify run` [#38155610508](https://github.com/acme/batch-jobs/actions/runs/38155610508), created 28 min 33 s after the window ended (2026-10-12 00:28:32 +08:00, which is 2026-10-11 16:28:32Z, so it is "yesterday" only on a UTC calendar and is probably the one you saw). One project's results transaction failed on an upsert that Postgres rejected, and no log kept the reason, so the cause below is a hypothesis. Code is ruled out as the trigger: the last good run and the failing run are the same SHA, `7b3a2a5`.

| Failure surface in the window | Records | Failures |
|---|---|---|
| GitHub Actions, acme/batch-jobs | 38 (aggregate 38): 36 success; 1 action_required ([#38122734831](https://github.com/acme/batch-jobs/actions/runs/38122734831), a PR waiting for approval, no jobs); 1 cancelled ([#38072096715](https://github.com/acme/batch-jobs/actions/runs/38072096715), a CI run on the same branch succeeded 7 s later, so superseded) | 0 |
| Vercel deployments, 2 projects | 14, all READY (production 6, preview 8); the team's 107 deployments hold no ERROR | 0 |
| Vercel runtime, 2 projects | 5xx 0, fatal 0; the 173 error level rows of one project are a single Node `pg` SSL mode warning written to stderr (163 responses 200, 7 responses 304, 3 responses 307); the other project has 0 rows | 0 |
| Vercel alerts | 0 groups | 0 |

**Timeline** (+08:00)
- 10-11 23:25:41 last good run [#38151223233](https://github.com/acme/batch-jobs/actions/runs/38151223233), 21 results classified for the project that fails next.
- 10-12 00:28:32 failing run created, 00:28:41 job started, 00:29:31 first failing log line, 00:29:34 finished.
- 10-12 01:24:17 next run [#38159499796](https://github.com/acme/batch-jobs/actions/runs/38159499796) succeeded, 35 classified.

**First failing log line**: `Classify proj_a1: failed. Failed query: insert into "thread_labels" ("thread_id", "project_id", "label_id", ... $36, timezone('utc', now())) on conflict ("thread_id") do update set ...`, then `{"threadsClassified":0,"passes":1,"projectsProcessed":4,...}` and `##[error]Process completed with exit code 1.`

**Last good and first bad**: both ran SHA `7b3a2a5` (compare: identical, 0 commits). On that SHA the workflow passed 22 times before and 4 times after the failure. The three runs share Node v22.23.2, an unchanged lockfile under `pnpm install --frozen-lockfile`, and the same runner image, so code, dependencies, and runner are not the trigger. Vercel activity for the 2 projects (83 events) holds only deployments and alias assignments, so no configuration or environment edit sits near the failure either. What is left is the input data, the database, and timing.

**Diagnosis** (stops here: a rerun needs a worktree and the job connects to a shared database, so none was made)
- Reproduction: not reproduced. The workflow has 717 runs in 30 days and 2 failures; the other, [#37880001959](https://github.com/acme/batch-jobs/actions/runs/37880001959) on 10-09 11:35:50, shows a different symptom (`Internal Server Error`). None of the 6 commits since the failure touches the worker, the shared net package, or the database package.
- Symptom site at `7b3a2a5`: `apps/worker/src/persist.ts:197-211` inside the transaction opened at `:88`. The error reaches `runs.ts:171` and sets `process.exitCode = 1`, so one project's failed write fails the whole workflow.
- Why the log has no reason (read-source L0: drizzle-orm 0.45.2, matches the lockfile at `7b3a2a5`, no patch): `pg-core/session.js:36-67` wraps the driver error in a `DrizzleQueryError` whose message holds only the SQL and parameters, and the driver error sits in `.cause`. `packages/net/src/index.ts:29-34` logs `error.message` only, so the constraint name and SQLSTATE are dropped before anything is written.
- Mechanism (hypothesis, not reproduced): the upsert hit a foreign key check against a row deleted after it was read. The 6 threads were created between 00:02 and 00:27, and 28.4 s passed between the previous project finishing (00:29:03.5) and this one failing (00:29:31.9). For it: the select on `labels` just before succeeded, so the connection was alive, and the last model call warning came 0.59 s earlier, so it was not a timeout. Against it: a transient database error mid transaction cannot be ruled out. The records that would settle it are the Postgres log around 00:29:31 or whether those 6 threads still exist, and both are outside the stores available here.

**Coverage**
- GitHub: the window 38 of 38 runs (aggregate 38); the search one window length to each side, clipped at now (2026-10-10 00:00 to 2026-10-12 11:30:38), 136 of 136 (aggregate 136); no cap met.
- Vercel (the team): deployments pulled team wide; the 17 ERROR and CANCELED records near the window all belong to a project outside the mapping. Runtime 5xx and fatal returned 0 rows for the whole window; the error level query met the 50 row cap and was sliced into 24 hourly slices (173 rows, none capped). The 24 slices before the window hold 201 rows with 4 real errors, at least 20 h 52 min from its start. Alerts 0; activity paged to its last page.
- Skipped: unpushed branches and agent sessions (the same SHA ran good and bad, so no local change can be the trigger), PRs, reviews, issues, and releases.
- Not reachable: the Postgres log and the `threads` and `labels` tables, the change history of the Actions secrets, the model provider.
- Mapping: batch-jobs to its clone (origin acme/batch-jobs, an exact `gh search repos` match) to the 2 Vercel projects whose `link.repo` is that repo; a project that only shares a name prefix is not mapped. The clone sits at `5c6f86c`, an ancestor of the failing SHA, and was not fetched, so all code was read with `git show 7b3a2a5:<path>`.
````
