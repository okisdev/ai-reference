# Authoring skills

Skills here follow a lean, imperative register. The benchmark is butflow: short, imperative, useful. A long `SKILL.md` buries its load-bearing directive (per-instruction compliance decays, mid-prompt instructions are under-attended, context rot accumulates). Keep the always-loaded body lean; push detail into references.

## Anatomy

A skill is a directory `skills/<name>/` with a `SKILL.md`:

```
---
name: <name>                # must equal the directory name
description: <one sentence>  # routing signal only; see the YAML note below
argument-hint: "<args>"      # optional
---

## Context
<live `!` probe lines: the gh / git state the skill needs>

## Instructions
<one imperative line of intent>

### Process
1. <imperative step>
...
```

Detail that is looked up rather than read every run (large tables, repeated mechanics, build sequences) goes in `skills/<name>/references/<file>.md` with a one-sentence pointer from `SKILL.md`. See `ship-pr/references/build-pr.md`, `ship-pr/references/monitor.md`, `verify-pr-comments/references/bot-signatures.md`.

## The diet

Every skill obeys these. They came from a full-collection pass that cut roughly 18 percent with rigor intact.

1. No `Runtimes that do not auto-run...` boilerplate paragraph. Claude Code always runs the `!` probes; keep the probe lines, drop the explanation.
2. No standalone `### Input` section. Fold the `$ARGUMENTS` note as a parenthetical into Process step 1.
3. No `Distinct from siblings` block. Collapse it to one parenthetical on the opening line, or put it in the description.
4. The `description` is one tight sentence (a routing signal the executing agent never reads), not a process summary.
5. The `Rules` section keeps only additive safety guards. Delete any bullet that restates a Process step.
6. Imperative, not rationale. State what to do; cut the why. The one exception is a why that prevents a specific, non-obvious model failure.
7. Prefer flat numbered or bulleted lists. Each `###` sub-heading costs two lines.

## Rigor over line count

Short is not the goal; lean is. Do not cut into the do-not-cut floor: verification ladders, exact gh and GraphQL commands, `--json` field lists, output templates and schemas, decision tables, and safety guards. That content is why a skill is more useful, and more correct, than a one-liner. Complex skills legitimately run longer than butflow because they do more; butflow is short partly by being repo-specific and delegating safety elsewhere. After tightening a skill, verify that every load-bearing command, query, and template survived verbatim.

## Conventions

- Naming: `verb-noun`, imperative, reads like the `/command` it becomes (`create-pr`, `verify-pr`, `ship-pr`).
- Register: in-repo formal. Sentence case, no em-dashes or en-dashes as punctuation, no hard wrapping of prose.
- Frontmatter YAML is strict: a `description` plain scalar cannot contain an unquoted `: ` (a colon then a space), or `npx skills` silently skips the whole skill. Quote the value, or rephrase the colon to a period or semicolon.
- Context probes must be portable to macOS bash 3.2: a `case` pattern inside `$()` needs a leading `(`.

## Before you ship

- `name:` equals the directory name.
- The skill is listed in `.claude-plugin/plugin.json` and `README.md`.
- `npx skills add <repo> -l` lists the skill (proves the frontmatter parses).
- Bump the `.claude-plugin/plugin.json` version.
