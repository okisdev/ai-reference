# A covering PR that does not cover (illustrative)

The bar for an issue that has a PR saying it fixes it: the PR counts as covering only after the issue's own repro ran on its head, the report says whether the head removes the cause or masks the symptom, and the issue's own theory of the cause is tested like any other claim. The issue, PR, and numbers are invented; the shape is what matters.

---

**Issue summary**: #2048 reports that `listAttachments()` still returns an attachment after `removeAttachment(id)`, and proposes bypassing the list cache.

**Method**: the issue's repro (`repro.mjs`: add one attachment, remove it, list) run twice from a fresh process on main `b41f9a0` and on PR #2061's head `7c9d0e2`, the second in a throwaway worktree.

| # | Claim | Result | Evidence |
|---|-------|--------|----------|
| 1 | After `removeAttachment`, `listAttachments()` still returns the attachment | Confirmed | Repro on `b41f9a0` prints `['att_1']` on both runs. `removeAttachment` deletes from `byId` (`attachments.ts:46`) but not from `order`, and `listAttachments` maps over `order` (`attachments.ts:59`). |
| 2 | `listAttachments` needs to bypass its cache | Refuted | `attachments.ts` holds no cache; the store is `byId` plus `order`. Bypassing would change nothing, since the cause is the stale id in `order`. |
| 3 | The attachment stays until the process restarts | Confirmed | `order` is module state, rebuilt only at startup from storage, and `removeAttachment` already deleted it there (`attachments.ts:45`). |

**Prior art**:
- PR #2061 (open, `Fixes #2048`, checks green) does not cover the issue. The repro on `7c9d0e2` still prints `['att_1']` on both runs. The diff filters `removed` stubs inside `useAttachments` (`use-attachments.ts:19`), so the hook hides the entry while `listAttachments()` still returns it: the PR masks the symptom in one consumer and leaves the cause reachable. Its new test mounts the hook and never calls the store, so it passes either way.
- PR #1875 (closed, not merged): bypassed the list on read. Closed with the maintainer's note that `listAttachments` has no cache to bypass, which matches claim 2.

**Conclusion**: valid. The load-bearing claim is that `removeAttachment` leaves the id in `order` (claim 1): run twice on `b41f9a0`, then attacked by looking for any other writer of `order`. There are two, `addAttachment` (`attachments.ts:38`) and the startup load (`attachments.ts:33`), and neither removes. The issue's cache theory is wrong, but the request stands.

**Extra findings**: `countAttachments()` returns `order.length` (`attachments.ts:64`), so it counts the removed attachment too. Read only, not run.

**Possible fix directions**: delete the id from `order` in `removeAttachment` (`attachments.ts:46`), then drop the filter in `useAttachments`, and have PR #2061's test call the store directly. Do not run `/verify-pr` on #2061 as the covering PR; it stays under Prior art until its head passes the repro.
