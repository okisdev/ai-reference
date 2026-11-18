---
description: A complete invented backlog tests exclusive batches, approval boundaries, decision handling, and carried merge flags.
tags: [quality, triage-backlog]
runs: 2
max_turns: 8
timeout_seconds: 240
allowed_tools: [Skill, Read, Bash]
---

Please triage all open issues and PRs in the invented repository `acme/relay`. Ship each with `--admin`. I want one plan I can approve, then I will ask for the next batch. Write the plan to a file in a scratchpad path and show me its contents. No batch has been approved yet, so do not post replies, close items, or merge anything. Use only the facts below. There is no network or repository checkout.

The list below is the complete open inventory. Each link uses the invented host `forge.invalid`. There are no other open items and no issue-to-PR closing references among these seven items.

- Issue #11, retry counter never resets, https://forge.invalid/acme/relay/issues/11. Merged PR #70 already added the reset and its test to the current default branch. It can be closed as fixed.
- Issue #12, queue length stays high after dequeue, https://forge.invalid/acme/relay/issues/12. Issue #14 already tracks the exact reproduction and is the canonical report. #12 can be closed as a duplicate.
- Issue #13, expired entries stay queued, https://forge.invalid/acme/relay/issues/13. The expiry comparison in `src/queue.ts` excludes the exact boundary. A small change and test fix it; no product choice is needed.
- Issue #14, queue length stays high after dequeue, https://forge.invalid/acme/relay/issues/14. `src/queue.ts` still counts a removed entry. A small change and test fix it; no product choice is needed.
- PR #81, receipt label spacing, https://forge.invalid/acme/relay/pulls/81. The contributor's branch is pushable, changes only `src/receipt.ts` and its test, and needs a small correction before verification and shipping. It is independent of #13 and #14.
- Issue #17, default retention period, https://forge.invalid/acme/relay/issues/17. The current default is seven days; the request proposes thirty. Either is technically valid and changes product behavior. Only the owner can choose; recommend seven days until usage evidence supports longer retention.
- Issue #18, cross-region replay, https://forge.invalid/acme/relay/issues/18. This real feature spans storage ownership, ordering guarantees, and migration of existing queues. It cannot fit one reviewable PR and needs a scoped follow-up.

The repository accepts a single reviewed PR for related fixes, and the contributor allows maintainers to push to PR #81. Draft closure replies for #11 and #12. Keep the decision item out of runnable work. Show the batch order and the exact state a later `next` will resume, including my `--admin` instruction.
