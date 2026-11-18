# Takeover review mechanics

The commands behind a review body for a PR whose author's code you changed. The decision rules (what the body says, and that it returns to its caller) live in SKILL.md.

## Baseline and head

- Baseline, the last commit in the PR author's leading run: `gh api repos/<o>/<r>/pulls/<n>/commits --paginate --slurp | jq -r 'add | (.[0].author.login // .[0].commit.author.name) as $a | reduce .[] as $c ({run: true, sha: null}; if .run and (($c.author.login // $c.commit.author.name) == $a) then {run: true, sha: $c.sha} else {run: false, sha: .sha} end) | .sha'`. `.author.login` is null for unlinked-email commits, so the reduce falls back to `.commit.author.name`. When a rebase or reset rewrote the branch so every commit shows the author, the leading run is the whole PR; take as baseline the head recorded before your first push instead (seen: five commits all attributed to the contributor while the run claimed its own commits were on the PR).
- Head: `gh api repos/<o>/<r>/pulls/<n> --jq .head.sha`.
- Audience, the first commit's author: `gh api repos/<o>/<r>/pulls/<n>/commits --jq '.[0].author.login // .[0].commit.author.name'`.
- What you changed: `git diff <baseline> <head>`; the author's version of a file: `git show <baseline>:<path>`.

## Thinking order

Work through these in order, then write only what the diff cannot say; they are an order to think in, never sections to emit (seen: 75 of 79 bodies came out in one rigid three-part template):

1. Shortcomings of the original: bugs, missing pieces, anti-patterns, correctness gaps, each at a baseline `file:line`, framed as a critique of the code and never as what a bot said.
2. What changed for each, in present tense, plus pure additions such as tests.
3. What remains or was deferred, each with why; a partial fix is named as partial, and nothing is invented to pad.

## Posting

The body always goes through `--body-file -` with a quoted heredoc, because `-b/--body "..."` mangles backticks:

- `gh pr review <n> --approve --body-file - <<'EOF'` ... `EOF`, or `--comment`, or `--request-changes` in the same form.
- To replace your existing review's body: `gh api --paginate --slurp repos/<o>/<r>/pulls/<n>/reviews | jq '[.[][] | select(.user.login=="<me>")] | last | .id'`, then `gh api --method PUT repos/<o>/<r>/pulls/<n>/reviews/<id> -f body="<text>"`; PUT edits the body only, never the review state.
