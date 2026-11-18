---
description: An ask about what changed upstream since the pinned version routes to read-source for its drift question.
tags: [routing, read-source]
runs: 2
max_turns: 6
timeout_seconds: 180
allowed_tools: [Skill, Read, Bash]
---

我们依赖的那个 CLI 刚发了新版本，看看从我们现在用的版本到最新版之间改了什么，我们这边有没有需要跟着改的地方？
