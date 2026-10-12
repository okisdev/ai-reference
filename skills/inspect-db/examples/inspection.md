# Inspection (illustrative)

The bar for an inspection: the answer first, the route and environment named once and true for every query, bounded queries with the evidence they returned, both sides of every drift quoted, and nothing written or printed that a reader could use to reach the database. The database, host, and numbers below are invented; the shape is what matters. The report's language follows the user; this structure and density do not change.

---

**Answer.** `orders.status` has drifted from the schema and the drift has already produced bad data: the live column is nullable with no default, `packages/db/schema.ts:41` declares it `notNull().default("pending")`, and 3 of 14208 rows hold NULL.

**Route.** `DATABASE_URL` from `.env` through `psql` (probe: `in .env`, ORM marker `drizzle`), host `ep-quiet-glade-a1b2c3.us-east-2.aws.neon.tech`, database `app`, which is the project's dev branch and not production. Read-only; nothing was written.

**Queries** (every one bounded, columns named):
- `\dt` listed 9 tables, `orders` among them.
- `\d orders` returned the live DDL quoted below.
- `SELECT count(*) FROM orders` returned 14208.
- `SELECT status, count(*) FROM orders GROUP BY status ORDER BY 2 DESC` returned pending 9120, paid 4501, refunded 584, NULL 3.
- `SELECT id, created_at FROM orders WHERE status IS NULL ORDER BY created_at DESC LIMIT 5` returned 3 rows, created 2026-09-30 to 2026-10-02.

**Drift**, both sides:

| | Live (`\d orders`) | Schema (`packages/db/schema.ts`) |
|---|---|---|
| `status` | `text`, nullable, no default | `:41` `text("status").notNull().default("pending")` |
| `user_id` index | `orders_user_id_idx` btree (`user_id`) exists | no index declared on `user_id` (`:52-58`) |

**Not determined.** Whether the migration that added `NOT NULL` ever ran on this branch, and whether production shows the same drift; neither was queried. Fixing either side needs `--write`.
