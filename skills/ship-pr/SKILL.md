---
name: ship-pr
description: Drive a change to a merged PR end to end, building or resuming the PR, looping over CI and review threads to address feedback, and merging once the repo's required-check gate passes.
argument-hint: "[task-or-pr] [--squash|--merge|--rebase] [--admin] [--delete-branch] [--approve] [--base <branch>] [--draft] [--advisory <check>]"
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

!`git log $(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@refs/remotes/origin/@@' || echo main)..HEAD --oneline 2>/dev/null || echo "(none or base not found)"`

## Instructions

Drive the change to a merged PR: implement if needed, branch, open the PR, then monitor CI and reviews until the merge gate passes, addressing feedback each cycle. Execute immediately without asking.

Delegate branch/commit/PR to their named skills (`create-branch`, `commit-changes`, `create-pr`); the should-this-merge judgment to `verify-pr`; review-thread triage to `verify-pr-comments`. Own only the monitor loop, the merge gate, and the merge. Invoke the others by name and act on their output; never inline or reimplement their logic.

Auxiliary skills, used only when relevant:
- **verify-issue**: optional upstream precursor when the change originates from an issue.
- **organize-commits**: optional pre-PR tidy, kept out of the unattended loop because it pauses for confirmation.
- **summarize-review**: when shepherding a contributor's PR rather than ship-pr's own change.
- **approve-pr**: when `--approve` is set, to post the maintainer approval near the merge gate; it owns the self-approval guard and the `gh pr review` write.

### Process

1. **Detect state and resume at the right step (adaptive entry).** Read the Context probes and resume at the first matching row. The leading positional of `$ARGUMENTS` is a change description, a PR number/URL to resume, or empty (operate on the current branch). Flag semantics that are not obvious from their names: `--advisory <check>` adds a check to the non-blocking set (repeatable) but cannot mark a human reviewer non-blocking; `--draft` is a hold short of merge, not a skip; the merge method (`--squash` default, `--merge`, `--rebase`) is validated early against `allowed_merge_methods` (step 3); `--approve` (off by default) delegates to `approve-pr` near the merge gate (condition (3)); a no-op on ship-pr's own PRs since GitHub blocks self-approval, so it applies only when shepherding another author's PR.

   | Priority | Condition | Action |
   |---|---|---|
   | 1 | `$ARGUMENTS` names a PR number/URL, or Existing PR is a URL | skip the build, enter the monitor loop (step 3), capturing the PR number |
   | 2 | uncommitted changes present | build the PR from branch and commit (step 2, `references/build-pr.md`) |
   | 3 | commits ahead of base but no open PR | build the PR from PR creation (step 2) |
   | 4 | only a task description on a clean tree | build the PR from implement (step 2) |
   | 5 | none of the above | nothing shippable; report and stop |

   Never force the full flow when a PR already exists. Detect GitButler once by comparing Current branch to `gitbutler/workspace` (the create side uses the `but` CLI only there); on that path the current-branch Existing PR probe cannot see the virtual branch's PR, so look it up by virtual branch name (`gh pr list --head <virtual-branch> --json number,url`). Derive OWNER and REPO from the Repository value; for an existing PR prefer its real base via `gh pr view <n> --json baseRefName`.

2. **Build the PR.** To build the PR (implement, branch, commit, changeset, open), follow `references/build-pr.md`; skip this when resuming an existing PR. When resuming an existing PR that is missing a required changeset, still add and push one per the changeset guidance in `references/build-pr.md`.

3. **Monitor by watching gh state, not a fixed clock.** Before the first wait, validate the configured merge method against the repo's `allowed_merge_methods` (`gh repo view --json squashMergeAllowed,mergeCommitAllowed,rebaseMergeAllowed`); if the requested method is not permitted, substitute the closest allowed (prefer squash, then rebase, then merge) and note the substitution rather than discovering the conflict at merge time. Then block on gh's own API-polling watch until the awaited state changes, run one idempotent monitor pass, then block again. `gh pr checks <n> --watch --interval <seconds>` is the primary wait (it returns the moment every check settles, review bots included since they report as checks); `gh run watch <run-id> --exit-status` is the single-run equivalent. When the rollup does not cover the wait, fall back to a short bounded gh poll per `references/monitor.md`. Right after pushing a fix, pause briefly before watching so the new run registers, or `--watch` may return immediately on the previous head's already-settled checks. Cap total wall-clock so a stuck check cannot loop forever.

4. **Run each monitor pass** following `references/monitor.md` for the full per-tick mechanics (gating-set discovery, check and reviewer classification, the reviewThreads read, merge-state handling, idempotency). Call `verify-pr` for the merge-worthiness recommendation only on the first pass after creation and after any substantial new commits, not every tick.

5. **Merge, then return to the default branch.** When the Merge gate holds, merge per the gate's command, then on this normal exit always return to the default branch and sync it so the local default carries the squashed merge and the next ship-pr starts clean: `git checkout <default> && git pull --ff-only` on the plain-git path; on the GitButler path stay on `gitbutler/workspace` and `but pull` instead of checking out. Then stop (the only normal exit). A `--draft` PR is a hold: keep watching but never `gh pr ready` or merge it until the user marks it ready. If the gate cannot clear, stop watching and report the blocker, leaving the PR branch checked out. Blockers:
   - a persistently red gating check
   - an unmet required approval
   - a DIRTY or conflict-blocked BEHIND branch
   - a fork head ship-pr cannot push to
   - an unreachable gating reviewer
   - `verify-pr` recommending close or redirect

   Cap iterations so the loop never runs forever; treat UNKNOWN merge or check states as still computing and re-poll rather than escalate.

### Addressing threads

Every unresolved thread is dispositioned and then resolved (three dispositions, reconciled with the governing rule below).

- **Valid feedback.** Fix in a follow-up commit (`commit-changes` on the plain-git path, `but commit` on the GitButler path, then push), then resolve the thread. The fix commit is already on the PR timeline, so do not add a reply that only points at it.
- **Invalid feedback.** Reply with a short rationale (it carries information the diff does not), then resolve.
- **Outdated thread** (`isOutdated` true). Resolve it; the moved diff is self-evident, so do not reply.

Use judgment on bot nits: common-sense suggestions a competent agent already follows are usually a silent resolve, and scope creep from a long bot-feedback loop is a signal to cut and merge.

ship-pr owns the writes (`verify-pr-comments` is read-only): build the reply body safely with `printf '%s' "$reply" | jq -Rs '{body: .}'` and post it via `gh api repos/$OWNER/$REPO/pulls/<n>/comments/<databaseId>/replies --method POST --input -` (inline `-f body='...'` breaks on backticks and code; databaseId is the REST integer from ship-pr's reviewThreads nodes), and resolve via `gh api graphql -f query='mutation($id:ID!){resolveReviewThread(input:{threadId:$id}){thread{isResolved}}}' -f id=<threadId>` (threadId is the opaque node id, so `-f` not `-F`).

Governing rule: do not add comments or changeset prose that only acknowledge review feedback; the test is, would you write it if no reviewer had flagged the code? If no, drop it.

### Merge gate

Three conditions, all required, plus the mergeability preconditions.

- **(1) Gating checks green.** Every GATING check is green; gating means the repo's required checks discovered in `references/monitor.md`, while advisory checks and review bots (deploy previews, AI reviewers, optional analyzers) never block whatever their state, purely because they are absent from the required set; never hardcode required checks or a bot name. When no required set is machine-discoverable (rulesets empty, legacy 404 or 403, `gh pr checks <n> --required` returns nothing), gate on every rollup check being green except the contexts named via `--advisory`, and merge only once all pass; this is the conservative reading, since it waits on checks a discovered required set would have excluded.
- **(2) Threads resolved.** Every review thread is resolved (ship-pr's reviewThreads read returns no `isResolved == false`).
- **(3) Reviewers satisfied.** The count of distinct current APPROVED reviewers meets the repo's `required_approving_review_count`, and no GATING reviewer is in CHANGES_REQUESTED (the latest-per-author reduction is empty for humans and required reviewers). Address the feedback and wait for re-approval; never dismiss the review. When `--approve` is set and the only shortfall is the approval count (no GATING reviewer in CHANGES_REQUESTED) with conditions (1) and (2) already holding, delegate to `/approve-pr <n>` (without `--merge`) to post the approval, then re-evaluate the gate; approve-pr gates its own write on a fresh verify-pr and no-ops on ship-pr's own PRs (self-approval is blocked), so `--approve` clears this condition only when shepherding another author's PR.
- **Preconditions.** `mergeable != CONFLICTING`; `mergeStateStatus` is CLEAN, accepting UNSTABLE or BLOCKED only when the sole outstanding cause is an excluded advisory check and conditions (1) to (3) independently hold, and never DIRTY or DRAFT. When `mergeStateStatus` is UNSTABLE, enumerate every non-passing check in `statusCheckRollup` and confirm each is advisory (absent from the discovered required set and not named by a human reviewer) before treating UNSTABLE as acceptable; if any non-passing check is not advisory, UNSTABLE blocks the merge. A `--draft` PR is a deliberate hold (see step 5). verify-pr supplies only the merge-worthiness recommendation (necessity and correctness, and a verdict of merge rather than close, redirect, or push back); the gating-versus-advisory classification in conditions (1) to (3) is ship-pr's own per-tick poll.
- **Merge.** When all hold, merge with the configured method, appending `--admin` only if the user opted in and `--delete-branch` if requested. Immediately before merging, independently re-verify all three conditions and all preconditions, and re-read `headRefOid`; abort and re-run one monitor pass if the head SHA no longer matches the one the gate evaluated. Even with `--admin`, this re-verification still runs: `--admin` may force past a BLOCKED or UNSTABLE state whose sole cause is an excluded advisory check; it never overrides an unmet condition (1), (2), or (3), and never merges a CONFLICTING, DIRTY, or DRAFT PR.

### Rules

- Commit and push all uncommitted work, including the changeset, before PR creation; never let create-pr open a PR over a dirty tree.
- One branch per change group; never touch another agent's branch or staged work.
