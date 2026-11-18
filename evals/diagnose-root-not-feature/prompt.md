---
description: A feature change with no failing symptom does not route to diagnose-root.
tags: [routing, diagnose-root]
runs: 2
max_turns: 4
timeout_seconds: 180
allowed_tools: [Skill, Read, Bash]
---

Goal: remove the recovery key option from the Rust sync client's settings struct and its two call sites. Nothing is failing; just describe the edit plan in a few lines, do not run anything.
