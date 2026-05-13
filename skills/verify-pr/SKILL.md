---
name: verify-pr
description: Verify a GitHub PR against its stated goal and the surrounding codebase (correctness, tests, conventions, side effects). Produces a maintainer-ready verdict that separates blocking issues from optional polish.
argument-hint: "<pr-number-or-url>"
---

## Context

Repository: !`gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null || echo "unknown"`
Default branch: !`git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@refs/remotes/origin/@@' || echo main`
Current branch: !`git branch --show-current 2>/dev/null`

## Instructions

Verify a GitHub PR multi-dimensionally. Execute immediately without asking. This skill is claim-driven (does the PR achieve what it claims?) rather than opinion-driven, which is what distinguishes it from a generic review skill.

Distinct from siblings:
- **verify-issue**, validates an issue's claims against the codebase.
- **verify-pr-comments**, validates review comments on a PR against the actual code.
- Generic `/review`, opinion-driven feedback. This skill produces a focused verdict instead.

### Input

`$ARGUMENTS` is a PR number (e.g. `4020`) or a full GitHub PR URL.

### Process

1. **Fetch PR state**: `gh pr view <num> --json number,title,body,headRefName,baseRefName,mergeable,mergeStateStatus,statusCheckRollup,reviews,comments,additions,deletions,files`. Then `gh pr diff <num>` for the patch. Parse the body for linked issues (`Closes #X`, `Fixes #X`, bare `#XXXX` references).

2. **Fetch the linked issue** (if any) via `gh issue view <issue-num>`. Correctness is judged against what the issue actually requested, not just what the PR claims to do; the gap between the two is itself a finding.

3. **Pick verification dimensions** for this PR. Default set:
   - **Correctness**, does the diff fix what the linked issue or PR description describes?
   - **Test quality**, are new tests adequate, and do they match the repo's existing test patterns (mock style, helper conventions, naming)?
   - **Style and conventions**, changeset format, naming, file structure, lint rules, casual-register conventions for changeset wording.
   - **Side effects**, does the change interact safely with adjacent code paths (other plugins, IME composition, related event handlers, neighbouring modules)?
   
   Skip dimensions that don't apply (e.g. no tests added: surface that as its own finding instead of running the dimension).

4. **Dispatch parallel investigation** for any dimension that requires reading 3+ files. Use `Explore` agents in parallel:
   - One agent for test quality vs repo patterns: compare the new test file to other tests in the same area; identify mismatches and coverage gaps.
   - One agent for style and convention compliance: compare the changeset, code style, file structure to recent merged work in the repo.
   
   For correctness and side effects, direct `Read`/`Grep` is usually enough; do those yourself to keep the synthesis sharp.

5. **Treat CI status as data, not verdict**. A green CI proves nothing about correctness, only that no automated check failed. Always read the diff. A bot's "no issues found" is one data point, not absolution.

6. **Classify each finding** as one of:
   - **Blocking**, must fix before merge (broken correctness, failing tests, a convention break a maintainer would catch).
   - **Polish**, would improve the PR but a maintainer would not push back (style preference, wording cleanup).
   - **Pre-existing**, gap that already existed before the PR. Surface it but do NOT block; suggest a follow-up issue.

7. **Report** in this structure:

   - **PR summary**, number, title, head SHA, mergeable state, link to the linked issue if any.
   - **Per-dimension verdict table**:

     | Dimension | Verdict | One-line note |
     |-----------|---------|---------------|
     | Correctness | OK / minor / fail | |
     | Test quality | OK / minor / fail | |
     | Style / conventions | OK / minor / fail | |
     | Side effects | OK / minor / fail | |
     | CI | green / failing | |

   - **Findings**, one subsection per non-OK dimension, with `file:line` evidence and a concrete suggested fix or pushback. Label each item Blocking, Polish, or Pre-existing.
   - **Final recommendation**, exactly one of:
     - **Merge as-is**, every dimension OK and no Blocking items.
     - **Merge after small fixes**, list each Blocking item with `file:line` and the concrete change.
     - **Push back**, significant rework needed; explain why.
   - **Optional follow-ups**, bulleted Pre-existing gaps and Polish items the author can take or leave, plus any adjacent issues worth opening.

### Rules

- The PR's claim is what its body and diff say. The PR's actual effect is what the code does. The "correctness" finding is the delta between the two.
- Read the diff yourself. Most bugs that ship are not caught by lint or type checks.
- Test quality means matching the codebase's established patterns. It does NOT mean enforcing your favourite framework or asserting style preferences as gaps.
- Pre-existing coverage gaps are not this PR's problem. Suggest a follow-up, do not block.
- Be specific about what a maintainer would push back on. Soft "could be better" feedback belongs in optional follow-ups, not in Blocking findings.
- Use the same language as the user's input when reporting.
- This skill is read-only analysis. Do not modify files; fixes happen in a follow-up step or a separate skill invocation.
