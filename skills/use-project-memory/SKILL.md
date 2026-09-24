---
name: use-project-memory
description: Read and write Claude project auto-memory so Claude, Grok, and Codex share one store that holds only durable facts the repository and GitHub cannot give. Use at the start of interactive repo work (not in a delegated run), when such a fact is learned, or when the user says remember / 记住 / 项目记忆.
argument-hint: "[note]"
---

## Context

Memory: !`python3 "$HOME/.agents/skills/use-project-memory/scripts/resolve.py"`

## Instructions

Use Claude auto-memory as the only project store. Read the index first. Admit a fact only when the admission test passes, write it as one short topic plus one index line, and check every write.

### Process

1. Parse `$ARGUMENTS` (a note to store, or empty to load). Resolve the directory with `python3 "$HOME/.agents/skills/use-project-memory/scripts/resolve.py"`. If the probe printed `missing`, that path is still the write target.
2. Read `MEMORY.md` in that directory. It is an index (Claude loads the first 200 lines or 25KB). Open a linked topic file when a line is relevant to the current task. `ARCHIVE.md`, when present, indexes closed sagas; grep it before re-diagnosing or re-attempting anything old.
3. On load (no note): apply the matching topic files and continue the original task. A stored claim is a point-in-time observation, not proof; before a load-bearing one gates the current work, confirm it still holds on the live tree. A memory never relaxes a gate that an installed skill, the repository's `AGENTS.md`, or the global instructions set (a wait, a check, an approval, a prohibition); when one tries, follow the gate and name the topic for `clean-memory`. When the index has more than twenty lines and `.clean-memory.json` in that directory is missing or older than thirty days, say so in one line and continue; `clean-memory` is the pass that verifies the store. Do not summarize the whole index unless asked.
4. Admission test, before any write: store only a fact that changes a later decision and that nothing else already gives (the tree, git history, a PR or issue, an instruction file, a skill). Route every other candidate:

   | Candidate | Home |
   |---|---|
   | What shipped, when, and in which PR; measurements and run ids; a session's progress, plan, analysis, or report | Nowhere: the commit, PR, or issue already carries it; a report the user wants kept goes to an issue or a published page |
   | A rule for working in the repository (a trap, a prohibition, a command) that the repository can publish | This store as `feedback` for the first sighting; once it recurs or a review catches it, the repository's `AGENTS.md` under its editing contract (`normalize-agents-md` owns the format), and the rule leaves this store, because Codex and Grok never load it |
   | A change to how a skill behaves | That skill's source, proposed to the user |
   | A habit that holds in every repository | The global instruction file, proposed to the user |
   | A user decision, an external system fact, cross-repository state, or a private operational fact that still gates later work | This store |

5. On write: find the topic that already covers the fact and rewrite it to current truth in place; never append a dated update, a log entry, or a second version. A topic holds one fact: the claim, its citation (a SHA, issue number, or `file:line`), and for `feedback` one Why line and one How to apply line; a claim without a citation is labeled inference, not written as fact. A path in another repository is cited on a line that names that repository, and a path that no longer exists is cited on a line that says it moved or was removed, because `clean-memory` checks every other path against this tree. Touch the index line only when the status or the retrieval cue changed.
6. On a new fact: create one kebab-case `.md` named for its subject, never for a date or a session, with YAML frontmatter (`name`, `description`, `metadata.type` of `user`, `feedback`, `project`, or `reference`, and `metadata.verified`, the date a `clean-memory` pass last confirmed the topic against the tree, left unset until then). Add exactly one index bullet of the form `- [title](file.md) — hook`. The hook is the shortest cue that finds the topic, never more than 80 characters: a status token when the topic tracks work (SHIPPED, CLOSED, OPEN, PARKED, DISPROVEN, SUPERSEDED), the retrieval cue, and any standing prohibition. Everything else belongs in the topic file.
7. Check every write with `python3 "$HOME/.agents/skills/use-project-memory/scripts/check.py" <each written file> --strict` (hook 80 characters, topic 4 KB, index 200 lines and 25 KB, bullets only in the index, the frontmatter fields) and rewrite until nothing this write introduced fails; problems it did not introduce are left for `clean-memory`. A topic over the limit is compacted to the claims that still hold, never split into several topics.
8. Index pressure: when `MEMORY.md` is past 180 lines or 22KB, first move terminal lines (shipped or closed, no live leftover, no standing prohibition, no recurring recipe) verbatim to `ARCHIVE.md`. Move lines, never delete them, and never move or rename topic files. A line whose value is a standing prohibition stays in `MEMORY.md` regardless of age.
9. First write in a missing directory: create the directory and a `MEMORY.md` that contains only the new bullet.

### Rules

- Do not append prose to `MEMORY.md`. Do not rewrite the whole index. Do not use Grok `/remember`, Grok `~/.grok/memory/`, or Codex `~/.codex/memories/` for project facts.
- Never delete someone else's entries; the only sanctioned reductions are topic compaction, verbatim line moves to `ARCHIVE.md`, a rule's promotion into `AGENTS.md`, and the evidence-backed dispositions of `clean-memory`.
- When the admission test cannot name the later decision a fact changes, do not write it.
- Worktrees of the same git repo share the primary worktree's directory. The resolver already picks that path.
