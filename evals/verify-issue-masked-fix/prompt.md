---
description: verify-issue does not count a PR as covering an issue when the issue's own repro still fails on its head.
tags: [quality, verify-issue]
runs: 2
max_turns: 12
timeout_seconds: 540
allowed_tools: [Skill, Read, Bash]
---

Use the verify-issue skill on this issue. Everything you need is below; do not fetch or run anything, and treat the repro outputs below as runs you made yourself.

Issue #3310 `sync worker waits hours between retries after repeated failures`, repository acme/sync, main at 4d9c0aa. Body: "When the endpoint is down, the delay between job retries keeps doubling: the 15th failure waits 68 minutes. Repro: `node repro.mjs` runs the worker against a server that always returns 500 under a fake clock and prints the delay before each retry. Expected: capped at 60 seconds. I think `backoff()` should take a max."

Code on main (packages/sync/src):
```ts
// worker.ts
export function backoff(attempt: number) {      // line 12
  return 250 * 2 ** attempt;                    // line 13
}

export async function retryLoop(job: Job) {     // line 40
  for (let attempt = 0; ; attempt++) {
    const result = await run(job);
    if (result.ok) return result;
    await sleep(backoff(attempt));              // line 44
  }
}

// poller.ts
export async function pollLoop(feed: Feed) {    // line 18
  for (let attempt = 0; ; attempt++) {
    if (await check(feed)) return;
    await sleep(backoff(attempt));              // line 21
  }
}
```

PR #3322 `fix(sync): cap retry delay at 60s`, head e1f2a3b, body "Caps the delay between retries at 60 seconds. Fixes #3310." Checks `test` and `lint` pass. Diff:
```diff
--- a/packages/sync/src/poller.ts
+++ b/packages/sync/src/poller.ts
@@ -19,4 +19,4 @@ export async function pollLoop(feed: Feed) {
   for (let attempt = 0; ; attempt++) {
     if (await check(feed)) return;
-    await sleep(backoff(attempt));
+    await sleep(Math.min(backoff(attempt), 60_000));
   }
```
It also adds `poller.test.ts`, which asserts `pollLoop` never sleeps longer than 60000 ms and passes.

Repro outputs, each run twice from a fresh process with identical results:
- main 4d9c0aa: `attempt 8: 64000 ms`, `attempt 12: 1024000 ms`, `attempt 14: 4096000 ms`
- PR head e1f2a3b, in a throwaway worktree: the same three lines
