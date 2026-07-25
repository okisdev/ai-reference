# Verify ladder

Run typecheck, then lint fix, then lint, then the narrowest test run covering the change, then build, chained with `&&` so the first failure stops the chain. Scope each rung to the touched package with `--filter` on pnpm workspaces.

## pnpm workspace commands

- Typecheck: `pnpm --filter <pkg> typecheck 2>&1 | tail -60`
- Lint fix: `pnpm lint:fix >/dev/null`
- Lint: `pnpm lint 2>&1 | tail -60`
- Narrowest test: `pnpm vitest run <file>`
- Build: `pnpm turbo build --filter=<pkg>`
- Chained: `pnpm --filter <pkg> typecheck 2>&1 | tail -60 && pnpm lint:fix >/dev/null && pnpm lint 2>&1 | tail -60 && pnpm vitest run <file> && pnpm turbo build --filter=<pkg>`

Always truncate with `tail` because full output floods the transcript.

## Failure decode

| Symptom | Meaning | Fix |
| --- | --- | --- |
| `ERR_PNPM_RECURSIVE_RUN_FIRST_FAIL` | The recursive run masks which package failed | Rerun per package with `--filter` to expose it |
| `Cannot find module '@<scope>/<pkg>'` right after editing that workspace package | The workspace dependency's dist is stale | Build the dependency first with `pnpm turbo build --filter=<dep>`, then run typecheck again |
| pnpm re-resolves dependencies mid-run and aborts | The verify-deps preflight is interfering | Prefix the run with `PNPM_CONFIG_VERIFY_DEPS_BEFORE_RUN=false` |
| `ERR_PNPM_ABORTED_REMOVE_MODULES_DIR_NO_TTY` | pnpm wants a TTY to confirm removing `node_modules` | Run the install or removal in a real terminal, or pass an explicit yes flag where supported |

## Non-workspace repos

Fall back to the root scripts in the same order: `npm run typecheck`, `npm run lint`, `npm run test`, `npm run build`. Skip a rung the repository does not define and say so in the report.
