---
name: release-changes
description: Deploy what changed, or cut a release, across a repository's targets (APIs, workers, web apps, databases, app store builds) in a safe order and prove each one live, when asked to deploy, push the schema and deploy, or release the platforms that changed.
argument-hint: "[deploy|release] [target...] [--dry-run]"
---

## Context

Repository: !`gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null || echo "unknown"`
Current branch: !`git branch --show-current 2>/dev/null || echo "(not a git repository)"`
Last tag: !`git describe --tags --abbrev=0 2>/dev/null || echo "(none)"`
Release docs: !`out=""; for f in RELEASING.md RELEASE.md CHANGELOG.md AGENTS.md Makefile; do test -e "$f" && out="$out $f"; done; echo "${out:-(none)}"`
Deploy configs: !`out=$(git ls-files 2>/dev/null | grep -E '(^|/)(wrangler\.(toml|jsonc?)|vercel\.json|fly\.toml|netlify\.toml|Dockerfile|eas\.json|app\.json|fastlane/Fastfile|drizzle\.config\.[jt]s|prisma/schema\.prisma)$' | head -20); echo "${out:-(none)}"`
Uncommitted changes: !`out=$(git status --short 2>/dev/null | head -5); echo "${out:-(none)}"`

## Instructions

**The one rule: everything the user named is in what ships, and every target ships from one verified head, in an order where no running code meets storage it cannot handle, and is proven live before the next one starts.** A great run names the release diff and each change the user asked for in it, deploys only the targets that diff touched, runs data steps where the order is safe, and reports every target with its new version or URL, the check that proved it live, and the version to roll back to. Open [examples/release.md](examples/release.md) before reporting and check the run against [examples/rejected.md](examples/rejected.md).

### Process

1. Parse `$ARGUMENTS`: the mode (`deploy` ships the named or changed targets from the current head; `release` also bumps versions, writes the changelog, and merges the PR, and is the mode for an ask to release), the targets the user named, the changes the user named ("this release must include X and Y"), and `--dry-run`, which stops after the plan in step 5. Refuse to ship from a dirty tree or from a head that is not on the remote, because a deploy must be reproducible from a commit.
2. Read the repository's own recipe first, because it outranks anything inferred: a `RELEASING.md` or the release section of `AGENTS.md`, `Makefile` targets, `package.json` scripts named like `deploy`, `release`, `migrate`, `db:push`, and CI workflows that deploy on tag or merge (a target CI deploys is shipped by merging or tagging, never by hand). Only where the recipe is silent, derive each target from the Context's deploy configs.
3. Fix the release diff: from the last release tag, or from the version each target runs now (`wrangler deployments list`, `vercel ls`, `fly releases`, the store's latest build) to the head. Confirm every change the user named is in it by its commit or merged PR, and stop naming each one missing before anything ships (seen: a release went out without the two changes the user had named as the most important).
4. Map the diff to targets: each changed path to the workspace package that owns it and that package's deploy config; a shared package marks every target that depends on it; list every untouched target as skipped with that reason.
5. Order the plan and show it once: an additive schema change (new table, nullable column) before the code that uses it; a destructive one (drop, rename, a new not-null without a default) after the code that stops depending on it; a backfill after the code that writes the new shape is live; staging before production when the repository has staging; servers before clients that call their new endpoints. Each data step shows its migration file or SQL. Before the first production write, record each target's current version as its rollback point.
6. In `release` mode, before deploying: get the PR head cleared (`verify-pr` when installed), bump versions only for the targets that changed and in the repository's convention (a build number only when the user asked for that), write the changelog entry keyed to the new version, commit them onto the PR branch, push, and confirm the remote head equals the commit you will deploy (clearing that head again when the bumps moved it), because what deploys must be exactly what merges.
7. Ship each target with the repository's own command, loading secrets through the repository's mechanism (a secrets manager wrapper, `wrangler secret`, the platform's env) and never printing a value; a destructive migration on production runs only after the user's explicit go in this conversation. An Apple build goes through `upload-testflight` when installed. Capture each target's new version, deployment id, or URL.
8. Prove each target live before moving on: a request to its health route or a real endpoint, a minute of its logs (`wrangler tail`, the platform's log command) without new errors, the migration recorded as applied, the backfilled rows counted (`inspect-db` when installed). A failed check stops the rollout and reports the rollback point; it is diagnosed (`diagnose-root` when installed), never retried blind.
9. In `release` mode, hand the PR to `ship-pr` when installed to merge after the hand-shipped targets are live; a target that CI deploys on merge or tag ships at this step instead, so wait for its deployment run after the merge (or the tag) and prove it live as in step 8 before reporting. Report per target: shipped with version and live check, skipped with reason, or failed with the rollback point.

### Rules

- Production data is never changed by a step the plan did not show, and never destructively without the user's go in this conversation.
- A target that CI deploys is never deployed by hand alongside it.
- Secret values never appear in commands echoed to the report, logs, or files.
