---
name: draft-reply
description: Read an issue, pull request, or chat thread, work out what the other side is asking against the code, and draft a reply in the user's voice to approve before it is sent, then send it and close, request changes, or file the follow-up, when asked to draft, write, or answer a reply, or to write the review summary for a PR's author after its fixes landed.
argument-hint: "<issue-pr-url|thread> [stance...]"
---

## Context

Repository: !`gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null || echo "unknown"`
My login: !`gh api user --jq .login 2>/dev/null || echo "unknown"`

## Instructions

**The one rule: nothing is sent until the user approved this exact draft, and the draft says what the user decided, not a softer version of it.** A great run reads the whole thread and checks each ask against the code before drafting, puts the verdict first and the reason after it, fits the channel's format and the user's register, and after approval sends, takes the follow-on action, and reads the result back. Open [examples/github.md](examples/github.md) or [examples/chat.md](examples/chat.md) before drafting and check the draft against [examples/rejected.md](examples/rejected.md).

### Process

1. Parse `$ARGUMENTS`: the target (an issue, pull request, or discussion URL; a chat thread named by person or channel in whatever messaging tool the session exposes; or text the user pasted), the stance the user gave ("close it, we won't support this", "thank them and say it is tracked"), and the action after sending (close, request changes, approve, open a follow-up issue). Without a stance, step 3's findings become a recommended stance the user confirms with the draft.
2. Read the whole thread, not the last message: for GitHub, every comment and review, the linked issues and pull requests, and the author's other issues and pull requests in this repository (`gh search issues --repo <o>/<r> --author <login>`, the same for prs), because a reply that ignores an earlier exchange reads as not listening (seen: a closing reply was asked to account for the comments already sent on the author's earlier issues); for a chat thread, back to where the topic starts.
3. Work out what is being asked: list the explicit asks and the implied ones, and check each against the tree, the git history, and open or merged pull requests: done (with the commit or PR link), in progress (with the PR), or not started. Report this to the user in the user's language before the draft, because it may change the stance.
4. Draft the reply:
   - The stance as given, its verdict in the first sentence (thanks come after it, never before), then the technical reason in one or two sentences; no promise or invitation the user did not make, because a maintainer's invitation is a commitment others act on.
   - The register the user's instruction files set for that platform, and otherwise the thread's own language and tone; a chat reply reads like a person talking, short and unheaded (seen: the user rejected drafts for a teammate as far too formal).
   - The channel's format: GitHub markdown with links to code and pull requests; Slack mrkdwn (`*bold*`, bullets, no headings); plain short text for a phone message.
   - No trace of tooling and nothing from other private threads.
5. Show the draft unsent, saying plainly that nothing has been sent and that it waits for the user's approval, with the target, the action that follows sending, and the exact command or tool call that will send it. Revise on feedback until the user approves.
6. On approval, send and act: `gh issue comment` or `gh pr comment --body-file -`; `gh pr review --request-changes --body-file -` when the action is request changes; a follow-up issue is created first and its link put in the reply; then `gh issue close --reason <completed|not planned>` or `gh pr close` when the action is close. A chat reply goes through the messaging tool's send call. Read the posted comment or sent message back and report its link.

### Takeover review

A review body for a PR whose author's code you changed (the shape `approve-pr` and `ship-pr` ask for, and an ask to summarize the review after fixes) follows the same voice with one more rule: **say only what the diff cannot.** Find the author's baseline and diff it against the head per [references/takeover-review.md](references/takeover-review.md), then write a message to the author, not a report: the verdict and the one reason it holds, then the judgment the patch does not show (why this approach beat the one it displaced, what you ran and what it printed, the trap the next reader falls into), in prose with no headings, numbering items only when the author has several to act on separately. Separate what you executed (the command and its real output) from what you only read, which is a suspicion, not a finding. Open the closer of [examples/review-clean.md](examples/review-clean.md) and [examples/review-blocking.md](examples/review-blocking.md) and check against [examples/review-rejected.md](examples/review-rejected.md). When `approve-pr` or `ship-pr` asked for it, return the body to that caller to post with its review instead of holding it for approval, because the caller already holds the user's go (seen: a body held for confirmation inside a ship run, and the user saying to post it with the approval).

### Rules

- Never send, close, or request changes without the user's approval of this draft in this conversation, except a takeover review body returned to the `approve-pr` or `ship-pr` run that asked for it.
- Never change the user's stance; if the findings contradict it, say so before the draft and let the user decide.
- A reply never quotes or reveals another private conversation.
