# AI Reference

A collection of skills for AI coding assistants. Packaged instructions that extend agent capabilities.

Follows the [Agent Skills](https://skills.sh) format.

## Available

### Skills

#### create-branch

Create a new branch off the default base, not the current HEAD, and move all uncommitted changes onto it; `--base` and `--keep-base` override the base.

**Triggers:** "Move these changes to a new branch", "Start a feat branch for this"

#### commit-changes

Commit only the uncommitted changes as conventional commits, one per purpose: it unstages what was already staged, stages each group by path, confirms the staged list before every commit, and proves each commit is signed when the repository signs. Existing commits stay untouched.

**Triggers:** "Commit my changes", "Split these changes into commits"

#### organize-commits

Regroup uncommitted changes and messy branch commits into clean commits by purpose, rewriting even pushed history after it prints the plan, records a recovery ref, and asks before every reset; the content stays identical.

**Triggers:** "Clean up the commits on this branch", "Reorganize this branch's history"

#### create-pr

Open a GitHub PR from the current branch with a title and body in the repository's conventions and the user's voice: its template, `closes #N` first, a `type(scope):` title from recent merges, a test plan split into verified and to verify, and guards against empty, WIP, behind-base, or merge-commit branches.

**Triggers:** "Open a PR", "Create a pull request for this branch"

#### verify-issue

Verify each claim of a GitHub issue against the codebase with `file:line` evidence, running repros for behavioral claims and reading pinned upstream source for third-party ones; a PR covers the issue only once the issue's repro passes on its head.

**Triggers:** "Verify issue #123", "Is this issue still valid?"

#### verify-pr

Judge a GitHub PR against its stated goal: whether it should exist at all, then correctness, tests, conformance to the repository's own precedents, and side effects. The verdict binds to the head it judged, and `--since <sha>` re-reads only what landed after it.

**Triggers:** "Should we merge PR #456?", "Verify this PR before merge". This is the whole-PR verdict; for per-comment triage of the review threads use `verify-pr-comments`.

#### verify-pr-comments

Fetch every review comment on a PR, from bots and humans, classify each by staleness, and verify the fresh claims against the current code, reporting which to accept, reject, or defer with fix drafts.

**Triggers:** "Check the PR review comments", "Verify the bot comments on #456"

#### summarize-review

Write a maintainer's summary review to a PR's author: the verdict and why it holds, then only what the diff cannot say for itself, with evidence behind each load-bearing claim.

**Triggers:** "Write the approval review for #789", "Summarize what we fixed on this PR"

#### approve-pr

Review a PR as a maintainer and post the GitHub approval when it earns one, otherwise report and decline. It owns the self-approval guard and the review write, and composes `verify-pr`, `verify-pr-comments`, `summarize-review`, and optionally `ship-pr` for the merge.

**Triggers:** "Approve PR #4621", "Review and approve this PR", "Approve and merge #4621"

#### ship-pr

Drive a change to a merged PR: implement if needed, branch, open the PR, then watch CI and review threads, fixing feedback each cycle, and merge once every check and review has settled on the head that merges. It resumes from whatever state exists, bounds every wait with a visible heartbeat, pins the merge to the head `verify-pr` judged, and follows merge queues.

**Triggers:** "Ship this change", "Take this PR to merge", "Open a PR and merge it when CI is green"

#### upgrade-deps

Upgrade every dependency the repository has (npm workspaces through taze, Python through uv, GitHub Actions through ratchet), repin SDK-governed packages, validate with the repository's own checks, and name every dependency left short of its latest release, leaving an uncommitted tree.

**Triggers:** "Upgrade all dependencies", "Bump deps and fix what breaks", "Refresh the lockfile"

#### find-icon

Find a verified icon for a brand, product, AI model, or UI concept down a source ladder (lucide, lobe-icons, svgl, simple-icons, then the vendor), prove it exists before writing code, and deliver it the way the repository already consumes icons.

**Triggers:** "Find an icon for Zed", "Add icons for the remaining providers", "Replace this text with an icon"

#### verify-ui

Render and verify a web UI change in a real browser through whichever browser tool the session exposes, mapped by operation across Chrome DevTools, Claude in Chrome, Gode, and others. It owns the dev server lifecycle, waits for hydration, backs each claim with a DOM query and a screenshot someone looked at, lists every state the change touches, and never kills processes by name.

**Triggers:** "Verify the UI change in the browser", "The spacing still looks wrong, check it", "Render this page and confirm the fix"

#### optimize-repo

Run the standing optimization pass: read the scope's idiom, strip comments and dead surface, replace hand-rolled code with the repository's own primitives, sweep each changed pattern everywhere, sync the docs, verify with the repository's own ladder, and stop at an uncommitted tree.

**Triggers:** "Optimize the codebase", "Clean this up and simplify", "Run an optimization pass, don't commit"

#### read-source

Answer a question about a dependency or an installed CLI from source at the pinned version, choosing the rung by the question: installed code, the published artifact, the upstream repository at the release tag, and docs last, never as proof. Every answer names the rung and version that proved it.

**Triggers:** "Does this API exist in our version?", "Check the source of this package", "When did this behavior change?"

#### inspect-db

Inspect a live database with real SQL before reasoning from ORM schema files: resolve the connection from the project's own configuration, read live DDL and rows, treat drift from the ORM files as the finding, and stay read-only unless `--write` gates a mutation behind a counted `SELECT`.

**Triggers:** "What's actually in the users table?", "Check the live schema against our drizzle schema", "Why does prod data look wrong?"

#### design-dashboard

Design or redesign an admin, ops, or customer dashboard in the repository's own design law: frame each screen's job, diagnose in measurements, take one contribution per reference, publish a blueprint, build the core and then the pages in waves, verify in a browser, and leave the contract in AGENTS.md.

**Triggers:** "Completely redesign the dashboard", "Every element is a big block, we need to show more", "The sidebar is a mess, split internal from customer-facing", "Design the console for this product"

#### plan-charts

Decide what a dashboard shows and in which chart form: inventory the data pages fetch and discard, prove each metric against production, choose the form by the question, place each answer so every mark links onward, and design the capture when no data exists yet.

**Triggers:** "What else could we show on the dashboard?", "We removed too many charts, which ones come back and in what form?", "What could become a monitor or a dataset?", "Which chart for this data, and where?"

#### use-project-memory

Read and write the project memory store that Claude, Codex, and Grok share, admitting only a fact that changes a later decision and that the tree, git, GitHub, or an instruction file cannot give. `scripts/check.py` holds every write to the store's limits, also as a PostToolUse hook in all three harnesses. A run another agent dispatched loads nothing, and Codex lists the skill only for explicit invocation.

**Triggers:** "Remember this about the repo", "What do we already know about this project?", "Write that into project memory"

#### diagnose-root

Diagnose a failure to its origin with a reproduction first: trace the wrong value back to where it starts, name the mechanism in one sentence, and fix at the origin only when a fix was asked, then sweep for the same cause and rerun the reproduction.

**Triggers:** "Why does this keep happening?", "Is this a root fix?", "Fix this properly, not a patch"

#### recap-activity

Recap what a person, team, project, or this computer did, or what failed and why, over any window, from every store that holds records (GitHub, Vercel, the workspace, this machine), read-only, and say so when nothing covers the window.

**Triggers:** "What did I ship in the org this week?", "Which Vercel deployments failed this month?", "Why did the app fail yesterday?", "Summarize how I used this computer last week"

#### mirror-reference

Adapt the load-bearing pattern of a reference URL, repository, or sibling path into this codebase's own idiom and primitives, never copying its classes, tokens, or names, and report where and why the result diverges.

**Triggers:** "Build something like this reference", "Look at kumo-ui and adapt the pattern", "Reference this but don't copy it"

#### distill-session

Review how the skills are being used across every project's sessions and propose skill edits, rules, or memory, each backed by a transcript quote and gated for durability, specificity, decision impact, and a concrete home; nothing applies without approval.

**Triggers:** "How are our skills being used?", "Turn yesterday's debugging into a skill edit", "Distill the last week of sessions"

#### normalize-agents-md

Rewrite instruction files and the docs they point agents at into short normative files within every harness's size caps: keep the rules, route descriptions, incidents, and inventories to their homes, take manuals for people off the agent's path, retire CLAUDE.md, and prove nothing was lost. `scripts/measure.py` measures the tree, judges a pass a week later with `--since`, and runs as a PostToolUse hook.

**Triggers:** "Clean up AGENTS.md", "Our CLAUDE.md has become a changelog", "Our DESIGN.md reads like a running log", "Our markdown files change every day", "Normalize the instruction files across the monorepo"

#### clean-memory

Verify a repository's project memory against the live tree and GitHub, then confirm, correct, compact, promote, archive, or delete each topic, so stale or wrong memories stop steering agents; `scripts/audit.py` checks every anchor a topic carries.

**Triggers:** "Clean up the project memory", "Half of these memories are outdated", "Check what memory still holds after the refactor"

## Installation

### Claude Code

```bash
npx skills add okisdev/ai-reference
```

Update with `npx skills update -g -y`. Change a skill in this repository and reinstall it; an installed copy edited in place is overwritten by the next update.

### OpenAI Codex and Grok

Codex scans `~/.agents/skills` (user) and `.agents/skills` (repo), not `~/.claude`, and it follows symlinks. Clone the repo and link the skills you want into a scanned path:

```bash
git clone https://github.com/okisdev/ai-reference.git
mkdir -p ~/.agents/skills
for d in ai-reference/skills/*/; do ln -s "$(cd "$d" && pwd)" ~/.agents/skills/"$(basename "$d")"; done
```

Grok scans `~/.grok/skills`, which should link to the same `~/.agents/skills` store. Enable or disable individual skills in `~/.codex/config.toml`. `ship-pr` and `use-project-memory` ship `allow_implicit_invocation: false`, so Codex never loads them on its own; invoke them explicitly (`$ship-pr`, `$use-project-memory`), and have AGENTS.md ask for the memory index when interactive Codex work should read it at the start. Claude Code runs each skill's `## Context` probes; in Codex and Grok the agent runs them itself before following the skill.

## Usage

Skills are available once installed, and the agent uses them when a task matches. For example:

```
Optimize the codebase
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
├── .github/workflows/validate-skills.yml
├── AUTHORING.md
├── CHANGELOG.md
├── evals/
│   └── <skill>-<case>/          (prompt.md plus graders/, for claude plugin eval)
├── scripts/
│   ├── check-probes.py
│   ├── test-measure.py
│   ├── test-memory-scripts.py
│   └── validate-skills.mjs
└── skills/
    └── <name>/                  (one directory per skill listed under "Available")
        ├── SKILL.md
        ├── examples/            (outputs that cleared the bar, and a rejected one)
        └── references/
```

CI validates every PR that touches skills: `scripts/validate-skills.mjs` checks that every frontmatter parses, `name:` matches its directory, no Context probe uses a positional parameter, and `plugin.json` and this README agree with the `skills/` tree, and `scripts/check-probes.py` runs every Context probe in an empty directory and in a repository without a remote, under bash and zsh, failing on any probe that exits non-zero. Run them locally with `npm install --no-save js-yaml && node scripts/validate-skills.mjs` and `python3 scripts/check-probes.py`.

The eval suite runs with `claude plugin eval . --trust-plugin --allow-tools Bash --no-publish --judge-model sonnet`: every skill has a routing case in the user's own words, and skills whose output a person reads have quality cases for their one rule, each scored with and without the plugin.

New skills follow [AUTHORING.md](AUTHORING.md).

## License

MIT
