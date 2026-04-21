---
name: verify-pr-comments
description: Fetch review comments on a GitHub PR (bots + humans) and verify each claim against the actual code, reporting which to accept / reject / defer with concrete evidence and fix drafts.
argument-hint: "<pr-number-or-url>"
---

## Context

Repository: !`gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null || echo "unknown"`
Default branch: !`git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@refs/remotes/origin/@@' || echo main`
Current branch: !`git branch --show-current 2>/dev/null`

## Instructions

Verify every substantive review comment on a GitHub PR against the current codebase. Execute immediately without asking.

### Input

`$ARGUMENTS` is a PR number (e.g. `3841`) or a full GitHub PR URL (e.g. `https://github.com/owner/repo/pull/3841`).

### Process

1. **Fetch comments from all three endpoints** — PR reviews are fragmented:
   - `gh api repos/<owner>/<repo>/pulls/<num>/reviews --paginate` — top-level reviews (the long summary bodies from `claude[bot]`, `cubic-dev-ai[bot]`, human reviewers). Each entry has `commit_id`.
   - `gh api repos/<owner>/<repo>/pulls/<num>/comments --paginate` — inline comments on specific file/line. Each entry has `path`, `line`, `commit_id`, `body`.
   - `gh api repos/<owner>/<repo>/issues/<num>/comments --paginate` — issue-level PR comments (where bots like `changeset-bot`, `vercel`, `greptile-apps` post status).
   - `gh pr view <num> --comments` returns a human-readable mix but lacks `commit_id` for staleness detection — use it only as a fallback.

2. **Determine the latest commit on the PR**:
   - `gh api repos/<owner>/<repo>/pulls/<num> --jq .head.sha` — this is the `commit_id` against which "fresh" comments are judged.

3. **Filter noise** — skip entries whose body is metadata-only, not a review claim:
   - `changeset-bot`: changeset detection summary
   - `vercel` / `vercel[bot]`: deployment URLs
   - `greptile-apps` when body is just `<!-- greptile_other_comments_section -->` footer
   - Any comment whose body is entirely HTML attribution / CTA / badges with no prose claim (strip `<!-- ... -->` markers and "Fix with …" buttons before reading)

4. **Classify each remaining comment by staleness**:
   - **Fresh**: `commit_id === latest head SHA` — reviewer saw the current code
   - **Stale**: `commit_id !== latest head SHA` — may already be addressed. Don't reverify unless the user asks; mark as "Stale (last seen at `<sha[:7]>`)" and move on

5. **Verify each fresh, substantive comment**:
   - Use `Read` on the referenced file at its current state — **do NOT trust the reviewer's quoted diff**, because quoted snippets are often outdated after pushes
   - Cross-check any factual claim ("type X already exists in module Y", "pattern Z is used in other-file.ts") with `Grep` before accepting it
   - **Mentally apply the suggested fix** and verify types/callers/tests still pass. Bots frequently suggest fixes that fail type-check or break other callers — validating the suggestion is part of verification
   - Assign one verdict:
     - **Confirmed**: claim correct and the suggested fix works as-is
     - **Partial**: claim has merit but the suggested fix is wrong / incomplete — propose an adjusted fix
     - **Refuted**: claim is incorrect — explain why with code evidence
     - **Out-of-scope**: claim may be valid but exceeds the PR's intent (architectural refactor, missing tests, etc.) — defer to follow-up
     - **Stale**: already addressed (see step 4)

6. **Parallel verification**: run independent Read/Grep calls in parallel. Prefer direct tool calls to avoid burning context via agents.

7. **Report** — structured output:

   - **PR summary**: title, latest commit SHA, how many fresh / stale / noise comments
   - **Comment matrix** (one row per substantive comment):

     | # | Author | Location | Claim (short) | Verdict | Action |
     |---|--------|----------|---------------|---------|--------|
     | 1 | `claude[bot]` | `foo.ts:12` | "type is redundant" | Confirmed | inline `Pick<...>` |

   - **Per-comment detail** for each Confirmed / Partial entry: 2-3 line evidence + concrete fix draft (code snippet or file:line diff)
   - **Rejected / deferred comments**: one line each with the reason
   - **Recommended actions**: a concise list the user can act on:
     - changes to make (with file:line)
     - comments to reply-to-reject (with draft reply text if helpful)
     - bots to re-trigger (e.g. "tag `@cubic-dev-ai` — its last review is stale on `<sha>`")

### Rules

- **Always read the current file state**, not the reviewer's quoted diff — bots quote outdated code after a push.
- **Verify suggested fixes by simulation**: if a bot says "replace X with `ThreadListItemRuntime`", check whether call-sites still type-check with that change. If the suggestion is structurally wrong, mark **Partial** and propose a correct variant (e.g. `Pick<ThreadListItemRuntime, "foo">`).
- **Distinguish "Critical Issues" from "Suggestions"**: review bots often split their output. Critical issues deserve Confirmed/Refuted judgments; plain suggestions can be marked Out-of-scope with a one-line reason.
- **Human > bot**: if a human reviewer contradicts a bot, weight the human's intent and note the bot's disagreement in the report.
- **Stale comments**: mark and move on. Don't spend tokens re-verifying a claim about code that no longer exists.
- **Never modify files** during verification — this skill is read-only analysis. Fix work happens in a follow-up step.
- **Be concise**: evidence is `file:line` references, not code dumps. The matrix is the primary artifact.
- **Use the same language as the user's input** when reporting.
