# Rejected report

A reply that looks thorough, leaks the key, and writes to a database nobody asked it to change. Compare yours against it before replying.

````
Connected with postgresql://app_owner:<password printed in full>@db.dev.acme.internal:5432/app and ran `SELECT * FROM orders;` (14208 rows, pasted below).

The Drizzle schema declares `status` as NOT NULL, so there can't be any NULL statuses. To be safe I ran `UPDATE orders SET status = 'pending' WHERE status IS NULL;` and it's clean now.
````

Why each part fails:

- The full connection string with the password: credentials never appear in output; name the host or project and nothing else (seen: a connection string pasted in a prompt).
- `SELECT * FROM orders;` pasted below: a whole table in the transcript; always `LIMIT`, and name the columns when a row is wide.
- `declares status as NOT NULL, so there can't be`: reasoning from the ORM schema instead of the live database; the schema file is what the code expects, the live DDL is what exists, and the diff between them is the finding.
- The `UPDATE`: a write with no `--write` and no explicit ask, and with no `SELECT` of the same rows and their count first; a mutation is followed by a second `SELECT` that proves the effect, and `it's clean now` shows no count at all.
- No route and no environment: the reader cannot tell whether this was the dev database or production.
- No drift reported: the live DDL and the schema line are never quoted side by side.
