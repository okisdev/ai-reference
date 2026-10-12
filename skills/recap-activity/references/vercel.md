# Vercel

## Identity and scope

- Account and teams: `vercel whoami` and `vercel teams ls`; the `id` column is the scope slug, and a check mark flags the current team. Pass `--scope <team>` to every command, because inside a linked directory a command otherwise narrows itself to the linked project.
- Projects and the repos behind them; a team maps to the GitHub orgs in `link.org`, one repo can back several projects, and an unlinked project has none:

```
vercel api "/v9/projects?limit=100" -X GET --paginate --scope <team> --raw > projects.json
jq '.[] | {name, id, repo: (if .link.repo then "\(.link.org)/\(.link.repo)" else null end)}' projects.json
```

- The API takes epoch milliseconds, while `logs`, `activity`, and `alerts` take ISO 8601 with an offset. Convert with `python3 -c 'import datetime,sys;print(int(datetime.datetime.fromisoformat(sys.argv[1]).timestamp()*1000))' 2026-01-15T00:00:00+08:00`.

## Deployments

```
vercel api "/v6/deployments?since=<ms>&until=<ms>&limit=100&state=ERROR,CANCELED" -X GET --paginate --scope <team> --raw > deployments.json
```

- Split the result by `state`. A failed deployment has `state` ERROR. The `state=ERROR` filter also returns BLOCKED deployments, whose commit author has no access to the team; they never build, have no log, and their `errorMessage` is the whole story. CANCELED records carry their reason in `errorMessage` too (most often `the commit didn’t affect this project` or an ignored build step), so group both by it, apart from failures. `errorCode` BLOCKED_PACKAGE is an ERROR, a vulnerable dependency that stopped the build, unrelated to state BLOCKED.
- Narrow with `&app=<project>` and `&target=production` or `&target=preview`; `state` takes a comma list such as `ERROR,CANCELED`. Preview records carry `target: null`.
- `--paginate` follows every page and returns one flat array within `since` and `until`; without it the response is `{deployments, pagination}`, and a non-null `pagination.next` means more pages.
- Fields: `uid`, `name`, `url`, `created`, `state`, `target`, `errorCode`, `errorMessage`, `inspectorUrl`, `source`, `creator.username`, `meta.githubCommitSha`, `meta.githubCommitRef`, `meta.githubCommitMessage`, `meta.githubCommitAuthorLogin`, `meta.githubRepo`.
- Cluster by `name`, `errorCode`, and `errorMessage` with URLs, hashes, ids, and package versions normalized, keeping exit codes, and show one raw message per cluster. A message that only reports an exit code (`Command "..." exited with 1`) hides different causes unless its `errorCode` names one (`out_of_memory`, `BUILD_EXCEEDED_MAXIMUM_TIME`, `BLOCKED_PACKAGE`): fetch the log of every such member and split the cluster by each log's first error line. The sample link is the latest member's `inspectorUrl`.
- The last good deployment before the first bad one, and whether the same project and target (and branch, for previews, through `meta.githubCommitRef`) still fails now:

```
vercel api "/v6/deployments?app=<project>&target=<target>&state=READY&until=<first-bad-created>&limit=1" -X GET --scope <team> --raw | jq '.deployments[0] | {uid, created, sha: .meta.githubCommitSha}'
vercel api "/v6/deployments?app=<project>&target=<target>&limit=1" -X GET --scope <team> --raw | jq '.deployments[0] | {uid, created, state}'
```

## Build log

```
vercel inspect <url-or-uid> --logs --scope <team> > build-<uid>.log 2>&1
grep -n -E 'Error|ERR!|error TS|Module not found|⨯|Failed' build-<uid>.log | head -20
```

The log arrives on stderr and the command exits 1 for a failed deployment; both are expected. The cause usually sits hundreds of lines above the final `Command "..." exited with 1`, so read around the first hit, not the tail. `errorCode` alone settles `out_of_memory` (exit 137; the out-of-memory report prints after the exit line) and `BUILD_EXCEEDED_MAXIMUM_TIME` (the log stops where the build hung).

## Runtime

```
vercel logs --project <project> --scope <team> --since <iso> --until <iso> --status-code 5xx --json > http-5xx.jsonl
vercel logs --project <project> --scope <team> --since <iso> --until <iso> --level error --json > errors.jsonl
```

- `vercel logs` returns at most 50 rows whatever `--limit` says, so a file of 50 rows is incomplete: bisect the window until every slice returns fewer than 50, then merge the slices deduplicated by `id`.
- A runtime failure is a 5xx response, a `--level fatal` row, or an error row that is not a warning. `--level error` also holds whatever a function wrote to stderr, such as Node `(node:N) Warning:` lines, so cluster by message prefix and set warnings apart before calling anything an error.
- Fields: `timestamp`, `deploymentId`, `requestMethod`, `requestPath`, `responseStatusCode`, `level`, `message`, `source`, `environment`, `branch`, `traceId`.
- An empty file means a clean window only once an unfiltered `--limit 3` query shows logs exist in it; retention depends on the plan.

## Team activity and alerts

```
vercel activity --all --scope <team> --since <iso> --until <iso> --json --limit 100 > activity-1.json
vercel alerts --all --scope <team> --since <iso> --until <iso> --json --limit 100 > alerts.json
```

- Use `--project <project>` instead of `--all` for one project, and `--type <type>` to narrow (`vercel activity types` lists them). Page with `--next <pagination.next>` until it is null.
- Events carry `type`, `createdAt`, `text`, and `user.username`; a person's events need the whole team paged, then `user.username` filtered. A person digest keeps event types other than `deployment` and `aliases-assigned`, which mirror merged PRs.
- Alerts return `{groups: [...]}`; anomaly groups belong in a why timeline.

## Traps

- `vercel ls` has no date filter and no error fields; use it only for a glance.
