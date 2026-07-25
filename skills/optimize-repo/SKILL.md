---
name: optimize-repo
description: Run an optimization pass over a repository or recent changes that simplifies and deletes, reuses existing primitives, conforms to repo conventions, syncs docs, verifies, and ends uncommitted.
argument-hint: "[scope] [--code-only|--docs-only]"
---

## Context

Current branch and default base: !`printf '%s (default base: %s)' "$(git branch --show-current 2>/dev/null || echo unknown)" "$(git symbolic-ref --short refs/remotes/origin/HEAD 2>/dev/null | sed 's|^origin/||' || echo main)"`

Dirty status: !`git status --short 2>/dev/null | head -10 || echo "(unable to read status)"`

Release evidence: !`git tag -l 2>/dev/null | head -3 || echo "(no tags)"`

Root package.json private field: !`test -f package.json && jq -r '.private // "unset"' package.json 2>/dev/null || echo "(no package.json)"`

## Instructions

Optimize the scope by deleting and simplifying first, reusing what the repository already has, conforming to its own paradigm, syncing docs, verifying with its own checks, and stopping at an uncommitted validated tree.

### Process

1. Parse `$ARGUMENTS` (scope is a path or `all`, defaulting to the changes since the default base when the current branch is a feature branch and the whole repository otherwise; `--code-only` and `--docs-only` limit the pass, otherwise process the whole scope).
2. Read before touching: map the scope's idiom, entry points, and in-repo prior art; no edit lands before this read.
3. Decide the release posture from evidence, not habit. A package with `private: true`, no version tags, and no published artifact gets no backward compatibility: no deprecation aliases, no compat shims, no old path kept, delete instead. A published package keeps compatibility and takes a changeset in the repository's format when `.changeset` exists. State the evidence in the report.
4. Simplify and delete: strip comments that fail the bar (a comment survives only when it states a why the code cannot show), remove dead code, unused files, and unused exports. Exempt primitives that look unused but are the repository's public building blocks; leave those in place.
5. Reuse: replace hand-rolled fragments with the repository's own primitives and helpers, searching the UI package and existing utilities first. Keeping a parallel implementation requires stating what existing thing was rejected and why.
6. Conform: audit the result against the repository's own paradigm. File placement matches neighbors, no new public API surface lands unless the task required it, and naming and structure follow the nearest precedent, cited by file.
7. Sweep for completeness: search the changed patterns across the whole scope and list every site as changed or consciously skipped with a reason. A many-site pattern never ships as a one-site fix.
8. Sync docs: update every doc the change invalidates, prune stale ones, and keep them minimal. With `--docs-only` over the whole repository, run the full inventory mode instead: list every README and doc, delete the obsolete ones outright, and rewrite the survivors into one coherent minimal structure.
9. Verify with the repository's own ladder, following [references/verify-ladder.md](references/verify-ladder.md) and truncating noisy output.
10. Stop at an uncommitted validated tree and report what was deleted, simplified, reused, skipped, and why. Committing composes `commit-changes`; shipping composes `ship-pr`.

### Rules

- Never weaken or delete failing tests to make verification pass.
- No new dependencies during an optimization pass.
- Backward compatibility removal requires the step 3 evidence in the report.
