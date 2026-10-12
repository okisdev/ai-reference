---
name: create-pr
description: create or open a GitHub pull request (PR) from the current branch with a title and body that follow the repo's conventions and the user's writing style
argument-hint: "[base-branch | --base <branch>] [--draft] [--cwd <path>]"
---

## Context

Repository: !`gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null`
Current branch: !`git branch --show-current`
Base branch (the repo default; step 1 replaces it when the arguments name a base): !`out=$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@refs/remotes/origin/@@'); echo "${out:-main}"`
Remote status: !`git status --short -b | head -1`
Existing PR: !`gh pr list --head "$(git branch --show-current)" --state open --json url -q '.[0].url // "(none)"' 2>/dev/null || echo "(none)"`
Commits: !`b=$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@refs/remotes/origin/@@'); b=${b:-main}; git log --pretty='%h %s' "$(git merge-base HEAD "$b")"..HEAD 2>/dev/null`
Diff stat: !`b=$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@refs/remotes/origin/@@'); b=${b:-main}; git diff --stat "$(git merge-base HEAD "$b")"..HEAD 2>/dev/null`
Recent merged PRs (style reference): !`gh pr list --state merged --limit 8 --json number,title --jq '.[] | "#\(.number) \(.title)"' 2>/dev/null`
Repo PR template (if present): !`for p in .github/pull_request_template.md .github/PULL_REQUEST_TEMPLATE.md docs/pull_request_template.md PULL_REQUEST_TEMPLATE.md pull_request_template.md; do [ -f "$p" ] && { echo "--- using: $p ---"; cat "$p"; exit 0; }; done; echo "(no template found)"`

## Instructions

Execute immediately without asking. Skip steps that don't apply.

1. **Pre-flight guards** (treat any `$ARGUMENTS` as the user input; a `--cwd <path>` names the repository or worktree to act in, so drop it and its value before reading the base, rerun the Context probes there with `git -C <path>` and `gh` run from `<path>`, and run every git and gh command there). Run in order.
   - Take the base from the arguments: `--base <branch>`, or a leading token that is not a flag and names a branch. When it differs from the `Base branch` probe, rerun Commits and Diff stat against it before composing (`git log --pretty='%h %s' $(git merge-base HEAD <base>)..HEAD` and `git diff --stat $(git merge-base HEAD <base>)..HEAD`); the guards below use that base.
   - Abort if the current branch is the base/default branch; run `/create-branch` first to move the work onto a feature branch.
   - Abort if no commits exist between branch and base ("nothing to PR").
   - Abort if any commit subject matches `/^(WIP|wip:?|fixup!|squash!)/i`, unless `--draft` was passed (then proceed and mark draft); to clean them up, run `/organize-commits`, then re-run.
   - Warn (don't block) if `git status --porcelain` is non-empty: "uncommitted changes will not be in this PR; run `/commit-changes` to include them."
   - Warn (don't block) if branch is N commits behind base.
   - Warn (don't block) if branch contains merge commits.

2. **Existing PR check.** If `Existing PR` above is a URL, print it and stop; do not re-create (to update, the user can `gh pr edit` or close the PR and re-run).

3. **Push.** If the branch has unpushed commits, run `git push -u origin HEAD`. Skip the push when already up-to-date.

4. **Compose the title.** Follow the title format below.

5. **Compose the body.** If a repo PR template was found above, use that template verbatim and fill in any HTML comment placeholders with content derived from commits and diff. Otherwise use the body format and body rules in [references/body-format.md](references/body-format.md).

6. **Create.** `gh pr create --head <current branch> --repo <Repository probe> --title <title> --body "$(cat <<'EOF' ... EOF)"`, with `--head <fork-owner>:<branch>` when the branch was pushed to a fork rather than to the Repository probe's repo (always HEREDOC the body to preserve formatting and avoid shell escaping; always pass `--head` and `--repo`, because multi-remote checkouts fail without them). Add `--base <base>` only when step 1 took a base from the arguments; otherwise omit `--base` so gh keeps defaulting to the repo default branch, and never feed a leading `--draft` to `--base`. Add `--draft` if pre-flight signaled it. Do not pass `--fill`, `--web`, or any reviewer/label/milestone flag unless the user explicitly asked.

7. **Print** the resulting PR URL.

### Title format

- Always start with a conventional commit type: `feat`, `fix`, `perf`, `refactor`, `docs`, `chore`, `test`, `build`, `ci`.
- Add a scope `(name)` only when the change is confined to one package or one app. Use the short slug (e.g. `react-ai-sdk`, `assistant-stream`), not the full `@org/...` namespace. Omit the scope when the change spans multiple packages or is repo-wide.
- Keep the full title under 72 characters (GitHub PR list truncation point).
- When commits mix types, pick the most user-facing one: `feat` > `fix` > `perf` > `refactor` > `docs` > `chore` > `test` > `build` > `ci`.
- Cross-check against `Recent merged PRs` above: the new title's prefix and scope shape should match local convention (if recent titles all use a scope and this PR is single-package, use a scope).

### Style

Apply to title and body; override the repo template's prose style (its section structure stays, the prose switches to ours).

- **casing**: casual register. Lowercase except proper nouns (`React`, `TypeScript`, `GitHub`), conventionally-uppercase acronyms (`API`, `HTTP`, `URL`), and case-sensitive code identifiers.
- **dash rule**: never use em dashes, en dashes, or hyphens used as sentence punctuation. Break thoughts with a period, semicolon, comma, or parentheses. Identifier hyphens (`react-ai-sdk`, `tool-call`) stay.
- **no hard wrap**: each paragraph and each bullet stays on one line however long it gets.
