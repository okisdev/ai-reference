---
name: commit-changes
description: Stage and commit only uncommitted file changes into clean, categorized commits; existing commits are left untouched.
argument-hint: "[--cwd <path>]"
---

## Context

Current branch: !`git branch --show-current 2>/dev/null || echo "(not a git repository)"`

Uncommitted changes: !`git status --short 2>/dev/null || echo "(not a git repository)"`

Uncommitted diff stat: !`git diff --stat HEAD 2>/dev/null || echo "(none or not a git repository)"`

## Instructions

**The one rule: each commit is one purpose and holds exactly the paths you planned for it.** A great run leaves a short series a reviewer can read commit by commit: subjects in the repo's own conventional style, foundational changes first, nothing pre-staged riding into the wrong commit, a clean tree at the end, and every new commit proven signed where signing is on. The bar is [examples/grouped.md](examples/grouped.md); open it before grouping and check the plan against [examples/rejected.md](examples/rejected.md).

Categorize **only the current uncommitted changes** into clean commits. Leave existing commits untouched.

1. `--cwd <path>` in `$ARGUMENTS` names the repository or worktree to act in: rerun the Context probes there with `git -C <path>` and run every git command there. Record the staged paths (`git diff --cached --name-only --no-renames`), then unstage everything with `git restore --staged :/` so no pre-staged file rides into a group's commit (seen: a tree that create-branch staged collapsed into the first commit). Read diffs (`git diff HEAD`). Untracked/new files don't appear in `git diff HEAD`; read those files directly so they're categorized, not missed. Group by **purpose** using conventional commits (`feat:`, `fix:`, `chore:`, `refactor:`, `docs:`, `style:`, `test:`, `perf:`, `ci:`, `build:`, `revert:`).
2. For each group, stage by explicit paths only: `git add <files>` (`git add -f <file>` only for a recorded path that git ignores), confirm `git diff --cached --name-only --no-renames` equals that group's list, then `git commit`. Never `git add -A` or `git add .`.
3. Verify `git status` is clean, show `git log --oneline` of new commits. When `git config commit.gpgsign` is true, prove each new commit is signed with exactly this check: `git cat-file commit <sha> | grep -c '^gpgsig'` prints 1 (seen: 376 of 540 runs improvised their own signing proof). A signing failure, at `git commit` or in this check, stops the run and is reported; never bypass it with `--no-gpg-sign` or `commit.gpgsign=false` (seen: one run turned signing off when the 1Password prompt failed).

Rules:

- One commit per distinct purpose, each independently meaningful; a single concern is one commit whatever its file count
- Assign each file to its primary category; don't split files across commits
- Dependency order: foundational first (config, types, rename, schema and generated definitions), then core logic, then wiring, then UI, then polish
- Match the repo's existing commit-message style (subject case, scope notation, body)
- If pre-commit hooks fail, fix the failure and re-commit; never bypass with `--no-verify` (seen: `--no-verify` appeared in 10 runs despite this rule)
- NEVER reset, rebase, modify existing commits, or force push
- No trace of tooling in a commit message: no `Co-Authored-By` trailer naming a coding tool, no generated-by line, no session link (seen: without a global rule, the default commit flow appended a coding tool's co-author trailer to every commit).
