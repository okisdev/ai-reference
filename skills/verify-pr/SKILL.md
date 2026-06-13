---
name: verify-pr
description: Verify a GitHub PR against its stated goal and the surrounding codebase. Judges first whether the PR should exist at all (necessity, redundancy, honest scope), then correctness, tests, conventions, and side effects. Produces a maintainer-ready verdict that can recommend closing a technically-clean but redundant PR, and separates blocking issues from optional polish.
argument-hint: "<pr-number-or-url>"
---

## Context

Repository: !`gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null || echo "unknown"`
Default branch: !`git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@refs/remotes/origin/@@' || echo main`
Current branch: !`git branch --show-current 2>/dev/null`

Runtimes that do not auto-run the commands above marked with `!` (Claude Code executes them and injects their output) should run each one to gather this context; treat any `$ARGUMENTS` or `$1` as the input the user provided.

## Instructions

Verify a GitHub PR multi-dimensionally. Execute immediately without asking.

This skill judges two things, in order:

1. **Should this PR exist at all?** Necessity and authenticity: is the problem real, is the value already delivered elsewhere, does it duplicate existing code or another PR, and does its description honestly match what it ships? A flawless PR can still not warrant merging.
2. **Does it achieve what it claims?** Correctness, tests, conventions, side effects.

Claim-driven and necessity-driven, not opinion-driven; that distinguishes it from a generic review skill. A clean technical report does NOT imply the PR should merge; necessity gates the verdict.

Distinct from siblings:
- **verify-issue**, validates an issue's claims against the codebase.
- **verify-pr-comments**, validates review comments on a PR against the actual code.
- Generic `/review`, opinion-driven feedback. This skill produces a focused verdict instead.

### Input

`$ARGUMENTS` is a PR number (e.g. `4020`) or a full GitHub PR URL.

### Process

1. **Fetch PR state**: `gh pr view <num> --json number,title,body,headRefName,baseRefName,mergeable,mergeStateStatus,statusCheckRollup,reviews,comments,additions,deletions,files`, then `gh pr diff <num>` for the patch. Parse the body for linked issues (`Closes #X`, `Fixes #X`, bare `#XXXX` references).

2. **Fetch the linked issue** (if any) via `gh issue view <issue-num>`. Judge correctness against what the issue actually requested, not just what the PR claims; the gap is itself a finding. Overpromising, a `Closes #X` that only partially delivers, is itself a necessity finding; see Rules.

3. **Search for duplication and prior art** (early, in parallel with reading the diff) to find out whether the PR is needed at all:
   - `gh pr list --search "<keywords>" --state all` and `gh issue list --search "<keywords>" --state all` for competing open PRs, an already-merged fix that supersedes this one, or a duplicate issue. A **closed** PR is as informative as an open one: read its closing comment, since an approach abandoned because it broke another consumer is often why this PR should not take the same path.
   - Grep the codebase for the feature or function the PR adds: does equivalent functionality already exist that the PR should reuse rather than re-implement?
   - Note any external or ecosystem artifact the PR may be reinventing (published package, sibling repo, existing CLI command, hosted service). If the same outcome is reachable by reusing one, the new code is redundant.

   Skipping this step is the most common way a "merge as-is" verdict turns out wrong.

4. **Pick verification dimensions**, evaluated in this order:
   - **Necessity and justification** (gating), should this PR exist? Check: (a) the problem is real and not already solved in the codebase; (b) it does not duplicate an existing, in-flight, or already-merged PR; (c) it does not re-implement functionality that already exists in the repo or an ecosystem artifact it should reuse (per step 3); (d) the linked issue's actual ask is met and not overpromised; (e) the value justifies the added code and its long-term maintenance surface. A PR can pass every other dimension and still fail here.
   - **Correctness**, does the diff fix what the issue or description describes? Reading that the code looks right is the floor. When the fix targets runtime behavior (a crash, thrown error, wrong output, environment difference), prove it: `git worktree add ../verify-<num> && cd ../verify-<num> && gh pr checkout <num>`, run the repro or the PR's added tests against the real code to confirm the bug is gone, then remove the worktree. A diff that looks correct but does not resolve the bug is the failure this catches.
   - **Test quality**, are new tests adequate and matched to the repo's existing patterns (mock style, helper conventions, naming)?
   - **Style and conventions**, changeset format, naming, file structure, lint rules, casual-register changeset wording.
   - **Side effects**, does the change interact safely with adjacent code paths (other plugins, IME composition, related event handlers, neighbouring modules)?

   Skip dimensions that don't apply (no tests added: surface that as its own finding instead of running the dimension). Never skip Necessity.

5. **Dispatch parallel investigation** for any dimension requiring 3+ files. Use `Explore` agents in parallel:
   - Necessity: search open and merged PRs and issues for overlap, and the codebase and ecosystem for functionality the PR duplicates or should reuse.
   - Test quality vs repo patterns: compare the new test file to other tests in the same area; identify mismatches and coverage gaps.
   - Style and convention compliance: compare the changeset, code style, file structure to recent merged work.

   For correctness and side effects, direct `Read`/`Grep` is usually enough; do those yourself to keep the synthesis sharp.

6. **Treat CI and review state as data, not verdict**. Green CI proves nothing about correctness, only that no automated check failed; always read the diff. A bot's "no issues found" is one data point, not absolution, and CI says nothing about necessity. Separate **gating** signals from **advisory** ones: some checks and reviewers (often an AI review bot) are configured non-blocking and must not be treated as merge blockers, while a human's `CHANGES_REQUESTED` and an unresolved review thread are real operational blockers even when every quality dimension is OK. Surface these; a clean quality read does not mean the PR is mergeable right now.

7. **Classify each finding**:
   - **Blocking**, must fix before merge; for necessity, a reason not to merge at all (redundant with existing code, duplicates another PR, premise does not hold, overpromised closure).
   - **Polish**, would improve the PR but a maintainer would not push back (style preference, wording cleanup).
   - **Pre-existing**, gap that predates the PR. Surface it but do NOT block; suggest a follow-up issue.

8. **Report** in this structure:

   - **PR summary**, number, title, head SHA, mergeable state, link to the linked issue if any.
   - **Per-dimension verdict table**:

     | Dimension | Verdict | One-line note |
     |-----------|---------|---------------|
     | Necessity | OK / minor / fail | fail = redundant or unjustified |
     | Correctness | OK / minor / fail | |
     | Test quality | OK / minor / fail | |
     | Style / conventions | OK / minor / fail | |
     | Side effects | OK / minor / fail | |
     | CI | green / failing | |

   - **Findings**, one subsection per non-OK dimension, with `file:line` (or PR, issue, repo) evidence and a concrete suggested fix, pushback, or redirect. Label each Blocking, Polish, or Pre-existing.
   - **Final recommendation**, exactly one of:
     - **Close or redirect**, the PR is redundant or unjustified: its goal is already met, or better met, by existing code, a published package, a sibling repo, or another PR. Name what covers it, and call out the one genuinely novel slice (if any) worth salvaging as a smaller follow-up.
     - **Merge as-is**, necessity holds and every other dimension is OK with no Blocking items.
     - **Merge after small fixes**, necessity holds; list each Blocking item with `file:line` and the concrete change.
     - **Push back**, necessity holds but the implementation needs significant rework; explain why.
   - **Merge readiness**, separate from the quality verdict: note any operational blocker that still gates the actual merge even when the recommendation is Merge as-is, namely a gating reviewer's `CHANGES_REQUESTED` or unresolved review threads (gating vs advisory per step 6). Point to `/verify-pr-comments` for working through the threads.
   - **Optional follow-ups**, bulleted Pre-existing gaps and Polish items the author can take or leave, plus any adjacent issues worth opening.

### Rules

- Distinguish the problem being real from the implementation being correct: a correct, well-tested implementation of an unneeded change is still a close.
- Redundancy is a Blocking-level necessity finding, not a polish note.
- The "correctness" finding is the delta between the PR's claim (body + diff) and its actual effect (what the code does); an inaccurate `Closes #X` (overpromised scope, or files or behavior the diff does not ship) is a finding even when the shipped code works.
- Read the diff yourself; most shipped bugs are not caught by lint or type checks.
- Test quality means matching the codebase's established patterns, not enforcing your favourite framework or asserting style preferences as gaps.
- Be specific about what a maintainer would push back on; soft "could be better" feedback belongs in optional follow-ups, not Blocking findings.
- Be concise: evidence is `file:line` references and observed results, not full code dumps; the verdict table and final recommendation are the primary artifacts.
- Use the same language as the user's input when reporting.
- This skill is read-only analysis; do not modify files (fixes happen in a follow-up step or a separate skill invocation). The one exception is step 4's throwaway repro worktree: check out the PR, run it against the real code, then remove the worktree. Never commit, never push to the PR.
