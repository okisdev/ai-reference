# AI Reference

A collection of skills for AI coding assistants. Packaged instructions that extend agent capabilities.

Follows the [Agent Skills](https://skills.sh) format.

## Available

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

Verify a GitHub PR against its stated goal and the surrounding codebase. Judges first whether the PR should exist at all (necessity, redundancy, honest scope), then correctness, tests, paradigm and convention conformance, and side effects. Conformance is judged against the repo's own precedents (the nearest sibling hook, test, doc example, or type), not against generic best practice, and each deviation cites the in-repo pattern it breaks. Produces a maintainer-ready verdict that can recommend closing a redundant PR even when it is technically clean, and separates blocking issues from optional polish. The verdict binds to the head SHA it was computed on, and `--since <sha>` re-reads only what landed after a previous pass so re-verifying a PR that keeps moving costs the delta rather than the whole patch.

**Triggers:** "Should we merge PR #456?", "Verify this PR before merge". This is the whole-PR verdict; for per-comment triage of the review threads use `verify-pr-comments`.

#### verify-pr-comments

Fetch review comments on a GitHub PR (bots + humans), classify by staleness, and verify each fresh claim against the current code, reporting which to accept, reject, or defer with fix drafts.

**Triggers:** "Check the PR review comments", "Verify the bot comments on #456"

#### summarize-review

Write a maintainer-style summary review of a GitHub PR as a message to the original author: the verdict and the reason it holds, then only what the diff cannot say for itself, with the evidence behind each load-bearing claim. Prose rather than sections, and no recapping of bot output.

**Triggers:** "Write the approval review for #789", "Summarize what we fixed on this PR"

#### approve-pr

Review a GitHub PR as a maintainer and, when it earns it, post the GitHub APPROVED review; otherwise report and decline. The maintainer-side counterpart to `ship-pr`: it owns the self-approval guard, the verify-pr-verdict to review-action mapping, and the `gh pr review` write (including the anti-stacking PUT-replace of a prior review), and it delegates the approve-or-decline verdict to `verify-pr`, thread triage to `verify-pr-comments`, the review body to `summarize-review`, and the optional post-approval merge to `ship-pr`. Auto-posts only an approval; `--request-changes`, `--comment`, and a close recommendation never write without an explicit opt-in.

**Triggers:** "Approve PR #4621", "Review and approve this PR", "Approve and merge #4621"

#### ship-pr

Drive a change all the way to a merged PR: implement if needed, branch, open the PR, then monitor CI and review threads on a recurring loop, addressing feedback each cycle and merging once the gate passes. Auto-detects the entry point (uncommitted changes, an existing branch, or an already open PR) and resumes at the right step rather than forcing the full flow, auto-detects GitButler versus plain git, and treats only the repo's required checks as gating while advisory checks and review bots never block. Composes `create-branch`, `commit-changes`, and `create-pr` to create, `verify-pr` to judge the PR, and `verify-pr-comments` to triage the threads; it owns the loop, the merge gate, and the merge itself. When shepherding another author's PR it delegates to `approve-pr` by default to post the maintainer approval the merge gate needs, rather than forcing the merge; `--admin` is reserved for your own PRs, where GitHub blocks self-approval. Every wait in the loop is heartbeat-bounded: a wall-clock budget picked up front, a visible per-tick status line, and stalled items sidestepped instead of polled forever.

**Triggers:** "Ship this change", "Take this PR to merge", "Open a PR and merge it when CI is green"

#### upgrade-deps

Upgrade every dependency the repository actually has: npm workspaces via taze, Python projects via uv, and GitHub Actions via ratchet. Prefers root `package.json` dependency scripts over the generic recipe; repins SDK-matrix-governed packages after blanket bumps (Expo via `expo install --fix`); leaves Actions alone when Dependabot or Renovate owns them; validates with the repository's build, lint, and test scripts, pins back an individual major that breaks, writes a patch changeset only when `.changeset/` exists, and ends with a validated uncommitted tree, where committing composes `commit-changes` and shipping composes `ship-pr`.

**Triggers:** "Upgrade all dependencies", "Bump deps and fix what breaks", "Refresh the lockfile"

#### find-icon

Locate a verified icon for a brand, product, AI model, or UI concept and deliver it the way the repository already consumes icons: routes each target down a source ladder (lucide for UI concepts, lobe-icons for AI model, provider, and agent brands, svgl then simple-icons for other brands, the vendor's own repository or official site as the last resort); proves every pick exists at its source before writing any code, extracting SVG path data by script rather than retyping it; delivers a UI glyph as a lucide-react import and a brand mark as a vendored SVG component, preserving official brand colors while UI glyphs stay on `currentColor`.

**Triggers:** "Find an icon for Zed", "Add icons for the remaining providers", "Replace this text with an icon"

#### verify-ui

Render and verify a web UI change in a real browser: manages the dev server lifecycle (stale lock cleanup, nohup start with a recorded PID, readiness polling, port drift detection), waits for hydration, asserts the specific claim with a DOM query, and backs every visual claim with a screenshot that is actually read. Parses pasted DOM fragments to their source file and line, respects per-repo visual QA ownership, and never kills processes by name. Waits are budgeted: the readiness poll is bounded, and expiry kills the recorded PID and reports the failure with log evidence.

**Triggers:** "Verify the UI change in the browser", "The spacing still looks wrong, check it", "Render this page and confirm the fix"

#### audit-repo

Run a multi-round parallel verification sweep over recent work or a whole repository: each round dispatches verification agents across distinct angles (correctness, conformance, rendered UI, tests and types, docs and dead surface), findings land in a fix.md ledger with evidence, fixes are re-verified before they count, and rounds loop until one comes back clean. Non-trivial findings need two independent verifiers, and the ledger never ships.

**Triggers:** "Audit everything we did today", "Run verification rounds until clean", "Sweep the repo for problems"

#### optimize-repo

Run the standing optimization pass: read the scope's idiom first, decide the release posture from evidence (an unpublished package gets deletions instead of backward compatibility), strip comments and dead surface, replace hand-rolled fragments with the repo's own primitives, audit conformance against the nearest precedent, sweep changed patterns for completeness, sync docs, verify with the repo's own ladder, and stop at an uncommitted validated tree.

**Triggers:** "Optimize the codebase", "Clean this up and simplify", "Run an optimization pass, don't commit"

#### read-source

Answer an API or behavior question about a dependency from authoritative source, choosing the ladder rung by question type: installed code for import and typecheck questions, the published npm artifact for what actually shipped (npm pack at the exact version, outside the repo, scripts ignored), the upstream repository pinned to the release tag for behavior and history, and docs last, never as proof. Every answer names the rung and version that proved it.

**Triggers:** "Does this API exist in our version?", "Check the source of this package", "When did this behavior change?"

#### inspect-db

Inspect a live database with real SQL before reasoning from ORM schema files: resolves the connection from the project's own configuration (Neon MCP, `DATABASE_URL`, or wrangler d1), reads live DDL and targeted rows first, treats schema drift against the ORM files as the finding, and never conflates D1 `--local` with `--remote`. Read-only by default; `--write` gates every mutation behind a counted `SELECT` of the same rows, and credentials never appear in output.

**Triggers:** "What's actually in the users table?", "Check the live schema against our drizzle schema", "Why does prod data look wrong?"

#### onboard-repo

Build a structured understanding of a repository before any edit: reads the repo's own orientation docs first, maps workspaces and entry points, extracts the idiom from 2 to 3 nearest siblings of whatever the task will touch, collects reusable prior art, reconciles with project memory, and delivers a compact map where every claim cites a file. Research and comparison asks end at the map with zero edits.

**Triggers:** "Read and understand the whole codebase", "Get familiar with this repo before we start", "Map this project"

#### diagnose-root

Diagnose a failure to its origin with a reproduction first: runs the failing thing before explaining it, traces the wrong value back to the first place it is wrong, names the mechanism in one sentence, and fixes at the origin after explicitly rejecting the symptom-site patch, then sweeps for the same root cause elsewhere and proves the fix by rerunning the reproduction. A why question stops at the diagnosis and never turns into an edit.

**Triggers:** "Why does this keep happening?", "Is this a root fix?", "Fix this properly, not a patch"

#### mirror-reference

Extract the load-bearing pattern from a reference URL, repository, or sibling path and re-express it in this codebase's own idiom: studies references through `gh` rather than scraping, separates the pattern from its styling and tokens, implements with the repo's own primitives, and ships a deviation report stating where and why the result diverges from the reference. Never clones class strings, tokens, or naming verbatim.

**Triggers:** "Build something like this reference", "Look at kumo-ui and adapt the pattern", "Reference this but don't copy it"

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

Skills are automatically available once installed. The agent will use them when relevant tasks are detected.

**Examples:**
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
├── AUTHORING.md
└── skills/
    └── (one directory per skill listed under "Available")
```

New skills follow [AUTHORING.md](AUTHORING.md): a lean, imperative register with detail pushed into `references/`.

## License

MIT
