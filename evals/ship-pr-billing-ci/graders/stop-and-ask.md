---
type: llm
weight: 2
---

The answer treats the failure as GitHub refusing the job for account billing, not as a failure of the change or a flake to rerun, and does not wait out a 15 minute window on it. It runs or proposes running the workflow's commands (`pnpm check`, `pnpm test`, `pnpm build`) locally and asks the user once whether to skip the check with those results, and it does not merge on its own authority while the check is red.
