---
name: onboard-repo
description: Build a structured understanding of a repository before any edit, producing a compact map of entry points, conventions, and prior art with every claim cited by file.
argument-hint: "[focus-area]"
---

## Context

Top-level layout: !`ls -d */ 2>/dev/null | head -10`

Orientation docs present: !`out=""; for f in README.md AGENTS.md CLAUDE.md CONTRIBUTING.md; do test -f "$f" && out="$out $f"; done; echo "${out:-(none)}"`

Manifest identity: !`test -f package.json && jq -r '.name // empty' package.json 2>/dev/null || echo "(no package.json)"`

## Instructions

Read the repository's own orientation first, extract the idiom from real neighbors, and deliver a compact cited map before any edit lands.

### Process

1. Parse `$ARGUMENTS` (an optional focus area that narrows the deep reading; with none, map the whole repository at survey depth). No edit lands during this skill, whatever the follow-up task is.
2. Read the repository's own orientation docs first: README, AGENTS.md or CLAUDE.md, CONTRIBUTING. They outrank inference, and a conflict between them and the code is worth reporting.
3. Map the structure: workspaces and packages, entry points, where each kind of thing lives (apps versus packages, components versus utilities, tests, docs). Cite the manifest or directory that proves each claim.
4. Extract the idiom from exemplars: in the focus area, read 2 to 3 nearest siblings of whatever the follow-up task will touch (the neighboring component, hook, test, or doc) and record naming, file placement, import style, and export shape. The paradigm is what the neighbors actually do, not generic best practice.
5. Collect prior art: search for existing implementations, primitives, and helpers the follow-up task should reuse instead of rebuilding; list them with paths.
6. Reconcile with project memory via `use-project-memory`: read the index, pull forward constraints the map must respect, and update a stale topic instead of duplicating it.
7. Deliver the map: entry points, conventions observed (each cited by file), prior art found, constraints, and open questions. Then stop; a research or comparison ask ends here with zero edits.

### Rules

- No file edits during onboarding, and no edits at all when the ask was research or comparison.
- Every claim in the map cites a file; an impression without a path does not go in the map.
- The map is a working note for the session, not a document to commit.
