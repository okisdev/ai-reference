---
name: ship-pr
description: Drive a change to a merged PR. Implement if needed, branch, open the PR, then loop over CI and review threads, address feedback, and merge once the gate passes. Auto-detects the entry point (uncommitted changes, an existing branch, or an open PR) and resumes there rather than forcing the full flow; auto-detects GitButler versus plain git; gates only on the repo's required checks while advisory checks and review bots never block. Composes make-branch, commit-changes, and make-pr to build the PR, verify-pr to judge it, and verify-pr-comments to triage threads; ship-pr is the looping orchestrator that owns the loop, the merge gate, and the merge, and reimplements none of their logic. Unlike the read-only verify skills it is action-taking; it commits, pushes, replies to and resolves threads, and merges. Use when the user wants a change shepherded end to end, not just reviewed.
argument-hint: "[task-or-pr] [--squash|--merge|--rebase] [--admin] [--delete-branch] [--base <branch>] [--draft] [--advisory <check>]"
---

## Context

Repository: !`gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null || echo "unknown"`
Default branch: !`git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@refs/remotes/origin/@@' || echo main`
Current branch: !`git branch --show-current`
Existing PR: !`gh pr view --json number,url -q '"#" + (.number|tostring) + " " + .url' 2>/dev/null || echo "(none)"`
Changesets: !`test -d .changeset && echo "yes (.changeset/)" || echo "(none)"`

### Uncommitted changes

!`git status --short`

### Commits ahead of base

!`git log $(git symbolic-ref --short refs/remotes/origin/HEAD 2>/dev/null | sed 's|^origin/||' || echo main)..HEAD --oneline 2>/dev/null || echo "(none or base not found)"`

Runtimes that do not auto-run the commands above marked with `!` (Claude Code executes them and injects their output) should run each one to gather this context; treat any `$ARGUMENTS` or `$1` as the input the user provided.

## Instructions

Drive the change to a merged PR: implement if needed, branch, open the PR, then monitor CI and reviews until the merge gate passes, addressing feedback each cycle. Execute immediately without asking.

ship-pr is the looping orchestrator. It owns only three things: the monitor loop, the merge gate, and the merge itself. Everything else is delegated: branch creation to `make-branch`, committing to `commit-changes`, PR authoring to `make-pr`, the should-this-merge judgment to `verify-pr`, and review-thread triage to `verify-pr-comments`. Invoke them by name and act on their output; never inline or reimplement their logic.

The only step gated behind a condition is the auto-merge, which never runs until the merge gate below holds; every other step proceeds without prompting.

Auxiliary skills, used only when relevant:
- **verify-issue**: optional upstream precursor when the change originates from an issue.
- **organize-commits**: optional pre-PR tidy, kept out of the unattended loop because it pauses for confirmation.
- **review-summary**: when shepherding a contributor's PR rather than ship-pr's own change.

### Input

`$ARGUMENTS` is optional. The leading positional is a description of the change to implement, a PR number or full GitHub PR URL to resume monitoring, or empty (operate on the current branch and its open PR, if any). Flags: exactly one of `--squash` (default), `--merge`, or `--rebase` selects the merge method, constrained at merge time to a method the repo's `allowed_merge_methods` permits; `--admin` opts into a protected-branch bypass on the final merge only, off by default; `--delete-branch` passes through to the final `gh pr merge`, deleting ship-pr's own merged branch, off by default; `--base <branch>` passes through to make-branch and make-pr; `--draft` passes through to make-pr and holds the loop short of merge; `--advisory <check>` (repeatable) names an extra check context non-blocking, layered on the structurally-discovered advisory set, and is the escape hatch when no required-check set is machine-discoverable. `--advisory` cannot mark a human reviewer non-blocking.

### Process

1. **Detect state and resume at the right step (adaptive entry).** Read the Context probes: if `$ARGUMENTS` names a PR or Existing PR is a URL, skip the build and go straight to the monitor loop (step 3), capturing the PR number; else if there are uncommitted changes, build the PR starting at branch and commit (step 2, `references/build-pr.md`); else if there are commits ahead of base but no open PR, build the PR starting at PR creation (step 2, `references/build-pr.md`); else if only a task description was given on a clean tree, build the PR starting at implement (step 2, `references/build-pr.md`); else nothing is shippable, so report and stop. Re-running on an open PR is a resume, not a restart; never force the full flow when a PR already exists. Detect GitButler once here by comparing Current branch to `gitbutler/workspace`; the create side uses the `but` CLI only on that branch, otherwise plain git. On the GitButler path the Existing PR probe (current-branch-based) cannot see the virtual branch's PR, so resume detection looks it up by the virtual branch name (`gh pr list --head <virtual-branch> --json number,url`). Derive OWNER and REPO by splitting the Repository value on `/`; for an existing PR prefer its real base via `gh pr view <n> --json baseRefName`.

2. **Build the PR.** To build the PR (implement, branch, commit, changeset, open), follow `references/build-pr.md`; skip this when resuming an existing PR. When resuming an existing PR that is missing a required changeset, still add and push one per the changeset guidance in `references/build-pr.md`.

3. **Monitor by watching gh state, not a fixed clock.** Drive the loop off GitHub state transitions rather than a wall-clock cadence: block on gh's own API-polling watch until the awaited state actually changes, run one idempotent Monitor cycle pass, then block again. `gh pr checks <n> --watch --interval <seconds>` is the primary wait; it polls the checks API and returns the moment every check settles, review bots included since they report as checks. `gh run watch <run-id> --exit-status` is the single-run equivalent. When the wait is on something the checks rollup does not cover (a just-pushed fix whose new run has not registered yet, an UNKNOWN merge state still computing, or a bot review that posts no check), fall back to a short bounded gh poll: re-query, sleep a few seconds, repeat, exit on the first change. Right after pushing a fix, pause briefly so the new run registers before watching, or `--watch` may return immediately on the previous head's already-settled checks. The block returns on the event, so there is no idle fixed-interval wakeup; a doubled or missed wake is still harmless because each pass is idempotent. Cap total wall-clock so a stuck check cannot loop forever.

4. **Run each monitor pass.** Per Monitor cycle: re-derive state from gh, run the operational gate as a lightweight per-tick poll, run ship-pr's own reviewThreads read and delegate claim classification to `verify-pr-comments`, apply fixes via `commit-changes` (or `but commit`), reply to and resolve threads per Addressing threads, and evaluate the Merge gate. Call `verify-pr` for the merge-worthiness recommendation only on the first pass after creation and after any substantial new commits, not every tick.

5. **Merge, then return to the default branch.** When the Merge gate holds, merge per the gate's command, then on this normal exit always return to the default branch and sync it so the local default carries the squashed merge and the next ship-pr starts clean: `git checkout <default> && git pull --ff-only` on the plain-git path; on the GitButler path stay on `gitbutler/workspace` and `but pull` instead of checking out. Then stop (the only normal exit). A PR opened with `--draft` is a hold: keep watching but never `gh pr ready` or merge it until the user marks it ready. If the gate cannot clear (a gating check persistently red, an unmet required approval with no path to it, a DIRTY branch or a BEHIND branch whose update conflicts and needs a rebase or the original author, a gating reviewer unreachable, a fork head ship-pr cannot push to and therefore cannot auto-update when BEHIND, or `verify-pr` recommending close or redirect), stop watching and report the blocker, leaving the PR branch checked out so the user can investigate. Cap iterations so the loop never runs forever; treat UNKNOWN merge or check states as still computing and re-poll rather than escalate.

### Monitor cycle

One idempotent pass. Parameterize OWNER and REPO from the Repository probe into every query and never hardcode them; re-fetch fresh state each pass and never cache the head SHA (`gh pr view <n> --json headRefOid`), since after pushing fixes the head moves, advisory bots re-run, and pending checks or threads clear.

- **Gating set.** Discover the required checks once, taking the first source that yields data: `gh pr checks <n> --required` (exit 0 all passed, 8 some pending, 1 some failed), then ruleset `required_status_checks[].context` via `gh api repos/$OWNER/$REPO/rules/branches/$BASE`, then legacy branch protection contexts; treat a 404 as not protected and a 403 as insufficient scope, both falling through rather than reading as no required checks. From the same ruleset or protection payload read `required_approving_review_count` for the approval gate.
- **Check state.** Block on `gh pr checks <n> --watch --interval <seconds>` to wait for the checks to settle without a fixed-cadence wakeup, then read `gh pr view <n> --json statusCheckRollup` to classify, normalizing both node shapes (CheckRun `.name` plus `.conclusion`, StatusContext `.context` plus `.state`) into pass (SUCCESS, NEUTRAL, SKIPPED), fail (FAILURE, ERROR, CANCELLED, TIMED_OUT, ACTION_REQUIRED), or pending (keeps looping; pending is not failure). `--watch` only blocks; the rollup is still what classifies gating versus advisory and pass versus fail. Do not trust the rollup `isRequired` field, unreliable on ruleset repos.
- **Reviewer states.** Reduce `gh pr view <n> --json reviews` to the latest state-changing review per author (APPROVED, CHANGES_REQUESTED, DISMISSED; COMMENTED never changes approval); list any gating reviewer (a human, or a ruleset-required reviewer) still in CHANGES_REQUESTED, and count distinct current APPROVED reviewers against `required_approving_review_count`. Classify bots structurally via `gh api repos/$OWNER/$REPO/pulls/<n>/reviews` `user.type == "Bot"`, never by login pattern.
- **Review threads.** Run ship-pr's own reviewThreads query (owner and repo parameterized, the number passed with `-F` as a JSON Int) selecting each thread's `id`, `isResolved`, `isOutdated`, and `comments(first: 1){nodes{databaseId}}`, paginating past `first: 100` via `pageInfo.hasNextPage` and `endCursor`; this read drives both resolution (the `id` to resolve, the `databaseId` to reply) and gate condition (2). Delegate only the valid-versus-noise-versus-stale claim classification to `verify-pr-comments`.
- **Merge state.** `gh pr view <n> --json mergeable,mergeStateStatus,isDraft`; wait on UNKNOWN; on BEHIND, when ship-pr owns the head branch, update it and re-poll (`gh pr update-branch <n>`, or rebase or merge the freshened base then push; `but pull` then restack on the GitButler path); treat BLOCKED as not-yet-mergeable (a required approval or check still outstanding) and keep polling; and never auto-merge DIRTY, CONFLICTING, or DRAFT.
- **Idempotency.** A resolved thread is skipped on the next read, so the gh state is the durable record that prevents a later tick from re-replying; resolve before the next tick.

### Addressing threads

Every unresolved thread is dispositioned and then resolved (three dispositions, reconciled with the governing rule below).

- **Valid feedback.** Fix in a follow-up commit (`commit-changes` on the plain-git path, `but commit` on the GitButler path, then push), then resolve the thread. The fix commit is already on the PR timeline, so do not add a reply that only points at it.
- **Invalid feedback.** Reply with a short rationale (it carries information the diff does not), then resolve.
- **Outdated thread** (`isOutdated` true). Resolve it; the moved diff is self-evident, so do not reply.

Use judgment on bot nits: common-sense suggestions a competent agent already follows are usually a silent resolve, and scope creep from a long bot-feedback loop is a signal to cut and merge rather than keep iterating.

ship-pr owns the writes (`verify-pr-comments` is read-only): reply via `gh api repos/$OWNER/$REPO/pulls/<n>/comments/<databaseId>/replies -f body='...'` (databaseId is the REST integer from ship-pr's reviewThreads nodes) and resolve via `gh api graphql -f query='mutation($id:ID!){resolveReviewThread(input:{threadId:$id}){thread{isResolved}}}' -f id=<threadId>` (threadId is the opaque node id, so `-f` not `-F`).

Governing rule: do not add comments or changeset prose that only acknowledge review feedback; the test is, would you write it if no reviewer had flagged the code? If no, drop it.

### Merge gate

Three conditions, all required, plus the mergeability preconditions.

- **(1) Gating checks green.** Every GATING check is green; gating means the repo's required checks discovered above, while advisory checks and review bots (deploy previews, AI reviewers, optional analyzers) never block whatever their state, purely because they are absent from the required set; never hardcode required checks or a bot name. When no required set is machine-discoverable (rulesets empty, legacy 404 or 403, `gh pr checks <n> --required` returns nothing), gate on every rollup check being green except the contexts named via `--advisory`, and merge only once all pass; this is the conservative reading, since it waits on checks a discovered required set would have excluded.
- **(2) Threads resolved.** Every review thread is resolved (ship-pr's reviewThreads read returns no `isResolved == false`).
- **(3) Reviewers satisfied.** The count of distinct current APPROVED reviewers meets the repo's `required_approving_review_count`, and no GATING reviewer is in CHANGES_REQUESTED (the latest-per-author reduction is empty for humans and required reviewers). Address the feedback and wait for re-approval; never dismiss the review.
- **Preconditions.** `mergeable != CONFLICTING`; `mergeStateStatus` is CLEAN, accepting UNSTABLE or BLOCKED only when the sole outstanding cause is an excluded advisory check and conditions (1) to (3) independently hold, and never DIRTY or DRAFT. A `--draft` PR is a deliberate hold (see step 5). verify-pr supplies only the merge-worthiness recommendation (necessity and correctness, and a verdict of merge rather than close, redirect, or push back); the gating-versus-advisory classification in conditions (1) to (3) is ship-pr's own per-tick poll.
- **Merge.** When all hold, merge: `gh pr merge <n>` with the configured method (`--squash` default, or `--merge` or `--rebase`, only a method `allowed_merge_methods` permits), appending `--admin` only if the user opted in and `--delete-branch` if requested. Even with `--admin`, independently re-verify all three conditions plus the preconditions immediately before merging; `--admin` may override a BLOCKED or UNSTABLE state whose sole cause is an excluded advisory check, and never to bypass them (resolve any conflict first).

### Rules

- ship-pr is action-taking (it commits, pushes, replies to and resolves threads, and merges); do not import verify-pr's read-only rule.
- The plain-git path assumes exclusive use of the working tree (make-branch stashes and restages the whole tree); concurrent-agent isolation comes only on the GitButler path via selective `but stage`.
- Commit and push all uncommitted work, including the changeset, before PR creation; never let make-pr open a PR over a dirty tree.
- Never merge past a red or pending gating check, an unmet required approval, an unresolved review thread, a gating reviewer in CHANGES_REQUESTED, or a conflicting or draft PR, even with `--admin`; re-verify the gate independently immediately before merging.
- One branch per change group; never touch another agent's branch or staged work.

**See also**: `/make-branch`, `/commit-changes`, and `/make-pr` build the PR, `/verify-pr` judges whether it should merge, and `/verify-pr-comments` triages the review threads.
