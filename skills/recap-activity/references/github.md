# GitHub

## Identity and scope

- Login: `gh api user --jq .login`. An org's members for a team recap: `gh api orgs/<org>/members --paginate --jq '.[].login'`.
- A bare repo name: `gh search repos "<name> in:name" --owner <org> --json fullName --jq '.[].fullName'`, keeping only an exact name match.
- Repos in scope, for per-repo calls: `gh repo list <org> --no-archived --limit 1000 --json name --jq '.[].name'`.
- Org node id for GraphQL: `gh api orgs/<org> --jq .node_id`.

## Window

Search qualifiers and `gh run list --created` take an offset range such as `2026-01-15T00:00:00+08:00..2026-01-15T23:59:59+08:00`, or a bound such as `>=2026-01-15T00:00:00+08:00`. A bare `2026-01-15` is the UTC day, which at +08:00 runs from 08:00 that day to 08:00 the next (seen: a bare date passed to GitHub was a UTC day, so a failure at 00:28 local landed in the wrong day). Pass REST parameters with `-X GET -f`, which encodes the offset; a raw `+` pasted into a URL turns into a space. Records come back stamped in UTC, so `jq` comparisons take the window's bounds in UTC (`YYYY-MM-DDTHH:MM:SSZ`).

## Person digest

`--limit 1000` is the search maximum; exactly 1000 results means the window must be split.

PRs opened or merged in the window, unioned by URL; count merged ones from the `--merged-at` file, because `state` is the state now:

```
gh search prs --author=<login> --owner=<org> --created="<range>" --limit 1000 --json url,number,title,state,isDraft,repository,createdAt,closedAt,labels > prs-opened.json
gh search prs --author=<login> --owner=<org> --merged-at="<range>" --limit 1000 --json url,number,title,state,isDraft,repository,createdAt,closedAt,labels > prs-merged.json
jq -s 'add | unique_by(.url)' prs-opened.json prs-merged.json > prs.json
```

PRs reviewed, in every review state, for any login. A review in the window updated its PR after the window's start, so search from the start and let review times settle membership; count reviewed PRs, with review events in parentheses:

```
gh api graphql --paginate -f query='query($q:String!,$login:String!,$endCursor:String){search(query:$q,type:ISSUE,first:100,after:$endCursor){pageInfo{hasNextPage endCursor} nodes{... on PullRequest{url title author{login} repository{nameWithOwner} reviews(author:$login,first:100){nodes{state submittedAt}}}}}}' -f q='is:pr reviewed-by:<login> -author:<login> org:<org> updated:>=<start>' -f login=<login> > reviews-pages.json
jq -s --arg s '<start UTC>' --arg e '<end UTC>' '[.[].data.search.nodes[] | .reviews = [.reviews.nodes[] | select(.submittedAt >= $s and .submittedAt <= $e)] | select(.reviews | length > 0)]' reviews-pages.json > reviews.json
```

Issues opened:

```
gh search issues --author=<login> --owner=<org> --created="<range>" --limit 1000 --json url,number,title,state,repository,createdAt,closedAt,labels > issues-opened.json
```

Issues and PRs commented on, kept only when one of the person's comments falls inside the window (`commenter:` matches comments of any age), minus the items already counted as opened in it:

```
gh api graphql --paginate -f query='query($q:String!,$endCursor:String){search(query:$q,type:ISSUE,first:100,after:$endCursor){pageInfo{hasNextPage endCursor} nodes{... on Issue{url title comments(last:100){nodes{author{login} createdAt}}} ... on PullRequest{url title comments(last:100){nodes{author{login} createdAt}}}}}}' -f q='commenter:<login> org:<org> updated:>=<start>' > comments-pages.json
jq -s --arg l '<login>' --arg s '<start UTC>' --arg e '<end UTC>' '[.[].data.search.nodes[] | {url, title, comments: [.comments.nodes[] | select(.author.login == $l and .createdAt >= $s and .createdAt <= $e)] | length} | select(.comments > 0)]' comments-pages.json > commented.json
```

Default branch commits, per repo in scope, deduped by SHA across repos (an empty repo answers HTTP 409; skip it). A subject with a trailing `(#N)` is a merged PR already counted, so report only the commits without one, the work that bypassed a PR:

```
gh api -X GET repos/<owner>/<name>/commits -f author=<login> -f since=<start> -f until=<end> -f per_page=100 --paginate --jq '.[] | {sha: .sha[0:7], date: .commit.author.date, subject: (.commit.message | split("\n")[0])}'
```

Why an open PR waits:

```
gh pr view <number> -R <owner>/<name> --json url,reviewDecision,mergeStateStatus,statusCheckRollup --jq '{url, reviewDecision, mergeStateStatus, checks: ([.statusCheckRollup[] | .conclusion // .state] | group_by(.) | map({(.[0]): length}) | add)}'
```

The aggregate counts to compare against, paired as PRs opened to `totalPullRequestContributions`, PRs reviewed to `totalPullRequestReviewContributions`, issues opened to `totalIssueContributions`, and default branch commits to `totalCommitContributions`. They leave out comment-only reviews and some private repository work, so a gap is expected (seen: GitHub's review contributions left out comment-only reviews, 172 PRs against the 175 counted):

```
gh api graphql -f query='query($login:String!,$org:ID!,$from:DateTime!,$to:DateTime!){user(login:$login){contributionsCollection(organizationID:$org,from:$from,to:$to){totalCommitContributions totalPullRequestContributions totalPullRequestReviewContributions totalIssueContributions}}}' -f login=<login> -f org=<node-id> -f from=<start> -f to=<end>
```

Without an org scope, drop `--owner` and `org:` from the searches and `organizationID` with its `$org` variable from the aggregate query.

## Org or repo digest

Swap `--owner=<org>` for `--repo=<owner>/<name>`, or `org:` for `repo:`, to narrow to one repo.

```
gh search prs --owner=<org> --merged-at="<range>" --limit 1000 --json url,number,title,author,repository,labels > merged.json
gh search issues --owner=<org> --created="<range>" --limit 1000 --json url,number,title,state,author,repository > issues-opened.json
gh release list -R <owner>/<name> --limit 100 --json tagName,name,publishedAt,isPrerelease > releases.json
```

Keep releases whose `publishedAt` falls inside the window; when the oldest of 100 is still inside it, raise `--limit`.

## Workflow runs

Per repo; for an org, loop over every repo in scope, because scheduled runs need no push.

```
gh run list -R <owner>/<name> --created="<range>" --limit 1000 --json databaseId,workflowName,displayTitle,event,headBranch,headSha,status,conclusion,createdAt,url > runs.json
jq '[.[] | select(.status == "completed" and (.conclusion | IN("success", "skipped", "neutral") | not))]' runs.json
gh api -X GET repos/<owner>/<name>/actions/runs -f created="<range>" -f per_page=1 --jq .total_count
```

The last line is the aggregate count for `runs.json`. An `action_required` run waits for an approval and has no jobs; a `cancelled` run is usually superseded, which the next run on the same branch starting right after it confirms. Neither is a failure unless its log says so. For a failed run:

```
gh run view <id> -R <owner>/<name> --json jobs --jq '.jobs[] | select(.conclusion == "failure") | {name, steps: [.steps[] | select(.conclusion == "failure") | .name]}'
gh run view <id> -R <owner>/<name> --log-failed > run-<id>.log
grep -n -i -E 'error|failed|fatal|exception|panic' run-<id>.log | head -40
```

Read around the earliest hit that names a cause; the final `##[error]` line usually carries only the exit code. The last good run of the same workflow, branch, and event before the first bad run's `createdAt` (here `2026-01-15T08:00:00Z`), and the changes since it:

```
gh run list -R <owner>/<name> --workflow "<workflow-name>" --branch <headBranch> --event <event> --status success --created="<2026-01-15T08:00:00Z" --limit 1 --json headSha,createdAt,url
gh api repos/<owner>/<name>/compare/<good-sha>...<bad-sha> --jq '{status, commits: [.commits[] | {sha: .sha[0:7], message: (.commit.message | split("\n")[0]), author: .author.login}]}'
```

## Traps

- Flags after `--` become search terms; keep every flag before it and only negated qualifiers after it.
- An open PR or issue reports `closedAt` as `0001-01-01T00:00:00Z`; a window filter on `closedAt` must skip open items.
- The events API (`/users/<login>/events`) stops at 300 events, a couple of days for a busy account; never use it for a window.
- Agents running with the user's credentials author as the user; the session index in [workspace.md](workspace.md) tells their PRs apart.
- A private security advisory repository (`<repo>-ghsa-*`, not flagged as a fork) replays its parent's default branch, so its commits dedupe against the parent's by SHA and its open PRs are listed as their own items (seen: three advisory repositories returned the same 84 commits as main).
