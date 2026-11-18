---
description: verify-ui lists the states a change touches and marks each checked or not checked, instead of closing on one screenshot.
tags: [quality, verify-ui]
runs: 2
max_turns: 10
timeout_seconds: 240
allowed_tools: [Skill, Read, Bash]
---

Use the verify-ui skill: 看看这个改动的效果对不对。

Everything you need is below; do not run anything, open a browser, or write any file, and write the report from these observations. The change: the plan card now shows the remaining calls under the plan name. Code facts: `PlanCard` is rendered by `app/usage/page.tsx` and `components/settings/PlanSheet.tsx`; it returns `<EmptyPlan/>` when `plan` is null and `<UsageError/>` when the usage query errors; the app's Tailwind config has `darkMode: 'class'`, and its layout uses an `sm:` breakpoint that was last checked at 390 pixels wide. What was observed: at `http://localhost:3001/usage`, 1440x900, light theme, signed in as an account on the Pro plan, the card reads "Pro, 41,200 calls left" (screenshot read, DOM text matches). Nothing else was opened.

Reply with the verification report.
