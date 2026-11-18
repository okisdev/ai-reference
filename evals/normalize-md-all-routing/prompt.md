---
description: An ask to question every markdown file in the repository, in the user's words, routes to normalize-md.
tags: [routing, normalize-md]
runs: 2
max_turns: 6
timeout_seconds: 180
allowed_tools: [Skill, Read, Bash]
---

仓库里所有的 md 文件都过一遍，看看哪些根本不该存在，哪些规则其实是错的。
