---
name: verify-pr
description: Verify a GitHub PR against its stated goal and the surrounding codebase, judging whether it should exist at all before correctness, tests, conventions, and side effects.
argument-hint: "<pr-number-or-url> [--since <sha>]"
---

## Context

Repository: !`gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null || echo "unknown"`
Default branch: !`git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@refs/remotes/origin/@@' || echo main`
Current branch: !`git branch --show-current 2>/dev/null`

## Instructions

Verify a GitHub PR multi-dimensionally (claim-driven and necessity-driven, not opinion-driven like generic `/review`; for issue verification use `/verify-issue`, for comment triage use `/verify-pr-comments`). Execute immediately without asking. Judge two things, in order:

1. **Should this PR exist at all?** Necessity and authenticity: is the problem real, is the value already delivered elsewhere, does it duplicate existing code or another PR, and does its description honestly match what it ships? A flawless PR can still not warrant merging; necessity gates the verdict.
2. **Does it achieve what it claims?** Correctness, tests, conventions, side effects.

### Process

1. **Fetch PR state** (the leading positional of `$ARGUMENTS` is a PR number like `4020` or a full GitHub PR URL): `gh pr view <num> --json number,title,body,headRefName,baseRefName,headRefOid,mergeable,mergeStateStatus,statusCheckRollup,reviews,comments,additions,deletions,files`, then `gh pr diff <num>` for the patch. Parse the body for linked issues (`Closes #X`, `Fixes #X`, bare `#XXXX` references). Keep `headRefOid`: the report ends with it, so a later pass can scope itself to whatever lands after this one.

   **Incremental re-verification** (`--since <sha>`): a PR under review is re-read every time its author pushes, and re-analyzing the whole patch each round costs enough that the re-read quietly gets skipped, which is the failure this exists to prevent. Given `--since <sha>`, the step 4 dimensions judge `git diff <sha>..<head>` (with `git log --oneline <sha>..<head>` for what landed) instead of the full patch, while the full-PR state from this step still loads as context. Necessity stays judged against the whole PR and is never re-derived from the delta, since a clean delta can still belong to a PR that should not exist. Confirm `<sha>` is an ancestor of the head (`git merge-base --is-ancestor <sha> <head>`); if it is not, a force-push rewrote the range, so say so and fall back to the full patch rather than reporting on a diff that does not mean what it claims.

2. **Fetch the linked issue** (if any) via `gh issue view <issue-num>`. Judge correctness against what the issue actually requested, not just what the PR claims; the gap is itself a finding. Overpromising, a `Closes #X` that only partially delivers, is itself a necessity finding; see Rules.

3. **Search for duplication and prior art** (early, in parallel with reading the diff) to find out whether the PR is needed at all:
   - `gh pr list --search "<keywords>" --state all` and `gh issue list --search "<keywords>" --state all` for competing open PRs, an already-merged fix that supersedes this one, or a duplicate issue. A closed PR is as informative as an open one: read its closing comment, since why an approach was abandoned is often why this PR should not take the same path.
   - Grep the codebase for the feature or function the PR adds: does equivalent functionality already exist that the PR should reuse rather than re-implement?
   - Note any external or ecosystem artifact the PR may be reinventing (published package, sibling repo, existing CLI command, hosted service). Verify a load-bearing claim about a third-party API by composing `read-source` rather than trusting docs or memory.

4. **Pick verification dimensions**, evaluated in this order:
   - **Necessity and justification** (gating), should this PR exist? Check: (a) the problem is real and not already solved in the codebase; (b) it does not duplicate an existing, in-flight, or already-merged PR; (c) it does not re-implement functionality that already exists in the repo or an ecosystem artifact it should reuse (per step 3); (d) the linked issue's actual ask is met and not overpromised; (e) the value justifies the added code and its long-term maintenance surface.
   - **Correctness**, does the diff fix what the issue or description describes? When the fix targets runtime behavior (a crash, thrown error, wrong output, environment difference), prove it: `git worktree add ../verify-<num> && cd ../verify-<num> && gh pr checkout <num>`, run the repro or the PR's added tests against the real code to confirm the bug is gone, then remove the worktree. For a UI-facing PR, render evidence composes `verify-ui`; a diff that reads right can still render wrong. A diff that looks correct but does not resolve the bug is the failure this catches.
   - **Test quality**, are new tests adequate and matched to the repo's existing patterns (mock style, helper conventions, naming)?
   - **Conventions and paradigm conformance**, does the change match how this codebase already does things? Judge each changed surface against its nearest in-repo precedent (the sibling hook, test, doc example, or type), not against generic best practice or your taste: changeset format, naming, export placement, file structure, lint rules, and the area's architectural patterns (state access, memoization, guards, module boundaries). A choice that mirrors an existing sibling conforms even when you would write it differently; a difference is a deviation only when you can cite the established pattern it breaks.
   - **Side effects**, does the change interact safely with adjacent code paths (other plugins, IME composition, related event handlers, neighbouring modules)?

   Skip dimensions that don't apply (no tests added: surface that as its own finding instead of running the dimension). Never skip Necessity.

5. **Dispatch parallel investigation** for any dimension requiring 3+ files. Use `Explore` agents in parallel:
   - Necessity: search open and merged PRs and issues for overlap, and the codebase and ecosystem for functionality the PR duplicates or should reuse.
   - Test quality vs repo patterns: compare the new test file to other tests in the same area; identify mismatches and coverage gaps.
   - Conventions and paradigm conformance: map each changed surface to its nearest in-repo precedent (sibling hook, test, doc example, type) and compare against THAT, citing paired `file:line` for the change and the pattern it breaks. Add a completeness-critic pass that re-checks each flagged deviation against the shipped code, since diff-summary pattern-matching both misses idioms and invents deviations.

   For correctness and side effects, use direct `Read`/`Grep`.

6. **Treat CI and review state as data, not verdict**. Green CI proves nothing about correctness, only that no automated check failed; always read the diff. A bot's "no issues found" is one data point, not absolution, and CI says nothing about necessity. Pending checks and unposted reviews are operational blockers until they settle; a completed bot review is data for `/verify-pr-comments`, not a skip. A human's `CHANGES_REQUESTED` and an unresolved review thread remain blockers even when every quality dimension is OK. Surface these; a clean quality read does not mean the PR is mergeable right now.

7. **Classify each finding**:
   - **Blocking**, must fix before merge; for necessity, a reason not to merge at all (redundant with existing code, duplicates another PR, premise does not hold, overpromised closure).
   - **Polish**, would improve the PR but a maintainer would not push back (style preference, wording cleanup).
   - **Pre-existing**, gap that predates the PR. Surface it but do NOT block; suggest a follow-up issue.

8. **Report** in this structure:

   - **PR summary**, number, title, head SHA, mergeable state, link to the linked issue if any. Name the scope judged: the whole patch, or `<sha>..<head>` when `--since` narrowed it.
   - **Per-dimension verdict table**:

     | Dimension | Verdict | One-line note |
     |-----------|---------|---------------|
     | Necessity | OK / minor / fail | fail = redundant or unjustified |
     | Correctness | OK / minor / fail | |
     | Test quality | OK / minor / fail | |
     | Conventions / paradigm | OK / minor / fail | deviation must cite the in-repo pattern it breaks |
     | Side effects | OK / minor / fail | |
     | CI | green / failing | |

   - **Findings**, one subsection per non-OK dimension, with `file:line` (or PR, issue, repo) evidence and a concrete suggested fix, pushback, or redirect. Label each Blocking, Polish, or Pre-existing.
   - **Final recommendation**, exactly one of:
     - **Close or redirect**, the PR is redundant or unjustified: its goal is already met, or better met, by existing code, a published package, a sibling repo, or another PR. Name what covers it, and call out the one genuinely novel slice (if any) worth salvaging as a smaller follow-up.
     - **Merge as-is**, necessity holds and every other dimension is OK with no Blocking items.
     - **Merge after small fixes**, necessity holds; list each Blocking item with `file:line` and the concrete change.
     - **Push back**, necessity holds but the implementation needs significant rework; explain why.
   - **Merge readiness**, separate from the quality verdict: note any operational blocker that still gates the actual merge even when the recommendation is Merge as-is, namely a pending check or unposted review, a human's `CHANGES_REQUESTED`, or unresolved review threads (step 6). Point to `/verify-pr-comments` for working through the threads.
   - **Optional follow-ups**, bulleted Pre-existing gaps and Polish items the author can take or leave, plus any adjacent issues worth opening.
   - **Verified head**, the `headRefOid` this pass judged, given as the `--since` value the next pass should use. The recommendation above is good for that SHA and no other.

### Rules

- Redundancy is a Blocking-level necessity finding, not a polish note.
- A recommendation binds to the head SHA it was computed on. Commits pushed after it are unverified however small they look, and green CI on them substitutes for nothing, since CI proves the tree builds and says nothing about the dimensions in step 4; re-run with `--since <that sha>`.
- An inaccurate `Closes #X` (scope, files, or behavior the diff does not ship) is a finding even when the shipped code works.
- This skill is read-only analysis; do not modify files (fixes happen in a follow-up step or a separate skill invocation). The one exception is step 4's throwaway repro worktree: check out the PR, run it against the real code, then remove the worktree. Never commit, never push to the PR.
- Use the same language as the user's input when reporting.
