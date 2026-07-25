# Database connections

Exact commands for each connection route, referenced from SKILL.md step 1 onward. Resolve the route before running any query.

## Connection routes

| Route | When it applies | First command |
| --- | --- | --- |
| Neon MCP | The project uses Neon. | `list_projects`, then `get_connection_string`, then `run_sql`. |
| Direct psql | A `DATABASE_URL` exists in `.env`. | Load the env, then `psql`. |
| wrangler d1 | A wrangler config declares `d1_databases`. | `npx wrangler d1 execute <db>`. |

## Env loading

Ad hoc scripts and `psql` need the env loaded explicitly:
```
set -a; . ./.env; set +a
```
Dotenv wiring in the app only covers the app's own entry points, not a command run directly in the shell. Never echo the loaded values.

## psql shapes

List tables:
```
psql "$DATABASE_URL" -c '\dt'
```
Table DDL:
```
psql "$DATABASE_URL" -c '\d <table>'
```
Targeted read:
```
psql "$DATABASE_URL" -c 'SELECT <cols> FROM <table> ORDER BY <col> DESC LIMIT 20'
```

## Drizzle

Compare `packages/*/schema.ts` (or the repo's schema path) against the live DDL from step 2. Push schema changes with:
```
set -a; . ./.env; set +a && pnpm exec drizzle-kit push
```
When the workspace bin misresolves, invoke the absolute bin instead, because the hoisted workspace binary can resolve against the wrong package root:
```
node node_modules/.pnpm/drizzle-kit@<ver>/node_modules/drizzle-kit/bin.cjs push
```

## D1

Remote:
```
npx wrangler d1 execute <db> --remote --json --command "..."
```
Local state lives at `.wrangler/state/v3/d1/miniflare-*/*.sqlite` and answers a different question than `--remote`. Say which environment each result came from.
