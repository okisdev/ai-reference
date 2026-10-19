---
description: normalize-agents-md takes a README that AGENTS.md calls the manual off the agent's path, moves the one rule inside it into AGENTS.md, and keeps the person-facing manual instead of cutting it or leaving the pointer.
tags: [quality, normalize-agents-md]
runs: 2
max_turns: 12
timeout_seconds: 540
allowed_tools: [Skill, Read, Bash]
---

Use the normalize-agents-md skill: 这个仓库的 md 文件经常被更改，README 越写越长，帮我收敛一下。

Everything you need is below; do not run commands, dispatch subagents, or write any file. This run covers the ledger and the rewrite only, so skip the loss check and measure.py. Repository: acme/notes, a desktop app. `apps/desktop/AGENTS.md`:

```md
# Notes desktop

The Electron app; `README.md` is its manual and the root `AGENTS.md` still applies.

## Rules

- Keep every IPC method behind a zod schema, because the renderer is untrusted.
```

`apps/desktop/README.md` is 41 KB and grew 6 KB last week; its outline and three excerpts:

```md
# Notes desktop

## Install
## Sync across devices
Turn on Sync in Settings › Account and sign in on the other device; notes, folders, and attachments follow within a few seconds, and a conflict keeps both versions side by side.
## Search
Search, the first row of the sidebar, finds notes by title and body while you type, newest first, and opens the one you pick where its folder would.
## Shortcuts
## Building
Never bump `electron` without rebuilding `better-sqlite3` against it, because the app crashes at launch with a NODE_MODULE_VERSION mismatch.
## Releasing
```

Reply with the ledger rows for the README pointer and each README excerpt (clause, disposition, reason), the rewritten `apps/desktop/AGENTS.md`, and what happens to the README.
