---
description: verify-ui drives the browser tools a session exposes, choosing the one that can emulate what the check needs, instead of a fixed family.
tags: [quality, verify-ui]
runs: 2
max_turns: 10
timeout_seconds: 240
allowed_tools: [Skill, Read, Bash]
---

Use the verify-ui skill: check that the Save button on the settings page is no longer cut off on a phone, in both the light and the dark theme.

Everything you need is below; do not run anything, open a browser, or write any file. The dev server already serves the app at `http://localhost:3001` (its log printed `Port 3000 is in use, using 3001 instead`). The repository's instructions leave visual review to the agent and name no browser tool. This session exposes two browser tools and no other: Gode's site tools (`open_site`, `list_sites`, `emulate_site` with viewport, mobile, touch, and color scheme options, `run_in_site`, `capture_site`, `read_site`, `act_on_site`, `close_site`) and Claude in Chrome (`tabs_create_mcp`, `navigate`, `resize_window`, `javascript_tool`, `computer`, `read_page`, `tabs_close_mcp`). Chrome DevTools MCP is not installed.

Reply with the browser calls you would make, in order, and the report skeleton with what each call checks.
