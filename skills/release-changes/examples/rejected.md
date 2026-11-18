# A run that gets overturned by the user (illustrative)

Each line below is a failure a release has shown in real runs, and the whole run reads as done. Compare your run against it.

````
Release requested: "ship the share links (#212) and the offline sync fix (#219)". Working tree has local edits to apps/api/wrangler.toml; deploying anyway.
Deploying every target: db, api, web, docs, marketing, ios.
Ran migration 0043_drop_legacy_slug.sql on production (drops notes.legacy_slug). The api that still reads legacy_slug deploys next.
Deployed api, web, docs, marketing. API_TOKEN=sk_live_9f2c... loaded for the deploy.
Bumped versions to 2.9.0 and merged the PR.
All targets released.
````

Why each line fails:

- `deploying anyway` from a dirty tree: a deploy must be reproducible from a commit, so a dirty tree or a head that is not on the remote stops the run.
- `Deploying every target`: only the targets the release diff touched ship, and docs and marketing had no changes; the rest are listed as skipped with that reason.
- `#212 (share links)` and `#219` never looked up: the run did not check that each named change is in the diff, and #219 was never merged, so it shipped without one of the two changes the user called most important (seen: a release went out without the two changes the user had named).
- `drops notes.legacy_slug` run before the api deploy: a destructive migration runs only after the code that stops depending on it is live, and only after the user's explicit go in this conversation; here the running api broke on the missing column.
- `API_TOKEN=sk_live_9f2c...` in the log: secret values never appear in echoed commands, logs, or files; load them through the repository's mechanism and print nothing.
- `Bumped versions ... and merged`: the bumps must be committed onto the PR branch before the merge, and the merge waits until the deploys succeed, so the shipped version and the merged tree never disagree.
- `All targets released.` with no check behind it: each target needs a health request or real endpoint, a minute of logs, and the migration recorded as applied before the next one starts; no check means no claim, and no rollback point was recorded either.
