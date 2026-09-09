---
name: plan-charts
description: "Decide what a dashboard shows and in which chart form, including forms and data it does not have yet, from what the product holds and production says, then build it in verified batches."
argument-hint: "[app-or-page] [--restore] [--observability]"
---

## Context

Chart kit: !`d=$(find . -name node_modules -prune -o -type d -iname charts -print 2>/dev/null | grep -v node_modules | head -1); if [ -n "$d" ]; then echo "$d: $(ls "$d" | sed -E 's/\.[jt]sx?$//' | tr '\n' ' ')"; else echo "(none)"; fi`

Schema files: !`top=$(git rev-parse --show-toplevel 2>/dev/null || pwd); out=$(git -C "$top" ls-files 2>/dev/null | grep -iE '(^|/)schema\.(ts|sql|prisma)$|/(schema|drizzle)/[^/]+\.(ts|sql)$' | head -5); echo "${out:-(none)}"`

Rollups and aggregates: !`top=$(git rev-parse --show-toplevel 2>/dev/null || pwd); out=$(git -C "$top" ls-files 2>/dev/null | grep -iE '(^|/)schema\.(ts|sql|prisma)$|/(schema|drizzle)/[^/]+\.(ts|sql)$' | sed "s#^#$top/#" | xargs grep -ohE '\b[a-z_]+(_daily|_hourly|_rollup|_aggregate|_summary)\b' 2>/dev/null | sort -u | head -12 | tr '\n' ' '); echo "${out:-(none)}"`

Chart rules in the contract: !`top=$(git rev-parse --show-toplevel 2>/dev/null || pwd); out=$(find "$top" -maxdepth 5 \( -name node_modules -o -name .claude -o -name .git \) -prune -o \( -iname AGENTS.md -o -iname CLAUDE.md \) -print 2>/dev/null | xargs grep -liE 'form follows|chart' 2>/dev/null | head -3); echo "${out:-(none)}"`

## Instructions

Inventory the data the product already has, prove each candidate metric is real in production, choose every form by the question it answers, place it where it leads somewhere, publish the grammar, and implement in verified batches.

### Process

1. Parse `$ARGUMENTS` (an app or page path, default the dashboard the conversation names; `--restore` when charts were removed and the ask is what to bring back, which adds the removal table; `--observability` when the surface is a telemetry tool such as Axiom, Grafana, or PostHog rather than product code, which swaps steps 2 and 8 for [references/observability.md](references/observability.md)). Name the audience and the question each page in scope answers; when composed by `design-dashboard`, take both from its framing.
2. Inventory before inventing: data pages already fetch and discard; rollups and aggregates and their grain; telemetry the code emits but never shows (metric registries, stats methods, log kinds, span attributes); tables with rows and no UI; what comparable products show for the same question, read through live web research, each candidate still needing a real or standard-defined source; and production facts read-only through `inspect-db` (row counts, null rates, distinct values, per-tenant cardinality, spelling variants of the same id). With `--restore`, list every removed visual with its page, its fate in the current tree, what it cost, and how it returns.
3. Prove each candidate is real before it earns a form: the field is written by the code path that should write it (an error rate reads 0.0% forever when the status was never written), spellings fold to one canonical id, the denominator exists, percentiles come from raw rows and never from a rollup that stores sums, and a trend has a per-bucket series behind it. A question with no source is designed per [references/capture.md](references/capture.md) (the standards test per field, the attributes bag, the compatibility rules) before it earns a tier C row.
4. Write the catalog per [references/catalog.md](references/catalog.md): metric, the question it answers, exact source, aggregation sketch, unlock tier (A data in hand, B one endpoint, C new field, D new dataset or deferred), what production says it would show, and the kill reason where it dies. Kill a candidate that is empty in production (design the empty state and the call that fills it instead), that duplicates a panel already answering the question, that quantizes magnitude away, or whose groups collapse to one or two slices for most tenants. A metrics page that usage shows only buyers open is frozen to one proof page, and the rest of its chart backlog is killed.
5. Choose the form by the question with [references/forms.md](references/forms.md). When no form in the kit answers the question, expand the vocabulary per its expanding section (sibling kits' unported forms with existing data, the organization's own library taxonomy, the world taxonomy by question family), admit a form only for a question a page answers badly, prefer a variant or a reuse, decide the engine as a fork in the blueprint, ship one exemplar and mirror the rest, and count a new form done only by its definition of done. Hue follows the entity, never its rank, and stays fixed across pages and themes; every metric declares its polarity; a single series takes the foreground neutral.
6. Place each answer by the Placement, Tiles, Time and buckets, and Interaction sections of [references/forms.md](references/forms.md), recording page, position, and link target in the catalog row.
7. Publish the grammar artifact in the shape [references/catalog.md](references/catalog.md) gives (verdict, removal table when restoring, production evidence, the rules, page by page with wireframes drawn from real series, the not-built list with reasons, batches). An analysis ask ends here.
8. Implement in batches, kit and exemplar page first: each batch passes typecheck, lint, and build, runs every new SQL shape read-only through `inspect-db` against the named staging or production connection, and is exercised through `verify-ui` (scrub a sparkline, toggle a legend, click a strip day, change the range, both themes, the empty variant). Seed staging through the app's own seed script or `inspect-db --write` against the staging connection named by host, never production, before judging a chart page. Once a tile or chart convention is set, sweep every instance in the app in one pass. Write the grammar into the repository's contract, and leave the tree uncommitted.

### Rules

- Unknown is never zero: a stat with a missing denominator reads "not available", never a dash and never a fake trend.
- A chart whose table is empty in production is an empty state that names how to fill it.
- Every chart's trailing slot carries the one sentence it is read for; the title is the question.
- No entrance animation on any chart; a legend toggle repaints and never rescales.
- Palette contrast per theme, axis hygiene, and the generic chart rejections are checked through `dataviz` before a chart ships; this skill adds only what the question decides.
- No chart component for a data shape the app does not have.
