---
name: verify-pr
description: Verify a GitHub PR against its stated goal and the surrounding codebase. Judges first whether the PR should exist at all (necessity, redundancy, honest scope), then correctness, tests, conventions, and side effects. Produces a maintainer-ready verdict that can recommend closing a technically-clean but redundant PR, and separates blocking issues from optional polish.
argument-hint: "<pr-number-or-url>"
---

## Context

Repository: !`gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null || echo "unknown"`
Default branch: !`git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@refs/remotes/origin/@@' || echo main`
Current branch: !`git branch --show-current 2>/dev/null`

## Instructions

Verify a GitHub PR multi-dimensionally. Execute immediately without asking.

This skill judges two separate things, in order:

1. **Should this PR exist at all?** Necessity and authenticity: is the problem real, is the value already delivered elsewhere, does it duplicate existing code or another PR, and does its description honestly match what it ships? A PR can be flawless and still not warrant merging.
2. **Does it achieve what it claims?** Correctness, tests, conventions, side effects.

It is claim-driven and necessity-driven, not opinion-driven, which is what distinguishes it from a generic review skill. A clean bill of health on the technical dimensions does NOT imply the PR should merge; necessity is evaluated first and gates the verdict.

Distinct from siblings:
- **verify-issue**, validates an issue's claims against the codebase.
- **verify-pr-comments**, validates review comments on a PR against the actual code.
- Generic `/review`, opinion-driven feedback. This skill produces a focused verdict instead.

### Input

`$ARGUMENTS` is a PR number (e.g. `4020`) or a full GitHub PR URL.

### Process

1. **Fetch PR state**: `gh pr view <num> --json number,title,body,headRefName,baseRefName,mergeable,mergeStateStatus,statusCheckRollup,reviews,comments,additions,deletions,files`. Then `gh pr diff <num>` for the patch. Parse the body for linked issues (`Closes #X`, `Fixes #X`, bare `#XXXX` references).

2. **Fetch the linked issue** (if any) via `gh issue view <issue-num>`. Correctness is judged against what the issue actually requested, not just what the PR claims to do; the gap between the two is itself a finding. Note whether the PR overpromises: a `Closes #X` that only partially delivers, or that describes files or behavior the diff does not actually ship, is a necessity and authenticity finding.

3. **Search for duplication and prior art** (do this early, in parallel with reading the diff). The point is to find out whether the PR is needed at all:
   - `gh pr list --search "<keywords>" --state all` and `gh issue list --search "<keywords>" --state all` for competing open PRs, an already-merged fix that supersedes this one, or a duplicate issue.
   - Grep the codebase for the feature or function the PR adds: does equivalent functionality already exist that the PR should reuse rather than re-implement?
   - Note any external or ecosystem artifact the PR may be reinventing: a published package, a sibling repo, an existing CLI command, a hosted service. If the same outcome is reachable by reusing one of these, the new code is redundant.
   
   Skipping this step is the most common way a "merge as-is" verdict turns out to be wrong.

4. **Pick verification dimensions** for this PR. Default set, evaluated in this order:
   - **Necessity and justification** (gating), should this PR exist? Check: (a) the problem is real and not already solved in the codebase; (b) it does not duplicate an existing, in-flight, or already-merged PR; (c) it does not fork or re-implement functionality that already lives in the repo, a published package, or a sibling repo it should reuse instead; (d) the linked issue's actual ask is met and not overpromised; (e) the value justifies the added code and its long-term maintenance surface. A PR can pass every other dimension and still fail here; a technically-clean but redundant PR is a close, not a merge.
   - **Correctness**, does the diff fix what the linked issue or PR description describes?
   - **Test quality**, are new tests adequate, and do they match the repo's existing test patterns (mock style, helper conventions, naming)?
   - **Style and conventions**, changeset format, naming, file structure, lint rules, casual-register conventions for changeset wording.
   - **Side effects**, does the change interact safely with adjacent code paths (other plugins, IME composition, related event handlers, neighbouring modules)?
   
   Skip dimensions that don't apply (e.g. no tests added: surface that as its own finding instead of running the dimension). Never skip Necessity.

5. **Dispatch parallel investigation** for any dimension that requires reading 3+ files. Use `Explore` agents in parallel:
   - One agent for necessity: search open and merged PRs and issues for overlap, and the codebase and ecosystem for existing functionality the PR duplicates or should reuse.
   - One agent for test quality vs repo patterns: compare the new test file to other tests in the same area; identify mismatches and coverage gaps.
   - One agent for style and convention compliance: compare the changeset, code style, file structure to recent merged work in the repo.
   
   For correctness and side effects, direct `Read`/`Grep` is usually enough; do those yourself to keep the synthesis sharp.

6. **Treat CI status as data, not verdict**. A green CI proves nothing about correctness, only that no automated check failed. Always read the diff. A bot's "no issues found" is one data point, not absolution. CI says nothing at all about necessity.

7. **Classify each finding** as one of:
   - **Blocking**, must fix before merge, or, for necessity, a reason not to merge at all (redundant with existing code, duplicates another PR, premise does not hold, overpromised closure).
   - **Polish**, would improve the PR but a maintainer would not push back (style preference, wording cleanup).
   - **Pre-existing**, gap that already existed before the PR. Surface it but do NOT block; suggest a follow-up issue.

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

   - **Findings**, one subsection per non-OK dimension, with `file:line` (or PR, issue, repo) evidence and a concrete suggested fix, pushback, or redirect. Label each item Blocking, Polish, or Pre-existing.
   - **Final recommendation**, exactly one of:
     - **Close or redirect**, the PR is redundant or unjustified: its goal is already met, or better met, by existing code, a published package, a sibling repo, or another PR. Name what covers it, and call out the one genuinely novel slice (if any) worth salvaging as a smaller follow-up.
     - **Merge as-is**, necessity holds and every other dimension is OK with no Blocking items.
     - **Merge after small fixes**, necessity holds; list each Blocking item with `file:line` and the concrete change.
     - **Push back**, necessity holds but the implementation needs significant rework; explain why.
   - **Optional follow-ups**, bulleted Pre-existing gaps and Polish items the author can take or leave, plus any adjacent issues worth opening.

### Rules

- Evaluate necessity first. A clean correctness, test, style, and side-effect report does NOT mean the PR should merge; if the PR is redundant or its premise does not hold, the technical dimensions are moot and the verdict is Close or redirect.
- Distinguish the problem being real from the implementation being correct. A correct, well-tested implementation of an unneeded change is still a close.
- Search for duplication before judging. An already-merged fix, a competing open PR, existing repo functionality, or a published package or sibling repo the PR reinvents all make it redundant. Redundancy is a Blocking-level necessity finding, not a polish note.
- The PR's claim is what its body and diff say. The PR's actual effect is what the code does. The "correctness" finding is the delta between the two; an inaccurate `Closes #X` (overpromised scope, or files or behavior the diff does not ship) is a finding even when the shipped code works.
- Read the diff yourself. Most bugs that ship are not caught by lint or type checks.
- Test quality means matching the codebase's established patterns. It does NOT mean enforcing your favourite framework or asserting style preferences as gaps.
- Pre-existing coverage gaps are not this PR's problem. Suggest a follow-up, do not block.
- Be specific about what a maintainer would push back on. Soft "could be better" feedback belongs in optional follow-ups, not in Blocking findings.
- Use the same language as the user's input when reporting.
- This skill is read-only analysis. Do not modify files; fixes happen in a follow-up step or a separate skill invocation.
