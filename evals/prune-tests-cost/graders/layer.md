---
type: llm
weight: 2
---

The answer moves the `clampBounds` cases of `window-bounds.spec.ts` into a unit test, keeping at most one end-to-end test for the debug bridge path, and keeps `terminal-survival.spec.ts` with its own launches because surviving a quit and relaunch crosses a real process boundary; it does not adopt one shared app launch across every e2e file as the main fix.
