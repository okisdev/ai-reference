---
description: approve-pr pushes small in-scope fixes on a contributor's PR the user asked to land, instead of drafting comments and waiting.
tags: [quality, approve-pr]
runs: 2
max_turns: 8
timeout_seconds: 240
allowed_tools: [Skill, Read, Bash]
---

/approve-pr 10547 --merge

Land this one today. Answer from this state only and say what you do next; do not run anything.

- assistant-ui/assistant-ui PR #10547 is by an outside contributor; I am a maintainer. `maintainerCanModify` is true.
- A verify-pr report on the current head `e03b7aa` (base `5d21c08`) says Merge after small fixes, with two Blocking items, both in files the PR already touches: `packages/react/src/thread.tsx:88` lacks a null check that the PR's own test `thread.test.tsx` covers once added, and `packages/react/src/thread.tsx:141` carries a comment that restates the next line and must go. It says both pass the fold-in test.
- No review threads are open and CI is green on `e03b7aa`.
