# Rejected report

A recap that reads fine and gets overturned by the first count anyone checks. Compare yours against it before posting.

````
Here's a quick summary of what happened last week and yesterday.

You opened around 170 PRs and merged most of them, and reviewed about 170 more. There were 90 failed deployments, mostly builds that were canceled because a newer one superseded them, so nothing to worry about.

Yesterday: I searched GitHub for 2026-10-11 and found no failures. Vercel returned 50 error logs for that day. I redeployed the latest build to confirm it passes now.

Vercel's team API needed a login, so there is nothing there.
````

Why each part fails:

- No heading, no absolute window: `last week` and `yesterday` are never turned into a start and end with the offset of the `Now` probe, so nobody can tell which days the numbers cover.
- `around 170`, `about 170`, `most of them`: estimated numbers; every count is computed from collected records and carries its figure, with no claim without a record link, id, or file behind it.
- `90 failed deployments`: a `state=ERROR` query also returns BLOCKED deployments, which never built; split by `state` and report them apart (seen: 56 of the 90 rows were BLOCKED, leaving 34 failures).
- `canceled because a newer one superseded them`: assumed instead of read; group CANCELED by the reason on the record (seen: 58 of 69 CANCELED records were monorepo skips, not superseded builds).
- `searched GitHub for 2026-10-11`: a bare date is the UTC day, so the search ran over the wrong span and found nothing (seen: a bare date passed to GitHub was a UTC day, so a failure at 00:28 local landed in the wrong day); pass the offset range. A day without failures also searches one window length to each side and names the nearest failure.
- `50 error logs`: 50 is the cap of `vercel logs`, not a count; bisect the window until every slice returns fewer than 50 (seen: a day of error rows silently stopped at 50 whatever `--limit` said, where 24 hourly slices held 173).
- `I redeployed the latest build`: the skill changes nothing anywhere; never rerun, redeploy, promote, or write, and pass `-X GET` to every REST call so a flag cannot turn it into a write (seen: `vercel api -F state=ERROR` was sent as a POST and validated as a deployment create).
- `needed a login, so there is nothing there`: a refused store is a gap, never an empty one; say what stays unknown and what would grant access, and mark the answer provisional.
- No links, no coverage list: the closing list names every store probed with its outcome, its exact window, any cap, aggregate disagreements, and what could not be reached.
