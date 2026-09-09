# Form follows the question

The question picks the form; the data's shape never does. A table answers "what happened" and cannot answer "is anything different today", so a page of key/value rows answers only the first question. Generic chart hygiene (dual axes, pies, palette contrast per theme) is checked through `dataviz`; this file adds only what the question decides.

## Question to form

| Question | Form | Notes |
|---|---|---|
| Is it changing | Trend area | One series takes the foreground neutral; five date ticks, four grid lines, mono axis |
| Is the mix changing | Stacked trend area | Hue by part, fixed order everywhere the parts appear |
| Is anything spiking above this table | Volume strip | Directly above the table; a click writes the bucket into the URL and filters the table |
| What is the mix now | Share bar with a ranked ledger | Replaces the donut; the bar is a column beside its label, never a track beneath it |
| Which is biggest | Category bars | Ranked; top n plus "Other" folds the tail to a fixed height |
| What is the shape of the population | Histogram | Reference lines for p50, p95, p99 in the trailing slot |
| Trend at cell scale | Sparkline | 96 by 24, scrubbable; only where a real per-bucket series exists |
| How close to the limit | Meter | Two stops (included, limit), status tone only; one per capacity |
| When, across two dimensions | Heatmap | Weekday by hour is a second order question, last |
| A person's year | Activity calendar | One import, 365 days |
| How concentrated | Concentration curve | Top k of n carry x percent in the trailing slot |
| Where the funnel loses | Funnel steps | Uniform rows (label, bar, count, share); no per-step prose |
| What moved a total | Waterfall | |
| Two quantities across orders of magnitude | Log or log-log scatter | Any metric spanning three or more orders of magnitude gets a log axis by default |
| Cohorts | Retention grid | |
| Hierarchy at scale (host, namespace, instance) | Treemap or icicle | Over a node graph once the count passes a few dozen; re-judge with real density |
| Spans on a time ruler | Trace view | Name, proportional bar, duration; hue by kind; one grammar for every trace on the site |
| Is the tail bad while the median is fine | Range bars | p50 to p95 bar with a p99 tick; a row form sharing the row grammar |
| What moved per row between two periods | Dumbbell bars | Previous and current dots with a connector toned by direction |
| How a judgment splits per row | Diverging stacked bars | Negative left, positive right, neutral centred, ranked by net |
| Where a share of one kind concentrates within another | Marimekko | Width is the share, fill is the outcome |
| Did the composition change, independent of volume | Normalized stacked area | A variant of the trend area, never a second component |
| Slower at peak, tail and bimodal at once | Latency heatmap (period by duration bucket) | Aggregated in SQL, never sampled |
| A sparse integer series | Sparkbar | A line through 0, 1, 0, 2 is lying |
| Did a change matter (a model switch, a setting) | Event marks on a trend area | From the audit log; an annotation lane, not a form |
| A count with no comparison | Key/value row | Not a tile |

## Rejected forms and why

- Donut or pie when most groups collapse to one or two real slices (check id spelling variants before trusting the slice count).
- Dot matrix or any form that quantizes magnitude away (one dot per period hides a tenfold change).
- A two-point sparkline; a trend needs a real per-bucket series.
- A metric switcher that hides two of three answers behind a click; small multiples instead.
- Logos or icons inside a chart; identity lives in the row.
- A node graph for a strict hierarchy at scale.
- A percentile band drawn from three static percentiles with no time series.
- A chart column repeating a value the page is already scoped to.

## Expanding the vocabulary

- When: a question no form in the kit answers well (answered today by a number or a stacked curve), or the user asks which forms exist that the product has not used.
- Survey order: sibling kits on the same stack for forms never ported, each checked for an existing data source; the organization's own chart library, even unfinished, for its taxonomy and coverage classification (scales, annotations, host properties, compositions, costumes, genuinely new forms); then the world taxonomy by question family: time, magnitude and rank, part to whole, distribution, correlation, deviation and change, flow and relation, retention, spatial.
- Deliver the cross-check as one table: question family, have, worth adding, not applicable, with a reason per cell.
- Admission: a form enters only for a question a current page answers badly, never for variety; a variant (normalize, events, band, cumulative) or an existing form in a new place beats a new component; a costume of an existing form is rejected by name; no data of that shape means not applicable; surfaces the contract mandates (a tile's sparkline) are out of scope.
- The rendering engine is a fork in the blueprint (the kit's own hand-drawn rows, the charting library already installed, the organization's library): name the missing host properties and the consumer count before recommending a swap, and never adopt an unfinished internal package for production until its owner says so.
- Row-class forms share one row grammar (28px row, label column, mark column, right-aligned mono value column, no divider): write one exemplar first and mirror the rest. Offer a mock of each candidate drawn from real series before the build is paid for.
- Write the completed vocabulary into the repository's contract as a question to form list, or the next agent defaults to curves.

## Definition of done for a new form

- Fixed height through the chart section, a trailing sentence naming the question, hue by entity, the hover key when time-bucketed, a skeleton with the same footprint, data through the page's input resolver and prefetch; a placement that duplicates an existing surface replaces it.
- A shared numeric scale across sibling rows draws dashed guide lines through every row at 1, 2, 5 step ticks with a label under each, from one shared helper; the axis's far edge is the next round step past the data max, never the raw max.
- Rows past a fixed count (eight) fold into one Other row; label overlap is a form defect.
- Tooltip position animation is off; a tooltip's change entries are their own block, one row per real diff entry with a time and a human label, identical entries collapsed with a count.
- A row is keyed by index and disambiguated in its label, never by a domain id that can repeat.
- A connector or point that looks accidental is a rendering defect to fix (one rounded track with square joins, a straight connector), not a data quirk to explain.
- Server-rendered date math is UTC, explicit, and identical in the page and its skeleton.
- Verified through `verify-ui` on a project with data, an empty project, the demo, both themes, and a narrow viewport.

## Placement

- The overview carries the summary and links onward; the detailed chart stays on the subject page.
- A volume strip sits directly above the table it filters.
- A tile appears only with a window, a comparison, and a denominator; small multiples replace a metric switcher.
- A variable-length panel is capped (top n plus Other) to a fixed height before it shares a grid row with a chart.
- Every mark links into the row-level view it summarizes: tile to page, strip bucket to filtered table, row to the list filtered by that entity.

## Tiles

- Window, comparison, and denominator by construction: "Runs, 14 days, +9% vs the previous 14 days, 21,391".
- Polarity is explicit per metric (`inverted` for cost, latency, errors); trend color keys to polarity, never to sign.
- A sparkline in a tile is scrubbable: the hovered bucket replaces the headline, the caption becomes that bucket versus the previous one in the same tone, and the label names the bucket; the first bucket of the range shows no delta.
- The tile links to its subject page; the overview shows six or fewer.
- A degenerate comparison (one comparable point) is a product call to surface, not a special case to hide.

## Color

- Chrome carries only the roles the repository's contract names; hue is reserved for state tones, at most one in-progress accent when the law defines one, and chart series.
- Hue follows the entity, never its rank: an entity kind with a closed set of parts owns fixed slots in fixed order everywhere; outcomes use status tones; an open-ended entity takes slots in first-seen order and keeps them when a filter removes a neighbour.
- Both themes keep the same hue per series and re-step lightness per theme; every series passes the palette checks in both modes.
- A single series takes the foreground neutral or the in-progress accent.

## Time and buckets

- One range per page in the URL, as UTC days or instants to the second.
- One function derives the bucket from the span (daily beyond three days, down to seconds for a range of seconds, capped near ninety bars) and is shared by URL state, SQL grouping, and axis labels.
- Daily rollups serve day granularity only; a narrower view recomputes from base rows; percentiles never come from a rollup.
- Bucket boundaries live in one fixed zone; the displayed zone is a render-time toggle applied on Apply, with Reset visible.
- Every time-bucketed chart on a page publishes and reads one hover key so scrubbing one marks the same bucket on all of them, tiles included; the link resets on navigation.

## Interaction

- A legend of two or more series toggles: a hidden series is only not drawn, the axis keeps its scale, the other series keep their place, the item goes hollow, the last visible one cannot be hidden; the state is page local.
- Focus rings suppressed for pointer clicks at the specific input event, never by disabling focus.
- A strip's selected bucket is outlined in the foreground neutral, never in a hue.

## Observability variants

- Rank latency by tail to median ratio (p99 over p50) per route or kind, not by absolute latency; averages hide a disproportionate tail.
- Frame a cache hit rate over routes that were meant to cache; a never-cacheable route is not a problem row.
- Isolate the failure mode a panel or alert watches: one call kind's latency, not a blended percentile dragged by unrelated long work.
- Scope thresholds from a measured baseline window, never a round number.
