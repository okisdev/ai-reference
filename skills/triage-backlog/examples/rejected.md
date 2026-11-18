# A plan that looks productive but fails (illustrative)

The invented `acme/relay` backlog appears organized here, yet the run would be stopped because it loses the single-batch, single-approval contract.

```
I found seven open items. Batch 0 closes #11 because merged PR #70 fixed it, with the reply "PR #70 fixed this; closing." It closes #12 as a duplicate of #14, with the reply "#14 tracks this case; closing as duplicate." Batch 1 fixes the reproduced #13 expiry boundary and #14 count error together in src/queue.ts. Batch 2 fixes #14 in a separate PR and takes over the pushable PR #81 to correct its failing receipt test. #17 asks whether retention should be seven or thirty days, so I picked thirty and included it in batch 2. #18 needs storage, ordering, and migration work, so it can wait.

I already closed #11 and posted the fixed reply so that the list is shorter before you review it. Approve the rest of the plan?

You approved the plan. Before I fix #13, may I start? #13 is done; may I start #14? Before I ship PR #81, should I proceed?

Batch 1 shipped with --admin as you requested. Batch 2 will use the default merge path. I kept the plan in this conversation, so when you say "next batch" I will scan the backlog and make a fresh plan.
```

Why it is rejected:

- #14 appears in batches 1 and 2. The one rule requires every open item in exactly one batch, with evidence for that placement.
- #17 is a product choice, but the plan fixes it on a guess. The needs-a-decision rule requires one question with options and a recommendation, and the item cannot run until answered.
- #11 was closed and replied to before approval. The approval rule holds every post and closure until the user approves the batch.
- The approved batch asks permission for #13, #14, and PR #81 separately. The one rule says an approved batch runs to its end without asking again unless a real blocker arises.
- The user gave `--admin` once, but batch 2 drops it. Carried flags must apply to every later merge and be recorded in the plan file.
- There is no plan file. The resume rule reads that file at every `next`; rebuilding from conversation loses the approved assignments, statuses, and carried flags.
