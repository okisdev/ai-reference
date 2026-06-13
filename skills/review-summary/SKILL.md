---
name: review-summary
description: Write a maintainer-style summary review of a GitHub PR with three sections (shortcomings, modifications, potential fixes), framed for the original author rather than a recap of bot comments. Runs after review fixes have already been applied and is author-facing. Use when you need to summarize what the author got wrong, what got fixed, and what is left, not to judge whether a PR should merge (that is verify-pr) or to triage incoming review comments (that is verify-pr-comments).
argument-hint: "[pr-number-or-url]"
---

## Context

Repository: !`gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null || echo "unknown"`
Default branch: !`git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@refs/remotes/origin/@@' || echo main`
Current branch: !`git branch --show-current 2>/dev/null`

Runtimes that do not auto-run the commands above marked with `!` (Claude Code executes them and injects their output) should run each one to gather this context; treat any `$ARGUMENTS` or `$1` as the input the user provided.

## Instructions

Generate a maintainer summary review for a PR after fixes have been applied. The primary audience is the **original author**, not a recap of bot comments. Output the body for the user to confirm; do not post unless explicitly asked.

### Input

`$ARGUMENTS` is a PR number (e.g. `3841`), a full PR URL, or empty. If empty, infer the PR from the current branch via `gh pr view --json number,title,headRefName`.

### Process

1. **Establish baseline and head**:
   - Baseline `<first-sha>` (last commit in the PR author's leading run, the commit just before the first commit by a different author): `gh api repos/<o>/<r>/pulls/<n>/commits --paginate --jq '(.[0].author.login // .[0].commit.author.name) as $a | reduce .[] as $c ({run: true, sha: null}; if .run and (($c.author.login // $c.commit.author.name) == $a) then {run: true, sha: $c.sha} else {run: false, sha: .sha} end) | .sha'`. `.author.login` is null for unlinked-email commits, so fall back to `.commit.author.name` when reducing.
   - Latest head SHA: `gh api repos/<o>/<r>/pulls/<n> --jq .head.sha`
   - First commit's author is the review's audience: `gh api repos/<o>/<r>/pulls/<n>/commits --paginate --jq '.[0].author.login'`

2. **Read the original author's code** at the first PR commit: `git show <first-sha>:<path>` for each changed file. This is the implementation under review.

3. **Diff baseline against head** with `git diff <first-sha> <head-sha>`; this authoritative diff is the "what we modified" section. Read full files at HEAD via the `Read` tool only where you need surrounding context the diff alone does not show.

4. **Identify shortcomings** in the original implementation:
   - Bugs (data corruption, edge cases, off-by-one, race conditions).
   - Missing functionality (incomplete API surface, expected bindings absent).
   - Anti-patterns (redundant indirection, dead code, misleading names).
   - Performance or correctness gaps (Unicode, concurrency).
   - Style nits worth raising (multi-line block comments, inconsistent naming).
   - Cite `file:line` in the original commit when concrete.
   - **Frame each as direct critique of the code, not as "the bot said X".** Do not name the bots.

5. **Identify modifications** between original and current:
   - For each shortcoming above, what concrete change resolved it.
   - Pure additions (new tests, docs, helpers) also count.
   - Use present tense ("renames X to Y", "replaces array with Map", "adds Z binding").

6. **Identify potential further fixes**: real issues that remain or are deferred; each bullet states why (out of scope for this PR, upstream library limitation, low ROI, ergonomic taste). Do not invent suggestions to pad.

7. **Assemble the review body** in this layout:

   ```markdown
   ## review

   <one-line verdict, e.g. "LGTM as `patch`." or "looks good with the items below.">

   ### shortcomings of the original implementation
   - <bullet>
   - <bullet>

   ### what we modified
   - <bullet>
   - <bullet>

   ### potential further fixes
   - <bullet>
   - <bullet>
   ```

8. **Posting commands.** When asked to post, use one of:
   - `gh pr review <num> --approve --body "<text>"` for approval
   - `gh pr review <num> --comment --body "<text>"` for non-approving comment
   - `gh pr review <num> --request-changes --body "<text>"` for changes requested
   - To replace an existing review's body, first resolve the review id with `gh api repos/<o>/<r>/pulls/<n>/reviews --jq '.[] | select(.user.login=="<me>") | .id'` (take the latest match), then `gh api --method PUT repos/<o>/<r>/pulls/<n>/reviews/<review-id> -f body="<text>"`.

### Rules

- **Specific over vague.** Name concrete identifiers; replace "the code is unclear" with what specifically is unclear and where.
- **One sentence per bullet** is the target. Multi-clause only when the *why* is non-obvious.
- **Lowercase bullet text** except for proper nouns, code identifiers as they appear in source, and acronyms (`API`, `CSI-u`, `React`, `CJK`).
- **No em dashes or en dashes** in prose; use commas, parentheses, or sentence breaks. Hyphens inside compound words (`grapheme-aware`, `kebab-case`) are fine.
- **Be honest about partial fixes.** If a modification is incomplete, list the remaining work under "potential further fixes".
- **Skip empty sections.** Omit any section (shortcomings, modified, or fixes) with nothing to say; don't pad.
- **Match the user's language** for the conversational reply; the review body itself stays in English unless the user directs otherwise.
