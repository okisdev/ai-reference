# The catalog and the grammar artifact

## Catalog row

Every candidate metric carries these fields; a row missing one is not a candidate yet.

| Field | Content |
|---|---|
| Metric | Name as it will appear |
| Question | The one question it answers, in the reader's words |
| Source | Exact `table.column` or event kind, verified by reading, never guessed |
| Aggregation | One line at SQL level (group by, window, denominator) |
| Tier | A data in hand (already fetched or one import), B one endpoint or query over an existing rollup, C a new field or capture designed per [capture.md](capture.md) with the standard that defines it named as the source when one exists, D a new dataset or deferred with the reason |
| Production says | The numbers a read-only query returned today (range, distribution, null rate, cardinality) and what they imply for the form |
| Form and place | From the question to form table; page, position, and what it links to |
| Fate | keep, restore, new form, do not build (with reason) |

Tiers decide order: A ships in the first batch, B in the second, C only with the capture, D never in this pass.

## Production evidence queries

Run read-only through `inspect-db` against the repository's own connection, and name the window. Recipes:

- Volume shape: count per day over the last 14 full days, platform wide and for the ten largest tenants; a flat line means no time series form.
- Reality of a status: count by status all time and in the window; a status the API never writes reads zero forever.
- Cardinality per tenant: distinct values of the grouping column per tenant in 30 days; one or two for most tenants means no donut.
- Spelling variants: distinct raw ids that fold to one canonical id; fold before charting.
- Distribution: percentiles (p50, p95, p99) and the share above a threshold from raw rows; a real shape earns a histogram.
- Composition: sums per part in the window; informative when no part dominates.
- Retention inputs: first seen per user against activity per day; a stacked area of new versus returning.
- Emptiness: row counts of every table a candidate would read; zero rows in production means an empty state, not a chart.
- Rhythm: count by hour of day for the largest tenant; a strong swing earns a heatmap, last.

## Removal table (with `--restore`)

One row per visual that existed at the base: what it was, page, fate at head (removed, restyled, orphaned file, query still running), what was lost in one sentence, and how it returns (restore, new form, keep, do not build). Orphaned files and discarded query results are named and deleted in the same change if they do not return.

## Grammar artifact

Published as an artifact, revised in place. Sections in order:

1. Verdict: what the previous pass got right and wrong, what charts are for on this surface (a compact index that leads to a filtered list), and where the return is cheap.
2. Removal table (restore runs only).
3. Production evidence: fact, numbers, implication for the chart layer.
4. The grammar: the rules the surface adopts, written to sit beside the repository's design contract (form follows the question; drawn on the page as a section with a fixed height and a trailing sentence; one time axis; hue by entity; every mark is a link; line budget; alignment; empty is drawn).
5. Page by page: for each page, the question it answers in its title, the tiles, the chart or strip, the rail, and a wireframe drawn from the real series with a caption naming the viewport and the count of ruled objects.
6. Not built: every candidate killed, with its reason.
7. Batches: kit and exemplar page, then breadth pages, then detail pages, each with its verification.
8. Status: what is implemented, what verification is still owed.

## Batch verification

- Typecheck, lint, and build across every package.
- Every new SQL shape executed read-only through `inspect-db` against the named staging or production connection.
- A browser pass per batch through `verify-ui`: scrub a sparkline, toggle a legend, click a strip day, change the range and the zone, both themes, and the empty variant.
- Thin staging data is seeded with variety (many tenants, providers, id spellings, outcome mixes) through the app's own seed script or `inspect-db --write` against the staging connection named by host, never production, before a chart page is judged.
- Synthetic or demo data is labelled, forward-only, and never backfilled history.
- The handoff names the surfaces not verified.
