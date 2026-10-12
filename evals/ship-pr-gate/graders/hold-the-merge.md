---
type: llm
weight: 2
---

The answer does not merge now. It names both blockers: the green checks are stale because the newest completed more than an hour ago and `main` has a commit after it, however small that commit is, so the head must be refreshed and the checks rerun before merging; and the review bot `coderabbit` is still working, which the merge waits for even though it is a bot and not a required reviewer. It names the checks and the bot by their exact names.
