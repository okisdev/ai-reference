# A file and rule challenge that clears the bar (illustrative)

The bar for the challenge: every markdown file answers who reads it and what breaks without it, every rule that stays carries the failure it prevents and its measured cost, untrue lines are rewritten from the code, and the loss check restores only what no ledger row decided. The repository, numbers, and files are invented; the shape is the bar.

Before (excerpts):

````md
<!-- AGENTS.md -->
- Run `make check` before finishing any change; it runs lint, typecheck, unit tests, the end-to-end specs mapped in `e2e/coverage.json`, and the Linux container rerun when a platform path changed.
- Keep `make check` under 60 seconds.
- `scripts/check-features.mjs` asserts every feature doc opens with a one-paragraph summary.
- Keep product copy byte for byte as it reads today.
````

````md
<!-- features/invoices.md -->
## Rules
- An invoice total is rounded once, at issue time.
## Interactions
- The list shows twelve rows per page with a gray header and a "New invoice" button at the top right.
````

````md
<!-- docs/plans/2025-q3-migration.md: the plan for a storage migration that finished in 2025 -->
````

Report, as the user reads it:

````
Files: 112 markdown files challenged. Deleted 3: docs/plans/2025-q3-migration.md (finished plan; no reader, no parser, no inbound link), docs/notes/sync-ideas.md and docs/notes/old-theme.md (no reader; their two rules moved to apps/desktop/AGENTS.md first). Proposed for deletion 1: docs/guides/self-host.md (a person may open it from the website, but its setup steps name a Docker image retired in 2026-03; rewrite or delete is yours). features/*.md (96 files) stay: scripts/check-features.mjs loads the folder, so they keep its front matter and sections.

Challenged rules, proposed (text left as found until you decide):
1. "Run make check before finishing any change": prevents shipping a break in a touched surface. Cost: median 14 min 20 s over the last 30 runs in .check/timings.json, every change; 9 of those runs started the Linux rerun for a change outside platform code, because 56 trigger paths are folder prefixes. Proposal: per change run lint, typecheck, unit tests, and the end-to-end specs mapped to the changed files themselves; run the full suite and the Linux rerun once before a release.
2. "Keep make check under 60 seconds": never true; the fastest of the last 30 runs took 4 min 51 s. Proposal: delete it, or make it a budget the estimate step enforces.
3. "Keep product copy byte for byte as it reads today": prevents drift during the 2025 copy migration, which finished; today it forbids every copy change. Proposal: delete.

Rewritten because untrue: "check-features.mjs asserts every feature doc opens with a one-paragraph summary" became "check-features.mjs asserts each feature doc's front matter and its Rules, Interactions, and Decisions sections" (read at scripts/check-features.mjs:41 to 77; it never checks an opening paragraph).

features/invoices.md: kept the rounding rule (prevents totals that differ by a cent between the list and the PDF; cost: none per change). Dropped the twelve rows, the gray header, and the button position (as-built description; the list component records it).

Loss check in a fresh subagent named 5 obligations absent from the new files: the three display details of features/invoices.md and two lines of the deleted plan. All five have drop rows with reasons, so none was restored. It named nothing without a row.
````

Why it clears the bar:

- Every file has a reader verdict with its proof, and the deletions split by evidence: a finished plan with no reader goes now, a guide a person may open is proposed with the reason it no longer holds.
- The three rules that cost the most or were never true are measured from the repository's own timing records and proposed with replacement text, while their text stays until the owner answers.
- The false enforcer claim is rewritten from the check's real assertions, cited by line, instead of being kept because a check exists.
- The loss check's findings are reconciled against the ledger, so deliberate cuts stay cut and the check still guards against accidents.
