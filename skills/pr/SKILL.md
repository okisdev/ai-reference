---
name: pr
description: Create a GitHub PR from the current branch with auto-generated title and summary based on commits.
argument-hint: "[base-branch]"
---

## Context

Current branch: !`git branch --show-current`
Base branch: $ARGUMENTS (default to repo's default branch)
Remote status: !`git status --short -b | head -1`

### Commits

!`git log --oneline $(git merge-base HEAD ${1:-$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@refs/remotes/origin/@@' || echo main)})..HEAD 2>/dev/null`

### Diff stat

!`git diff --stat $(git merge-base HEAD ${1:-$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@refs/remotes/origin/@@' || echo main)})..HEAD 2>/dev/null`

## Instructions

Create a PR immediately without asking. Execute these steps:

1. **Push** if the branch is behind remote or has unpushed commits: `git push -u origin HEAD`
2. **Analyze** all commits and diffs to understand the full scope of changes.
3. **Create PR** with `gh pr create`:
   - Title: concise, under 70 chars, conventional commit style if all commits share a theme
   - Body: use the format below, derived from actual changes — not generic filler
   - If a PR already exists for this branch, print its URL instead

### Body format

```
## Summary
<3-5 bullet points covering the key changes, grouped by theme>

## Test plan
<Bulleted checklist of things to verify>
```

### Rules

- Always use HEREDOC for the body to preserve formatting
- Summarize by purpose, not by file — the reviewer can see the diff
- Keep bullet points concise (one line each)
- Do NOT ask for confirmation — just create it
- Print the PR URL when done
