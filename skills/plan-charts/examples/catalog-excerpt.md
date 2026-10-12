# A catalog that clears the bar (illustrative)

The bar for a catalog: every row names the question it answers, the exact column it reads, what a read-only production query said it would show, and a form chosen by the question; a candidate that production kills is listed with its reason, not drawn. The product and the numbers are invented; the shape is the bar.

---

Audience: staff on an internal ops console. Page in scope: Overview. Production figures come from read-only queries through `inspect-db` over the last 14 full days.

**Runs per day**

- Question: are we handling more or fewer runs than last week?
- Source: `runs.created_at`, fetched and discarded by `getRunCounts()` at `app/page.tsx:41`
- Aggregation: count per UTC day, platform wide and for the ten largest tenants
- Tier: A
- Production says: 300 to 1,900 per day with a weekday swing in every large tenant, so the series is not flat and earns a time form
- Form and place: trend area (the question is "is it changing"), one series in the foreground neutral, in the Overview chart section; a click on a day links to `/runs` filtered to that UTC day
- Fate: restore (removed in the earlier pass, its query still runs)

**Latency tail**

- Question: is the slow end getting worse while the typical request stays fine?
- Source: `request_log.duration_ms`, written at `src/ingest/log.ts:88`
- Aggregation: p50, p95, and p99 per route over 14 days from raw rows, never from `request_daily`, which stores sums
- Tier: B
- Production says: 48,213 rows in the window; p50 1.2 s, p95 8.9 s, p99 31 s; 3% of rows above 10 s, so the tail is real
- Form and place: range bars (p50 to p95 with a p99 tick) in the routes table, ranked by p99 over p50; each row links to the route's trace list filtered above p95
- Fate: new form

**Error rate**

- Question: is anything failing right now?
- Source: `request_log.status`, null on 48,213 of 48,213 rows because `src/ingest/log.ts:88` writes `duration_ms` and never sets it
- Aggregation: not computable today; a tile would read 0.0% forever
- Tier: C
- Production says: no non-null status exists, so the Overview shows "not available" and the call that fills it
- Capture: store the status as `http.response.status_code`, the standard's name; keep `status` accepted on write and returned as an alias on read; migrate stored rows once
- Form and place: tile with window, comparison, and denominator once the capture ships, inverted polarity
- Fate: new form, shipped with the capture

**Not built**

- Requests by provider donut: after folding the spellings `openai`, `OpenAI`, and `open-ai`, 31 of 40 tenants have one provider, so the donut is a single slice for most readers.
- Webhook delivery funnel: `webhook_attempts` has 0 rows in production, so the page shows an empty state that names how to fill it (add an endpoint in Settings) instead of a chart.
