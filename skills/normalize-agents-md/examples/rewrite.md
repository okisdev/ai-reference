# A rewrite that clears the bar (illustrative)

The bar for a rewrite: every clause of the old file is kept as one rule, moved to a named home, or dropped for a stated reason, so the loss check has nothing left to find. The repository, numbers, and files are invented; the shape is the bar.

Before, `CLAUDE.md` (excerpt):

````md
# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

Relay is a job queue and worker pool for internal services, written in TypeScript on Node 22 with pnpm. It started in 2024 as a weekend project and now carries 40 services.

## Repository structure

- `apps/api/`: the HTTP API
- `apps/worker/`: the worker process
- `packages/queue/`: the queue implementation
- `packages/pool/`: the worker pool

## Rules

- Always run `pnpm test` before committing. In March a hotfix skipped it, release 2.4.1 shipped with a broken lease renewal (#212), and it took two days to trace.
- Write clean, maintainable code and follow best practices.
- Never import from `packages/pool/src` outside `packages/pool`; `architecture.test.ts` asserts the import layering.
- The retry budget is per job, not global, because a global budget lets one failing job starve every other job. We argued about this for weeks (#198).
- Before changing anything under `apps/worker/src/lease/`, run `pnpm --filter worker test:integration`; it needs Docker running and takes about four minutes.
````

Before, `apps/worker/AGENTS.md`, with its Commands section uncommitted (the committed file is the title line):

````md
# worker

## Commands

- `pnpm --filter worker dev`: run the worker against local Redis.
````

After, `AGENTS.md` (excerpt; the file also ends with the standard's `Editing this file` section, copied verbatim):

````md
# relay

Job queue and worker pool for internal services; the README carries the rest.

## Commands

- `pnpm test`: gates every commit.

## Rules

- `architecture.test.ts` asserts that `packages/pool/src` is imported only inside `packages/pool`; when this file and the test disagree, the test wins.
- Keep the retry budget per job, because a global budget lets one failing job starve every other job.

## Where things live

- `apps/worker/AGENTS.md` carries the worker's rules.
````

After, `apps/worker/AGENTS.md`, rewritten on top of the user's line:

````md
# worker

The worker process; the root AGENTS.md still applies.

## Commands

- `pnpm --filter worker dev`: run the worker against local Redis.
- `pnpm --filter worker test:integration`: gates any change under `src/lease/`; needs Docker running and takes about four minutes.
````

Report, as the user reads it:

````
CLAUDE.md retired (214 lines, 11.2 KB). AGENTS.md 41 lines, 2.9 KB against the 8 KB root target; Codex chain 3.1 of 32 KiB at apps/worker; Grok 2,931 of 10,000 characters.
apps/worker/AGENTS.md had uncommitted changes (pending diff: +4 lines, the dev command under a new Commands heading); rewritten on top of it, the user's line kept.
Moved: the lease integration test command to apps/worker/AGENTS.md, because only worker changes need it.
Kept as a pointer: the import layering rule, after reading architecture.test.ts and its assertion on deep imports.
Dropped: the scaffold preamble (placeholder); the project overview (README carries it); the repository structure list (inventory, ls gives it); the March incident and release 2.4.1 (#212 and git carry it); "write clean, maintainable code" (generic advice); the weeks of debate behind the retry budget (#198 carries it).
Loss check in a fresh subagent: no obligation of the old file is missing from the new files or their destinations. measure.py --strict: clean; that is the command to wire into CI.
````

Why it clears the bar:

- Each of the five old rules is accounted for: three stay (one as a pointer to the test that enforces it), one moves down to the package it applies to, and one goes as generic advice. The preamble, overview, structure list, and incident story go with a reason each.
- Every kept rule is one bullet with at most one because-clause, and the incident story, the dates, and the issue numbers are gone.
- The dirty file is rewritten on top of the working copy, its pending diff is named, and the user's line survives.
- `CLAUDE.md` is retired rather than left as a stub, the placeholder preamble goes with it, and the report ends with the loss check and the `--strict` run.
