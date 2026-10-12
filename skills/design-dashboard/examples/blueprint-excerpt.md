# A blueprint that clears the bar (illustrative)

The bar for a blueprint: a verdict the user can disagree with in three short paragraphs, a diagnosis in measurements pinned to `file:line`, every fork decided on the spot with its basis, the gain stated in numbers, and the open decisions batched with a recommendation each so one reply settles them. The console below is invented and the excerpt skips sections 4 to 8 and 10; the shape and the density are the bar.

---

**1. Verdict**

The console shows what the product knows and lets nobody act on it: 9 of its 12 views are aggregates with no queue, no filter that survives a reload, and no row that links anywhere.

The direction is a decide-first console: three queues (approvals, failed runs, expiring keys) as the entry, every dimension a filtered link, and the aggregates folded into one proof page.

Most of the return is cheap: ten of the twelve pages change only through four shared primitives, and the two queues need one endpoint each. The earlier pass was right to chase charts and wrong about their form: it drew a donut for a mix that is one slice for most tenants.

**2. Diagnosis in measurements** (`scripts/density.mjs apps/console`, judged against the contract in `apps/console/AGENTS.md`)

| Measure | Found | Contract | Where |
|---------|-------|----------|-------|
| Body size | 14px | 13px | `app/globals.css:6` |
| Table row height | 44px | 32px | `components/ui/table.tsx:31` |
| Hand-styled panels | 37 | 0 | `rounded-xl border bg-card p-6`, in 21 files |
| Shadow classes / transition-all | 22 / 41 | 0 / explicit property lists | project wide |
| Content widths | 3 (`max-w-5xl`, `max-w-4xl`, none) | 1600 / 880 / 560 | page files |
| Rows per screen, busiest list, 1440x900 | 11 | follows from the row height | `/runs` |

URL state: 6 of 8 lists keep their filters in `useState` (`app/runs/page.tsx:58`), so a copied URL never reproduces the view. Existence: the `/usage` trend reads `usage_daily`, which holds 0 rows in production (read-only `select count(*)`), so the trend is deleted and the page carries an empty state that names the call that fills it (`app/usage/chart.tsx:14`). Dead code from the earlier pass: `UsageDonut` and a discarded `getProviderMix()` result at `app/page.tsx:41`.

**3. What each reference contributes**

| Reference | Take | Not take | Direction |
|-----------|------|----------|-----------|
| `../billing-console` (sibling, same stack) | Page skeleton, URL state, the kit port | Its sidebar grouped by measure | Moved lists from tabs to a volume strip on 2026-08-14 (`a1b2c3d`) |
| `acme/atlas` | Filter bar order and the queue grammar | Its serif face and tinted ground | Dropped its right rail in 2026-09 (`d4e5f6a`) |

**9. Fork decisions**

- Font: keep the app's sans; atlas's serif belongs to its brand, and the contract sets one body base.
- Detail: a page, not a drawer, because a trace needs the full 1200 px; the drawer serves only previews from a queue row.
- Rendering engine: the kit's own rows for list forms and the installed charting library for the one trend area; the sibling's unfinished chart package does not enter production until its owner says so.
- Time range: one range per page in the URL, as UTC days.

**11. Quantified gain**

Rows per screen on `/runs`: 11 to 19. Content width on `/runs` at 1440x900: 1024 to 1216. Tiles that carry a trend: 0 of 6 to 6 of 6. Hairlines in the busiest panel: 14 to 3.

**12. Open decisions**

1. Does the anonymous status page keep its run counts? Recommend no: it shows more than the signed-in console does today, which is a defect.
2. Are approvals in this pass? Recommend yes: one endpoint (`POST /approvals/:id`) and the queue page, with its audit event.
3. Does the sidebar become resizable? Recommend fixed: nothing in this console needs the width.

**Wireframe**, `/runs` at 1440x900, 3 ruled objects (stats grid, volume strip, table):

```
 Runs                                                          last 14 days
 | Runs, 14d  13,870  +9% | Failed, 14d  412  -12% | p95, 14d  8.9s  +3% |
 [search]  [status v]  [project v]  [range v]                       clear
 ▁▂▃▅▃▂▇▃▂▁▂▃▅▃                      volume strip, click a day to filter
 ID         Project    Status    Duration    Cost [not yet real]    When
 run_8f2a   billing    failed    31.2s       $0.42                  4m
 run_8f29   sync       passed    2.1s        $0.01                  4m
 ...
```

Each tile's delta is against the previous 14 days. The cost column is computed from the rate card in the UI because the ledger has no cost column, so its head carries the marker until the seam exists.
