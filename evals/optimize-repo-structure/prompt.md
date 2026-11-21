---
description: optimize-repo redraws the module map from what the code does and proposes merging modules that do the same job, instead of only deleting dead lines inside the current folders.
tags: [quality, optimize-repo]
runs: 2
max_turns: 8
timeout_seconds: 300
allowed_tools: [Skill, Read, Bash]
---

Use the optimize-repo skill on this private service (no version tags, never published). Everything you need is below; do not run commands and do not change files, tell me what the pass would change and why.

`src/` today:
- `src/notify/email.ts` builds a message from a template and sends it through the mailer; `src/notify/slack.ts` builds a message from the same template engine and posts it to Slack. Both copy the same 40-line retry loop.
- `src/alerts/dispatch.ts` decides who to notify and then calls `notify/email.ts` or `notify/slack.ts`; `src/reminders/dispatch.ts` does the same for reminders, with its own copy of the recipient lookup.
- `src/utils/format.ts` has one function, `formatMoney`, used only by `src/billing/invoice.ts`.
- `src/billing/invoice.ts` has a commented-out block of 30 lines and an unused export `legacyTotal`.
