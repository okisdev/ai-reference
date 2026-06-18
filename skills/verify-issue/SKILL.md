---
name: verify-issue
description: Fetch a GitHub issue and verify its claims against the codebase with concrete evidence.
argument-hint: "<issue-number-or-url>"
---

## Context

Repository: !`gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null || echo "unknown"`
Default branch: !`git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@refs/remotes/origin/@@' || echo main`

## Instructions

Verify a GitHub issue against the current codebase. Execute immediately without asking.

Reading the code is the floor, not the ceiling. Match verification depth to what the conclusion rests on; escalate past reading when it hinges on runtime behavior, an environment difference, a third-party API's real shape, or a flaw in the issue's own reasoning. When verification surfaces a PR that already covers the issue, hand off to `/verify-pr` rather than re-deriving the fix here.

### Process

1. **Fetch issue**: Run `gh issue view $ISSUE_NUMBER --json title,body,labels,state,author,comments` (`$ARGUMENTS` is an issue number like `3766` or a full GitHub issue URL). Extract the title, body, every technical claim, and the issue's own proposed conclusion or fix.

2. **Decompose into claims, and find the load-bearing one**: Sort each claim into the bucket that determines how it's verified:
   - **Codebase claim**, about how a specific file, function, type, or behavior works. Verify by reading the code.
   - **Scope claim**, about what is or isn't handled anywhere in the project. Verify by full-repo search, not just the named file.
   - **External claim**, about web standards, ARIA specs, third-party library behavior, runtime APIs, or browser conventions. Verify against authoritative sources and judge how load-bearing the claim is.

   Then identify the **load-bearing claim**, the one the conclusion actually hinges on. The issue's own framing and reasoning (its "because X, option Y is safe") are claims to test, not premises to accept; verify that one deepest.

3. **Search for prior art** (parallel with step 5): Run `gh pr list --search "<keywords>" --state all` and `gh issue list --search "<keywords>" --state all` to surface duplicate issues, in-flight PRs, or already-merged fixes. Pull the diff and CI status of any exact match. Read the closing comment of any closed PR or closed duplicate issue: the reason a fix was abandoned, or a duplicate closed as wontfix, by-design, or not-planned, is often the real answer.

4. **Choose verification depth per claim**: escalate up this ladder per the intro's triggers; don't run the whole ladder on every claim, spend depth where the conclusion rests.
   - **L0 Read**: read the actual source. The default for codebase claims.
   - **L1 Search**: full-repo grep for scope claims; confirm the behavior isn't compensated for elsewhere (if the issue says "key X is unhandled in file Y", grep the whole repo for X). Note whether any test covers the path.
   - **L2 Reproduce**: for any claim about runtime behavior (a crash, a thrown error, wrong output, an environment-specific difference), run it, don't infer it. Write a minimal repro with the repo's own test runner, import the **real** code under test, and observe the actual result. Use the same repro to test the issue's **proposed fix's** premise, not just the bug. If a behavioral claim does not reproduce on current code, check `git log` / `git blame` for a fixing commit before concluding; 'already fixed in `<sha>`' is a distinct outcome from 'never valid', and the two warrant different responses to the issue.
   - **L3 Upstream**: for external, library, or runtime-API claims, verify against the canonical source, fetched via `gh` from the upstream repo (`gh api repos/<owner>/<repo>/contents/<path>?ref=<tag-or-sha>`, decode the base64), not the possibly-stale or transformed copy in `node_modules`. Check the version range that matters, not just `main`. Don't trust the issue's characterization of a third-party API, or your own memory of it.
   - **L4 Adversarial**: for the load-bearing claim and the issue's conclusion, try to **refute** it, not confirm it. Spell out what would have to be true for the conclusion to be wrong, then check each. When refutation spans many files or sources, dispatch independent agents in parallel (an `Explore` agent for upstream source, a separate refuter prompted to break the conclusion) so the check isn't anchored on your first read.

5. **Verify each claim** at the chosen depth, gathering concrete evidence (file paths, line numbers, exact snippets, observed repro output, upstream source refs). Run independent checks in parallel. Keep light verification (L0/L1) as direct `Read`/`Grep`/`Glob` to keep context tight; fan heavier work (L2 repro, L3 upstream, L4 refutation) out to agents when it spans many files or sources.

6. **Report** in this structure, in the same language as the user's input, noting version differences when a claim references a specific version:

   - **Issue summary**, one line on what the issue requests.
   - **Verification table**, one row per claim. Note the method when it went beyond reading:

     | # | Claim | Result | Evidence |
     |---|-------|--------|----------|
     | 1 | description | Confirmed / Refuted / Partial / Already fixed in `<sha>` | `file:line`, or "confirmed by repro", or "checked against <lib> source v0.79 to v0.86". Brief explanation. |

   - **Prior art**, related open, merged, or closed PRs and issues from step 3, with number, state, and a one-line summary (for a closed PR, why it was closed; for a closed duplicate issue, the close reason, such as wontfix, by-design, or not-planned).
   - **Conclusion**, whether the issue is valid. State which claim is load-bearing and how deeply it was verified. Call out any inaccurate framing in the issue body, especially reasoning the issue relied on that turned out wrong, even when the practical request still stands. If a duplicate was closed as wontfix, by-design, or not-planned, treat that as the maintainer already having ruled on this exact request and factor it into the validity call.
   - **Extra findings**, adjacent gaps surfaced during verification that aren't in the issue itself.
   - **Possible fix directions**, brief suggestions if the issue is valid and no covering PR exists. If a covering PR (open or closed) was found, recommend running `/verify-pr` on it instead of proposing a new fix, and note why a closed one was abandoned.
