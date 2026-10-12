---
description: verify-pr pushes back on a fix that quiets the reported symptom while its cause stays reachable.
tags: [quality, verify-pr]
runs: 2
max_turns: 12
timeout_seconds: 540
allowed_tools: [Skill, Read, Bash]
---

Use the verify-pr skill on this PR. Everything you need is below; do not fetch or run anything, and treat CI as green.

PR #771 `fix(config): stop serving stale config after an update`, head 9c1e44b, base 2a7d013, closes #765.
Issue #765: after `updateConfig("theme", "dark")`, pages keep showing the old theme until restart.

Diff (packages/config/src/config-store.ts):
```diff
@@ -40,7 +40,11 @@ export function getConfig(key: string) {
   const hit = cache.get(key);
-  if (hit) return hit.value;
+  if (hit && Date.now() - hit.at < 5_000) return hit.value;
   const value = readFromDisk(key);
   cache.set(key, { value, at: Date.now() });
   return value;
 }
```

Unchanged code in the same file:
```ts
// line 61
export function getConfigSync(key: string) {
  return cache.get(key)?.value ?? readFromDisk(key);
}

// line 88
export function updateConfig(key: string, value: string) {
  writeToDisk(key, value);
}
```
`getConfigSync` is what the page renderer calls.
