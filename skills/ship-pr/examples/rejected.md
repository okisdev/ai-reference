# A run that gets stopped by the user (illustrative)

Each line below is a failure ship-pr has shown in real runs. Compare your run against it.

````
Opened #418. Waiting for CI...
(9 minutes of silence)
Still pending.
lint failed; pushed a fix. Pushed the thread fix too.
The review bot is still running, but bots are optional, so skipping it.
All checks green (they finished yesterday). Merging with --admin.
gh pr merge exited 1: failed to delete local branch. The merge failed.
````

Why each line fails:

- `Waiting for CI...` then silence: every tick names each pending item, its age, and whether it is alive (seen: users asking to check CI after 5 to 30 silent minutes).
- `Still pending.`: an item that is pending but no longer moving is different from one still running; say which.
- Two pushes in a row: each push cancels and restarts every run and review on the head; commit locally and push once the head settles.
- `bots are optional, so skipping it`: a pending review bot is not skippable because it is a bot (seen: merges that went in while a review bot was still running).
- `they finished yesterday`: a green that completed more than an hour before the base moved is stale; refresh the head and wait for the fresh run (seen: an old green let a logically conflicting merge land red on the default branch).
- `Merging with --admin` when the user never passed it: `--admin` is the user's call for this request, and on another author's PR it comes only after the approval path, for what an approval cannot clear (seen: `--admin` merged another author's PR past its review requirement when nobody had asked for it).
- `The merge failed.`: `--delete-branch` can fail after the merge succeeded; confirm the outcome from `gh pr view <n> --json state,mergedAt`.
