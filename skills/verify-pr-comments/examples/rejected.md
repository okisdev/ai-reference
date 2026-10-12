# Rejected triage

A triage that reads fine and gets overturned. Compare yours against it before posting.

````
Reviewed all the comments on #3841.

1. claude[bot]: type is redundant. Valid, will apply.
2. cubic-dev-ai[bot]: 5/5 critical, must fix before merge.
3. greptile-apps: stale, it was posted three days ago.
4. changeset-bot: fine.
5. vercel: deployed.

Everything else is fresh. Fix 1 and 2, then it is good to merge.
````

Why each part fails:

- `Valid, will apply`: the claim was taken from the reviewer's quoted snippet; read the file at the head, cross-check what the comment asserts, and apply the suggestion in your head before a verdict.
- `5/5 critical, must fix`: a badge, confidence score, or severity label is not evidence in either direction; the verdict comes from the code path.
- `stale, it was posted three days ago`: age since posting is not staleness. Inline comments are judged by the thread's `isOutdated`, review bodies by `commit_id`, and issue-level comments by `updated_at` against the head commit's date, because bots edit them in place (seen: staleness was misjudged; users said many reviews update one conversation).
- `changeset-bot: fine`, `vercel: deployed`: metadata is counted as noise in the PR summary and never gets a verdict.
- `Everything else is fresh`: no head SHA, no counts, no comment matrix, so nothing says which head the verdicts hold for.
- `good to merge`: whether the PR should merge is `/verify-pr`; this skill reports verdicts and actions.
- No fix drafts, no ordered actions, no bot to re-trigger: the user cannot act on it without redoing the triage.
