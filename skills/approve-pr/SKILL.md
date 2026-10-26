---
name: approve-pr
description: Approve a GitHub PR as a maintainer once verify-pr clears it, posting the GitHub approval or declining, with an optional hand-off to ship-pr for the merge.
argument-hint: "<pr-number-or-url> [--merge] [--request-changes] [--comment] [--squash|--admin|--delete-branch]"
---

## Context

Repository: !`gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null || echo "unknown"`
Default branch: !`out=$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@refs/remotes/origin/@@'); echo "${out:-main}"`
Current branch: !`git branch --show-current 2>/dev/null || echo "(not a git repository)"`
My login: !`gh api user --jq .login 2>/dev/null || echo "unknown"`

## Instructions

**The one rule: approve the head you judged, once, then stop.** The approval binds to the SHA `verify-pr` reported, is posted once (refreshed in place when you already approved), and ends the skill, since `ship-pr` owns the checks and the merge. The bar is a note a maintainer would sign: the verdict and the one reason it holds, what you ran against what you only read, and what still stands and why it does not block. Open [examples/approval.md](examples/approval.md), or [examples/decline.md](examples/decline.md) when the decision table says do not approve, before writing, and check the draft against [examples/rejected.md](examples/rejected.md).

Review a GitHub PR as a maintainer and, when it earns it, post the single GitHub approval; otherwise report and decline. Auto-post only the approval; non-approving writes need an explicit opt-in. Execute immediately without asking.

Delegate the approve-or-decline verdict to `verify-pr` (consume its recommendation, from a current report when the workflow already holds one), the unresolved-thread triage to `verify-pr-comments`, the review body to `summarize-review` when your own commits are on the PR, and the optional post-approval merge to `ship-pr` (it owns the merge gate and the merge, and validates the merge method). Own only the self-approval guard, the verdict-to-action mapping, and the `gh pr review` write. Invoke the others by name and act on their output; never inline or reimplement their logic.

### Process

1. **Parse the PR and flags.** The leading positional of `$ARGUMENTS` is a PR number (e.g. `4621`) or a full PR URL; flags follow. The default with no flag is approve-only. `--merge` hands the PR to `ship-pr` after a successful approval, forwarding any pass-through merge flags (`--squash`, `--admin`, `--delete-branch`) to it unvalidated; `--request-changes` and `--comment` opt into a non-approving write. Derive OWNER and REPO from the Repository probe.

2. **Fetch PR state and run the self-approval guard.** Read `gh pr view <n> --repo <o>/<r> --json number,author,headRefOid,state,reviewDecision`. If `state` is not `OPEN`, report and stop. Self-approval guard (owned): if `author.login` equals the My login probe, stop before any write. GitHub rejects approving your own PR (`Can not approve your own pull request`), so report that it needs a different maintainer, or `/ship-pr <n>` to drive your own change to merge while it waits for someone else's approval. When commits by your login sit on the PR, also read whether the base branch's gate counts your approval: `require_last_push_approval` in `gh api repos/<o>/<r>/rules/branches/<base>` and in the branch protection, and any review gate check whose output names ignored reviewers. When it does not count, post nothing and report the reviewer or waiver the merge needs instead (seen: an approval posted after the approver's own push, which the gate answered with "okisdev ignored (wrote a commit here)"). Record `headRefOid` for the stale-head recheck in step 5.

3. **Take verify-pr as the gate.** When the current workflow already holds a complete verify-pr report (verdict table, final recommendation, and Verified head) whose Verified head and base equal the freshly fetched `headRefOid` and `baseRefOid` from step 2, use it instead of invoking verify-pr again, since a retargeted base changes the diff without moving the head; otherwise invoke `/verify-pr <n>`. Consume its final recommendation verbatim, one of close or redirect, merge as-is, merge after small fixes, or push back. Do not re-derive correctness or necessity. Reuse skips only the invocation: step 4 still reads thread state fresh, the decision table still applies, and step 5 still rechecks the head. An approval binds to the SHA verify-pr reported as its Verified head, so on a re-approval after the author pushed, pass `--since <the previously approved head>` and judge that delta rather than approving a head nobody read.

4. **Triage unresolved threads.** Read the review threads with the recipe in [`verify-pr-comments/references/threads.md`](../verify-pr-comments/references/threads.md) (`reviewThreads` is GraphQL-only, not a `gh pr view --json` field) and count the unresolved ones with the `jq -s` filter shown there. Read them fresh every time, including when step 3 reused a report. If any are unresolved, invoke `/verify-pr-comments <n>`. A thread that is Fresh and valid (Confirmed or Partial) and unaddressed blocks approval; Resolved, Stale, Refuted, and Out-of-scope threads do not. Branch protection may not enforce thread resolution, so treat this as a policy gate rather than relying on the merge to block.

5. **Map the verdict to an action and post.** Apply the decision table below. Reach the approval only on merge as-is with no fresh blocking thread.

   Draft the body to fit what actually happened. When commits of yours sit on the PR (compare the commit authors against the My login probe), this is a takeover and the report belongs to `/summarize-review <n>`. When you changed nothing, write it here: a short conversational note to the author, prose, no headings, saying the verdict and the one reason it holds, the evidence behind whatever the approval rests on (what you executed against what you only read, on each side of the change; seen: a note claimed a local run failed without the fix when that side came from a CI log), and anything still standing with why it does not block. A paragraph or two is the whole of it. Cite a maintainer's decision by the comment that made it, not by a later PR that applied it (seen: a later PR was cited as authority when an earlier maintainer comment ruled). Say nothing the diff already says, since re-narrating the patch back to the person who wrote it is what makes an approval read like a form.

   Then re-read `headRefOid`, and if it moved since step 2 abort and re-run from step 3 (a stale approval keeps gating code nobody judged). Then resolve your latest prior review:
   ```bash
   gh api --paginate --slurp repos/<o>/<r>/pulls/<n>/reviews | jq '[.[][] | select(.user.login=="<me>")] | last | {id, state}'
   ```
   If it is already `APPROVED`, refresh the body in place rather than stacking a duplicate (`gh api --method PUT repos/<o>/<r>/pulls/<n>/reviews/<id> -f body="<text>"`); otherwise submit a fresh review:
   ```bash
   gh pr review <n> --repo <o>/<r> --approve --body-file - <<'EOF'
   <body>
   EOF
   ```
   After posting, read `reviewDecision`; if it is still `REVIEW_REQUIRED`, report what is outstanding (for example a code-owner review on a protected path). Then stop; only the `--merge` hand-off in step 7 continues, and this skill never watches checks, since `ship-pr` owns the wait (seen: it kept watching checks after posting until the user said CI was fine).

6. **On a decline, write only the opt-in path.** When an opt-in flag authorizes a non-approving write (`--request-changes` for a push back, `--comment` for a note), post it via `--body-file -`. Otherwise report verify-pr's recommendation and any blocking thread, and stop without writing.

7. **Optional `--merge` hand-off.** Only when `--merge` was passed and the approval posted, hand the PR number and any pass-through flags to `/ship-pr <n>` and stop. Never merge directly.

### Decision table

| Condition (fresh verify-pr verdict + thread state) | Action |
|---|---|
| PR authored by the My login probe | stop before any write; self-approval is platform-blocked; report it needs a different maintainer |
| merge as-is, no fresh blocking thread | post the approval (step 5) |
| merge as-is, but a Fresh valid (Confirmed/Partial) unaddressed thread | do not approve; report the blocking thread |
| merge after small fixes | do not approve; report the remaining blocking items; `--comment` only on opt-in |
| push back | do not approve; report verify-pr's rationale verbatim; `--request-changes` only on explicit opt-in |
| close or redirect | do not approve; report the close recommendation verbatim; never execute the close |

### Rules

- No trace of tooling in anything posted under the user's name: no `Co-Authored-By` trailer naming a coding tool, no generated-by line, no session link (seen: tool trailers and session links the user had to strip from merged PRs).
- The only state-changing `gh pr review` this skill posts without an explicit opt-in is the approval. `--request-changes` and `--comment` require an opt-in; a close or redirect recommendation is reported, never executed.
- Pass every review body via `--body-file -` with a quoted heredoc (`<<'EOF'`), never `-b/--body "..."`; the summarize-review body carries backticks and code that string interpolation mangles.
- `PUT /pulls/<n>/reviews/<id>` edits the body text only, never the review state; it cannot upgrade a prior COMMENTED, CHANGES_REQUESTED, or DISMISSED review to APPROVED. Submit a fresh `--approve` to change state.
- Approval and merge are independent gates: post the approval regardless of check state; the merge stays gated by ship-pr.
