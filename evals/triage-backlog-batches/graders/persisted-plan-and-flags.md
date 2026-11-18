---
type: llm
weight: 2
---

The agent actually writes a plan file in the scratchpad and presents one approvable plan, not merely a proposed filename. The file records scope, each item's batch and pending status, the next runnable batch, and the user's `--admin` instruction for every later merge, including after a `next` resume. No batch is executed before approval, and the plan does not ask for separate confirmation on each item once a batch is approved.
