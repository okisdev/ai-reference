---
description: design-dashboard writes its design contract as rules the next surface follows, never as a description of the dashboard it built.
tags: [quality, design-dashboard]
runs: 2
max_turns: 10
timeout_seconds: 300
allowed_tools: [Skill, Read, Bash]
---

Use the design-dashboard skill. The build is done and verified, so only its last step is left: leave the design contract in the app's AGENTS.md. Everything you need is below; do not run anything or write any file.

What was built: a Usage dashboard in `apps/web` showing the plan badge, three `RingGauge` cells for calls, storage, and seats, a `TrendArea` of daily calls with five date ticks, a `PeriodChart` comparing this month with the last, and an empty state with a one-line explanation. Decisions made during the build: every figure is right aligned in mono with tabular figures; each chart ends with a sentence naming the question it answers; a share is drawn only when the values span its scale, otherwise the absolute quantity is drawn; hue follows the entity and never its rank.

Reply with the exact lines you add to `apps/web/AGENTS.md`.
