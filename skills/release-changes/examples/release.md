# A run that clears the bar (illustrative)

What the user sees from a good run: the release diff fixed first with both named changes found by PR, untouched targets skipped, one ordered plan shown once, a rollback point recorded before the first production write, and every target proven live before the next starts. Names, versions, and SHAs are invented; the shape is the bar.

The invented monorepo `acme-notes` has `apps/api` (a worker), `apps/web`, `packages/db` (migrations), and `apps/ios`. The user said: "release this, it must include the share links (#212) and the offline sync fix (#219)."

````
Mode: release. Tree is clean, head 9d4e1b7 is on origin/main. Last tag v2.8.0. RELEASING.md names the order and the commands; following it.
Release diff v2.8.0..9d4e1b7: 31 commits. #212 (share links) is in as merge 5a02c8e. #219 (offline sync fix) is in as merge e7f3b91. Both named changes are present.
Targets: packages/db changed (migration 0042_add_share_token.sql, adds a nullable column), apps/api changed, apps/web changed, apps/ios changed. Skipped: apps/docs (no changes since v2.8.0), apps/marketing (no changes since v2.8.0).
Plan, shown once:
  1. db: apply 0042_add_share_token.sql (additive, runs before the code that uses it).
  2. api: deploy the worker.
  3. web: deploy after api, because it calls the new /shares endpoint.
  4. ios: archive and upload the build after the api is live.
Rollback points recorded: api deployment 7c1d (v2.8.0), web deployment 3b90 (v2.8.0), db at migration 0041, ios build 214 stays live until review passes.
verify-pr cleared head 9d4e1b7. Bumped api, web, and ios to 2.9.0 in the PR branch, changelog entry keyed to 2.9.0, committed as 2c8a5d4. docs and marketing keep their versions.
db: applied 0042 with the repository's migrate script, secrets loaded through its secrets wrapper. Checked: migration table lists 0042 as applied, `share_token` exists and is nullable.
api: deployed as 2.9.0 (deployment f41a). Checked: GET /health returns 200 with version 2.9.0; a minute of `wrangler tail` shows 0 new errors; POST /shares returns a token.
web: deployed as 2.9.0 (deployment a96e). Checked: the home page and a share link return 200; a minute of logs shows 0 new errors.
ios: build 2.9.0 (215) uploaded through upload-testflight and processed in TestFlight.
Merged the PR with ship-pr after the deploys succeeded (merge commit 6b13f0e).
Report:
  db: shipped, migration 0042 applied, rollback is revert plus a down migration (column is additive).
  api: shipped 2.9.0, live check passed, rollback to deployment 7c1d.
  web: shipped 2.9.0, live check passed, rollback to deployment 3b90.
  ios: shipped build 215 to TestFlight, previous build 214.
  docs, marketing: skipped, no changes in the diff.
  Time, 37 min total: review and fixes 9, verification 1 run 11, db 1, api 3, web 3, ios archive and upload 6 (beside web), TestFlight processing 8, merge 2. Longest: verification.
````

Why it clears the bar:

- The release diff is fixed from the last tag and both changes the user named are confirmed by their merged PRs before anything ships.
- Only the targets the diff touched ship; the two untouched ones are listed as skipped with the reason.
- The additive migration runs first, the api before the web app and the app build that call its new endpoint, and the plan is shown once before the first production write.
- Every rollback point is recorded before the first production write, so a failed check has somewhere to go.
- Each target is proven live with its own check (health request, a minute of logs, migration applied) before the next one starts.
- The version bumps ride inside the PR that merges, and the merge comes after the deploys succeed.
- No secret value appears anywhere in the log.
- The report closes with each phase's wall time, so a slow release shows where its time went.
