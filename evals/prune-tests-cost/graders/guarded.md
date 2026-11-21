---
type: llm
weight: 2
---

The answer shows how coverage holds before anything is deleted (a plan of these checks passes, since the user asked for nothing to run): it has the new `clampBounds` unit tests fail on a deliberately broken `clampBounds` (a planted regression) before the end-to-end `window-bounds` tests it replaces are deleted (keeping one for the bridge wiring is fine), and it names `welcome.spec.ts:10` as the test that still guards the main window opening when `app.spec.ts:88` is deleted.
