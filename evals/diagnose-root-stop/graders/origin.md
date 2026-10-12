---
type: llm
weight: 2
---

The diagnosis names the origin as `src/format.ts` (lines 2 to 5): `new Date("2026-01-15")` is midnight UTC, and the local getters read it in the runner's timezone. It states the mechanism in one sentence (a date-only ISO string is parsed as UTC, and in America/New_York that instant is still the 14th) and treats the two CI failures as the observed reproduction instead of claiming a local one. If it mentions a workaround such as setting the timezone in CI or changing the expected value, it says that only hides the cause.
