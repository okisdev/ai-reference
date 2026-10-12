---
description: verify-pr-comments marks a bot comment edited in place before the head as Stale and judges one edited after the head as Fresh.
tags: [quality, verify-pr-comments]
runs: 2
max_turns: 12
timeout_seconds: 540
allowed_tools: [Skill, Read, Bash]
---

Use the verify-pr-comments skill on this PR. Everything you need is below; do not fetch or run anything.

PR #512 `fix(cart): round totals to cents` in acme/shop. Latest head d4e5f6a, committed 2026-10-09T14:00:00Z (its `.commit.committer.date`). Reviews: none. Inline comments: none. Review threads: none.

Issue-level comments (`issues/512/comments`):
- id 9001, `cubic-dev-ai[bot]`, created_at 2026-10-06T09:05:00Z, updated_at 2026-10-07T09:30:00Z. Body: "1 issue. `src/cart/total.ts:22` rounds each line before summing, so totals drift by a cent on carts with many lines. Round once at the end."
- id 9002, `claude[bot]`, created_at 2026-10-06T09:00:00Z, updated_at 2026-10-09T15:20:00Z. Body: "Issues found. `src/cart/total.ts:29`: `applyDiscount` can return a negative total when the discount exceeds the subtotal. Clamp at zero."
- id 9003, `vercel[bot]`, created_at 2026-10-06T09:01:00Z, updated_at 2026-10-09T14:05:00Z. Body: "Deployment ready: https://shop-git-fix-cart-acme.vercel.app"

`src/cart/total.ts` at d4e5f6a:
```ts
18  export function cartTotal(lines: Line[]) {
19    const sum = lines.reduce((acc, l) => acc + l.price * l.qty, 0);
20    return Math.round(sum * 100) / 100;
21  }
28  export function applyDiscount(subtotal: number, discount: number) {
29    return subtotal - discount;
30  }
```
