---
description: normalize-md weighs process rules on their measured cost, rewrites a false enforcer claim, keeps a deliberate rewrite at the loss check, and restores a proposed rule a draft dropped.
tags: [quality, normalize-md]
runs: 2
max_turns: 8
timeout_seconds: 300
allowed_tools: [Skill, Read, Bash]
---

Use the normalize-md skill on this repository's root `AGENTS.md`. Nothing here is on disk; answer from these facts with the ledger rows for these four lines and the report you would give me, and do not run anything.

The four lines of `AGENTS.md` under Rules:

1. `Run make check before finishing any change; it runs lint, typecheck, unit tests, the e2e specs mapped in e2e/coverage.json, and the Linux container rerun when a platform path changed.`
2. `Keep make check under 60 seconds.`
3. `scripts/check-features.mjs asserts every feature doc opens with a one-paragraph summary.`
4. `Keep product copy byte for byte as it reads today.`

Facts you have measured:

- `.check/timings.json` holds the last 30 `make check` runs: median 14 min 20 s, fastest 4 min 51 s, slowest 31 min. 9 of the 30 ran the Linux rerun for changes outside platform code, because 56 of its trigger paths are folder prefixes.
- `scripts/check-features.mjs` lines 41 to 77 assert each feature doc's front matter and that it has Rules, Interactions, and Decisions sections; nothing in it reads an opening paragraph.
- Line 4 came in with a copy migration that finished in 2025; `git log` shows no copy change since, and two later PRs were told to revert copy edits because of it.
- A loss check you ran in a fresh subagent named two obligations missing from your draft: line 3's opening-paragraph claim, which your ledger had rewritten to what the check asserts, and line 4, which your ledger marks `propose removal` but which your draft had dropped.
