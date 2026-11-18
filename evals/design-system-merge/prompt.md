---
description: design-system merge moves shared principles into one file, leaves each product its extends line and its one difference, and marks an unstated reason as inferred.
tags: [quality, design-system]
runs: 2
max_turns: 10
timeout_seconds: 300
allowed_tools: [Skill, Read, Bash]
---

Use the design-system skill to merge these two products' design docs into one shared system. Everything you need is below; do not run commands and do not write files, show me the files you would write.

`pine-web/DESIGN.md`:

```
# Pine design
1. One accent per screen, because two primaries make users hunt for the next step.
2. Motion explains, never decorates, because ornamental motion reads as lag.
3. Every list has empty, loading, and error states, because users meet the unhappy states first.
Radius: 8 for cards. Enter animation: 180ms.
```

`fern-app/DESIGN.md`:

```
# Fern design
1. One accent per screen, because two primaries make users hunt for the next step.
2. Motion explains, never decorates, because ornamental motion reads as lag.
3. Every list has empty, loading, and error states, because users meet the unhappy states first.
Radius: 12 for cards. Enter animation: 180ms.
Labels name the outcome ("Save changes", never "OK").
```

The shared system lives in the repository `grove-design` at `DESIGN.md`. I never said why the label rule exists. Reply in English.
