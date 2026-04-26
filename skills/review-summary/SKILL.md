---
name: review-summary
description: Write a maintainer-style summary review of a GitHub PR with three sections (shortcomings, modifications, potential fixes), framed for the original author rather than a recap of bot comments.
argument-hint: "[pr-number-or-url]"
---

## Context

Repository: !`gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null || echo "unknown"`
Default branch: !`git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@refs/remotes/origin/@@' || echo main`
Current branch: !`git branch --show-current 2>/dev/null`

## Instructions

Generate a maintainer summary review for a PR after fixes have been applied. The review's primary audience is the **original author**, not a recap of bot comments. Output the body for the user to confirm; do NOT post unless explicitly asked.

### Input

`$ARGUMENTS` is a PR number (e.g. `3841`), a full PR URL, or empty. If empty, infer the PR from the current branch via `gh pr view --json number,title,headRefName`.

### Process

1. **Establish baseline and head**:
   - First commit on the PR (original author's work):
     `gh api repos/<o>/<r>/pulls/<n>/commits --paginate --jq '.[0].sha'`
   - Latest head SHA:
     `gh api repos/<o>/<r>/pulls/<n> --jq .head.sha`
   - The author of the first commit is the review's audience (`gh api repos/<o>/<r>/pulls/<n>/commits --paginate --jq '.[0].author.login'`).

2. **Read the original author's code** at the first PR commit: `git show <first-sha>:<path>` for each changed file. This is the implementation being reviewed.

3. **Read the current code** at HEAD via the standard `Read` tool. The diff between original and current is the "what we modified" section.

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

6. **Identify potential further fixes**:
   - Real issues that remain or are deferred. Each bullet states why (out of scope for this PR, upstream library limitation, low ROI, ergonomic taste).
   - Do not invent suggestions to pad the section. If nothing remains, omit the section entirely.

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

8. **Output the review body**. Do not post unless the user says "post" / "send" / "approve". When asked to post, use one of:
   - `gh pr review <num> --approve --body "<text>"` for approval
   - `gh pr review <num> --comment --body "<text>"` for non-approving comment
   - `gh pr review <num> --request-changes --body "<text>"` for changes requested
   - To replace an existing review's body: `gh api --method PUT repos/<o>/<r>/pulls/<n>/reviews/<review-id> -f body="<text>"`.

### Rules

- **Audience is the original author.** Frame each shortcoming as direct critique of the code, not as a summary of automated review output.
- **Specific over vague.** Cite `file:line` and concrete identifiers. Replace "the code is unclear" with what specifically is unclear and where.
- **No bot recap.** Do not list which bot found which issue. The author cares about the issue, not the source.
- **One sentence per bullet** is the target. Multi-clause only when the *why* is non-obvious.
- **Lowercase bullet text** except for proper nouns, code identifiers as they appear in source, and acronyms (`API`, `CSI-u`, `React`, `CJK`).
- **No em dashes or en dashes** in prose — use commas, parentheses, or sentence breaks. Hyphens inside compound words (`grapheme-aware`, `kebab-case`) are fine.
- **Be honest about partial fixes.** If a modification is incomplete, also list the remaining work under "potential further fixes".
- **Skip empty sections.** If everything in the original was sound (no shortcomings) or nothing was modified, omit that section. Don't pad.
- **Don't post unprompted.** Always output the body for the user to confirm first.
- **Match the user's language** for the conversational reply (the review body itself stays in English, per typical GitHub conventions, unless the user directs otherwise).
