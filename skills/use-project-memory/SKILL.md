---
name: use-project-memory
description: Read and write Claude project auto-memory so Claude, Grok, and Codex share one store that holds only durable facts the repository and GitHub cannot give; load it when a person starts work in a repository (a run another agent dispatched with a brief skips that load), and use it when work surfaces a user decision, an external system fact, or a private operational fact that no commit, PR, issue, or instruction file can hold (never an analysis, plan, or build status just delivered), or when the user says remember / 记住 / 项目记忆.
argument-hint: "[note]"
---

## Context

Memory: !`python3 "$HOME/.agents/skills/use-project-memory/scripts/resolve.py" 2>/dev/null || echo "(resolver unavailable)"`

## Instructions

**The one rule: write only a fact that changes a later decision and that nothing else already records.** A request to remember an analysis, an audit, a plan, or a build status gets no topic: say where the content belongs and write nothing. The bar is one cited fact, the decision it changes, and a hook that finds it: open [examples/topic.md](examples/topic.md) before a write, and check the draft against [examples/rejected.md](examples/rejected.md).

Use Claude auto-memory as the only project store. Read the index first. Admit a fact only when the admission test passes, write it as one short topic plus one index line, and check every write.

### Process

1. A run another agent dispatched skips the load at its start and reads nothing: its first message is a brief (a header naming a lane, a goal, a verification command, or acceptance criteria), and the agent that wrote it already holds what the run needs; an explicit ask to remember or recall still runs the rest of this process (seen: 777 of 999 Codex runs dispatched as briefs loaded this skill and 669 read the index, each reasoning it was "Preparing to start interactive repo work"). Otherwise parse `$ARGUMENTS` (a note to store, or empty to load). Take the store directory from the Context `Memory:` line (`dir <path>`); run `python3 "$HOME/.agents/skills/use-project-memory/scripts/resolve.py"` only when that line is empty or shows an error (seen: 64 of 80 runs reran resolve.py though the Context line already held its output). If the probe printed `missing`, that path is still the write target.
2. Read `MEMORY.md` in that directory. It is an index (Claude loads the first 200 lines or 25KB). Open a linked topic file when a line is relevant to the current task. `ARCHIVE.md`, when present, indexes closed sagas; grep it before re-diagnosing or re-attempting anything old.
3. On load (no note): apply the matching topic files and continue the original task. A stored claim is a point-in-time observation, not proof; before a load-bearing one gates the current work, confirm it still holds on the live tree. A memory never relaxes a gate that an installed skill, the repository's `AGENTS.md`, or the global instructions set (a wait, a check, an approval, a prohibition); when one tries, follow the gate and name the topic for `clean-memory`. When the index has more than twenty lines and `.clean-memory.json` in that directory is missing, older than thirty days, or records an after count the index has since grown past by half, say so in one line and continue; `clean-memory` is the pass that verifies the store (seen: seven days after a pass, a store held 30 topics, every one written or rewritten since, with dated status in its index and no `.clean-memory.json` to compare against). Do not summarize the whole index unless asked.
4. Admission test, before any write: store only a fact that changes a later decision and that nothing else already gives, whether the tree, git history, a PR or issue, an instruction file, or a skill (seen: 49 percent of sampled writes failed this test, among them analyses, audits, and BUILT status saved as topics, such as a requested hand-off latency analysis).
5. Before any write, read [references/write.md](references/write.md) (the routing table for every candidate the test rejects, the topic and index format, the check command, index pressure, and first-write setup) and follow it.

### Rules

- Do not append prose to `MEMORY.md`. Do not rewrite the whole index. Do not use Grok `/remember`, Grok `~/.grok/memory/`, or Codex `~/.codex/memories/` for project facts.
- Never delete someone else's entries; the only sanctioned reductions are topic compaction, verbatim line moves to `ARCHIVE.md`, a rule's promotion into `AGENTS.md`, and the evidence-backed dispositions of `clean-memory`.
- When the admission test cannot name the later decision a fact changes, do not write it.
- Worktrees of the same git repo share the primary worktree's directory. The resolver already picks that path.
