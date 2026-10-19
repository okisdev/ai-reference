---
name: verify-ui
description: Render and verify a web UI in a real browser, loaded before using chrome-devtools or claude-in-chrome, when asked to look at a result, take a screenshot, open localhost, check mobile or dark mode, or act on pasted-image feedback (看看效果, 截图, 打开浏览器).
argument-hint: "[url-or-route] [--port <n>] [--mobile]"
---

## Context

Dev script: !`jq -r '.scripts.dev // "(none)"' package.json 2>/dev/null || echo "(none)"`

Framework marker: !`if find . -maxdepth 1 -name 'next.config.*' -print -quit | grep -q .; then echo "next.config"; elif find . -maxdepth 1 -name 'vite.config.*' -print -quit | grep -q .; then echo "vite.config"; else echo "(unknown)"; fi`

Listening dev ports: !`out=$(lsof -nP -iTCP:3000-3010 -sTCP:LISTEN 2>/dev/null | head -5); echo "${out:-(none)}"`

## Instructions

**The one rule: every visual claim rests on what the browser rendered and you read.** A diff that reads right, a green build, and a 200 response all stop short of pixels, and a fix claim needs the broken state and the fixed state under the same URL, viewport, and steps. The bar is a report where each claim sits beside the evidence that decides it, with the URL, port, and viewport it was measured at, every page that renders a shared component, and what was not checked: open [examples/render-check.md](examples/render-check.md) before reporting, and check the draft against [examples/rejected.md](examples/rejected.md).

Verify the claimed visual state in a real rendered browser with a screenshot or DOM assertion as evidence, manage the dev server lifecycle cleanly, and never kill processes by name.

### Process

1. Parse `$ARGUMENTS` (a route or full URL, `--port <n>`, `--mobile` for a phone viewport; with no arguments, take the target from the conversation instead: a pasted DOM fragment like `[<div class="..."> in Component (at path/file.tsx:85:6)]` names the exact source component and file, a pasted image is the reference state, a localhost URL is the page under test).
2. Read the repository's standing instructions (`AGENTS.md`, `CLAUDE.md`, project memory) for visual QA ownership before opening anything. When they say the user reviews visuals themselves, make the change, start no browser loop, and hand over. When they require asking before opening a browser, ask once.
3. Reuse before building: a server already serving the app when the ports probe shows one listening, and the repo's own browser harness (Playwright or Cypress suites, Storybook, an Electron debug launch) when one exists, since it already knows startup, auth, and fixtures; otherwise start the dev server. Clear stale dev locks first (for Next.js, remove `.next/dev`, since a stale lock points at a reused PID and breaks startup), then start the dev script with `nohup`, redirect output to a scratch log, and record the PID. Follow [references/browser-loop.md](references/browser-loop.md) for the exact lifecycle commands.
4. Poll readiness with `curl --retry --retry-connrefused` against the expected port, then read the actual port from the log. Frameworks silently shift port when the default is busy (Next.js moves to 3001 on EADDRINUSE), and a hardcoded URL then tests the wrong app. Bound the poll (about 90 seconds); when it expires, stop waiting, capture the log tail as the failure evidence, kill the recorded PID, and report the startup failure instead of retrying past the budget.
5. Navigate with the browser tooling (Chrome DevTools MCP: `navigate_page`, `resize_page`, `emulate`, `evaluate_script`, `take_screenshot`) and size the viewport to the context the feedback came from; `--mobile` or a phone screenshot as the reference means a phone viewport.
6. Wait for hydration before asserting. Navigation resolves before the app hydrates, so sleep 1 to 2 seconds or poll for an app marker inside `evaluate_script` before querying.
7. Assert the specific claim. Query the exact node (the pasted fragment's file and line locate the component; open that file rather than guessing from class names), take a screenshot, read it, and judge the result against the ask. Then list the states the change touches (each viewport the surface supports, light and dark, empty, loading, error, and each flag or permission that changes the surface) and check each or mark it not checked with the reason, because one screenshot of one state never closes a run (seen: one screenshot of one viewport, then "真实代码渲染确认…提交这个 PR").
8. Iterate only when the request authorized fixing. Apply the edit, let hot reload pick it up, re-assert and re-screenshot the same URL at the same viewport, and report with the evidence. A "this fixes X" claim needs both sides: capture the broken state from the pre-change code first (same URL, viewport, and steps), then the fixed state, since an after-only screenshot cannot show that anything changed. A fix to a shared component is re-asserted on every page that renders it, not only the page the feedback named. When the request asked only to look, or a read-only caller composes this skill for evidence, apply no edit: capture the state, report what the screenshots and assertions show, label any change you suggest as not applied, and hand the finding back (seen: a read-only caller's run was told to apply edits).
9. Tear down. Kill only the recorded PID of the server this skill started, and leave any pre-existing server running.

### Rules

- Never `pkill`, `killall`, or kill by process name. Use only the exact PID recorded at startup, and only for a server this skill started.
- A curl 200 proves liveness, not visual correctness; every visual claim carries a screenshot or DOM assertion as evidence.
- Never screenshot-loop in a repository whose standing instructions say the user reviews visuals themselves.
- Never add Playwright or another browser dependency to the project just for this verification; use what is installed or the browser tooling.
- Never inject DOM or app state to produce the state under test; drive the UI the way a user would, and use state inspection only to confirm what was observed.
- In a workspace showing personal or customer data, do not save screenshots or snapshots without the user's agreement.
- Run every browser check through this process, a quick look at localhost and a check another skill composes included; a raw `chrome-devtools` or `claude-in-chrome` call skips the standing-instructions check, the port read, the hydration wait, and the teardown (seen: browser checks in 82 sessions ran through raw browser tools without it).
