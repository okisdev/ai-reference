---
description: diagnose-root answers a why question with the origin and the mechanism and stops, with no edit and no finished patch.
tags: [quality, diagnose-root]
runs: 2
max_turns: 12
timeout_seconds: 300
allowed_tools: [Skill, Read, Bash]
---

Use the diagnose-root skill: 看看为什么这个测试失败了。

Everything you need is below; do not run anything. CI failed on this test twice with the same output (the second was a rerun of the same commit) and it passes on my laptop, which is in +08:00. CI runs in America/New_York.

CI output:
```
FAIL  src/format.test.ts > formats an ISO date
AssertionError: expected '2026-01-14' to be '2026-01-15'
```

src/format.test.ts:
```ts
import { expect, test } from "vitest";
import { formatDay } from "./format";

test("formats an ISO date", () => {
  expect(formatDay("2026-01-15")).toBe("2026-01-15");
});
```

src/format.ts:
```ts
1  export function formatDay(iso: string): string {
2    const d = new Date(iso);
3    const y = d.getFullYear();
4    const m = String(d.getMonth() + 1).padStart(2, "0");
5    const day = String(d.getDate()).padStart(2, "0");
6    return `${y}-${m}-${day}`;
7  }
```
