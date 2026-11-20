---
description: prune-tests moves unit-provable logic out of an end-to-end test behind a planted regression, keeps the one that crosses a real boundary, fixes a waited-out fake at its cause instead of the retries the user suggests, and names what still guards each deletion.
tags: [quality, prune-tests]
runs: 2
max_turns: 8
timeout_seconds: 240
allowed_tools: [Skill, Read, Bash]
---

Use the prune-tests skill on these tests. Answer from this state only; do not run anything. Give the plan for each test and how you will show nothing lost coverage.

Our desktop suite takes 14 minutes. My idea: add `retries: 2` and a 30 s timeout for the phones tests since they flake on CI, and make every e2e file share one app launch. Durations are from the last run.

```ts
// e2e/window-bounds.spec.ts (5 tests like this, 48 s total)
test('keeps a window on a smaller display', async () => {
  const app = await launch()
  const r = await app.evaluate(({ bridge }) => bridge.clampBounds({ x: 3000, y: 0, width: 800, height: 600 }, { width: 1440, height: 900 }))
  expect(r).toEqual({ x: 640, y: 0, width: 800, height: 600 })
  await app.close()
})

// e2e/terminal-survival.spec.ts (1 test, 21 s)
test('a shell survives relaunch', async () => {
  let app = await launch()
  const pid = await startShell(app)
  await app.close()
  app = await launch()
  expect(await attachedShellPid(app)).toBe(pid)
})

// src/main/phones-service.test.ts (5 tests like this, 25.4 s total)
class FakeChild extends EventEmitter { killed = false; kill() { this.killed = true } }
test('stops a running phone', async () => {
  const child = new FakeChild()
  const service = new PhonesService({ spawn: () => child })
  await service.start('iPhone')
  await service.stop('iPhone') // stop() sends kill(), then waits for 'exit' or a 5000 ms grace timer
  expect(child.killed).toBe(true)
})

// src/export/export.test.ts (0.01 s)
test('legacy exporter is gone', () => {
  expect(existsSync('src/export/legacy.ts')).toBe(false)
})

// e2e/app.spec.ts:88 (6 s)
test('window opens', async () => { const app = await launch(); expect(await app.mainWindowVisible()).toBe(true) })
// e2e/welcome.spec.ts:10
test('shows welcome', async () => { const app = await launch(); expect(await app.mainWindowVisible()).toBe(true); await expect(app.welcome()).toBeVisible() })
```

`clampBounds` lives in `src/main/window-bounds.ts` and imports nothing.
