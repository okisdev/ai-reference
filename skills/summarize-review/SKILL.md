---
name: summarize-review
description: Write a maintainer-style summary review of a GitHub PR (shortcomings, modifications, potential fixes) for the original author, run after review fixes are applied.
argument-hint: "[pr-number-or-url]"
---

## Context

Repository: !`gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null || echo "unknown"`
Default branch: !`git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@refs/remotes/origin/@@' || echo main`
Current branch: !`git branch --show-current 2>/dev/null`

## Instructions

Output the body for the user to confirm; do not post unless explicitly asked.

### Process

1. **Establish baseline and head** (`$ARGUMENTS` is a PR number, a full PR URL, or empty; if empty, infer the PR from the current branch via `gh pr view --json number,title,headRefName`):
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

6. **Identify potential further fixes**: real issues that remain or are deferred; each bullet states why (out of scope for this PR, upstream library limitation, low ROI, ergonomic taste). Be honest about partial fixes: if a modification is incomplete, list the remaining work here. Do not invent suggestions to pad.

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
