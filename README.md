# AI Reference

A collection of skills for AI coding assistants. Packaged instructions that extend agent capabilities.

Follows the [Agent Skills](https://skills.sh) format.

## Available

### Flows

Most work follows one of these paths.

- **Change to merge:** `verify-issue` or `diagnose-root`, the change, then `ship-pr` (which composes `create-branch`, `commit-changes`, `create-pr`, `verify-pr`, `verify-pr-comments`, `approve-pr`).
- **Backlog:** `triage-backlog`, then per item `adopt-pr`, `approve-pr`, and `ship-pr`; `draft-reply` writes what gets posted.
- **Shipping:** `release-changes`, with `upload-testflight` for Apple builds.
- **UI:** `design-system` once, then `build-ui` (or `design-dashboard`), `plan-charts`, `find-icon`, `verify-ui`, and `review-ui`; `mirror-reference` for an outside reference.
- **Evidence:** `read-source`, `inspect-db`, `recap-activity`.
- **Upkeep:** `optimize-repo`, `upgrade-deps`, `normalize-md`, `clean-memory`, `organize-commits`, and `distill-session` to tune the skills from their use.

### Skills

#### create-branch

Create a new branch off the default base, not the current HEAD, and move all uncommitted changes onto it; `--base` and `--keep-base` override the base.

**Triggers:** "Move these changes to a new branch", "Start a feat branch for this"

#### commit-changes

Commit only the uncommitted changes as conventional commits, one per purpose: it unstages what was already staged, stages each group by path, confirms the staged list before every commit, and proves each commit is signed when the repository signs. Existing commits stay untouched.

**Triggers:** "Commit my changes", "Split these changes into commits" ([example](skills/commit-changes/examples/grouped.md))

#### organize-commits

Regroup uncommitted changes and messy branch commits into clean commits by purpose, rewriting even pushed history after it prints the plan, records a recovery ref, and asks before every reset; the content stays identical.

**Requires:** `commit-changes`

**Triggers:** "Clean up the commits on this branch", "Reorganize this branch's history" ([example](skills/organize-commits/examples/regroup.md))

#### create-pr

Open a GitHub PR from the current branch with a title and body in the repository's conventions and the user's voice: its template, `closes #N` first, a `type(scope):` title from recent merges, a test plan split into verified and to verify.

**Triggers:** "Open a PR", "Create a pull request for this branch" ([example](skills/create-pr/examples/fix.md))

#### verify-issue

Verify each claim of a GitHub issue against the codebase with `file:line` evidence, running repros for behavioral claims and reading pinned upstream source for third-party ones; a PR covers the issue only once the issue's repro passes on its head.

**Triggers:** "Verify issue #123", "Is this issue still valid?" ([example](skills/verify-issue/examples/already-fixed.md))

#### verify-pr

Judge a GitHub PR against its stated goal: whether it should exist at all, then correctness, tests, conformance to the repository's own precedents, and side effects. The verdict binds to the head it judged, and `--since <sha>` re-reads only what landed after it.

**Triggers:** "Should we merge PR #456?", "Verify this PR before merge" ([example](skills/verify-pr/examples/merge.md))

#### verify-pr-comments

Fetch every review comment on a PR, from bots and humans, classify each by staleness, and verify the fresh claims against the current code, reporting which to accept, reject, or defer with fix drafts.

**Triggers:** "Check the PR review comments", "Verify the bot comments on #456" ([example](skills/verify-pr-comments/examples/triage.md))

#### approve-pr

Review a PR as a maintainer and post the GitHub approval when it earns one, otherwise report and decline. It owns the self-approval guard and the review write, hands a PR that needs fixes to `adopt-pr`, and optionally the merge to `ship-pr`.

**Requires:** `verify-pr`, `verify-pr-comments`, `draft-reply`

**Triggers:** "Approve PR #4621", "Review and approve this PR" ([example](skills/approve-pr/examples/approval.md))

#### ship-pr

Drive a change to a merged PR: implement if needed, branch, open the PR, then watch CI and review threads, fixing feedback each cycle, and merge once every check and review has settled on the head that merges.

**Requires:** `create-branch`, `commit-changes`, `create-pr`, `verify-pr`, `verify-pr-comments`, `approve-pr`, `draft-reply`

**Triggers:** "Ship this change", "Take this PR to merge" ([example](skills/ship-pr/examples/run.md))

#### adopt-pr

Take over another author's PR as a maintainer: judge it, decide whether to amend it on its own branch or supersede it, fix and trim it in a task worktree, stop for review or push when told to ship, and hand it to approval and merge. The contributor's commits and credit stay.

**Triggers:** "Take over this contributor's PR and fix it", "Optimize this PR but don't commit yet" ([example](skills/adopt-pr/examples/adopt.md))

#### triage-backlog

Sort every open issue and PR into one batch each (close now, fix now, needs a decision, follow-up) with the evidence behind it, then run each approved batch to its end without asking again. The plan lives in a file, so "next batch" resumes it and the flags given once carry to every item.

**Triggers:** "Go through all open issues and PRs and batch them", "What's the next batch?" ([example](skills/triage-backlog/examples/plan.md))

#### draft-reply

Read an issue, PR, or chat thread, check what the other side asks against the code, and draft a reply in the user's voice and the channel's format; nothing is sent until the user approves that draft, after which it posts and closes, requests changes, or files the follow-up.

It also writes the maintainer's review summary to a PR's author after a takeover, saying only what the diff cannot, and returns it to `approve-pr` or `ship-pr` to post with the review.

**Triggers:** "Draft a closing reply, don't send it yet", "Send and close" ([example](skills/draft-reply/examples/github.md))

#### release-changes

Deploy what changed, or cut a release, in a safe order, with every named change confirmed in what ships and each target proven live with a rollback point. Release mode also bumps versions, writes the changelog, and merges the PR.

**Triggers:** "Push the schema and deploy the API", "Deploy the platforms that changed" ([example](skills/release-changes/examples/release.md))

#### upload-testflight

Archive an Xcode app through the repository's own path, bump only the build number unless told otherwise, upload, confirm App Store Connect has the build and finished processing, and add it to a testing group with notes from the commits.

**Triggers:** "Send a TestFlight build, bump only the build", "Upload the next build and submit it for testing" ([example](skills/upload-testflight/examples/upload.md))

#### upgrade-deps

Upgrade every dependency the repository has (npm workspaces through taze, Python through uv, GitHub Actions through ratchet), repin SDK-governed packages, validate with the repository's own checks, and name every dependency left short of its latest release, leaving an uncommitted tree.

**Triggers:** "Upgrade all dependencies", "Bump deps and fix what breaks" ([example](skills/upgrade-deps/examples/run.md))

#### find-icon

Find a verified icon for a brand, product, AI model, or UI concept down a source ladder (lucide, lobe-icons, svgl, simple-icons, then the vendor), prove it exists before writing code, and deliver it the way the repository already consumes icons.

**Triggers:** "Find an icon for Zed", "Add icons for the remaining providers" ([example](skills/find-icon/examples/delivery.md))

#### verify-ui

Render and verify a web UI change in a real browser through whichever browser tool the session exposes. It owns the dev server lifecycle, waits for hydration, backs each claim with a DOM query and a screenshot someone looked at, and lists every state the change touches.

**Triggers:** "Verify the UI change in the browser", "The spacing still looks wrong, check it" ([example](skills/verify-ui/examples/render-check.md))

#### optimize-repo

Run the standing optimization pass: read the scope's idiom, strip comments and dead surface, replace hand-rolled code with the repository's own primitives, sweep each changed pattern everywhere, sync the docs, verify with the repository's own ladder, and stop at an uncommitted tree.

**Triggers:** "Optimize the codebase", "Clean this up and simplify" ([example](skills/optimize-repo/examples/pass.md))

#### read-source

Answer a question about a dependency or an installed CLI from source at the pinned version (installed code, the published artifact, the upstream tag, docs last), naming the rung and version that proved it.

**Triggers:** "Does this API exist in our version?", "Check the source of this package" ([example](skills/read-source/examples/answer.md))

#### inspect-db

Inspect a live database with real SQL before reasoning from ORM schema files: resolve the connection from the project's own configuration, read live DDL and rows, treat drift from the ORM files as the finding, and stay read-only unless `--write` gates a mutation behind a counted `SELECT`.

**Triggers:** "What's actually in the users table?", "Check the live schema against our drizzle schema" ([example](skills/inspect-db/examples/inspection.md))

#### design-system

Create, extract, merge, or update a design system agents read before UI work: principles, tokens, exact register values, reject rules, and an exemplar per component across the user's projects; products that share a taste extend one system.

**Triggers:** "Turn our projects' design rules into one shared design system", "Write down how we design so you stop drifting" ([example](skills/design-system/examples/system.md))

#### build-ui

Build or redesign a surface from the governing design system, reading its exemplars instead of asking for references, comparing variants when the direction is open, and covering every state.

**Triggers:** "Redo the settings page in our design", "Build a filter dropdown like our others" ([example](skills/build-ui/examples/build.md))

#### review-ui

Review UI against its design system and the craft of layout, color, type, motion, copy, accessibility, and states, with severity, the rule broken, and the exact fix for each finding.

**Triggers:** "What's wrong with this page's design?", "Review the UI in this diff" ([example](skills/review-ui/examples/review.md))

#### personal-web-design

The maintainer's personal web design system: taste, exact values, components, and reject rules a web product's `DESIGN.md` extends.

**Requires:** `design-system`

**Triggers:** "Build this page in my style" ([example](skills/personal-web-design/examples/applied.md))

#### personal-macos-design

The same taste for Mac apps in SwiftUI or a desktop web stack.

**Requires:** `design-system`

**Triggers:** "Add a menu bar item in my style" ([example](skills/personal-macos-design/examples/applied.md))

#### personal-ios-design

The same taste for iPhone and iPad, where native bars, Dynamic Type, and 44 point targets win.

**Requires:** `design-system`

**Triggers:** "Design this iPhone screen my way" ([example](skills/personal-ios-design/examples/applied.md))

#### design-dashboard

Design or redesign an admin, ops, or customer dashboard in the repository's own design law: frame each screen's job, diagnose in measurements, publish a blueprint, build the core and then the pages in waves, verify in a browser, and write its decisions into the governing design system.

**Requires:** `plan-charts`, `mirror-reference`, `verify-ui`, `design-system`

**Triggers:** "Completely redesign the dashboard", "Every element is a big block, we need to show more" ([example](skills/design-dashboard/examples/blueprint-excerpt.md))

#### plan-charts

Decide what a dashboard shows and in which chart form: inventory the data pages fetch and discard, prove each metric against production, choose the form by the question, place each answer so every mark links onward, and design the capture when no data exists yet.

**Triggers:** "What else could we show on the dashboard?", "We removed too many charts, which ones come back and in what form?" ([example](skills/plan-charts/examples/catalog-excerpt.md))

#### diagnose-root

Diagnose a failure to its origin with a reproduction first: trace the wrong value back to where it starts, name the mechanism in one sentence, and fix at the origin only when a fix was asked, then sweep for the same cause and rerun the reproduction.

**Triggers:** "Why does this keep happening?", "Is this a root fix?" ([example](skills/diagnose-root/examples/diagnosis.md))

#### recap-activity

Recap what a person, team, project, or this computer did, or what failed and why, over any window, from every store that holds records (GitHub, Vercel, the workspace, this machine), read-only, and say so when nothing covers the window.

**Triggers:** "What did I ship in the org this week?", "Which Vercel deployments failed this month?" ([example](skills/recap-activity/examples/digest.md))

#### mirror-reference

Adapt the load-bearing pattern of a reference outside this repository (a URL, another repository, or a sibling checkout) into this codebase's own idiom and primitives, never copying its classes, tokens, or names, and report where and why the result diverges.

**Triggers:** "Build something like this reference", "Look at kumo-ui and adapt the pattern" ([example](skills/mirror-reference/examples/deviation.md))

#### distill-session

Review how the skills are being used across every project's sessions and propose skill edits, rules, or memory, each backed by a transcript quote and gated for durability, specificity, decision impact, and a concrete home; nothing applies without approval.

**Triggers:** "How are our skills being used?", "Turn yesterday's debugging into a skill edit" ([example](skills/distill-session/examples/proposal.md))

#### normalize-md

Challenge every markdown file in a repository on whether it should exist and whether each line is true and worth its cost, then rewrite what stays into short rules within every harness's caps. `scripts/measure.py` inventories every markdown file and runs as a PostToolUse hook.

**Triggers:** "Clean up AGENTS.md", "Go through every md in the repo and question it" ([example](skills/normalize-md/examples/challenge.md))

#### clean-memory

Keep the project memory store that Claude, Codex, and Grok share small and true, verifying every topic against the live tree and GitHub. `scripts/check.py` holds each write to the store's limits, also as a PostToolUse hook.

**Triggers:** "Remember this about the repo", "Clean up the project memory" ([example](skills/clean-memory/examples/pass.md))

## Installation

### Claude Code

```bash
npx skills add okisdev/ai-reference
```

Each skill also installs on its own, and one marked **Requires** installs with what it needs:

```bash
npx skills add okisdev/ai-reference --skill clean-memory
npx skills add okisdev/ai-reference --skill organize-commits commit-changes
```

Update with `npx skills update -g -y`. Change a skill in this repository and reinstall it; an installed copy edited in place is overwritten by the next update.

### OpenAI Codex and Grok

Codex scans `~/.agents/skills` (user) and `.agents/skills` (repo), not `~/.claude`, and it follows symlinks. Clone the repo and link the skills you want into a scanned path:

```bash
git clone https://github.com/okisdev/ai-reference.git
mkdir -p ~/.agents/skills
for d in ai-reference/skills/*/; do ln -s "$(cd "$d" && pwd)" ~/.agents/skills/"$(basename "$d")"; done
```

Grok scans `~/.grok/skills`, which should link to the same `~/.agents/skills` store. Codex loads `ship-pr` only when invoked (`$ship-pr`). Codex and Grok agents run each skill's `## Context` probes themselves.

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

## Contributing

Changes to a skill follow [AUTHORING.md](AUTHORING.md); the checks a change runs are in [AGENTS.md](AGENTS.md).

## License

MIT
