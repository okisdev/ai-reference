# Address review threads

Invoked from ship-pr's monitor loop whenever the reviewThreads read returns an unresolved thread.

Every unresolved thread is dispositioned and then resolved (three dispositions, reconciled with the governing rule below).

- **Valid feedback.** Fix in a follow-up commit (`commit-changes` on the plain-git path, `but commit` on the GitButler path, then push), then resolve the thread. The fix commit is already on the PR timeline, so do not add a reply that only points at it.
- **Invalid feedback.** Reply with a short rationale (it carries information the diff does not), then resolve.
- **Outdated thread** (`isOutdated` true). Resolve it; the moved diff is self-evident, so do not reply.

Use judgment on bot nits: common-sense suggestions a competent agent already follows are usually a silent resolve, and scope creep from a long bot-feedback loop is a signal to cut and merge.

ship-pr owns the writes (`verify-pr-comments` is read-only): build the reply body safely with `printf '%s' "$reply" | jq -Rs '{body: .}'` and post it via `gh api repos/$OWNER/$REPO/pulls/<n>/comments/<databaseId>/replies --method POST --input -` (inline `-f body='...'` breaks on backticks and code; databaseId is the REST integer from ship-pr's reviewThreads nodes), and resolve via `gh api graphql -f query='mutation($id:ID!){resolveReviewThread(input:{threadId:$id}){thread{isResolved}}}' -f id=<threadId>` (threadId is the opaque node id, so `-f` not `-F`).

Governing rule: do not add comments or changeset prose that only acknowledge review feedback; the test is, would you write it if no reviewer had flagged the code? If no, drop it.
