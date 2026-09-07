# Instruction file standard

An instruction file holds the facts an agent cannot infer from the tree in a minute and the rules it would otherwise break. Everything else costs every session and reaches two of the three harnesses truncated.

## Layout

| File | Role |
|---|---|
| `AGENTS.md` | The canonical file, at the repository root and in any package that needs rules of its own. Every harness reads it. |
| `CLAUDE.md` | Exactly `@AGENTS.md` and a newline. A `## Claude Code` section below the import holds only content no other harness can use (plan mode, hooks, Claude-only tools). |
| `CLAUDE.local.md` | Personal and gitignored; never touched. |
| Nested `AGENTS.md` | The path-scoped layer that all three harnesses share: Codex and Grok concatenate root to cwd, Claude loads it when it reads files in that directory. `.claude/rules/` is Claude-only and never holds a rule another harness needs. A directory earns one by the coverage test below, never by existing. |
| `GEMINI.md`, `.cursor/rules/*.mdc`, `.github/copilot-instructions.md` | Harness mirrors; left as found, with any duplication of AGENTS.md reported rather than resolved. |

## Caps and targets

| Limit | Value | Source |
|---|---|---|
| Codex chain | 32 KiB shared by every AGENTS.md from repository root to cwd, root first; the tail is truncated silently | `project_doc_max_bytes` default in codex-rs `core/src/agents_md.rs` |
| Grok per file | 10,000 characters, truncated with a warning | Grok CLI 1.0.x README, AGENTS.md section |
| Claude per file | No cap under 4 MiB; the official target is under 200 lines, and adherence drops with length | code.claude.com/docs/en/memory |
| Root target | 8 KB and about 100 lines | Leaves room for a managed block and for growth before the next pass |
| Nested target | 5 KB and about 60 lines | A package file is read on top of the root |

`measure.py --strict` fails on a hard cap and reports the targets.

## Altitude test

Apply to one clause. A clause that fails the first question leaves the file; one that fails a later question is rewritten or moved.

1. What would an agent do differently because of this clause? No trigger and no observable action means it is description, history, or rationale.
2. Could an agent recover it from the tree in under a minute (`ls`, a manifest, the test it names)? Then the tree is the source of truth and the copy will drift.
3. Would it be false after the next refactor or the next file added? Then it is a census written at the wrong altitude.
4. Does it apply to most sessions in this directory? A rule for one package belongs in that package's file.
5. Can a reader judge compliance without knowing the incident? If not, keep the rule and the one failure class it prevents, and move the story.

## Routing

| Content | Test | Destination |
|---|---|---|
| Directive | States an obligation or prohibition with a trigger | Stays; one bullet, at most one because-clause |
| Rationale beyond one clause | Removing it would not let a forbidden alternative pass the rule | Drop; a decision record goes to project memory |
| Incident narrative | Dates, PR or issue numbers, measurements, "used to", "once", "the failure this rule names" | Project memory topic with the citation, or nowhere, since git already has it |
| Inventory | Lists files, directories, modules, or symbols with descriptions the tree carries | Delete; roles unreadable from names go to the existing ARCHITECTURE.md or docs page |
| Implementation detail | How one module works at a depth only its maintainer needs | The code, its tests, or docs |
| Mechanically enforced | A named test, lint, script, or CI job asserts it, confirmed by reading the assertion | One-line pointer: "`architecture.test.ts` asserts import layering; when this file and the test disagree, the test wins" |
| Command or verification recipe | Non-obvious build, test, lint, typecheck, and their scope | Stays; scripts obvious from the manifest are dropped |
| Pointer | Names the owning file and the decision that requires reading it; a line that only says what a directory holds is an inventory | Stays |
| Product description | What the app is, features, user setup, written for a reader | One title line stays; the rest goes to README when README lacks it, else is dropped |
| Agent-facing README section | A README section addressed to agents or stating obligations for code changes | AGENTS.md through this table; README keeps at most one pointer line |
| Contributor process | PR etiquette addressed to contributors | CONTRIBUTING.md in a public repository, with one pointer left |
| Generic best practice | Names nothing repo-specific | Delete; global instructions carry habits |
| Package-scoped rule in the root | Applies only under one package | That package's AGENTS.md |
| Placeholder | Would read the same in any repository: a generator's block, a scaffold preamble, a template heading with nothing repo-specific under it, a title that names the file, a TODO | Delete; a file that was only placeholder goes with its stub; a generator with a switch is turned off in the same pass (see Placeholders and generators) |

## Coverage

A directory without an AGENTS.md gets one only when at least one of these holds, and only when at least one rule or command then survives the altitude test:

1. The ledger moves a rule down to it from the root or an ancestor.
2. Its verification command or toolchain differs from the root: another package manager, a different language runtime, a deploy tool of its own, a test or typecheck entry the root does not run.
3. Its own README, manifest, or scripts name a trap an agent working there would hit.

Examples and templates never get one; the root's rules cover them. A file with nothing to say is not created, because an empty nested file costs a read in every harness and invites the next accretion. A repository with no root file gets the minimal root from the template: title line, commands, the editing contract, and the CLAUDE.md stub.

## Template

Root:

```md
# <repo name>

<One line: what this repository is. The README carries the rest.>

## Commands

- `<command>`: <what it gates and when to run it>

## Rules

- <Imperative rule>, because <the failure it prevents>.
- `<check>` asserts <invariant>; when this file and the check disagree, the check wins.

## Where things live

- `<path>` owns <concern>; read it before changing <what>.
- `packages/<name>/AGENTS.md` carries that package's rules.

## Editing this file

- One rule per bullet, imperative, with at most one because-clause naming the failure it prevents.
- A lesson from one session goes to commit messages, issues, or the maintainer's memory store; a rule enters here only when the same mistake repeats or a review catches it.
- A rule an existing check asserts is a one-line pointer to that check, not a restatement.
- Keep this file under 8 KB and any nested AGENTS.md under 5 KB; no inventories, dates, issue numbers, or module internals.
```

Nested (a package or app):

```md
# <package name>

<One line: what this package is; the root AGENTS.md still applies.>

## Commands

- <Only commands that differ from the root.>

## Rules

- <Only rules the root does not carry, or explicit local exceptions.>

## Where things live

- <Only pointers local to this package.>
```

Empty headings are dropped. Rules are grouped under sub-headings only past about twelve bullets. The Editing this file section is copied verbatim into every root file; it is the anti-accretion contract, and a repository never gets a softened copy.

## Placeholders and generators

A placeholder is text that would read the same in any repository: the fixed block a framework writes, a scaffold preamble ("This file provides guidance to Claude Code"), a template heading with nothing repo-specific under it, a title that names the file instead of the project, a TODO or fill-in marker, a section that restates the README. Placeholders are deleted whatever wrote them; a file that was only placeholder is deleted together with its CLAUDE.md stub. Content is not a placeholder because a tool wrote it: a compiled output that carries this repository's own rules (Ruler's rendered block) is edited at its source and never deleted.

A generator that would write the placeholder back is switched off in the same pass when it has a switch. When it has none, or the marker is unknown, the placeholder is still deleted and the report names the marker, so a re-creation shows up in the next pass and the generator is then hunted down.

| Generator | Markers or signature | Behavior | Switch |
|---|---|---|---|
| Next.js `next dev` (16.3 and later) | `<!-- BEGIN:nextjs-agent-rules -->` to `<!-- END:nextjs-agent-rules -->`, legacy `<!-- NEXT-AGENTS-MD-START -->` to `<!-- NEXT-AGENTS-MD-END -->` | Written when an AI agent runs `next dev` and the current block is missing: appended to an existing AGENTS.md, else to CLAUDE.md, else scaffolded as AGENTS.md plus a `CLAUDE.md` holding `@AGENTS.md`; content outside the markers survives byte for byte | `agentRules: false` in that app's next.config. Keep one root line saying Next docs live in `node_modules/next/dist/docs` and are read before writing Next code. A directory under `templates/` ships to users, so it is reported and left as found |
| `create-next-app`, `create-expo-app`, Claude `/init`, Codex and Cursor scaffolds | The scaffold preamble, a file-name title, template headings | Written once at creation, never again | None needed; delete |
| Ruler | `# START Ruler Generated Files` to `# END Ruler Generated Files` | Compiled from `.ruler/` sources, repo-specific | Not a placeholder; edit `.ruler/`, report it |
| Unknown markers | Any other `BEGIN` and `END` pair with generic wording | Owner not identified | Delete and report the marker |

`@path` imports load at launch in Claude (four hops deep, no context saved) and are plain text to Codex and Grok; an import line is never edited or moved, and a symlinked `CLAUDE.md` stays a symlink. A CLAUDE.md stub whose AGENTS.md is deleted goes with it.

## README and AGENTS.md

The two files have different readers and the skill sorts content by reader, in both directions. README answers a person deciding whether and how to use the project: what it is, why, install, run, features, configuration, license, where to contribute. AGENTS.md answers an agent about to change the code: obligations, the commands that gate a change, traps, where things live. The test for one clause is who acts on it: a person reading about the project keeps it in README, an agent editing the code gets it in AGENTS.md, and a clause both need lives in one file with a one-line pointer from the other.

README sections that were written for agents (headings naming agents, Claude, Codex, Cursor, or Copilot; convention, rule, gotcha, or guideline sections that only matter when changing code; do-not lists) are ledgered like any instruction file, moved into AGENTS.md through the routing table, and replaced in the README by at most one line saying where agent instructions live. Human-facing content found in AGENTS.md (product description, feature lists, user setup, architecture overviews written for readers) moves to the README when the README lacks it and is dropped when the README already carries it. The README is edited only in the sections the ledger names; its other content, structure, and badges are left as found. The loss check covers the old README as well as the old instruction files.

A README-only directory that is not a workspace package or app gets no AGENTS.md, because no harness loads anything there; its agent-facing sections move to the nearest ancestor AGENTS.md instead.

## Ledger

One row per clause: file, line, clause (first 80 characters), category, disposition (`keep`, `move <destination>`, `drop <reason>`), evidence (the enforcer path read, the existence check run, or the memory topic written). The loss check reads this ledger against the rewritten files, and the report's moved and dropped lists are derived from it.
