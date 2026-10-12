# Triage of a bot and human review (illustrative)

The bar for a comment triage: the head and its commit date are stated, staleness is read from the signal each comment type carries (an issue comment a bot edits in place is judged by `updated_at`, not by when it was first posted), every Confirmed or Refuted verdict is pinned to the code at the head or to a probe, and the actions come out ordered by what blocks. The PR, bots, and numbers are invented; the shape is what matters.

---

**PR summary**: #3841 `feat(thread): keep scroll position when a reply regenerates`, head `9f3e2d1` (committed 2026-10-09T14:00:00Z). 9 entries: 4 fresh, 2 stale, 1 resolved, 2 noise (`changeset-bot`, `vercel[bot]`).

| # | Author | Location | Claim (short) | Verdict | Action |
|---|--------|----------|---------------|---------|--------|
| 1 | `maintainer-ana` | `thread-view.tsx:71` | "the scroll effect re-runs on every token" | Confirmed | depend on `messages.length` |
| 2 | `cubic-dev-ai[bot]` | `use-scroll-anchor.ts:27` | "`Math.round` releases the anchor early on fractional `scrollTop`" | Partial | use a tolerance, not the bot's suggestion |
| 3 | `claude[bot]` | `thread-view.tsx:48` | "`viewportRef.current` is null on first render" | Refuted | reply to reject |
| 4 | `cubic-dev-ai[bot]` | issue comment, updated 2026-10-09T15:20:00Z | "the abort path has no test" | Out-of-scope | follow-up issue |
| 5 | `greptile-apps` | `thread-store.ts:134` | "a new array on every token" | Resolved | none |
| 6 | `claude[bot]` | review on `b7a1c40` | summary review | Stale (last seen at `b7a1c40`) | re-trigger |
| 7 | `claude[bot]` | issue comment, updated 2026-10-08T09:30:00Z | "2 issues" | Stale (updated `2026-10-08T09:30:00Z`) | re-trigger |

**Confirmed #1** (`thread-view.tsx:71`, human). The effect depends on `[messages]`, and `appendToken` builds a new array per token (`thread-store.ts:134`). Probe, effect runs while streaming a 200 token reply: 201 on the head, 2 with `[messages.length]`. Fix: `}, [messages.length]);`

**Partial #2** (`use-scroll-anchor.ts:27`). The diagnosis holds: with `scrollHeight` 2000, `clientHeight` 966 and the `scrollTop` of 1033.5 a 2x display reports, `Math.round(2000 - 1033.5)` is 967, above 966, so the anchor releases while the user sits at the bottom. The suggested `Math.floor(el.scrollTop) + el.clientHeight >= el.scrollHeight` still fails there (1033 + 966 = 1999, below 2000). Fix draft:

```diff
-  const atBottom = Math.round(el.scrollHeight - el.scrollTop) <= el.clientHeight;
+  const atBottom = el.scrollHeight - el.scrollTop - el.clientHeight < 1;
```

**Rejected / deferred**
- #3 Refuted: `viewportRef.current` logged at effect entry over 3 mounts on the head was an `HTMLDivElement` each time, and `thread-view.tsx:52` returns early on null anyway.
- #4 Out-of-scope: valid, but the abort path test needs an end to end harness the repo does not have; it deserves its own review.
- #5 Resolved by the author; not re-verified.

**Recommended actions**
1. `thread-view.tsx:71`: change the dependency to `messages.length` (#1).
2. `use-scroll-anchor.ts:27`: apply the tolerance comparison above, not the bot's suggestion (#2).
3. Reply to reject #3 with the probe result.
4. Open a follow-up issue for the regenerate abort test (#4).
5. Re-trigger `@claude`: its review (last seen at `b7a1c40`) and its issue comment (updated 2026-10-08T09:30:00Z) both predate the head.
