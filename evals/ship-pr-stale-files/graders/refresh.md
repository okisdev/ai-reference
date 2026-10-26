---
type: llm
weight: 2
---

The answer does not merge on the current green: `main`'s newer commit changed `sync/retry.ts`, a file the PR changes, so the head is refreshed (for example with `gh pr update-branch 418`) and the fresh checks are awaited before the gate is read again. It gives that overlap as the reason, not the age of the checks alone.
