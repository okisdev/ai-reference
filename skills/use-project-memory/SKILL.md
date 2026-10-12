---
name: use-project-memory
description: Read and write Claude project auto-memory so Claude, Grok, and Codex share one store that holds only durable facts the repository and GitHub cannot give; use at the start of interactive repo work (not in a delegated run), when work surfaces a user decision, an external system fact, or a private operational fact that no commit, PR, issue, or instruction file can hold (never an analysis, plan, or build status just delivered), or when the user says remember / 记住 / 项目记忆.
argument-hint: "[note]"
---

## Context

Memory: !`python3 "$HOME/.agents/skills/use-project-memory/scripts/resolve.py"`

## Instructions

Use Claude auto-memory as the only project store. Read the index first. Admit a fact only when the admission test passes, write it as one short topic plus one index line, and check every write.

### Process

1. Parse `$ARGUMENTS` (a note to store, or empty to load). Take the store directory from the Context `Memory:` line (`dir <path>`); run `python3 "$HOME/.agents/skills/use-project-memory/scripts/resolve.py"` only when that line is empty or shows an error. If the probe printed `missing`, that path is still the write target.
2. Read `MEMORY.md` in that directory. It is an index (Claude loads the first 200 lines or 25KB). Open a linked topic file when a line is relevant to the current task. `ARCHIVE.md`, when present, indexes closed sagas; grep it before re-diagnosing or re-attempting anything old.
3. On load (no note): apply the matching topic files and continue the original task. A stored claim is a point-in-time observation, not proof; before a load-bearing one gates the current work, confirm it still holds on the live tree. A memory never relaxes a gate that an installed skill, the repository's `AGENTS.md`, or the global instructions set (a wait, a check, an approval, a prohibition); when one tries, follow the gate and name the topic for `clean-memory`. When the index has more than twenty lines and `.clean-memory.json` in that directory is missing or older than thirty days, say so in one line and continue; `clean-memory` is the pass that verifies the store. Do not summarize the whole index unless asked.
4. Admission test, before any write: store only a fact that changes a later decision and that nothing else already gives (the tree, git history, a PR or issue, an instruction file, a skill).
5. Before any write, read [references/write.md](references/write.md) (the routing table for every candidate the test rejects, the topic and index format, the check command, index pressure, and first-write setup) and follow it.

### Rules

- Do not append prose to `MEMORY.md`. Do not rewrite the whole index. Do not use Grok `/remember`, Grok `~/.grok/memory/`, or Codex `~/.codex/memories/` for project facts.
- Never delete someone else's entries; the only sanctioned reductions are topic compaction, verbatim line moves to `ARCHIVE.md`, a rule's promotion into `AGENTS.md`, and the evidence-backed dispositions of `clean-memory`.
- When the admission test cannot name the later decision a fact changes, do not write it.
- Worktrees of the same git repo share the primary worktree's directory. The resolver already picks that path.
