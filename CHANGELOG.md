# Changelog

All notable changes to this collection. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and versions match `.claude-plugin/plugin.json`. Changes before 0.0.41 live in the merged pull requests.

## [0.0.43] (2026-10-12)

### Added

- Quality bars: every skill whose output a person reads opens its Instructions with its one rule and points at `examples/`, holding outputs that cleared the bar and a rejected one with each fault named against the rule it breaks.
- Rules carry the fault that taught them as `(seen: ...)`, drawn from four months of usage records and the incidents behind earlier fixes.
- An eval suite under `evals/` for `claude plugin eval`: a routing case per skill in the user's own words, all 25 routing correctly, and ten quality cases for the one rules, each scoring 1.0 with the skills against 0 to 0.8 without them.
- `scripts/check-probes.py`, run in CI: every Context probe must exit 0 in an empty directory and in a repository without a remote, under bash and zsh.
- A sizing step for long runs in clean-memory, distill-session, recap-activity, and design-dashboard.
- commit-changes, organize-commits, create-pr, approve-pr, summarize-review, and ship-pr keep tool trailers, generated-by lines, and session links out of everything posted under the user's name; the commit eval caught the default flow adding a coding tool's co-author trailer.

### Fixed

- 22 Context probes exited non-zero without gh authentication or a GitHub remote, which stopped Claude Code from loading the skill at all.
- ship-pr's description names the user's shorthand (ship it, 走流程, merge it), so it routes without a global rule.

## [0.0.42] (2026-10-12)

Merged as #34.

### Changed

- Context probes no longer use positional parameters and print their fallback when the command fails; the validator rejects positional parameters in probes.
- commit-changes owns the index, create-pr takes `--base` and always passes `--head` and `--repo`, and ship-pr drops its contradiction about quiet pending items and defines a bounded poll.
- verify-pr judges cause versus symptom, reads AGENTS.md and CLAUDE.md first, fetches only the delta on `--since`, and never waits on CI; approve-pr reuses a same-head verify-pr report.
- use-project-memory narrows its trigger and its hook judges only what a write introduced; nine descriptions lead with the user's own words.

### Removed

- audit-repo, onboard-repo, verify-cli, and create-verify-skill, after no demand since June.

## [0.0.41] (2026-10-12)

Merged as #33.

### Added

- recap-activity, which recaps what a person, team, project, or this computer did, or what failed, over a time window from whatever records exist.

### Changed

- diagnose-root counts a remote failure's recorded log as its observation; distill-session includes transcripts of sessions started in task worktrees.
