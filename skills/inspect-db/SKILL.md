---
name: inspect-db
description: Inspect a live database with real SQL before reasoning from ORM schema files, resolving the connection from the project's own configuration and staying read-only unless explicitly asked to write.
argument-hint: "[table-or-question] [--write]"
---

## Context

DATABASE_URL presence: !`test -f .env && grep -q '^DATABASE_URL=' .env && echo "in .env" || echo "(none)"`

ORM marker: !`if find . -maxdepth 1 -name 'drizzle.config.*' -print -quit | grep -q .; then echo "drizzle"; elif test -f prisma/schema.prisma; then echo "prisma"; elif { test -f wrangler.jsonc && grep -q d1_databases wrangler.jsonc; } || { test -f wrangler.toml && grep -q d1_databases wrangler.toml; }; then echo "wrangler d1"; else echo "(none)"; fi`

Packages with a database directory or schema file: !`out=$(find . -name node_modules -type d -prune -o \( -type d \( -iname db -o -iname database \) -o -iname schema.prisma -o -iname schema.ts \) -print 2>/dev/null | head -10); echo "${out:-(none)}"`

## Instructions

**The one rule: the live database answers first.** Read it with targeted SQL before reasoning from the ORM schema, treat any mismatch between the two as the finding, and stay read-only unless `--write` or an explicit ask says otherwise; a great report names the route and environment every query ran against, quotes both sides of every drift, backs each claim with a bounded query, and never prints a credential. The bar is [examples/inspection.md](examples/inspection.md): open it before writing, and check the draft against [examples/rejected.md](examples/rejected.md).

### Process

1. Parse `$ARGUMENTS` (a table name or a question about the data; `--write` opts into mutations and schema pushes, otherwise the whole session is read-only). Pick the connection route from the probes per [references/connect.md](references/connect.md): the Neon MCP tools when the project uses Neon, the `DATABASE_URL` from `.env` otherwise, and wrangler d1 for Cloudflare D1.
2. Read live structure first: list tables, then the DDL of the target table (`information_schema` or the platform equivalent). Assume drift; the live database is the authority for what exists right now, the ORM schema file is the authority for what the code expects, and the diff between them is the finding to report.
3. Read live data with targeted queries: always `LIMIT`, always name columns when a row is wide, never dump a whole table into the transcript.
4. Compare against the ORM schema files (drizzle schema, prisma schema) and report mismatches with both sides quoted.
5. For Cloudflare D1, never conflate `--local` (the miniflare sqlite under `.wrangler/state`) with `--remote` (production); name which one every query ran against.
6. With `--write`: `SELECT` the exact target rows first and report the count before any `UPDATE` or `DELETE` touches them, run the mutation, then `SELECT` again to prove the effect. For schema pushes, run the ORM's push through the repo's own tooling per [references/connect.md](references/connect.md) and rerun step 2 to confirm the live DDL moved.
7. Report the queries run, which connection route and environment they ran against, the row or DDL evidence, and any schema drift found.

### Rules

- Read-only is the default; no `INSERT`, `UPDATE`, `DELETE`, DDL, or schema push without `--write` or an explicit ask.
- A destructive statement always follows a `SELECT` of the same rows with the count reported.
- Connection strings and credentials never appear in output; name the host or project, never the full URL, and that includes a connection string the user pasted into the prompt (seen: a connection string pasted in a prompt).
