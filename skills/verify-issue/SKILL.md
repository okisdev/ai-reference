---
name: verify-issue
description: Fetch a GitHub issue and verify its claims against the codebase with concrete evidence. Escalates past surface code reading when the conclusion warrants it, running repros, checking upstream source, and adversarially testing the load-bearing claim.
argument-hint: "<issue-number-or-url>"
---

## Context

Repository: !`gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null || echo "unknown"`
Default branch: !`git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@refs/remotes/origin/@@' || echo main`

## Instructions

Verify a GitHub issue against the current codebase. Execute immediately without asking.

Reading the code is the floor, not the ceiling. A confident report that only confirms what the source appears to say is worthless when the issue's conclusion hinges on a behavior the source doesn't reveal (a runtime crash, an environment difference, a third-party API's actual shape) or on a piece of the issue's own reasoning that happens to be wrong. Match verification depth to what the conclusion actually rests on.

### Input

`$ARGUMENTS` is an issue number (e.g. `3766`) or a full GitHub issue URL (e.g. `https://github.com/owner/repo/issues/3766`).

### Process

1. **Fetch issue**: Use `github-repos` MCP (`get_issue`) if available, otherwise `gh issue view $ISSUE_NUMBER --json title,body,labels,state,author,comments`. Extract the title, body, every technical claim, and the issue's own proposed conclusion or fix.

2. **Decompose into claims, and find the load-bearing one**: Sort each claim into the bucket that determines how it's verified:
   - **Codebase claim**, about how a specific file, function, type, or behavior works. Verify by reading the code.
   - **Scope claim**, about what is or isn't handled anywhere in the project. Verify by full-repo search, not just the named file.
   - **External claim**, about web standards, ARIA specs, third-party library behavior, runtime APIs, or browser conventions. Verify against authoritative sources and judge how load-bearing the claim is.
   
   Then identify the **load-bearing claim**: the one the conclusion actually hinges on. The issue's own framing and reasoning (its "because X, option Y is safe") are themselves claims to test, not premises to accept. A polished writeup can be right about six facts and wrong about the one that decides the outcome; that one deserves the deepest verification.

3. **Search for prior art** (parallel with step 5): Run `gh pr list --search "<keywords>" --state all` and `gh issue list --search "<keywords>" --state all` to surface duplicate issues, in-flight PRs, or already-merged fixes. Pull the diff and CI status of any exact match. A **closed** PR is as informative as an open one: read its closing comment, because the reason a fix was abandoned is often the real answer to the issue (an approach that looked correct but broke another consumer). Skipping this step is the most common way a verification report becomes obsolete on arrival.

4. **Choose verification depth per claim**: default to reading the code, and escalate up this ladder when a claim is load-bearing, is about runtime behavior, is about a third-party or environment API, or is counterintuitive. Don't run the whole ladder on every claim; spend the depth where the conclusion rests.
   - **L0 Read**: read the actual source. The default for codebase claims.
   - **L1 Search**: full-repo grep for scope claims; confirm the behavior isn't compensated for elsewhere (if the issue says "key X is unhandled in file Y", grep the whole repo for X). Note whether any test covers the path; absent coverage often explains how the bug slipped through.
   - **L2 Reproduce**: for any claim about runtime behavior (a crash, a thrown error, wrong output, an environment-specific difference), run it, don't infer it. Write a minimal repro using the repo's own test runner (or a throwaway script), import the **real** code under test, observe the actual result, then delete the throwaway and never commit it. Reading says "this looks like it would throw"; running proves whether it does. Use the same repro to test the issue's **proposed fix's** premise, not just the bug. For bugs that depend on real DOM, CSS, or focus behavior that a unit runner can't reproduce, this is where Chrome DevTools MCP or Playwright earns its keep; for pure logic, a unit test is enough.
   - **L3 Upstream**: for external, library, or runtime-API claims, verify against the actual canonical source, fetched via `gh` from the upstream repo (`gh api repos/<owner>/<repo>/contents/<path>`, decode the base64), not the possibly-stale or transformed copy in `node_modules`. Check the version range that matters, not just `main`. Don't trust the issue's characterization of a third-party API, or your own memory of it.
   - **L4 Adversarial**: for the load-bearing claim and the issue's conclusion, try to **refute** it, not confirm it. Spell out what would have to be true for the conclusion to be wrong, then go check each of those. When the refutation requires reading across many files or sources, dispatch independent agents in parallel (an `Explore` agent for upstream source, a separate refuter prompted to break the conclusion) so the check isn't anchored on your first read.

5. **Verify each claim** at the chosen depth, gathering concrete evidence (file paths, line numbers, exact snippets, observed repro output, upstream source refs). Run independent checks in parallel. Keep light verification (L0/L1) as direct `Read`/`Grep`/`Glob` to keep context tight; fan heavier work (L2 repro, L3 upstream spelunking, L4 refutation) out to agents when it spans many files or sources.

6. **Report**: Present findings in this structure:

   - **Issue summary**, one line on what the issue requests.
   - **Verification table**, one row per claim. Note the method when it went beyond reading:

     | # | Claim | Result | Evidence |
     |---|-------|--------|----------|
     | 1 | description | Confirmed / Refuted / Partial | `file:line`, or "confirmed by repro", or "checked against <lib> source v0.79 to v0.86". Brief explanation. |

   - **Prior art**, related open, merged, or closed PRs and issues from step 3, with number, state, and a one-line summary (for a closed PR, why it was closed).
   - **Conclusion**, whether the issue is valid. State which claim is load-bearing and how deeply it was verified. Call out any inaccurate framing in the issue body, especially reasoning the issue relied on that turned out wrong, even when the practical request still stands.
   - **Extra findings**, adjacent gaps surfaced during verification that aren't in the issue itself.
   - **Possible fix directions**, brief suggestions if the issue is valid and no covering PR exists. If a covering PR (open or closed) was found, recommend reviewing it instead of proposing a new fix, and note why a closed one was abandoned.

### Rules

- Always read the actual source before judging. Never guess from type names or file names alone.
- The issue's own reasoning is a claim, not a premise. The most consequential error in a well-written issue is usually in its justification, not its facts; verify the "because" as hard as the "what".
- Identify the load-bearing claim and verify it deepest. Confirming peripheral claims while assuming the crux is the classic way a confident report ends up wrong.
- For behavioral claims, reproduce, don't infer. A crash, a throw, wrong output, or an environment difference is cheap to run and expensive to get wrong from reading. Use the repo's test runner or a throwaway script against the real code, observe the actual result, delete the throwaway, and don't commit it.
- For external, library, or runtime-API claims, verify against canonical upstream source via `gh` (not `node_modules`), across the version range that matters, not your memory of the API.
- Adversarially verify the conclusion before endorsing it: state what would make it wrong, then check those things.
- Distinguish codebase claims from external/spec claims. Flag inaccurate framing of standards even when the practical conclusion still holds; do not let a polished writeup smuggle in unverified citations.
- If a claim references a specific version, verify against the current code and note version differences.
- Match escalation to stakes: don't run a repro or fetch upstream source for a claim that reading settles, and don't settle a load-bearing behavioral claim by reading alone.
- Use the same language as the user's input when reporting.
- Be concise. Evidence is `file:line` references and observed results, not full code dumps.
- If `github-repos` MCP is unavailable, fall back to `gh` CLI.
