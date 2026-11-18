---
description: A Chinese request to handle every open issue and PR in batches routes to triage-backlog.
tags: [routing, triage-backlog]
runs: 2
max_turns: 6
timeout_seconds: 180
allowed_tools: [Skill, Read, Bash]
---

把这个仓库所有还开着的 issue 和 PR 都看一遍，按批次处理。先给我一份可以一次确认的计划，每批做完再告诉我下一批。
