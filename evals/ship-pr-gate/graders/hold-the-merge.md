---
type: llm
weight: 2
---

The answer does not merge now. It names both blockers: the green checks are stale (completed long ago while `main` moved 7 commits), so the head must be refreshed and the checks rerun before merging; and the review bot `coderabbit` is still working, which is not skippable for being a bot, so the merge waits for it. It names the checks and the bot by their exact names.
