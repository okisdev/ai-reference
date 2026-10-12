---
description: An ask to read a library's source in the user's own words routes to read-source.
tags: [routing, read-source]
runs: 2
max_turns: 6
timeout_seconds: 180
allowed_tools: [Skill, Read, Bash]
---

结合 zod 的源代码看看，z.coerce.boolean() 解析字符串 "false" 会得到什么。
