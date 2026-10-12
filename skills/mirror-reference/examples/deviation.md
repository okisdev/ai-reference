# A deviation report that clears the bar (illustrative)

The bar for a mirror: each reference contributes one named pattern class as a take and a not-take, every adopted pattern is attributed, the implementation stands on this repository's own primitives with nothing in the diff traceable to a reference's skin, and each deviation is argued from this repository's idiom. The references and the repository are invented; the shape is the bar.

---

**Ask**: build the runs list at `apps/web/app/runs` following `acme/atlas` for the filter bar and `../billing-console` for the page skeleton, without copying either. Atlas was studied through `gh` (shallow clone), the billing console by reading the sibling path. Edited: `app/runs/page.tsx`, `app/runs/filters.tsx`, `components/ui/toolbar.tsx`, `app/runs/page.test.tsx`.

| Pattern class | Reference | Take | Not take | Built from | Deviation and why |
|---------------|-----------|------|----------|------------|-------------------|
| Interaction grammar (filter bar) | `acme/atlas` | The order (search, facets, ranges, clear) and the rule that a facet writes the URL | Its chip look, its `Popover` wrapper, its token names | `Toolbar` and `FilterField` from `components/ui/`; URL state through `useQueryState` as in `app/projects/page.tsx:34` | Atlas replaces the URL on every keystroke; here typing replaces and a facet click pushes, as `AGENTS.md:57` requires |
| Page skeleton | `../billing-console` | The sequence of tiles, filter bar, and table | Its fixed 1200 px rail and its own table | `PageShell` and `DataTable` from `components/ui/` | The rail width comes from `PageShell`, so the reference's 1200 px only matches the middle step |

**Direction.** Atlas moved from filter tabs to facets in `3f9a2c1` (2026-08-14, from `git log --follow -- src/filters`), so facets are the direction worth taking; its docs site still shows tabs.

**Reuse.** `Toolbar` already carried the layout, so no `FilterBar` was added; it gained one `facets` slot, which two other pages already needed.

**Matches.** The facet order and the shareable URL. Everything else differs by design.

**Copy check.** Atlas's distinctive class strings and token names (`rounded-xl`, `bg-zinc-900/60`, `--atlas-surface`) return no hits in the diff.

**Verified.** `pnpm --filter web typecheck` and `lint` pass; `verify-ui` rendered `/runs` at 1440x900 and 390x844, and a facet click changed both the URL and the rows.
