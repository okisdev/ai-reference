---
name: use-project-memory
description: Read and write Claude project auto-memory so Claude, Grok, and Codex share one store. Use at the start of repo work, when a durable project fact is learned, or when the user says remember / 记住 / 项目记忆.
argument-hint: "[note]"
---

## Context

Memory: !`python3 "$HOME/.agents/skills/use-project-memory/scripts/resolve.py"`

## Instructions

Use Claude auto-memory as the only project store. Read the index first. Write a topic file plus one index line.

### Process

1. Parse `$ARGUMENTS` (a note to store, or empty to load). Resolve the directory with `python3 "$HOME/.agents/skills/use-project-memory/scripts/resolve.py"`. If the probe printed `missing`, that path is still the write target.
2. Read `MEMORY.md` in that directory. It is an index (Claude loads the first 200 lines or 25KB). Open a linked topic file when a line is relevant to the current task.
3. On load (no note): apply the matching topic files and continue the original task. Do not summarize the whole index unless asked.
4. On write: search the directory for an existing topic that already covers the fact and update it. Otherwise create one kebab-case `.md` with YAML frontmatter (`name`, `description`) and the fact in the body. Add exactly one index bullet: `- [title](file.md) one-line summary`. Keep `MEMORY.md` under 200 lines and 25KB by moving detail into topic files, never by deleting someone else's entries.
5. First write in a missing directory: create the directory and a `MEMORY.md` that contains only the new bullet.

### Rules

- Do not append prose to `MEMORY.md`. Do not rewrite the whole index. Do not use Grok `/remember`, Grok `~/.grok/memory/`, or Codex `~/.codex/memories/` for project facts.
- A new topic needs a one-sentence reason to exist. If you cannot give one, do not write it.
- Worktrees of the same git repo share the primary worktree's directory. The resolver already picks that path.
