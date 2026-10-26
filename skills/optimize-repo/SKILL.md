---
name: optimize-repo
description: Extract, decouple, refactor, simplify, remove redundancy and dead code, and reuse existing helpers, then verify and leave the changes uncommitted.
argument-hint: "[scope] [--code-only|--docs-only]"
---

## Context

Current branch and default base: !`b=$(git symbolic-ref --short refs/remotes/origin/HEAD 2>/dev/null | sed 's|^origin/||'); b=${b:-main}; printf '%s (default base: %s)' "$(git branch --show-current 2>/dev/null || echo unknown)" "$b"`

Dirty status: !`git rev-parse --git-dir >/dev/null 2>&1 && { out=$(git status --short | head -10); echo "${out:-(clean)}"; } || echo "(unable to read status)"`

Release evidence: !`out=$(git tag -l 2>/dev/null | head -3); echo "${out:-(no tags)}"`

Root package.json private field: !`test -f package.json && jq -r '.private // "unset"' package.json 2>/dev/null || echo "(no package.json)"`

## Instructions

**The one rule: delete before you polish, and run code to prove the riskiest deletion safe.** A great pass leaves a smaller tree that behaves the same and a report that shows it: the release posture with its evidence, what was deleted, simplified, reused, and skipped and why, every site of a changed pattern accounted for, and the repository's own ladder passing with failures visible. The bar is [examples/pass.md](examples/pass.md): open it before reporting, and check the draft against [examples/rejected.md](examples/rejected.md).

Optimize the scope by deleting and simplifying first, reusing what the repository already has, conforming to its own paradigm, syncing docs, verifying with its own checks, and stopping at an uncommitted validated tree.

### Process

1. Parse `$ARGUMENTS` (scope is a path or `all`, defaulting to the changes since the default base when the current branch is a feature branch and the whole repository otherwise; `--code-only` and `--docs-only` limit the pass, otherwise process the whole scope). A bare ask to extract, decouple, or refactor, in any language, runs this pass over the scope it names instead of an ad hoc edit (seen: asks to extract, decouple, and refactor went ad hoc in 34 sessions).
2. Read before touching: map the scope's idiom, entry points, and in-repo prior art; no edit lands before this read.
3. Decide the release posture from evidence, not habit. A package with `private: true`, no version tags, and no published artifact gets no backward compatibility: no deprecation aliases, no compat shims, no old path kept, delete instead. A published package keeps compatibility and takes a changeset in the repository's format when `.changeset` exists. State the evidence in the report.
4. Simplify and delete: strip comments that fail the bar (a comment survives only when it states a why the code cannot show), remove dead code, unused files, and unused exports. Aim past local cleanup: prefer the restructuring that makes a whole branch, mode, helper, or layer disappear over polishing what could vanish. For the riskiest removal, name the one fact it is safe because of and prove that fact by running real code (a test or scratch script importing the shipped path); a safety fact that stays unproven is reported as unproven, not assumed. When the scope includes work this session authored, run this review in a fresh subagent with none of the authoring context, because an authoring context defends its own output. Exempt primitives that look unused but are the repository's public building blocks; leave those in place.
5. Reuse: replace hand-rolled fragments with the repository's own primitives and helpers, searching the UI package and existing utilities first. Keeping a parallel implementation requires stating what existing thing was rejected and why.
6. Conform: audit the result against the repository's own paradigm. File placement matches neighbors, no new public API surface lands unless the task required it, and naming and structure follow the nearest precedent, cited by file.
7. Sweep for completeness: search the changed patterns across the whole scope and list every site as changed or consciously skipped with a reason. Then check where grep cannot see: serialized strings and wire formats, other languages in the repo, generated files, and the pinned or patched source of libraries that consume the pattern. A many-site pattern never ships as a one-site fix.
8. Sync docs: replace each sentence the change made false, delete what it made obsolete, prune stale docs, and keep them minimal, never appending an account of the change (what it did belongs in the commit and PR), stripping AI tells on the way (puffery, chatbot phrases, decorative emojis, em-dash punctuation). An instruction file (`AGENTS.md`, `CLAUDE.md`), or a doc one orders agents to read (`normalize-agents-md`'s read-path docs, such as a `DESIGN.md`), is not a doc to keep in sync: a line the change invalidates that fails `normalize-agents-md`'s altitude test (an inventory, a module internal, a description the tree carries) is deleted, not updated, and only its rules, commands, and pointers are rewritten. With `--docs-only` over the whole repository, run the full inventory mode instead: list every README and doc, delete the obsolete ones outright, and rewrite the survivors into one coherent minimal structure.
9. Verify with the repository's own ladder, following [references/verify-ladder.md](references/verify-ladder.md) and truncating noisy output under `set -o pipefail`.
10. Stop at an uncommitted validated tree and report what was deleted, simplified, reused, skipped, and why, opening with the net line count (`git diff --shortstat`) and closing with one doc sync line (the docs changed, or none needed). A net gain is named by what it added and why that outweighs a deletion, because a pass that grows the tree has not deleted before it polished (seen: a pass reported as cleanup added 9,281 lines and deleted 7,640). Committing composes `commit-changes`; shipping composes `ship-pr`.

### Rules

- Never weaken or delete failing tests to make verification pass.
- No new dependencies during an optimization pass.
- Backward compatibility removal requires the step 3 evidence in the report.
