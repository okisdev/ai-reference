# AI Reference

A collection of skills and agents for AI coding assistants. Packaged instructions that extend agent capabilities.

Follows the [Agent Skills](https://skills.sh) format.

## Available

### Agents

#### code-simplifier

Expert code simplification agent. Preserves functionality while improving clarity and maintainability.

**Capabilities:**
- Applies project-specific coding standards from CLAUDE.md/AGENTS.md
- Flattens nested conditionals with early returns
- Improves variable and function naming
- Removes dead/unused code
- Avoids over-simplification that hurts readability
- Knows when NOT to simplify

### Skills

#### create-branch

Create a new branch and move all uncommitted changes to it. Defaults to branching off the default base so unrelated commits don't leak in; supports `--base` and `--keep-base` overrides.

**Triggers:** "Move these changes to a new branch", "Start a feat branch for this"

#### commit-changes

Stage and commit only the current uncommitted changes into clean, conventional-commit groups. Leaves existing commits untouched.

**Triggers:** "Commit my changes", "Split these changes into commits"

#### organize-commits

Reorganize uncommitted changes and/or messy commits on the current branch into clean, categorized commits grouped by purpose.

**Triggers:** "Clean up the commits on this branch", "Reorganize this branch's history"

#### create-pr

Create a GitHub PR from the current branch with a title and body that follow the repo's conventions and the user's writing style. Auto-detects the repo's PR template, places `closes #N` at the top of the body, derives a `type(scope):` title from recent merged PRs, splits the test plan into "already verified" vs "reviewer should verify", and runs pre-flight guards for empty PR / WIP commits / behind-base / merge commits.

**Triggers:** "Open a PR", "Create a pull request for this branch"

#### verify-issue

Fetch a GitHub issue and verify each of its claims against the current codebase with concrete `file:line` evidence. Escalates past surface code reading when the conclusion depends on it: running repros for behavioral claims, checking canonical upstream source for third-party and runtime claims, and adversarially testing the load-bearing claim and the issue's own reasoning.

**Triggers:** "Verify issue #123", "Is this issue still valid?"

#### verify-pr

Verify a GitHub PR against its stated goal and the surrounding codebase. Judges first whether the PR should exist at all (necessity, redundancy, honest scope), then correctness, tests, paradigm and convention conformance, and side effects. Conformance is judged against the repo's own precedents (the nearest sibling hook, test, doc example, or type), not against generic best practice, and each deviation cites the in-repo pattern it breaks. Produces a maintainer-ready verdict that can recommend closing a redundant PR even when it is technically clean, and separates blocking issues from optional polish.

**Triggers:** "Should we merge PR #456?", "Verify this PR before merge". This is the whole-PR verdict; for per-comment triage of the review threads use `verify-pr-comments`.

#### verify-pr-comments

Fetch review comments on a GitHub PR (bots + humans), classify by staleness, and verify each fresh claim against the current code, reporting which to accept, reject, or defer with fix drafts.

**Triggers:** "Check the PR review comments", "Verify the bot comments on #456"

#### summarize-review

Write a maintainer-style summary review of a GitHub PR with three sections: shortcomings in the original implementation, what was modified during review, and potential further fixes. Frames feedback for the original author rather than recapping bot output.

**Triggers:** "Write the approval review for #789", "Summarize what we fixed on this PR"

#### ship-pr

Drive a change all the way to a merged PR: implement if needed, branch, open the PR, then monitor CI and review threads on a recurring loop, addressing feedback each cycle and merging once the gate passes. Auto-detects the entry point (uncommitted changes, an existing branch, or an already open PR) and resumes at the right step rather than forcing the full flow, auto-detects GitButler versus plain git, and treats only the repo's required checks as gating while advisory checks and review bots never block. Composes `create-branch`, `commit-changes`, and `create-pr` to create, `verify-pr` to judge the PR, and `verify-pr-comments` to triage the threads; it owns the loop, the merge gate, and the merge itself.

**Triggers:** "Ship this change", "Take this PR to merge", "Open a PR and merge it when CI is green"

## Installation

### Claude Code

```bash
npx skills add okisdev/ai-reference
```

### OpenAI Codex

Codex scans `~/.agents/skills` (user) and `.agents/skills` (repo), not `~/.claude`, and it follows symlinks. Clone the repo and link the skills you want into a scanned path:

```bash
git clone https://github.com/okisdev/ai-reference.git
mkdir -p ~/.agents/skills
for d in ai-reference/skills/*/; do ln -s "$(cd "$d" && pwd)" ~/.agents/skills/"$(basename "$d")"; done
```

Enable or disable individual skills in `~/.codex/config.toml`. `ship-pr` ships `allow_implicit_invocation: false`, so Codex will not auto-trigger it; invoke it explicitly. Each skill's `## Context` probes are auto-run by Claude Code; in Codex the agent must run them itself before following the skill.

## Usage

Skills and agents are automatically available once installed. The agent will use them when relevant tasks are detected.

**Examples:**
```
Simplify my recent changes
```
```
Move these uncommitted changes to a new feat branch
```
```
Verify the review comments on PR #123
```

## Structure

```
.
├── .claude-plugin/plugin.json
├── AUTHORING.md
├── agents/
│   └── code-simplifier.md
└── skills/
    └── (one directory per skill listed under "Available")
```

New skills follow [AUTHORING.md](AUTHORING.md): a lean, imperative register with detail pushed into `references/`.

## License

MIT
