# Answer (a behavior question)

The bar for a source answer: the answer first in one sentence, then the rung that proved it, the exact version or ref, and the file and line with the code quoted, and the docs only as confirmation of intent. The version is the project's pin, never the default branch. Reading settled this one, so no script ran; a call that reading cannot settle gets a scratch run, and one that cannot be run is reported as unproven. The package source and line numbers below were read for real; the project that pins `zod@3.23.8` is invented. The report's language follows the user; this structure and density do not change.

---

**Answer.** `z.coerce.boolean()` turns the string `"false"` into `true`. It passes the input through JavaScript's `Boolean()`, so every non-empty string is `true`, `"0"` included, and only the empty string becomes `false`.

**Proof.** Rung L2, upstream source at the tag of the pinned version: `colinhacks/zod` at `v3.23.8`, the version in `pnpm-lock.yaml`. L0 was not available, since this checkout has no `node_modules`.
- `src/types.ts:1750-1754`: `ZodBoolean._parse` runs `if (this._def.coerce) { input.data = Boolean(input.data); }` before it checks the type.
- `src/types.ts:5248-5252`: `coerce.boolean` is `ZodBoolean.create({ ...arg, coerce: true })`, so `z.coerce.boolean()` takes that branch.

**Intent.** The README at the same tag documents it (`README.md:597` to `604`: any truthy value is coerced to `true`, and `schema.parse("false")` is `true`). Docs confirm the intent here; they are not the proof.

**Not used.** The default branch. It is a different version and ships `z.stringbool()`, which `3.23.8` does not contain (no match in `src/types.ts` at the tag), so reading it would describe an API the project cannot import.
