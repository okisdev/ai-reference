# Admitted topic (illustrative)

The bar for a write: one fact that the tree, git history, a PR or issue, and the instruction files cannot give, the later decision it changes, a citation, and an index hook that finds it in under 80 characters. The repository, job, and numbers are invented; the shape is the bar.

Topic `staging-db-weekly-reset.md`:

````md
---
name: staging-db-weekly-reset
description: "The shared staging Postgres is reset every Sunday 02:00 UTC by a job outside this repository"
metadata:
  type: reference
---

The platform team's job in the `acme/infra` repository, `jobs/staging-reset.yml:4`, restores the shared `relay-staging` database from the Friday snapshot every Sunday at 02:00 UTC. Rows written after Friday do not survive, and nothing in `acme/relay` schedules, mentions, or can stop the job.

**How to apply:** keep long-lived fixtures in `scripts/seed.ts`, not in staging, and run a migration rehearsal that must outlive a weekend on a branch database. A staging row that vanished on a Sunday is this job, not a bug in `src/queue/lease.ts`.
````

Index line, added to `MEMORY.md` (the em dash is the format's own separator):

````md
- [staging-db-weekly-reset](staging-db-weekly-reset.md) — resets Sundays 02:00 UTC; no long-lived rows
````

Why it clears the bar:

- It changes a later decision: where a fixture lives, and how a row that vanished on a Sunday is read.
- Nothing else gives it. The job lives in another repository, so this tree, its git history, its PRs and issues, and its `AGENTS.md` say nothing about it.
- One fact, one citation: a `file:line` in the repository that owns the job. That path sits on a line that names the repository, so `clean-memory` does not count it as a dead anchor, and the line number keeps the topic from being flagged uncited.
- It states current truth under a name for its subject, with no date or session in the name, at 0.7 KB of the 4 KB limit, and `metadata.verified` stays unset until a `clean-memory` pass confirms it.
- The hook is the retrieval cue plus the standing prohibition, 44 of 80 characters, and does not summarize the body.
