---
description: mirror-reference carries over a reference page's information layout, its grouping and per-row flags, while leaving its styling.
tags: [quality, mirror-reference]
runs: 2
max_turns: 12
timeout_seconds: 300
allowed_tools: [Skill, Read, Bash]
---

Use the mirror-reference skill: 参考 https://status.example.net/regions 的诊断页，重做我们的网络诊断，不必完全照抄。

Everything you need is below; do not fetch, run, or write anything. The reference page shows one card per region, grouped by continent; each card is headed by the region's country flag and name, then three rows (latency in ms, packet loss in percent, time of the last check) each with a colored status dot, and failing regions sort to the top of their group. Its styling: a dark navy theme, the Inter font, and rounded 16 px cards with drop shadows. Our page today is a title "Network" and one gray line of text per region ("tokyo: 182 ms, 0% loss"). Our design system has `Card`, `StatusDot`, `Flag`, and `SectionHeader`, a light theme, 8 px radii, and no shadows.

Reply with the take and not-take table and the planned page structure.
