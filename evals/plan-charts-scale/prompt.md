---
description: plan-charts holds a share form against the real values and draws the absolute quantity when most accounts sit near zero.
tags: [quality, plan-charts]
runs: 2
max_turns: 12
timeout_seconds: 300
allowed_tools: [Skill, Read, Bash]
---

Use the plan-charts skill: 用量页现在全是文字，帮我决定每个账户的额度用量该怎么展示。

Everything you need is below; do not run anything or write any file. The page lists accounts, each with a monthly allowance of API calls. Production over the last 30 days, 1,240 accounts: 1,170 used under 2 percent of their allowance, 52 used 2 to 50 percent, 12 used 50 to 80 percent, and 6 used over 80 percent (the highest 96 percent). Absolute use ranges from 0 to 2.1 million calls, and the median account made 3,400 calls. The page answers two questions: who is using the product, and who is close to their limit.

Reply with the catalog row for allowance use and the form you choose for each question, with the reason.
