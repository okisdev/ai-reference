---
description: verify-ui lists the states a change touches and marks each checked or not checked, instead of closing on one screenshot.
tags: [quality, verify-ui]
runs: 2
max_turns: 10
timeout_seconds: 240
allowed_tools: [Skill, Read, Bash]
---

Use the verify-ui skill: 看看这个改动的效果对不对。

Everything you need is below; do not run anything, open a browser, or write any file, and write the report from these observations. The change: the plan card now shows the remaining calls under the plan name. The card renders on `/usage` and in the Settings › Plan sheet; it has an empty state for accounts without a plan and an error state when the usage request fails; the app supports light and dark themes and is used at 1440 and 390 pixels wide. What was observed: at `http://localhost:3001/usage`, 1440x900, light theme, signed in as an account on the Pro plan, the card reads "Pro, 41,200 calls left" (screenshot read, DOM text matches). Nothing else was opened.

Reply with the verification report.
