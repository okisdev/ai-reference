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

Two parts set the quality bar, and every skill whose output a person reads carries them:

- The intent line under `## Instructions` opens with the one rule that matters, in bold (`**The one rule: ...**`), then names what a great result looks like and points at the examples.
- `skills/<name>/examples/` holds one output that cleared the bar for each distinct shape of output the skill produces, usually one or two (real ones when they exist, each opening with a sentence on why it is the bar) and one rejected output whose every fault is named against the rule it breaks. The skill tells the agent to open the closest example before producing its output and to check the draft against the rejected one.

## The diet

Every skill obeys these. They came from a full-collection pass that cut roughly 18 percent with rigor intact.

1. No `Runtimes that do not auto-run...` boilerplate paragraph. Claude Code always runs the `!` probes; keep the probe lines, drop the explanation.
2. No standalone `### Input` section. Fold the `$ARGUMENTS` note as a parenthetical into Process step 1.
3. No `Distinct from siblings` block. Collapse it to one parenthetical on the opening line, or put it in the description.
4. The `description` is one tight sentence (a routing signal the executing agent never reads), not a process summary.
5. The `Rules` section keeps only additive safety guards. Delete any bullet that restates a Process step.
6. Imperative, with the fault that taught the rule. State what to do and cut generic rationale; when a rule came from a real failure, end it with `(seen: <the failure, in the words that reported it>)`, one clause and no story, because a rule that carries the fault that taught it is followed more reliably than the rule alone.
7. Prefer flat numbered or bulleted lists. Each `###` sub-heading costs two lines.

## Rigor over line count

Short is not the goal; lean is. Do not cut into the do-not-cut floor: verification ladders, exact gh and GraphQL commands, `--json` field lists, output templates and schemas, decision tables, and safety guards. That content is why a skill is more useful, and more correct, than a one-liner. Complex skills legitimately run longer than butflow because they do more; butflow is short partly by being repo-specific and delegating safety elsewhere. After tightening a skill, verify that every load-bearing command, query, and template survived verbatim.

## Conventions

- Naming: `verb-noun`, imperative, reads like the `/command` it becomes (`create-pr`, `verify-pr`, `ship-pr`).
- Register: in-repo formal. Sentence case, no em-dashes or en-dashes as punctuation, no hard wrapping of prose.
- Frontmatter YAML is strict: a `description` plain scalar cannot contain an unquoted `: ` (a colon then a space), or `npx skills` silently skips the whole skill. Quote the value, or rephrase the colon to a period or semicolon.
- A `description` leads with the job in the user's own words, in the language they type it, not with the skill's mechanism.
- Context probes must be portable to macOS bash 3.2: a `case` pattern inside `$()` needs a leading `(`.
- Context probes exit 0 in every environment, because Claude Code refuses to load a skill when any probe exits non-zero: end a probe that can fail with a fallback (`cmd 2>/dev/null || echo "(none)"`, or `out=$(...); echo "${out:-(none)}"` after a pipeline). `scripts/check-probes.py` runs every probe in an empty directory and in a fresh repository without a remote, under bash and zsh (seen: gh probes without a fallback kept create-pr, verify-pr, and ship-pr from loading in any session where gh was unauthenticated).
- A skill that can run longer than a few minutes sizes the job first: it tells the user the size and a time estimate before starting, runs `date` at each step, and reports when a step runs past twice its share.
- Context probes never use positional parameters, awk fields included, because Claude Code replaces `$N` with an argument before the shell runs and model invocations pass prose, so parse `$ARGUMENTS` in the Process (the validator enforces it).
- A piped check keeps its exit status with `set -o pipefail`, because `cmd | tail` reports tail's success.
- Waits and monitors: a step that waits on an external process states a heartbeat (a visible per-tick status line plus a liveness re-check, not just still-pending) and a wall-clock budget with the expiry action spelled out (keep waiting through the expected window, drop only a still-pending item that has gone quiet well past it, surface failed items as blockers, kill and report owned processes). No skill ships an unbounded wait. A command bound delivers SIGTERM (the ship-pr step 3 wrapper), never a bare `alarm; exec`: Go binaries such as gh catch SIGALRM and keep running.
- Process steps are written to be copied into the executing agent's plan verbatim, one self-contained action each; a consciously skipped step stays visible as `skip: <reason>` rather than silently dropped. An agent that paraphrases a checklist drops its gates.

## Evals

Every skill has a routing case in the user's own words, and a skill whose output a person reads has a quality case for its one rule: `evals/<skill>-<case>/prompt.md` plus `graders/*.md`, in the format `claude plugin eval init --bare` writes. A case puts the whole scenario in its prompt, because an eval run has no network, a redirected home, and an empty working directory, and it allows `[Skill, Read, Bash]` so the skill's probes can run. Routing graders are `tool_used` on `Skill` with `arm: both`; quality graders are `llm` judges with a concrete criterion, or `regex` with the pattern in frontmatter. A quality criterion states the outcome the user asked for, so that the skill's own success check cannot satisfy it alone (a digest whose counts are right but which never says what was produced fails). A case passes with the skill, and the delta against the no-plugin arm says what the skill adds.

## How a skill improves

Watch it run on a real ask, name what is wrong in one sentence, turn that sentence into the rule with its `(seen: ...)`, add an eval case that fails without the fix, fix it, and look again. The usage records (`distill-session`) say where to look first: rules the agent ignored, verdicts the user overturned, and asks that never routed.

A skill whose goal must hold after it runs (docs that stay rules, a memory store that stays small, a contract the next session keeps) is judged on the tree a week after its first real runs, never on its own checks passing: it names the measurement that shows the property held (`measure.py --since`, `check.py --dir`), and `distill-session` takes that measurement. A guard that holds such a property runs as a PostToolUse hook in every harness that edits here (Claude Code, Codex, Grok) and parses each one's payload, because a Claude-only hook misses most writes (seen: a normalizer whose every run passed its checks while the README it exempted grew 18 KB in four days, and a Claude-only hook that never saw Codex's edits).

## Before you ship

- `python3 scripts/check-probes.py` passes, and `claude plugin eval . --trust-plugin --allow-tools Bash --no-publish` passes the cases of every touched skill.
- `node scripts/validate-skills.mjs` passes. It enforces the mechanical checks (frontmatter parses, `name:` equals the directory name, the skill is listed in `.claude-plugin/plugin.json` and `README.md`), and CI runs the same script on every PR touching skills.
- `npx skills add <repo> -l` lists the skill (proves the consumer-side CLI parses the frontmatter too).
- `python3 scripts/test-memory-scripts.py` passes when a change touches `use-project-memory/scripts/check.py` or `clean-memory/scripts/audit.py`; CI runs it beside the validator.
- `python3 scripts/test-measure.py` passes when a change touches `normalize-agents-md/scripts/measure.py`; CI runs it beside the validator.
- Bump the `.claude-plugin/plugin.json` version.
