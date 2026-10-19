---
description: A run another agent dispatched with a brief does its package without loading use-project-memory or reading the memory index.
tags: [quality, use-project-memory]
runs: 2
max_turns: 8
timeout_seconds: 240
allowed_tools: [Skill, Read, Bash]
---

fusion-brief: v1
context-mode: isolated
package-type: consult
goal: say which of the two `formatBytes` implementations below in acme/web returns "1.5 KB" for 1536, and why.
scope: the two snippets below; read only, run nothing.
acceptance: one verdict line naming the implementation, then the reason in one sentence.

A: `const formatBytes = (n) => (n / 1024).toFixed(1) + " KB";`
B: `const formatBytes = (n) => Math.round(n / 1024) + " KB";`
