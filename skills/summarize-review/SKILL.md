---
name: summarize-review
description: Write a maintainer-style summary review of a GitHub PR for the original author, run after review fixes are applied.
argument-hint: "[pr-number-or-url]"
---

## Context

Repository: !`gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null || echo "unknown"`
Default branch: !`out=$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@refs/remotes/origin/@@'); echo "${out:-main}"`
Current branch: !`git branch --show-current 2>/dev/null || echo "(not a git repository)"`

## Instructions

**The one rule: say only what the diff cannot.** The body is a message from a maintainer to the author: the verdict and the one reason it holds, then the judgment the patch does not show (why this approach beat the one it displaced, what you ran and what it printed, the trap the next reader falls into), in prose. Open the closer of [examples/clean.md](examples/clean.md) and [examples/blocking.md](examples/blocking.md) before writing, and check the draft against [examples/rejected.md](examples/rejected.md).

Output the body for the user to confirm; do not post unless explicitly asked. When `approve-pr` or `ship-pr` invoked this skill, return the body to that caller to post without asking for confirmation (seen: a body held for confirmation inside a ship run, and the user saying to post it with the approval).

### Process

1. **Establish baseline and head** (`$ARGUMENTS` is a PR number, a full PR URL, or empty; if empty, infer the PR from the current branch via `gh pr view --json number,title,headRefName`):
   - Baseline `<baseline-sha>` (last commit in the PR author's leading run): `gh api repos/<o>/<r>/pulls/<n>/commits --paginate --jq '(.[0].author.login // .[0].commit.author.name) as $a | reduce .[] as $c ({run: true, sha: null}; if .run and (($c.author.login // $c.commit.author.name) == $a) then {run: true, sha: $c.sha} else {run: false, sha: .sha} end) | .sha'`. `.author.login` is null for unlinked-email commits, so fall back to `.commit.author.name` when reducing. When a rebase or reset rewrote the branch so every commit shows the author, the leading run is the whole PR; take as baseline the head recorded before your first push instead (seen: five commits all attributed to the contributor while the run claimed its own commits were on the PR).
   - Latest head SHA: `gh api repos/<o>/<r>/pulls/<n> --jq .head.sha`
   - First commit's author is the review's audience: `gh api repos/<o>/<r>/pulls/<n>/commits --paginate --jq '.[0].author.login'`

2. **Read the original author's final baseline**, the code as their last commit in the leading run left it: `git show <baseline-sha>:<path>` for each changed file.

3. **Diff baseline against head** with `git diff <baseline-sha> <head-sha>`; this authoritative diff is what you changed. Read full files at HEAD via the `Read` tool only where you need surrounding context the diff alone does not show.

4. **Identify shortcomings** in the original implementation:
   - Bugs (data corruption, edge cases, off-by-one, race conditions).
   - Missing functionality (incomplete API surface, expected bindings absent).
   - Anti-patterns (redundant indirection, dead code, misleading names).
   - Performance or correctness gaps (Unicode, concurrency).
   - Style nits worth raising (multi-line block comments, inconsistent naming).
   - Cite `file:line` in the baseline when concrete.
   - **Frame each as direct critique of the code, not as "the bot said X".** Do not name the bots.

5. **Identify modifications** between original and current:
   - For each shortcoming above, what concrete change resolved it.
   - Pure additions (new tests, docs, helpers) also count.
   - Use present tense ("renames X to Y", "replaces array with Map", "adds Z binding").

6. **Identify potential further fixes**: real issues that remain or are deferred; each bullet states why (out of scope for this PR, upstream library limitation, low ROI, ergonomic taste). Be honest about partial fixes: if a modification is incomplete, list the remaining work here. Do not invent suggestions to pad.

7. **Write it as a message to the author**, not a report for the record. Open with the verdict and the one reason it holds, then say the things the diff cannot say for itself: why this approach beat the one it displaced, what you ran and what it printed, the trap the next reader falls into. Stop there.

   Cut anything the diff already shows. A line narrating a change the author made and the reader can see is the padding this format exists to avoid, and steps 4 to 6 are an order to think in, never sections to emit (seen: 75 of 79 bodies came out in one rigid three-part template). A review earns its length only through judgment that is not visible in the patch.

   Prose, no headings, and no `## review` line: GitHub labels the state, so a heading spends the opening saying nothing. Reach for structure only when the author has several separable things to act on, and then number them so each can be replied to on its own. Length tracks what the author has to do, so a clean approval is a paragraph or two while blocking feedback earns whatever its items need.

   Name the evidence for a load-bearing claim inline as you make it, separating what you executed from what you read: quote the command and its real output for the first, say plainly that the second is a reading. A claim about runtime behavior that was only read is a suspicion, not a finding. Where an obvious cheaper check would report the opposite, say so, since the next person reaches for it otherwise.

   No trace of tooling in the body: no generated-by line, no session link, no `Co-Authored-By` trailer naming a coding tool (seen: tool trailers and session links the user had to strip from merged PRs).

8. **Posting commands.** This skill drafts the body; for the full maintainer approve flow (the should-approve gate, the self-approval guard, and anti-stacking) use `/approve-pr`. When asked to post this body directly, pass it via `--body-file -` with a quoted heredoc so backticks and code survive (`-b/--body "..."` mangles them), with one of:
   - `gh pr review <num> --approve --body-file - <<'EOF'` ... `EOF` for approval
   - `--comment` for a non-approving comment, `--request-changes` for changes requested (same `--body-file -` form)
   - To replace your existing review's body, resolve its id with `gh api --paginate --slurp repos/<o>/<r>/pulls/<n>/reviews | jq '[.[][] | select(.user.login=="<me>")] | last | .id'`, then `gh api --method PUT repos/<o>/<r>/pulls/<n>/reviews/<review-id> -f body="<text>"`; PUT edits the body text only, never the review state.
