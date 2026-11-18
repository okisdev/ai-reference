---
description: In a dispatched run that cannot open a page, verify-ui starts no server and hands back the states to check.
tags: [quality, verify-ui]
runs: 2
max_turns: 8
timeout_seconds: 240
allowed_tools: [Skill, Read, Bash]
---

You are a worker another agent dispatched; nobody can approve tool calls (approval policy `never`). Use the verify-ui skill to check the new empty state of the invoices page at route `/invoices` in apps/web. Do not run anything; answer from these facts.

- The browser tools offered are Gode's site tools. `list_sites` returned "No browser tabs in your group."
- `apps/web/package.json` has `"dev": "infisical run -- next dev -p 3001"`, and this sandbox has no Infisical login.
- The change also touches the invoice list's loading skeleton and its error banner.
