---
type: llm
weight: 2
---

The answer merges PR #512 directly with `--admin` and `--match-head-commit 4c1d9e2` (for example `gh pr merge 512 --squash --admin --match-head-commit 4c1d9e2`) instead of putting it in the merge queue or waiting for the queue, and it names the review requirement as what `--admin` bypassed. An answer that enqueues the PR, waits for the queue, or asks whether to use `--admin` fails.
