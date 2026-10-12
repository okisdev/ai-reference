# A pass that clears the bar (illustrative)

What the user reads from a good pass: the release posture with its evidence, what went and why, the riskiest removal proven by running code, every site of a changed pattern accounted for, and a ladder whose failures cannot hide. The repository, paths, and counts are invented; the shape is the bar.

---

**Scope**: `packages/sync`, the path the ask named, on `feat/retry-budget`; the tree was clean at the start.

**Release posture**: `@acme/sync` has `private: true`, no tags, and no published artifact (`npm view @acme/sync` returns 404), so nothing is kept for compatibility: the old `createQueue` export and the `legacy` mode are deleted, not aliased, and no changeset is needed.

**Deleted**

- `src/legacy-queue.ts` (212 lines), the `mode: "legacy"` branch at `src/worker.ts:48`, and the 3 tests that only covered that branch
- 9 unused exports in `src/index.ts`, and `src/utils/sleep.ts`
- 11 comments that restated the next line

**Simplified**

- `retry.ts` and `backoff.ts` each carried a copy of the jitter formula; both now import `computeDelay` from `src/retry/delay.ts` (extract)
- `Worker` takes a `Transport` argument instead of importing `http.ts` and `ws.ts`, so `worker.ts` depends on neither (decouple)

**Reused**: `@acme/shared` `delay` replaces `sleep`, and `parseDuration` replaces the two hand-rolled parsers at `worker.ts:71` and `config.ts:33`.

**Skipped**: `src/compat/v1-shim.ts` looks unused but is the documented entry for v1 consumers (`README.md:40`), so it stays.

**Riskiest removal**: the `legacy` branch. It is safe because the default path never reaches it, which a scratch script importing the built entry (`dist/index.js`) showed by running three jobs through a default `Worker` and printing `mode=standard` for each; the only caller that set `legacy` was the deleted test.

**Sweep**: the inline jitter pattern `Math.random() *` had 4 sites. `retry.ts:22`, `backoff.ts:17`, and `scheduler.ts:90` changed; `scripts/bench.ts:5` is skipped because the benchmark must keep a naive baseline. Where grep cannot see: `config.schema.json` still listed `legacy` in an enum, so it was removed and `types.gen.ts` regenerated with `pnpm gen`; no other language or doc in the repository names the mode.

**Docs**: `packages/sync/README.md` lost its legacy section. `AGENTS.md:31` listed the module tree, which the tree already carries, so the line is deleted, not updated.

**Verification**: `set -o pipefail; pnpm --filter @acme/sync typecheck 2>&1 | tail -60 && pnpm lint:fix >/dev/null && pnpm lint 2>&1 | tail -60 && pnpm vitest run packages/sync && pnpm turbo build --filter=@acme/sync` passed: typecheck 0 errors, lint 0 problems, 48 tests passed (51 before; the 3 removed covered only the deleted branch and no other test was touched), build succeeded.

**Tree**: uncommitted, 21 files, +96 / -611. Committing composes `commit-changes`.
