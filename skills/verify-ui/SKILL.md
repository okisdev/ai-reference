---
name: verify-ui
description: Render and verify a web UI change in a real browser with a managed dev server, DOM assertions, and screenshots when asked to verify UI work or act on visual feedback.
argument-hint: "[url-or-route] [--port <n>] [--mobile]"
---

## Context

Dev script: !`jq -r '.scripts.dev // "(none)"' package.json 2>/dev/null || echo "(none)"`

Framework marker: !`if ls next.config.* >/dev/null 2>&1; then echo "next.config"; elif ls vite.config.* >/dev/null 2>&1; then echo "vite.config"; else echo "(unknown)"; fi`

Listening dev ports: !`lsof -nP -iTCP:3000-3010 -sTCP:LISTEN 2>/dev/null | head -5 || echo "(none)"`

## Instructions

Verify the claimed visual state in a real rendered browser with a screenshot or DOM assertion as evidence, manage the dev server lifecycle cleanly, and never kill processes by name.

### Process

1. Parse `$ARGUMENTS` (a route or full URL, `--port <n>`, `--mobile` for a phone viewport; with no arguments, take the target from the conversation instead: a pasted DOM fragment like `[<div class="..."> in Component (at path/file.tsx:85:6)]` names the exact source component and file, a pasted image is the reference state, a localhost URL is the page under test).
2. Read the repository's standing instructions (`AGENTS.md`, `CLAUDE.md`, project memory) for visual QA ownership before opening anything. When they say the user reviews visuals themselves, make the change, start no browser loop, and hand over. When they require asking before opening a browser, ask once.
3. Reuse a server already serving the app when the ports probe shows one listening; otherwise start one. Clear stale dev locks first (for Next.js, remove `.next/dev`, since a stale lock points at a reused PID and breaks startup), then start the dev script with `nohup`, redirect output to a scratch log, and record the PID. Follow [references/browser-loop.md](references/browser-loop.md) for the exact lifecycle commands.
4. Poll readiness with `curl --retry --retry-connrefused` against the expected port, then read the actual port from the log. Frameworks silently shift port when the default is busy (Next.js moves to 3001 on EADDRINUSE), and a hardcoded URL then tests the wrong app. Bound the poll (about 90 seconds); when it expires, stop waiting, capture the log tail as the failure evidence, kill the recorded PID, and report the startup failure instead of retrying past the budget.
5. Navigate with the browser tooling (Chrome DevTools MCP: `navigate_page`, `resize_page`, `emulate`, `evaluate_script`, `take_screenshot`) and size the viewport to the context the feedback came from; `--mobile` or a phone screenshot as the reference means a phone viewport.
6. Wait for hydration before asserting. Navigation resolves before the app hydrates, so sleep 1 to 2 seconds or poll for an app marker inside `evaluate_script` before querying.
7. Assert the specific claim. Query the exact node (the pasted fragment's file and line locate the component; edit that file rather than guessing from class names), take a screenshot, read it, and judge the result against the ask.
8. Iterate. Apply the edit, let hot reload pick it up, re-assert and re-screenshot the same URL at the same viewport, and report with the evidence.
9. Tear down. Kill only the recorded PID of the server this skill started, and leave any pre-existing server running.

### Rules

- Never `pkill`, `killall`, or kill by process name. Use only the exact PID recorded at startup, and only for a server this skill started.
- A curl 200 proves liveness, not visual correctness; every visual claim carries a screenshot or DOM assertion as evidence.
- Never screenshot-loop in a repository whose standing instructions say the user reviews visuals themselves.
