---
description: build-ui reads the exemplar the system names and the repository's primitive instead of asking for a reference or hand-rolling the component, and lists the states it will cover.
tags: [quality, build-ui]
runs: 2
max_turns: 10
timeout_seconds: 300
allowed_tools: [Skill, Read, Bash]
---

Use the build-ui skill for this ask. Everything you need is below; do not run commands and do not write code, tell me your plan and what you read.

Ask: build a filter dropdown for the orders list in `shop-web`.

State of the repositories (you may treat these as read):

- `shop-web/AGENTS.md` contains the line `Design system: design-systems:acme/DESIGN.md`.
- `design-systems/acme/DESIGN.md` has the Exemplars section line: `- **Dropdown**: shop-web:src/ui/menu.tsx, current, tokens only, tested.` It also has a Reject list entry: `A stock spinner → the 5 row skeleton.`
- `shop-web/src/ui/menu.tsx` exports a `Menu` primitive with `Menu.Trigger`, `Menu.Item`, and keyboard type-ahead, covered by `menu.test.tsx`.
- Other sibling repositories exist: `legacy-console` (stale) and `admin-web`.

Reply in English with: which files you read, what you reuse, and the states you will cover.
