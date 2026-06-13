---
name: make-pr
description: create or open a GitHub pull request (PR) from the current branch with a title and body that follow the repo's conventions and the user's writing style; auto-detects the base branch and fills the repo's PR template when one is present
argument-hint: "[base-branch] [--draft]"
---

## Context

Repository: !`gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null`
Default branch: !`git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@refs/remotes/origin/@@' || echo main`
Current branch: !`git branch --show-current`
Base branch: !`case "$1" in (""|--*) git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@refs/remotes/origin/@@' || echo main;; (*) echo "$1";; esac` (defaults to the repo default branch above)
Remote status: !`git status --short -b | head -1`
Existing PR: !`gh pr list --head "$(git branch --show-current)" --state open --json url -q '.[0].url // "(none)"' 2>/dev/null || echo "(none)"`

### Commits

!`git log --pretty='%h %s' $(git merge-base HEAD $(case "$1" in (""|--*) git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@refs/remotes/origin/@@' || echo main;; (*) echo "$1";; esac))..HEAD 2>/dev/null`

### Diff stat

!`git diff --stat $(git merge-base HEAD $(case "$1" in (""|--*) git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@refs/remotes/origin/@@' || echo main;; (*) echo "$1";; esac))..HEAD 2>/dev/null`

### Recent merged PRs (style reference)

!`gh pr list --state merged --limit 8 --json number,title --jq '.[] | "#\(.number) \(.title)"' 2>/dev/null`

### Repo PR template (if present)

!`for p in .github/pull_request_template.md .github/PULL_REQUEST_TEMPLATE.md docs/pull_request_template.md PULL_REQUEST_TEMPLATE.md pull_request_template.md; do [ -f "$p" ] && { echo "--- using: $p ---"; cat "$p"; exit 0; }; done; echo "(no template found)"`

Runtimes that do not auto-run the commands above marked with `!` (Claude Code executes them and injects their output) should run each one to gather this context; treat any `$ARGUMENTS` or `$1` as the input the user provided.

## Instructions

Execute immediately without asking. Skip steps that don't apply, do not prompt for confirmation.

### Process

1. **Pre-flight guards.** Run in order; abort or warn as specified.
   - Abort if the current branch is the base/default branch; run `/make-branch` first to move the work onto a feature branch.
   - Abort if no commits exist between branch and base ("nothing to PR").
   - Abort if any commit subject matches `/^(WIP|wip:?|fixup!|squash!)/i`, unless `--draft` was passed (then proceed and mark draft); to clean them up, run `/organize-commits`, then re-run.
   - Warn (don't block) if `git status --porcelain` is non-empty: "uncommitted changes will not be in this PR; run `/commit-changes` to include them."
   - Warn (don't block) if branch is N commits behind base.
   - Warn (don't block) if branch contains merge commits.

2. **Existing PR check.** If `Existing PR` above is a URL, print it and stop; do not re-create (to update, the user can `gh pr edit` or close the PR and re-run).

3. **Push.** If the branch has unpushed commits, run `git push -u origin HEAD`. Skip the push when already up-to-date.

4. **Compose the title.** Follow the title format below.

5. **Compose the body.** If a repo PR template was found above, use that template verbatim and fill in any HTML comment placeholders with content derived from commits and diff. Otherwise use the body format below.

6. **Create.** `gh pr create --title <title> --body "$(cat <<'EOF' ... EOF)"`. Pass `--base <base>` only when a non-flag base-branch positional was provided (`$1` is non-empty and does not start with `--`); otherwise omit `--base` so gh keeps defaulting to the repo default branch, and never feed a leading `--draft` to `--base`. Add `--draft` if pre-flight signaled it. Do not pass `--fill` (it overrides our structured body), `--web` (defeats the no-confirmation contract), `--reviewer`, `--label`, or `--milestone` unless the user explicitly asked.

7. **Print** the resulting PR URL.

### Title format

- Always start with a conventional commit type: `feat`, `fix`, `perf`, `refactor`, `docs`, `chore`, `test`, `build`, `ci`.
- Add a scope `(name)` only when the change is confined to one package or one app. Use the short slug (e.g. `react-ai-sdk`, `assistant-stream`), not the full `@org/...` namespace. Omit the scope when the change spans multiple packages or is repo-wide.
- Keep the full title under 72 characters (GitHub PR list truncation point).
- When commits mix types, pick the most user-facing one: `feat` > `fix` > `perf` > `refactor` > `docs` > `chore` > `test` > `build` > `ci`.
- Cross-check against `Recent merged PRs` above: the new title's prefix and scope shape should match local convention (if recent titles all use a scope and this PR is single-package, use a scope).

### Body format (when no repo template was found)

```
closes #<n>

## summary

- <2 to 4 bullets, lead with user-visible change, then implementation>

## breaking changes

- <removed/renamed APIs, changed defaults, migration steps; OMIT this whole section if none>

## test plan

### already verified

- [x] <exact command + observable outcome, e.g. `pnpm --filter @x/y test` -> 42/42 green>

### reviewer should verify

- [ ] <concrete reproduction step naming the UI path / flag / API call and the expected observable outcome>

## notes

- <follow-ups, known limitations, attribution; OMIT this whole section if none>
```

Body rules:

- The `closes #<n>` line is the very first line of the body, with no heading, before `## summary`. Use the lowercase keyword `closes`. For multiple issues, repeat the keyword on its own line: `closes #10` then `closes #11`. For cross-repo: `closes owner/repo#<n>`. Omit the line entirely when no issue is referenced. Issue numbers come from: explicit user mention in conversation, branch name patterns like `fix/4005-foo`, or commit subjects mentioning `#<n>`.
- All section headings are lowercase.
- Pre-check `[x]` only for items actually verified before the push. Leave `[ ]` for things the reviewer needs to do.
- Skip the entire `## test plan` section for docs-only, types-only, or changeset-only PRs. Replace it with a single line: `no test plan, <one-clause reason>` (e.g. `no test plan, docs only`).
- Omit `## breaking changes` and `## notes` sections entirely when they have no content. No empty headings.
- Summary leads with the user-visible change in the first bullet; implementation detail comes after, not a flat list of internal plumbing as equal-weight bullets.

### Style

These rules apply to both the title and the body, and they override any style cues in the repo's PR template content (the template's section structure stays; the prose style switches to ours).

- **casing**: casual register. Lowercase except proper nouns (`React`, `TypeScript`, `GitHub`), conventionally-uppercase acronyms (`API`, `HTTP`, `URL`), and case-sensitive code identifiers.
- **dash rule**: never use em-dashes (`—`), en-dashes (`–`), or hyphens used as sentence punctuation. Break thoughts with a period, semicolon, comma, or parentheses. Identifier hyphens (`react-ai-sdk`, `tool-call`) stay.
- **no hard wrap**: each paragraph and each bullet stays on one line however long it gets. The GitHub renderer handles soft wrapping.

### Rules

- Always use HEREDOC for `--body` to preserve formatting and avoid shell escaping.
- Summarize by purpose, not by file. The reviewer can see the diff.
- If the branch is on a fork, `gh pr create` handles the cross-repo head:base wiring automatically; do not override.
- Print the PR URL when done.
