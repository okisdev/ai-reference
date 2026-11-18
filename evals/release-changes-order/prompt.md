---
description: release-changes stops on a named change missing from the diff, orders the API before the destructive migration, and skips a docs-only target.
tags: [quality, release-changes]
runs: 2
max_turns: 8
timeout_seconds: 240
allowed_tools: [Skill, Read, Bash]
---

Use the release-changes skill to plan this release. Answer from this state only; do not run anything and do not touch the network.

I said this release must include the CSV export (#301) and the slug cleanup (#305). The repository is a monorepo with `apps/api` (a worker deployed with `wrangler deploy`), `packages/db` (SQL migrations applied with `pnpm db:migrate`), and `apps/docs` (a static docs site). The tree is clean and the head is on the remote. The last tag is v1.4.0, and the repository has no staging environment.

State of the release diff v1.4.0..HEAD:

- Merged PR #305 (slug cleanup) is in the diff. It changes `apps/api/src/notes.ts` so the API no longer reads the `notes.legacy_slug` column, and adds `packages/db/migrations/0017_drop_legacy_slug.sql`, which runs `ALTER TABLE notes DROP COLUMN legacy_slug`.
- The API currently running in production still reads `notes.legacy_slug`.
- A change to `apps/docs/content/getting-started.md`, a docs page.
- No merged PR or commit for #301 (CSV export) exists in the diff; its branch is still open.
