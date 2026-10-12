# Rejected report

A pass that reads fine and gets sent back. Compare yours against it before reporting.

````
Cleaned up the sync package. Removed some unused code and refactored the worker to be more modular. Kept the old createQueue export as a deprecated alias so nothing breaks, and added lodash for the retry math. One flaky test kept failing so I skipped it. Ran `pnpm typecheck | tail -20` and it looks fine. Committed as "refactor: cleanup".
````

Why each part fails:

- `Cleaned up the sync package. Removed some unused code`: no list of what was deleted, simplified, reused, and skipped, each with its reason; the report is the only way the user can review a refactor.
- `refactored the worker to be more modular`: no read of the scope's idiom or prior art first and no nearest precedent cited by file, so it is an ad hoc edit rather than the pass (seen: asks to extract, decouple, and refactor went ad hoc in 34 sessions).
- `Kept the old createQueue export as a deprecated alias`: a package with `private: true`, no tags, and no published artifact gets no alias and no shim; delete instead, and state the evidence for that posture in the report.
- `added lodash`: no new dependencies during an optimization pass, and the repository's own helpers come first.
- `One flaky test kept failing so I skipped it`: failing tests are never weakened or skipped to make verification pass; a flaky test is a finding to report.
- `pnpm typecheck | tail -20` and `it looks fine`: without `set -o pipefail` the pipe reports tail's exit status, so a failing typecheck passes, and the other rungs of the ladder never ran (seen: the ladder piped checks into tail and hid failures until `set -o pipefail`).
- No riskiest removal and no sweep: no safety fact was proven by running code, and the repeated pattern was fixed at one site while its other sites still carry the copy.
- `Committed as "refactor: cleanup"`: the pass stops at an uncommitted validated tree; committing composes `commit-changes`.
