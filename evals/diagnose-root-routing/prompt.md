---
description: An everyday why-did-this-fail ask routes to diagnose-root.
tags: [routing, diagnose-root]
runs: 2
max_turns: 6
timeout_seconds: 180
allowed_tools: [Skill, Read, Bash]
---

看看为什么这个测试失败了：src/cart/total.test.ts 里的 applies the coupon once 报错 expected 90 to be 81。
