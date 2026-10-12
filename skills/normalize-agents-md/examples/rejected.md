# Rejected rewrite

A rewrite that shrinks the file and gets overturned at the loss check. It starts from the same `CLAUDE.md` and the same uncommitted `apps/worker/AGENTS.md` as `rewrite.md`. Compare yours against it before reporting.

````md
# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

@AGENTS.md
````

````md
# AGENTS.md

## Project overview

Relay is a job queue and worker pool for internal services, written in TypeScript on Node 22 with pnpm. It started in 2024 as a weekend project and now carries 40 services.

## Rules

- Always run `pnpm test` before committing and never import from `packages/pool/src`; in March a hotfix skipped the tests and release 2.4.1 shipped with a broken lease renewal (#212).
- Write clean, maintainable code and follow best practices.
- `apps/` holds the api and the worker; `packages/` holds the queue and the pool.
````

````
Done. CLAUDE.md slimmed to a stub and the content merged into AGENTS.md (11.2 KB to 3.1 KB). Skipped apps/worker/AGENTS.md: uncommitted changes. Removed the retry budget and lease test rules as too specific.
````

Why each part fails:

- The `CLAUDE.md` stub: every `CLAUDE.md` is retired, because even an `@AGENTS.md` stub switches Claude Code back to CLAUDE.md-only loading; a stub is for a repository that must serve Claude Code before 2.1.277 or Bedrock, Vertex, or Foundry, and the report says so.
- The scaffold line in the stub: a placeholder never survives. `measure.py` flags `placeholder` on both files and `claude-md` on the stub, and this report shows no run of it.
- `# AGENTS.md`: a title that names the file instead of the project is a placeholder.
- The project overview: product description goes to the README; only the title and its one-line summary stay.
- The first bullet holds two rules and the incident story: one rule per bullet with at most one because-clause, and the narrative goes nowhere because git and the PR carry it. The import rule is asserted by `architecture.test.ts`, so it becomes a one-line pointer to the test.
- `Write clean, maintainable code`: generic best practice that names nothing in this repository.
- `apps/ holds the api and the worker`: an inventory line that only says what a directory holds; `ls` gives it.
- The retry budget and lease test rules removed `as too specific`: a rule is never dropped to shorten a file, and the lease command moves down to the package it applies to; overflow past a target is reported, not cut.
- `Skipped apps/worker/AGENTS.md: uncommitted changes`: a dirty file is rewritten on top of the working copy and its pending diff is named (seen: it skipped an AGENTS.md with uncommitted changes that the user wanted it to build on).
- `Done` with a size headline: no moved and dropped lists and no loss check, so nobody can tell that the two removed rules were load-bearing; the loss check is exactly what would have found them.
