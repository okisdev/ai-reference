---
description: ship-pr stops at the first tick on CI that GitHub refused for billing, instead of waiting out the window.
tags: [quality, ship-pr]
runs: 2
max_turns: 8
timeout_seconds: 240
allowed_tools: [Skill, Read, Bash]
---

Use the ship-pr skill's monitor pass to decide what to do next for my PR #88 on acme/notes. Answer from this state only; do not run anything.

- Head `91be0c4`; verify-pr says Merge as-is on that head. No review threads, no required approvals.
- Check `CI / check` concluded FAILURE 2 seconds after it started, with 0 steps run. Its annotation reads: "The job was not started because recent account payments have failed or your spending limit needs to be increased."
- The latest `CI / check` run on `main` ended the same way an hour ago.
- The workflow runs `pnpm check`, `pnpm test`, and `pnpm build`.
- The check completed 40 seconds ago.
