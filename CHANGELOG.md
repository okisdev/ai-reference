# Changelog

All notable changes to this collection. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and versions match `.claude-plugin/plugin.json`. Changes before 0.0.41 live in the merged pull requests.

## [0.0.51] (2026-11-18)

### Added

- triage-backlog sorts every open issue and PR into one batch each (close now, fix now, needs a decision, follow-up), keeps the plan in a file so the next batch resumes it, carries the flags given once to every item, and runs an approved batch to its end.
- release-changes deploys what changed or cuts a release: it confirms every named change is in what ships, maps the diff to targets, orders schema and data steps so running code never meets storage it cannot handle, proves each target live with a rollback point, and in release mode bumps versions, writes the changelog, and merges the PR.
- upload-testflight archives through the repository's own path, bumps only the build number unless told otherwise, and counts a build as sent only once App Store Connect shows it processed.
- draft-reply reads an issue, PR, or chat thread, checks each ask against the code, and drafts a reply in the user's voice and the channel's format that is sent only after approval, then closes, requests changes, or files the follow-up.
- adopt-pr takes over another author's PR on its own branch, or supersedes it when it cannot be saved, and stops for review or ships when told to, keeping the contributor's commits and credit.

### Changed

- read-source answers what changed upstream between our pin and the latest release and which changes touch our integration.
- mirror-reference starts an open "what can we learn from this" ask with a survey of what to adopt, what to skip, and what the reference lacks.
- ship-pr treats a check the repository's `AGENTS.md` declares advisory like `--advisory`, and counts a deployment status that never updated after its deployment finished as passed.
- normalize-md's doc hook leaves changelogs alone, because they are history by design.
- approve-pr hands a PR that needs fixes to adopt-pr instead of pushing them itself.
- normalize-md's markdown inventory reads the history in one log pass and each code file once, so a repository of a few hundred markdown files measures in under a second instead of two minutes.
- An eval case whose delta stays 0 is rewritten, kept with the `guard` tag when it guards a mistake the skill once made, or deleted; a change runs the cases it can affect, and the full suite runs once per version bump.
- Skills, references, examples, and evals name only invented accounts, repositories, and tools: a private product's browser tools become a generic site-tools server, a private review bot leaves the bot table, and real logins and repositories give way to neutral ones.

### Removed

- use-project-memory is merged into clean-memory, which now writes a fact the user asks to remember only when it passes the admission test, and keeps the write check and its hook; the harness loads the memory index on its own.
- summarize-review is merged into draft-reply as its takeover review, which approve-pr and ship-pr now require.

## [0.0.50] (2026-11-18)

### Added

- normalize-md replaces normalize-agents-md and covers every markdown file in a repository: each file is challenged on its readers and what breaks without it (deleted when nobody reads it, proposed for deletion when a person may), each line on whether the code still bears it out, and each rule on the failure it prevents against its measured cost, with process and verification rules weighed every pass and proposed to the owner rather than kept or cut silently. The loss check now restores only what no ledger row decided, and `measure.py` inventories every markdown file with the readers it can prove.
- `validate-skills.mjs` caps a `SKILL.md` at 20 KiB and now catches `composes` of a skill that is not required.
- A root `AGENTS.md` names the checks a change runs and points at AUTHORING.md's sections; AUTHORING.md is cut to rules and README.md drops its structure tree.
- A normalize-md pass over this repository corrected commands that no longer worked (summarize-review's paginated baseline, recap-activity's Vercel log flags, the pnpm build allowlist), fetched the base SHA that verify-pr and approve-pr compare against, and removed rules that repeated a Process step.
- distill-session ships `scripts/episodes.py`, which lists skill episodes from the Claude, Codex, and Grok stores on this machine or another one over ssh, counts a Codex or Grok episode only when the agent reads the skill's `SKILL.md`, and hashes installed skill folders so a hand edit to an installed copy is found before a reinstall overwrites it.
- Eval cases for an admin merge past a merge queue, CI refused for billing, fixes pushed on a contributor's PR, and an unattended browser check, plus routing cases that diagnose-root, verify-ui, and mirror-reference stay unloaded for a feature change, a docs read, and an in-repo exemplar.

### Changed

- ship-pr merges directly when the user passed `--admin` or said to skip the queue, lets a PR added to an `--admin` batch inherit it, says a peer review never stands in for verify-pr, asks once to skip CI that GitHub refused for billing at the first tick, and passes one `Assisted-by` pull request link in a squash body.
- verify-pr builds a runnable repro worktree (the pinned package manager, the built workspace dependencies, `pipefail`), falls back to staged context and an in-memory harness in a sandbox, marks Necessity inconclusive when the duplicate search never ran, and says whether a small fix list is pushable; approve-pr pushes such fixes when the user asked to land the PR.
- commit-changes gives one command for staging several groups from pathspec files; create-branch uses a given branch name as is and infers a bare slug; create-pr folds a bundled release title into its headline change.
- read-source reads a worktree's pin from the main checkout, reads Rust crates and Maven or AAR artifacts from their caches, and stops retrying upstream reads in a sandbox without network.
- diagnose-root leaves feature changes and audits alone and counts a host run quoted in a brief as observed; verify-ui settles what an unattended run may do before any setup and hands back each route with its states; mirror-reference leaves in-repo exemplars alone.
- normalize-md's hook says the edit was applied and its findings are advisory.
- ship-pr keeps its gate rules in `SKILL.md` and moves the watch mechanics, the draft handling, and the merge body format into `references/monitor.md`, which brings it under the new cap.

## [0.0.49] (2026-11-06)

### Added

- Every skill works when installed alone. `metadata.requires` and **Requires** in the README name what must install together (ship-pr, approve-pr, organize-commits, design-dashboard), and `validate-skills.mjs` fails on a read of another skill's files outside that list, on a required composition with no fallback, and on copies that differ.

### Changed

- clean-memory carries its own `check.py`, `resolve.py`, and `references/write.md`, and recap-activity its own `references/stores.md`; a skill names any other skill only as an option.
- The memory resolver names a store's folder as Claude Code does: every character other than an ASCII letter or digit becomes a dash, and a name past 200 characters is cut and gains a hash of the path. The audit takes the store from it instead of keeping a second encoding.

## [0.0.47] (2026-10-26)

### Added

- verify-ui maps every browser operation (open, viewport, color scheme, script, screenshot, page snapshot, input, console, close) across Chrome DevTools MCP, Claude in Chrome, and a site-tools MCP server with the traps each has shown, and gives sandboxed or unattended runs a path that reads an open tab or hands the browser pass back.
- use-project-memory ships `agents/openai.yaml` with `allow_implicit_invocation: false`, so Codex lists it only for explicit invocation.
- Eval cases for a browser tool chosen from the ones a session exposes and for an old green whose base moved under the PR's own files.

### Changed

- verify-ui drives whichever browser tool the session exposes instead of naming Chrome DevTools tools, takes the one that can emulate a viewport and a color scheme when several are present, opens pages where the tool opens them by default, closes what it opened, counts a scripted event as injection, and reads a control's own state back after an action.
- ship-pr pins the merge to verify-pr's verified head with `--match-head-commit`, follows a merge queue until the PR merges, refreshes an old green only when the base moved under the PR's own files, watches several PRs from one request separately, bounds a loop by 45 minutes without a settled head, reruns a tracked flake and a timed-out review bot once, rescans open PRs before a follow-up PR, runs the CI test target before opening a PR, commits single-purpose review fixes directly with their hooks and signature in view, and claims only checks that ran.
- organize-commits gives each commit kept out of a regroup its own plan line; read-source reads tag naming from the latest release and reads installed CLIs by their binary; diagnose-root names the condition that separates intermittent failures; recap-activity dedupes the commits of advisory repositories; plan-charts draws relative ranges back from now with gaps and verifies one entity and sliver shares; upgrade-deps restores devDependencies that mirror a peer range; normalize-agents-md edits only with the editing tool; approve-pr says on which side of a change each run happened.
- Skill text is English: descriptions drop their Chinese trigger phrases, and seen clauses paraphrase reports made in another language. AUTHORING.md records that rule, that a skill names operations and takes the tool from the session, and that a skill is changed here and reinstalled rather than edited in its installed copy.
- README.md describes each skill in a few sentences and stays under its 16 KB target; the detail lives in each SKILL.md.
- The documented eval command judges with sonnet, because the default haiku judge failed answers that met their criterion; normalize-agents-md rewords a line that makes a doc win over the code to cover rules only, and verify-ui ends a read-only check with the finding and the cause's exact `file:line`.

## [0.0.46] (2026-10-20)

### Added

- `measure.py --since <commit or date>` reports how much each instruction file, read-path doc, and README, DESIGN, or ARCHITECTURE doc grew since then, so a normalization pass is judged on the tree a week later instead of on its own checks; report mode flags a pointed doc past its 16 KB target and lists every large doc off the agent's path.
- `measure.py --hook` and `check.py --hook` read Codex `apply_patch` and Grok edit payloads as well as Claude Code's, so the same doc and memory checks run as PostToolUse hooks in all three harnesses.
- Eval cases for a README manual taken off the agent's path, the markdown churn routing ask, an output-first digest, a share form held against real values, a reference's information layout, a states list in a render check, a pending CI row, an approval the base branch would ignore, and a design contract of rules only.

### Changed

- normalize-agents-md judges a doc by whether an instruction file points agents at it, not by who it was written for: a manual for people leaves the agent's path with its rules moved into AGENTS.md, the editing contract keeps person-facing docs from changing with every code change, every pass starts from the growth table and keeps a ledger, the loss check brief names no intended drop, and a moved as-built description never becomes a nested AGENTS.md.
- The doc hook also checks status lines and growth past 16 KB in every README, DESIGN, and ARCHITECTURE doc, and `since <date>` or `deployed <date>` lines count as status lines; `check.py` flags such dated status lines in memory topics and the index.
- use-project-memory stops at once in a run another agent dispatched, writes only through each harness's editing tool, and nudges for `clean-memory` when the index regrows by half; clean-memory always writes its sidecar.
- recap-activity's digest says what was produced before it counts anything; plan-charts holds each form against the values production would show; mirror-reference carries a reference's information layout when that layout is what makes it worth following; verify-ui lists every state a change touches as checked or not checked; optimize-repo reports its net line count and a doc sync line.
- verify-pr reads its CI row from the checks on the head; ship-pr prints a status line before each wait, keeps waits to 270 seconds, merges in the same turn once verify-pr clears the head, accepts `--approve`, and uses `--admin` on another author's PR only when the user passed it, after the approval path; approve-pr posts no approval the base branch would ignore from the account that pushed the last commit.
- distill-session scans every project's store when the ask is how the skills are used, works from per-invocation episodes when sessions outnumber its cap, and measures lasting goals on the tree; AUTHORING.md asks the same of every skill whose goal must hold after it runs.

## [0.0.45] (2026-10-15)

### Fixed

- `measure.py` counts a read order written with "before" first ("Before a UI change, read …") as one, so the doc it names is required and its target applies.

## [0.0.44] (2026-10-15)

### Added

- normalize-agents-md holds the docs an instruction file orders agents to read, such as a `DESIGN.md` every UI change reads first or a README named as the route registry, to its standard: they keep the rules every surface follows, lose as-built descriptions, orders to update them alongside code, and status lines, get a 16 KB target, and each pointer to them names the section a change needs. A new example shows the bar for such a rewrite.
- `measure.py` lists read-path docs with the line that points at each, and the accretion orders and status lines in every file, and gains `--hook`, a Claude Code PostToolUse check that flags what one write adds to an instruction file or read-path doc: a status line, an order to update a doc alongside code, history, a unit past 600 characters, or growth past a target.
- `scripts/test-measure.py`, run in CI, and two eval cases: a routing case for a design doc grown into a running log, and a quality case for its rewrite.

### Changed

- The root template's `Editing this file` contract becomes `Editing docs`: docs state what must stay true, a change replaces a sentence it made false instead of appending, a rule enters when the owner decides it, a mistake repeats, or a review catches it, and an amendment that would pass a target settles the file first.
- optimize-repo's doc sync replaces what a change made false and never appends an account of it; design-dashboard's contract states rules, never the surfaces built under them; use-project-memory routes descriptions of what the code does nowhere.
- normalize-agents-md never takes user-level instruction files into scope, even from the home directory.

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
