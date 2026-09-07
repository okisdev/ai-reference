# Instruction file standard

An instruction file holds the facts an agent cannot infer from the tree in a minute and the rules it would otherwise break. Everything else costs every session and reaches two of the three harnesses truncated.

## Layout

| File | Role |
|---|---|
| `AGENTS.md` | The canonical file, at the repository root and in any package that needs rules of its own. Every harness reads it. |
| `CLAUDE.md` | Exactly `@AGENTS.md` and a newline. A `## Claude Code` section below the import holds only content no other harness can use (plan mode, hooks, Claude-only tools). |
| `CLAUDE.local.md` | Personal and gitignored; never touched. |
| Nested `AGENTS.md` | The path-scoped layer that all three harnesses share: Codex and Grok concatenate root to cwd, Claude loads it when it reads files in that directory. `.claude/rules/` is Claude-only and never holds a rule another harness needs. |
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
| Product description | What the app is | One title line; the rest is README |
| Contributor process | PR etiquette addressed to contributors | CONTRIBUTING.md in a public repository, with one pointer left |
| Generic best practice | Names nothing repo-specific | Delete; global instructions carry habits |
| Package-scoped rule in the root | Applies only under one package | That package's AGENTS.md |
| Generated or managed block | Between markers | Byte-identical; never paraphrased, never moved |

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

## Managed blocks and imports

| Owner | Markers | Behavior |
|---|---|---|
| Next.js `next dev` (16.3 and later) | `<!-- BEGIN:nextjs-agent-rules -->` to `<!-- END:nextjs-agent-rules -->` | Rewritten on every dev start; content outside the markers survives byte for byte; with no AGENTS.md present it scaffolds one plus a `CLAUDE.md` holding `@AGENTS.md` |
| Next.js legacy | `<!-- NEXT-AGENTS-MD-START -->` to `<!-- NEXT-AGENTS-MD-END -->` | Stripped and replaced by the current block |
| Ruler | `# START Ruler Generated Files` to `# END Ruler Generated Files` | Regenerated from `.ruler/`; the source is edited, never the output |

`@path` imports load at launch in Claude (four hops deep, no context saved) and are plain text to Codex and Grok; an import line is never edited or moved, and a symlinked `CLAUDE.md` stays a symlink.

## Ledger

One row per clause: file, line, clause (first 80 characters), category, disposition (`keep`, `move <destination>`, `drop <reason>`), evidence (the enforcer path read, the existence check run, or the memory topic written). The loss check reads this ledger against the rewritten files, and the report's moved and dropped lists are derived from it.
