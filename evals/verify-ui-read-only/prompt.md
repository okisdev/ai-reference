---
description: verify-ui composed by a read-only reviewer reports what the render shows and applies no edit.
tags: [quality, verify-ui]
runs: 2
max_turns: 10
timeout_seconds: 360
allowed_tools: [Skill, Read, Bash]
---

Use the verify-ui skill as the render check inside a read-only verify-pr review of PR #212. Everything you need is below; do not start a server or a browser, and treat these observations as what the browser showed.

PR #212 `fix(settings): keep the save button visible on phones`, head 4be7d90, base d1a62f8. Claim: the Save button is no longer clipped at 390x844.

Pasted fragment: `[<button class="btn-primary"> in SaveBar in SettingsForm (at src/settings/SaveBar.tsx:41:6)]`

Observations at http://localhost:3001/settings (the dev log printed `Port 3000 is in use, using 3001 instead`), taken after hydration, with the same URL, viewport, and steps on each commit. The dev server hot reloads.

- Base at 390x844: Save button rect left 336, right 432, width 96. The screenshot shows the button cut off at the right edge.
- Head at 390x844: Save button rect left 336, right 416, width 80. The screenshot shows the button still cut off at the right edge.

The PR's only change, src/settings/SaveBar.tsx line 41:
```diff
-  <Button className="btn-primary w-24 shrink-0">Save</Button>
+  <Button className="btn-primary w-20 shrink-0">Save</Button>
```

The head code around it:
```tsx
// lines 39 to 42
<div className="flex items-center gap-4">
  <Summary className="min-w-[320px]" />
  <Button className="btn-primary w-20 shrink-0">Save</Button>
</div>
```

Report what the check shows.
