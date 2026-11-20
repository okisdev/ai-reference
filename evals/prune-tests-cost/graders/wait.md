---
type: llm
weight: 2
---

The answer finds that every `phones-service.test.ts` test waits out the 5000 ms grace timer because `FakeChild.kill()` never emits `exit`, fixes it by having the fake emit `exit` (or with a fake clock), and declines the suggested retries and 30 s timeout as hiding the cause rather than adopting them.
