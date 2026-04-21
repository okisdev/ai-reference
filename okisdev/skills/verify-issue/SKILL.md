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

### Input

`$ARGUMENTS` is an issue number (e.g. `3766`) or a full GitHub issue URL (e.g. `https://github.com/owner/repo/issues/3766`).

### Process

1. **Fetch issue**: Use `github-repos` MCP (`get_issue`) if available, otherwise `gh issue view $ISSUE_NUMBER --json title,body,labels,state,author`. Extract the issue title, description, and all technical claims.

2. **Extract claims**: Parse the issue body and list every verifiable technical claim. A claim is any statement about how the code works, what types exist, what fields are missing, what behavior occurs, etc.

3. **Verify each claim**: For each claim, search the codebase using Grep/Glob/Read to find the relevant source code. Gather concrete evidence (file paths, line numbers, exact code snippets).

4. **Parallel verification**: Run as many verification searches in parallel as possible. Use direct tool calls (Read, Grep, Glob) rather than agents to avoid context-length issues.

5. **Report**: Present findings in a structured format:

   - **Issue summary**: one-line description of what the issue requests
   - **Verification table**: one row per claim

     | # | Claim | Result | Evidence |
     |---|-------|--------|----------|
     | 1 | description | Confirmed/Refuted/Partial | `file:line` — brief explanation |

   - **Conclusion**: Is the issue valid? Any additional findings beyond what was reported?
   - **Possible fix directions**: Brief suggestions if the issue is valid

### Rules

- Always read the actual source code before making a judgment — never guess from type names or file names alone
- If a claim references a specific version, verify against the current code (note version differences if any)
- Report additional issues discovered during verification as "extra findings"
- Use the same language as the user's input when reporting
- Be concise — evidence should be file:line references, not full code dumps
- If `github-repos` MCP is unavailable, fall back to `gh` CLI
