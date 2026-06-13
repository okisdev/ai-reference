---
name: verify-pr-comments
description: Fetch review comments on a GitHub PR (bots + humans) and verify each claim against the actual code, reporting which to accept / reject / defer with concrete evidence and fix drafts.
argument-hint: "<pr-number-or-url>"
---

## Context

Repository: !`gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null || echo "unknown"`
Default branch: !`git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@refs/remotes/origin/@@' || echo main`
Current branch: !`git branch --show-current 2>/dev/null`

Runtimes that do not auto-run the commands above marked with `!` (Claude Code executes them and injects their output) should run each one to gather this context; treat any `$ARGUMENTS` or `$1` as the input the user provided.

## Instructions

Verify every substantive review comment on a GitHub PR against the current codebase. Execute immediately without asking.

**Distinct from siblings**: `/verify-pr` judges whether a PR should merge; `/verify-issue` validates an issue's claims; this skill validates the review comments left ON a PR. Use `/verify-pr` to decide whether to merge; use this one when responding to reviewers.

### Input

`$ARGUMENTS` is a PR number (e.g. `3841`) or a full GitHub PR URL (e.g. `https://github.com/owner/repo/pull/3841`).

### Process

1. **Fetch comments from all three endpoints** (PR reviews are fragmented):
   - `gh api repos/<owner>/<repo>/pulls/<num>/reviews --paginate`: top-level reviews (long summary bodies from `claude[bot]`, `cubic-dev-ai[bot]`, human reviewers). Each has `commit_id`.
   - `gh api repos/<owner>/<repo>/pulls/<num>/comments --paginate`: inline comments on a file/line. Each has `path`, `line`, `commit_id`, `body`.
   - `gh api repos/<owner>/<repo>/issues/<num>/comments --paginate`: issue-level PR comments (where `changeset-bot`, `vercel`, `greptile-apps` post status).
   - `gh pr view <num> --comments`: human-readable mix but lacks `commit_id` for staleness detection; fallback only.

2. **Fetch resolution state for inline-comment threads** via GraphQL (REST does not expose this):
   ```bash
   gh api graphql -F owner=<owner> -F repo=<repo> -F num=<num> -f query='
     query($owner: String!, $repo: String!, $num: Int!) {
       repository(owner: $owner, name: $repo) {
         pullRequest(number: $num) {
           reviewThreads(first: 100) {
             nodes {
               isResolved
               isOutdated
               comments(first: 10) { nodes { databaseId } }
             }
           }
         }
       }
     }'
   ```
   Build a map from inline comment ID to its thread's `isResolved` and `isOutdated`. Resolved-thread comments had a real review claim that was already addressed; they carry the **Resolved** verdict and are excluded from re-verification (not collapsed into Stale), re-verifying only if the user explicitly asks.

3. **Determine the latest commit**: `gh api repos/<owner>/<repo>/pulls/<num> --jq .head.sha`. Fresh comments are judged against this `commit_id`.

4. **Filter noise** by skipping entries whose body is metadata, not a review claim:
   - `changeset-bot`: changeset detection summary.
   - `vercel` / `vercel[bot]`: deployment URLs.
   - `greptile-apps` when body is just the `<!-- greptile_other_comments_section -->` footer.
   - Any body that is entirely HTML attribution / CTA / badges with no prose claim. Strip `<!-- ... -->` markers and "Fix with …" buttons before reading.

   Resolved-thread comments are not noise; they carry a real, already-addressed claim. They appear in the matrix with the **Resolved** verdict (step 2) but are skipped for active verification.

5. **Classify each remaining comment by staleness**:
   - **Inline comments**: judge by `isOutdated` from the reviewThreads map (step 2). `isOutdated: true` => **Stale**; `isOutdated: false` => **Fresh**, verify it. A push changes the head SHA, so exact `commit_id` equality over-marks inline comments whose target code is untouched; `isOutdated` reflects whether the commented lines actually moved.
   - **Top-level review summary bodies**: these carry no thread, so reserve `commit_id` equality for them. `commit_id === latest head SHA` => **Fresh**, verify it; otherwise **Stale**.
   - Mark stale entries "Stale (last seen at `<sha[:7]>`)" and move on; don't reverify unless the user asks.

6. **Verify each fresh, substantive comment**:
   - `Read` the referenced file at its current state. Do NOT trust the reviewer's quoted diff; snippets go outdated after pushes.
   - Treat ```` ```suggestion ```` blocks as the primary, testable artifact (GitHub renders them as one-click "Commit suggestion" buttons). Read the suggestion first, surrounding prose as justification; verify it in isolation: would applying it compile and match existing patterns?
   - Cross-check any factual claim ("type X exists in module Y", "pattern Z is used in other-file.ts") with `Grep` before accepting it.
   - Mentally apply the suggested fix and verify types/callers/tests still pass; bots frequently suggest fixes that fail type-check or break callers.
   - Assign one verdict:
     - **Confirmed**: claim correct and the suggested fix works as-is.
     - **Partial**: claim has merit but the fix is wrong or incomplete; propose an adjusted fix (e.g. `Pick<ThreadListItemRuntime, "foo">` rather than the bare type).
     - **Refuted**: claim incorrect. Explain why with code evidence.
     - **Out-of-scope**: valid but exceeds the PR's intent (architectural refactor, missing tests, etc.). Defer to follow-up.
     - **Resolved**: a human marked the thread resolved (step 2).
     - **Stale**: outdated against the current code (step 5).

7. **Parallel verification**: run independent Read/Grep calls in parallel. Prefer direct tool calls over agents to save context.

8. **Report** in structured output:

   - **PR summary**: title, latest commit SHA, counts of fresh / stale / resolved / noise comments.
   - **Comment matrix** (one row per substantive comment):

     | # | Author | Location | Claim (short) | Verdict | Action |
     |---|--------|----------|---------------|---------|--------|
     | 1 | `claude[bot]` | `foo.ts:12` | "type is redundant" | Confirmed | inline `Pick<...>` |

   - **Per-comment detail** for each Confirmed / Partial entry: 2 to 3 line evidence plus a concrete fix draft (code snippet or `file:line` diff).
   - **Rejected / deferred comments**: one line each with the reason.
   - **Recommended actions**, a concise list the user can act on:
     - changes to make (with `file:line`).
     - comments to reply-to-reject (with draft reply text if helpful).
     - bots to re-trigger (e.g. "tag `@cubic-dev-ai`, its last review is stale on `<sha>`").

### Bot signature reference

See `references/bot-signatures.md` for the bot-signature table; skim it when classifying authors.

### Rules

- **Distinguish "Critical Issues" from "Suggestions"**: review bots often split their output. Critical issues deserve Confirmed/Refuted judgments; plain suggestions can be marked Out-of-scope with a one-line reason.
- **Human > bot**: if a human reviewer contradicts a bot, weight the human's intent and note the bot's disagreement in the report.
- **Never modify files** during verification. This skill is read-only analysis; fix work happens in a follow-up step.
- **Be concise**: evidence is `file:line` references, not code dumps. The matrix is the primary artifact.
- **Use the same language as the user's input** when reporting.
