# ai-reference

Agent skills published through `npx skills` and as a Claude Code plugin; README.md is the catalog for people.

## Commands

- `npm install --no-save js-yaml && node scripts/validate-skills.mjs`: asserts frontmatter, the 20 KiB `SKILL.md` cap, probe parameters, the `plugin.json` and README listings, and standing alone; run it before shipping any change, and CI runs it on every PR touching skills.
- `python3 scripts/check-probes.py`: runs every Context probe in an empty directory and a repository without a remote, under bash and zsh (zsh must be installed); it passes before shipping.
- `claude plugin eval . --trust-plugin --allow-tools Bash --no-publish --judge-model sonnet --case '<skill>-*'`: passes the cases a change can affect (the skill's routing case when its description changes, the quality case of each rule it touches, and the routing cases of neighbors a description change could steal from) before shipping, and the full suite once per version bump, judged by sonnet because the default haiku judge fails answers that meet a criterion; a case with an open flaky issue is reported, not blocking.
- `npx skills add <repo> -l`: lists the skill before shipping, which proves the consumer-side CLI parses its frontmatter.
- `python3 scripts/test-memory-scripts.py`: passes when a change touches the `check.py`, `resolve.py`, or `audit.py` of `clean-memory`.
- `python3 scripts/test-measure.py`: passes when a change touches `skills/normalize-md/scripts/measure.py`.
- `python3 scripts/test-episodes.py`: passes when a change touches `skills/distill-session/scripts/episodes.py`.

## Rules

- Bump the `.claude-plugin/plugin.json` version in every PR that ships a skill change, because CHANGELOG.md entries are keyed to it.
- `scripts/validate-skills.mjs` and `scripts/check-probes.py` assert the mechanical rules of AUTHORING.md; when AUTHORING.md and a script disagree, the script wins.

## Where things live

- Read AUTHORING.md's Anatomy and Conventions before writing or editing a `SKILL.md`.
- Read AUTHORING.md's Standing alone before a skill names another skill or reads a file outside its folder.
- Read AUTHORING.md's Evals before adding or changing a case under `evals/`.
- Read AUTHORING.md's Rigor over line count before cutting a skill's text.

## Editing docs

- One rule per bullet, imperative, with at most one because-clause naming the failure it prevents in general terms, never the pages, labels, or dates of the incident that taught it.
- This file and every doc it points agents at state what must stay true, never what currently is: what a change did goes in its commit and PR, what the code does stays in the code, and status goes to the tracker.
- A change that makes a sentence here false replaces that sentence in the same change, and never appends an account of the change.
- A doc written for people (a README manual, a guide) changes when the owner asks or at a release, never as a side effect of a code change; a change that makes one of its sentences false replaces that sentence.
- A lesson from one session goes to commit messages, issues, or the maintainer's memory store; a rule enters only when the owner decides it, the same mistake repeats, or a review catches it.
- A rule an existing check asserts is a one-line pointer to that check, not a restatement.
- A rule that sets what to run, when, or how often is added with the failure it prevents and its measured cost in the commit or PR that adds it, so the next reader can weigh it instead of only obeying it.
- Keep this file under 8 KB, any nested AGENTS.md under 5 KB, and each doc it points agents at under 16 KB, with no inventories, dates, issue numbers, or module internals; an amendment that would pass a target settles the file first.
- Edit these files with the editing tool, never through a shell script or heredoc, so every amendment stays reviewable and the doc hook sees it.
