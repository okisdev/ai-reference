---
description: An everyday ask to look at a table in the live database routes to inspect-db.
tags: [routing, inspect-db]
runs: 2
max_turns: 6
timeout_seconds: 180
allowed_tools: [Skill, Read, Bash]
---

看看数据库里 orders 这张表，status 字段有没有空值。
