---
name: normalize-agents-md
description: Rewrite a repository's AGENTS.md and CLAUDE.md files into short normative instruction files, routing incidents, inventories, and module internals to where they belong, within the size caps every harness reads.
argument-hint: "[scope]"
---

## Context

Instruction files and caps: !`python3 "$HOME/.agents/skills/normalize-agents-md/scripts/measure.py" . 2>/dev/null | head -25 || echo "(measure script unavailable)"`

Uncommitted instruction files: !`out=$(git status --short 2>/dev/null | grep -E '(AGENTS|CLAUDE|GEMINI)[^/]*\.md$' | head -5); echo "${out:-(none)}"`

Docs homes present: !`out=""; for f in README.md CONTRIBUTING.md ARCHITECTURE.md docs; do test -e "$f" && out="$out $f"; done; echo "${out:-(none)}"`

## Instructions

Rewrite every instruction file in scope into a short normative document: keep the rules, move everything else to its owning home, prove nothing load-bearing was lost, and stop at an uncommitted tree.

### Process

1. Parse `$ARGUMENTS` (a scope path, default the repository root; every instruction file under the scope is processed, and files above it are read for inheritance only). Keep the Context measurement as the before state. A file with uncommitted changes is `skip: uncommitted changes`, because another session may own it.
2. Read [references/standard.md](references/standard.md) (layout, caps, altitude test, routing table, template), then the project memory index via `use-project-memory`, then the repository's docs homes (README, CONTRIBUTING, ARCHITECTURE.md, `docs/`), so moved content lands in an existing home.
3. Inventory each file in scope: harness owner, symlink target, `@import` lines, managed blocks, and the nested files whose scope it overlaps. Files under vendored, generated, or fixture trees are classified and left unchanged.
4. Build the ledger in the scratchpad, never in the repository: split each editable file into clauses (a bullet holding several rules yields several entries), classify each clause with the standard's categories, and assign `keep`, `move <destination>`, or `drop <reason>`. A clause that claims a test, lint, or script enforces it stays a rule until the enforcer is found and its assertion read. A path or command the clause names is checked for existence, and a factual claim about the tree (a directory holds no X, a file is the only Y) is checked by grep; a stale one is corrected or dropped, never carried forward.
5. Write destinations before touching the source: incidents and decisions become a project memory topic via `use-project-memory` with the SHA or issue as citation; package-scoped rules go down into that package's AGENTS.md (created with the CLAUDE.md stub when missing); contributor process rules go to CONTRIBUTING.md when the repository is public; roles nobody can read from names go to the existing ARCHITECTURE.md or docs page, never a docs tree created for this; everything else goes nowhere.
6. Rewrite each file to the standard's template: one rule per bullet with at most one because-clause naming the failure it prevents, a rule an existing check asserts becomes a one-line pointer, a nested file holds only what the root does not. Managed blocks and import lines stay byte-identical. CLAUDE.md becomes exactly `@AGENTS.md` and a newline, plus a `## Claude Code` section only for Claude-only content; a diverging CLAUDE.md and AGENTS.md pair merges into AGENTS.md; CLAUDE.local.md is never touched. Then reread the result section by section and delete every survivor an agent could get from one `ls` or one manifest read, because filler survives the first pass in slimmed form, most often as pointers that only say what a directory holds.
7. Loss check in a fresh subagent with none of the rewriting context: hand it the old file, the new file, and the destinations, and ask for every obligation in the old file absent from the new file and its destinations. Restore or consciously drop each item it names, and record the reason. Then rerun `python3 "$HOME/.agents/skills/normalize-agents-md/scripts/measure.py" <scope> --strict`: every file within the caps, and every overflow past a target named with the rules that could not be cut.
8. Report per file the before and after bytes and lines, the Codex chain and Grok cap status, moved items with destinations, dropped items with reasons, contradictions resolved, skipped files, and the `measure.py --strict` command a repository can wire into CI. Stop at an uncommitted tree; committing composes `commit-changes`, shipping composes `ship-pr`.

### Rules

- A rule the file says nothing enforces is never dropped; it moves to the top of Rules.
- Nothing moves into an instruction file from memory, docs, or a session; the flow is one way.
- A size target is never met by deleting a rule; overflow is reported instead.
- No new dependency; the measure script stays Python 3 standard library.
