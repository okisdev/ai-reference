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

#### branch

Create a new branch and move all uncommitted changes to it. Defaults to branching off the default base so unrelated commits don't leak in; supports `--base` and `--keep-base` overrides.

**Triggers:** "Move these changes to a new branch", "Start a feat branch for this"

#### commit-changes

Stage and commit only the current uncommitted changes into clean, conventional-commit groups. Leaves existing commits untouched.

**Triggers:** "Commit my changes", "Split these changes into commits"

#### organize-commits

Reorganize uncommitted changes and/or messy commits on the current branch into clean, categorized commits grouped by purpose.

**Triggers:** "Clean up the commits on this branch", "Reorganize this branch's history"

#### pr

Create a GitHub PR from the current branch with auto-generated title and summary derived from actual commits and diff.

**Triggers:** "Open a PR", "Create a pull request for this branch"

#### verify-issue

Fetch a GitHub issue and verify each of its claims against the current codebase with concrete `file:line` evidence.

**Triggers:** "Verify issue #123", "Is this issue still valid?"

#### verify-pr-comments

Fetch review comments on a GitHub PR (bots + humans), classify by staleness, and verify each fresh claim against the current code — reporting which to accept, reject, or defer with fix drafts.

**Triggers:** "Check the PR review comments", "Verify the bot comments on #456"

#### surge

Operate and troubleshoot [Surge](https://nssurge.com) via `surge-cli`: command discovery, runtime diagnostics, state inspection (dump/watch/test), and environment mutation via key-paths.

**Triggers:** "Inspect Surge state", "Switch Surge proxy mode", "Dump Surge policy"

## Installation

```bash
npx skills add okisdev/ai-reference
```

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
├── agents/
│   └── code-simplifier.md
└── skills/
    ├── branch/
    ├── commit-changes/
    ├── organize-commits/
    ├── pr/
    ├── surge/
    ├── verify-issue/
    └── verify-pr-comments/
```

## License

MIT
