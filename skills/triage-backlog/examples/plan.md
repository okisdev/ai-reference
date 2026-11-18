# A plan that clears the bar (illustrative)

This is the bar because all nine open items have one evidence-backed place in a durable plan, and one approval lets each runnable batch finish without repeated permission requests. The repository, numbers, links, and source paths below are invented.

## Plan presented for one approval

Repository: `acme/relay`. Scope: all open issues and PRs, with no label filter. Plan file: `scratchpad/acme-relay-backlog.md`. Carried instruction: ship each fix with `--admin`, including later batches and a resumed `next`. Status at presentation: all nine items are pending; no reply has been posted and no item has been closed or merged.

### Batch 0: close now

| Item | Evidence and disposition | Status |
| --- | --- | --- |
| Issue #11, retry counter never resets | Merged PR #70 added the reset in `src/queue.ts`; the current branch contains it. Close now. | Pending approval |
| Issue #12, queue length stays high after dequeue | Issue #14 already tracks the same count error and has the same reproduction. Close now as duplicate. | Pending approval |
| PR #80, second receipt formatter | Merged PR #74 introduced the same formatter and its tests; this branch adds no remaining behavior. Close now as superseded. | Pending approval |

Draft replies for batch 0, held until approval:

- #11: "The reset landed in PR #70 and is present on the current branch. Closing this as fixed."
- #12: "Issue #14 tracks this same queue count error. Closing this as a duplicate so the discussion stays there."
- #80: "PR #74 already landed the formatter and its tests. This proposal has no remaining change to merge, so I am closing it as superseded."

### Batch 1: fix now, queue handling

| Item | Evidence and disposition | Status |
| --- | --- | --- |
| Issue #13, expired entries stay queued | Reproduces in `src/queue.ts` when an expiry equals the dequeue time; the comparison is exclusive. Fix now. | Pending approval |
| Issue #14, queue length stays high after dequeue | Reproduces in `src/queue.ts` because the removed entry is still counted. Fix now. | Pending approval |

One reviewable PR will fix both issues in `src/queue.ts` and its tests.

### Batch 2: fix now, receipts

| Item | Evidence and disposition | Status |
| --- | --- | --- |
| Issue #15, receipt omits a zero total | Reproduces in `src/receipt.ts` because zero takes the empty-value branch. Fix now. | Pending approval |
| PR #81, receipt label spacing | The contributor's pushable branch changes `src/receipt.ts` and has a failing spacing case to correct. Fix now on that branch. | Pending approval |

The issue fix and PR correction touch the same file, so both land through the contributor's branch as one reviewed PR. Ship it with `--admin` after verification and approval.

### Batch D: needs a decision, never run until answered

| Item | Evidence and disposition | Status |
| --- | --- | --- |
| Issue #17, default retention period | Current behavior is seven days; the request asks for thirty. Both defaults fit the existing implementation, and choosing one changes product behavior. Needs a decision. | Waiting for owner answer |

Decision question: Should new queues keep entries for seven days (current default) or thirty days? I recommend seven days until usage evidence supports a longer default, since thirty days increases retained data for every new queue. Once answered, classify the chosen work in a new runnable batch; do not implement a guess.

### Batch F: follow-up

| Item | Evidence and disposition | Status |
| --- | --- | --- |
| Issue #18, cross-region replay | The request spans storage, replay order, and migration of existing queues. It needs a design and several reviewable PRs. Follow-up with a scoped design for storage ownership, ordering guarantees, and migration before implementation. | Deferred |

Please approve this plan once, or move items between batches in the same reply. Approval will authorize batch 0 and each fix-now batch as presented. Batch D still requires its product answer.

## Report after batch 1

The approved plan file now records batch 0 as complete: #11 was closed ([item](https://forge.invalid/acme/relay/issues/11)), #12 was closed ([item](https://forge.invalid/acme/relay/issues/12)), and #80 was closed ([item](https://forge.invalid/acme/relay/pulls/80)). Their drafted replies were posted after approval.

| Batch 1 item | Outcome and link |
| --- | --- |
| Issue #13 | Fixed in merged [PR #82](https://forge.invalid/acme/relay/pulls/82); [issue #13](https://forge.invalid/acme/relay/issues/13) is closed. |
| Issue #14 | Fixed in the same merged [PR #82](https://forge.invalid/acme/relay/pulls/82); [issue #14](https://forge.invalid/acme/relay/issues/14) is closed. |

Both open-item lists were refreshed after batch 1. No new item appeared, and none of the remaining items changed disposition. The plan file records the outcomes and retains `--admin` for the next batch.

Next is batch 2: fix #15 and correct the pushable contributor PR #81 together in `src/receipt.ts`, then verify, approve, and ship that PR with `--admin`. Batch D remains unanswered, and batch F remains a follow-up. A later `next` reads `scratchpad/acme-relay-backlog.md` and resumes batch 2.

## Why it clears the bar

- Each of the nine open items appears in exactly one batch with concrete evidence for its disposition.
- The user can approve the whole plan in one reply; batch 0 drafts stay unposted until then, and the approved fix batch runs without item-by-item confirmation.
- The plan file preserves statuses, the next batch, and the once-given `--admin` instruction across resumes.
- The batch 1 report names each item's outcome and link, then refreshes the inventory before presenting batch 2.
