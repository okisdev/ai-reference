# Rejected report

A report that reads fine and gets overturned. Compare yours against it before posting.

````
Issue #2048 says removed attachments still show up in the list. I read `attachments.ts` and the claim looks right.

PR #2061 has `Fixes #2048` and CI is green, so the issue is already covered. Recommend running /verify-pr on it.

The issue suggests bypassing the cache in `listAttachments`, which seems reasonable.

Conclusion: valid issue, covered by #2061.
````

Why each part fails:

- `I read ... and the claim looks right`: a claim about runtime behavior that was only read is a suspicion; run the issue's repro, twice from a reset state, and show its output.
- `Fixes #2048 and CI is green, so the issue is already covered`: a PR covers an issue only after the issue's own repro has run on its head and stopped failing, and a `Fixes` line and green CI are not that evidence (seen: four covering PRs were accepted without running the issue's repro on their head and overturned when the user asked whether they really fixed the root and whether anything was actually tested).
- `Recommend running /verify-pr on it`: that hand-off is for a PR confirmed as covering; a PR whose head still shows the symptom stays under Prior art and the report proposes the fix direction.
- `which seems reasonable`: the issue's own theory of the cause is a claim to test with the same repro; here there is no cache to bypass.
- No table: one row per claim, each with a result (Confirmed, Refuted, Partial, Inconclusive, or Already fixed in `<sha>`) and its evidence.
- `Conclusion: valid issue`: the conclusion names the load-bearing claim and how deeply it was verified, and calls out where the issue's framing was wrong.
- No Prior art: open PRs are listed with their state, and closed ones are read for the reason they were abandoned.
