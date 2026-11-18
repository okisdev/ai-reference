# Authoring skills

Rules every skill under `skills/` follows; AGENTS.md names the section each kind of change reads first. Where a skill breaks a rule here, the skill is fixed.

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

Detail that is looked up rather than read every run (large tables, repeated mechanics, build sequences) goes in `skills/<name>/references/<file>.md` behind a one-sentence pointer from `SKILL.md`, because every line of `SKILL.md` loads on every run; `ship-pr/references/monitor.md` is the model.

Two parts set the quality bar, and every skill whose output a person reads carries them:

- The intent line under `## Instructions` opens with the one rule that matters, in bold (`**The one rule: ...**`), then names what a great result looks like and points at the examples.
- `skills/<name>/examples/` holds one output that cleared the bar for each distinct shape of output the skill produces, usually one or two (real ones when they exist, each opening with a sentence on why it is the bar) and one rejected output whose every fault is named against the rule it breaks. The skill tells the agent to open the closest example before producing its output and to check the draft against the rejected one.

## The diet

Every skill obeys these.

1. No `Runtimes that do not auto-run...` boilerplate paragraph. Claude Code always runs the `!` probes; keep the probe lines, drop the explanation.
2. No standalone `### Input` section. Fold the `$ARGUMENTS` note as a parenthetical into Process step 1.
3. No `Distinct from siblings` block. Collapse it to one parenthetical on the opening line, or put it in the description.
4. The `description` is one tight sentence, a routing signal rather than instructions the run follows, never a process summary.
5. The `Rules` section keeps only additive safety guards. Delete any bullet that restates a Process step.
6. Imperative, with the fault that taught the rule. State what to do and cut generic rationale; when a rule came from a real failure, end it with `(seen: <the failure, in the words that reported it>)`, one clause and no story, because a rule that carries the fault that taught it is followed more reliably than the rule alone.
7. Prefer flat numbered or bulleted lists. Each `###` sub-heading costs two lines.

## Rigor over line count

- `validate-skills.mjs` caps each `SKILL.md` at 20 KiB; when this file and the script disagree, the script wins.
- A skill near the cap moves procedural mechanics (watch commands, wrappers, formats) into references and keeps every decision rule in `SKILL.md`, because a rule that only a reference holds gets skipped.
- Never cut verification ladders, exact gh and GraphQL commands, `--json` field lists, output templates and schemas, decision tables, or safety guards when tightening a skill, because they are what make it more correct than a one-liner.
- After tightening a skill, verify that every load-bearing command, query, and template survived verbatim.

## Conventions

- Naming: `verb-noun`, imperative, reads like the `/command` it becomes (`create-pr`, `verify-pr`, `ship-pr`).
- Register: in-repo formal. Sentence case, no em-dashes or en-dashes as punctuation, no hard wrapping of prose.
- Quote a `description` that contains `: `, or rephrase the colon to a period or semicolon, because `npx skills` silently skips a skill whose frontmatter does not parse; `validate-skills.mjs` fails on it.
- A `description` leads with the job in the user's own words, not with the skill's mechanism, and is written in English; a phrase in another language goes in only when a routing eval in that language fails without it.
- Skill text is English. A `(seen: ...)` clause paraphrases a report made in another language instead of quoting it, and examples are written in English; another language appears only where a skill needs the exact string. Eval prompts keep the language users type, because they test that those asks still route.
- A step that drives an outside tool names the operation it needs and takes the tool from those the session exposes; vendor tool names live in a reference table beside each tool's traps, never in a Process step, because tools differ across machines and change over time.
- Context probes must be portable to macOS bash 3.2: a `case` pattern inside `$()` needs a leading `(`.
- Every Context probe exits 0 in every environment (end a fallible one with `cmd 2>/dev/null || echo "(none)"`, or `out=$(...); echo "${out:-(none)}"` after a pipeline), because Claude Code refuses to load a skill when a probe exits non-zero; `scripts/check-probes.py` asserts it.
- A skill that can run longer than a few minutes sizes the job first: it tells the user the size and a time estimate before starting, runs `date` at each step, and reports when a step runs past twice its share.
- Context probes never use positional parameters, awk fields included, because Claude Code substitutes `$N` before the shell runs; `validate-skills.mjs` fails on them, so parse `$ARGUMENTS` in the Process.
- A piped check keeps its exit status with `set -o pipefail`, because `cmd | tail` reports tail's success.
- A step that waits on an external process states a heartbeat (a visible status line per tick plus a liveness recheck) and a wall-clock budget with its expiry action (keep waiting through the expected window, drop only an item gone quiet well past it, surface failures as blockers, kill and report owned processes); no skill ships an unbounded wait.
- A command bound delivers SIGTERM, as the wrapper in ship-pr's `references/monitor.md` does, never a bare `alarm`; `exec`, because `gh` and other Go binaries catch SIGALRM and keep running.
- Process steps are written to be copied into the executing agent's plan verbatim, one self-contained action each; a consciously skipped step stays visible as `skip: <reason>` rather than silently dropped. An agent that paraphrases a checklist drops its gates.

## Standing alone

A skill works when it is the only one installed, because `npx skills add --skill` installs a single folder.

- A skill that cannot do its job without another declares it in `metadata.requires`, a space-separated list, and its README entry repeats it under **Requires**; keep the list to what the skill's own output depends on.
- Any other skill is named as an option: the step still succeeds without it ("read the source at the pinned version (`read-source` when installed)"), or the skill is only suggested to the user.
- A Context probe reaches its own script through `d="${CLAUDE_SKILL_DIR}"; python3 "${d:-$HOME/.agents/skills/<name>}/scripts/<file>"`, and a Process step names `<this skill's directory>`, because an install lands in `~/.agents/skills` or `~/.claude/skills` depending on its agents, and Claude Code substitutes only the exact `${CLAUDE_SKILL_DIR}`.
- A skill reads files only from its own folder or from a skill it requires; a script or reference that two independent skills need is a copy in each, listed in `identicalCopies` in `scripts/validate-skills.mjs`, which fails when they differ.

## Evals

- Every skill has a routing case in the user's own words, and a skill whose output a person reads has a quality case for its one rule: `evals/<skill>-<case>/prompt.md` plus `graders/*.md`, in the format `claude plugin eval init --bare` writes.
- A case puts the whole scenario in its prompt and allows `[Skill, Read, Bash]`, because an eval run has no network, a redirected home, and an empty working directory.
- Routing graders are `tool_used` on `Skill` with `arm: both`; quality graders are `llm` judges with a concrete criterion, or `regex` with the pattern in frontmatter.
- A quality criterion states the outcome the user asked for, so that the skill's own success check cannot satisfy it alone.
- A case passes with the skill and scores lower without it; a case whose delta stays 0 across runs is rewritten so the no-skill arm is not handed the answer, kept with the `guard` tag only when it guards a mistake the skill itself once made, or deleted, because each run of it is paid.

## How a skill improves

Watch it run on a real ask, name what is wrong in one sentence, turn that sentence into the rule with its `(seen: ...)`, add an eval case that fails without the fix, fix it, and look again. The usage records (`distill-session`) say where to look first: rules the agent ignored, verdicts the user overturned, and asks that never routed. Change a skill here and reinstall it (`npx skills update -g -y`), because an installed copy edited in place diverges per machine and the next update overwrites it.

A skill whose goal must hold after it runs (docs that stay rules, a memory store that stays small, a contract the next session keeps) is judged on the tree a week after its first real runs, never on its own checks passing: it names the measurement that shows the property held (`measure.py --since`, `check.py --dir`), and `distill-session` takes it.

A guard that holds such a property runs as a PostToolUse hook in every harness that edits here (Claude Code, Codex, Grok) and parses each one's payload, because a Claude-only hook misses the other harnesses' writes.

## Before you ship

Before shipping, run the checks AGENTS.md lists under Commands.
