---
description: distill-session routes a lesson a match can enforce to a check, catches a silent user edit, and marks an unstated why as inferred.
tags: [quality, distill-session]
runs: 2
max_turns: 8
timeout_seconds: 300
allowed_tools: [Skill, Read, Bash]
---

Use the distill-session skill to turn these transcript excerpts into proposals for my skills collection (acme/agent-skills). The excerpts are all you have; do not read any files or run anything, and answer with the proposal table only.

- `a1b2.jsonl:88`, user: "don't use `git add -A` here, stage the files by name"
- `c3d4.jsonl:140`, user: "again, no `git add -A`"
- `e5f6.jsonl:52`, user: "why did you `git add -A` again?" (the commit-changes skill already says "Never `git add -A`")
- `a7b8.jsonl:210`, the agent wrote `transition: opacity 400ms ease-in` into `Dialog.tsx`; at `:233` a notice shows the user changed it to `transition: opacity 200ms ease-out` outside the agent's edits, and said nothing.
- `c9d0.jsonl:77`, the agent wrote `transition: transform 350ms ease-in` into `Popover.tsx`; at `:91` a notice shows the user changed it to `transition: transform 200ms ease-out` outside the agent's edits, and said nothing.
