---
description: normalize-agents-md rewrites a design doc that AGENTS.md orders agents to read into rules only, dropping the as-built description, the drift log, and the orders to update the doc alongside code.
tags: [quality, normalize-agents-md]
runs: 2
max_turns: 12
timeout_seconds: 540
allowed_tools: [Skill, Read, Bash]
---

Use the normalize-agents-md skill: 这个 DESIGN.md 越写越长，像流水账，帮我收敛成规章。

Everything you need is below; do not run commands, dispatch subagents, or write any file. This run covers the ledger and the rewrite only, so skip the loss check and measure.py. Repository: acme/ledger, an Electron app. `apps/desktop/AGENTS.md` line 6 says: "Read `DESIGN.md` before any UI change." `apps/desktop/DESIGN.md` (excerpt):

```md
# Design

Where this file and the code disagree, this file wins. A new font, color, or control style is a change to this file first.

## Tables

Numbers in a table are right aligned in mono with tabular figures. A table never draws a rule between rows of one kind; rows are separated by rhythm and a hover fill.

## Accounts page

The Accounts page lists every account of the workspace, the one used last first, at most 50 at a time: each row shows the account's color swatch, its name, its balance in mono, the bank it syncs from, and when it last synced, and a row whose sync failed shows Failed in red with a Retry button.

## Drift found on 2026-09-12

- D4, density (2026-09-12): Reports used 40 pixel rows and Accounts 32, so the two lists read as two apps. List rows are 32 pixels everywhere.

## Building

Build only from the components this file names; if one is missing, add it to `src/design` and to this file in the same change.
```

Reply with the ledger rows (clause, disposition, reason), the rewritten excerpt, and the rewritten AGENTS.md line.
