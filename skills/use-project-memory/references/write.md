# Writing memory

Read before any write.

## Routing

Route every candidate that fails the admission test in `SKILL.md`:

| Candidate | Home |
|---|---|
| What shipped, when, and in which PR; measurements and run ids; a session's progress, plan, analysis, or report | Nowhere: the commit, PR, or issue already carries it; a report the user wants kept goes to an issue or a published page |
| What the code currently does: a surface, a route, a module's mechanism | Nowhere: the code is its record; a decision in it that would regress silently becomes a test, or a rule in the repository's instruction files |
| A rule for working in the repository (a trap, a prohibition, a command) that the repository can publish | This store as `feedback` for the first sighting; once it recurs or a review catches it, the repository's `AGENTS.md` under its editing contract (`normalize-agents-md` owns the format), and the rule leaves this store, because Codex and Grok never load it |
| A change to how a skill behaves | That skill's source, proposed to the user |
| A habit that holds in every repository | The global instruction file, proposed to the user |
| A user decision, an external system fact, cross-repository state, or a private operational fact that still gates later work | This store |

## Write

1. On write: find the topic that already covers the fact and rewrite it to current truth in place; never append a dated update, a log entry, or a second version. A topic holds one fact: the claim, its citation (a SHA, issue number, or `file:line`), and for `feedback` one Why line and one How to apply line; a claim without a citation is labeled inference, not written as fact. A path in another repository is cited on a line that names that repository, and a path that no longer exists is cited on a line that says it moved or was removed, because `clean-memory` checks every other path against this tree. Touch the index line only when the status or the retrieval cue changed.
2. On a new fact: create one kebab-case `.md` named for its subject, never for a date or a session, with YAML frontmatter (`name`, `description`, `metadata.type` of `user`, `feedback`, `project`, or `reference`, and `metadata.verified`, the date a `clean-memory` pass last confirmed the topic against the tree, left unset until then). Add exactly one index bullet of the form `- [title](file.md) — hook`. The hook is the shortest cue that finds the topic, never more than 80 characters: a status token when the topic tracks work (SHIPPED, CLOSED, OPEN, PARKED, DISPROVEN, SUPERSEDED), the retrieval cue, and any standing prohibition. Everything else belongs in the topic file.
3. Write topics and the index with the harness's editing tool (Claude Code's Edit and Write, Codex's `apply_patch`, Grok's `search_replace`), never `sed -i`, a heredoc, or a script, because `check.py --hook` runs as a PostToolUse hook on those tools in all three harnesses and sees nothing else (seen: a dated status line reached an index through `sed -i`, past the hook). Check every write with `python3 "$HOME/.agents/skills/use-project-memory/scripts/check.py" <each written file> --strict` (hook 80 characters, topic 4 KB, index 200 lines and 25 KB, bullets only in the index, the frontmatter fields, and no dated status line such as "since 2026-10-19" or "deployed 2026-10-15" outside the frontmatter). Pass every file the write touched, `MEMORY.md` included when the index changed, whichever harness wrote it; read the output for what this write introduced (its added lines, a topic it grew past 4 KB, an index it grew past the budget). Rewrite until nothing this write introduced fails; problems it did not introduce are left for `clean-memory`. A topic over the limit is compacted to the claims that still hold, never split into several topics.
4. Index pressure: when `MEMORY.md` is past 180 lines or 22KB, first move terminal lines (shipped or closed, no live leftover, no standing prohibition, no recurring recipe) verbatim to `ARCHIVE.md`. Move lines, never delete them, and never move or rename topic files. A line whose value is a standing prohibition stays in `MEMORY.md` regardless of age.
5. First write in a missing directory: create the directory and a `MEMORY.md` that contains only the new bullet.
