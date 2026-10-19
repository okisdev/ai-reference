---
description: verify-pr fills its CI row from the checks on the head and reports pending checks as pending, never from a local test run.
tags: [quality, verify-pr]
runs: 2
max_turns: 12
timeout_seconds: 420
allowed_tools: [Skill, Read, Bash]
---

Use the verify-pr skill on this PR. Everything you need is below; do not fetch or run anything.

PR #812 `fix(export): escape commas in CSV cells`, head 4be21c0, base 91aa0d3, closes #799 (a cell containing a comma splits into two columns). Diff: in `src/export/csv.ts` the cell writer now wraps a value containing a comma, a quote, or a newline in quotes and doubles inner quotes; a new test covers all three cases. Running `pnpm test` locally on the head passed: 41 files, 212 tests. `gh pr view 812 --json statusCheckRollup` on 4be21c0: `build` SUCCESS, `test` IN_PROGRESS, `e2e` QUEUED.

Reply with the full report.
