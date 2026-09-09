# The dashboard contract

A dashboard is drawn in a written contract, and the contract belongs to the repository, not to this skill. This file says where to find it, what it must decide, what to start from when nothing exists, and how to write it down. Brand identity (palette hue, faces, a print or product metaphor, motion signatures) always comes from the organization's own law; this file carries structure and density only.

## Discovery ladder

Read in order. The first rung that answers a dimension wins; lower rungs fill the gaps, and every value taken from the last rung is written into the repository's own contract in the same pass so the next session finds it on rung 1.

1. The app's own instruction file: a design contract section in `AGENTS.md` or `CLAUDE.md` (search for `design contract`, `type sizes`, `line budget`, `radius`). A test or lint that asserts a rule outranks the prose; a kit precedent that disagrees with the prose is reported as a defect and not followed.
2. The organization's published law: a machine-readable design document the brand serves (for example a `design.md` in the tree, a `/design.md` route, or a served design skill). When one exists, follow it for register, palette, type roles, motion, and the closed token and component API.
3. The organization's own prior blueprints and design artifacts, and a chart or UI library it built but has not wired in, read before any external reference.
4. A sibling app on the same stack whose contract is proven in production. The same framework, CSS engine, component library, table library, and chart library justify a direct port of tokens and kit; anything less is a rebuild in this app's primitives.
5. The brand's own surfaces (marketing site, docs) read through `mirror-reference` for what they do with radius, elevation, rules, type, and hue, then translated to application density.
6. The defaults below.

## What every contract decides

| Dimension | The contract states | Default when nothing exists |
|---|---|---|
| Type scale | A closed set of sizes on one body base; numbers, identifiers, costs, and durations in mono with tabular figures | 12 / 13 / 14 / 16 / 18 / 24 on a 13px base, with an 11px mono eyebrow role for section labels, table heads, and captions |
| Density | Sidebar row, button and chip, input and select, table row, page title, section title, description | 28px rows and buttons, 32px inputs and table rows, 18px page title, 13px section title, 12px descriptions, 16px panel padding, 24px between charts, 12px under a heading |
| Hierarchy | From spacing, weight, and hairlines, never from boxes; which objects are self-ruled | A bordered table, a stats grid, and a key/value ledger carry internal rules; nothing else does; machine content (JSON, code, traces) sits on a borderless muted field |
| Line budget | A rule separates objects of different kinds; rows of one kind are separated by rhythm and a hover fill | No rule under a section title; a row that carries a mark (bar, swatch, status dot) has no divider; two marks never stack; an empty state is never boxed; one panel never draws rules from more than one source |
| Radius by role | The roles and their steps, smallest to largest | Smallest on badges and kbd, then compact controls and bordered groups, then floating surfaces, then dialogs; full radius only for dots, avatars, radios, and tracks; badges are never pills |
| Color | Which roles may carry hue, and how neutrals are produced | Neutrals only through semantic token utilities, on one tint or a mirrored light theme; borders and fills as alpha over the ground; chrome achromatic; hue for state, severity, at most one in-progress accent when the law defines one, and chart series, which keep the same hue in both themes with their own lightness per theme; never a raw grey, black, or white class |
| Elevation | Whether shadows exist and where a floating surface gets its lift | Zero shadows; a floating surface lifts with a ring and a lighter ground |
| Motion | The ceiling, explicit property lists, entrance animation off on charts, reduced motion honored, a focus-visible ring on every control | 300ms |
| Frame | Three containers with one job each; what the sidebar, header, and content rail own | Sidebar lists places grouped by question, each entry named for the entity it lists and never for the measure that describes it, with the user menu holding outbound links, theme, and sign out; header carries the crumb, the entity id in mono with copy, and the command palette; the content rail owns padding and max width and pages set neither |
| Shell widths | Wide, detail, form | 1200 to 1600, 880, 560 |
| URL state | Filters, sort, paging, ranges, and tabs as search params; navigation pushes and typing replaces; a copied URL reproduces the view; ranges as UTC days or instants; the bucket derived from the span by one function shared with SQL and axis labels; a view earns its own URL only by changing the unit of analysis, and a selector over the same unit is a query parameter | 25 / 50 / 100 rows, default 50 |
| Detail grammar | One header, then sections; a fact edited as a live control lower on the page is not repeated read-only in the header | Header of two lines (name and status, then dotted mono facts), sections of key/value rows, tables, or a trace, a rail for facts on wide screens |
| List grammar | Tiles, filter bar, strip, table; an index page shows one headline per destination and never that destination's own chart; a list is drawn at ten and a hundred times today's row count and past the first screen collapses by default and searches; a word repeated in every row moves to the column head or a group label | Tiles only with a window and a comparison; one filter bar directly under the tiles in the order search, facets by use, ranges, clear; a volume strip directly above the table it filters; numeric columns right aligned mono with units in the column head |
| Identifiers and links | Shown whole and copyable; every entity mention a link through one helper | A value with no page of its own links to the list filtered to it |
| Tiles | Window, comparison, denominator, polarity | A number without a comparison is a key/value row, not a tile; unknown is never zero; a zero-count badge is suppressed, not rendered |
| States | Skeletons match the footprint; failed reads render errors, never empty arrays; a panel under a range picker honours it or declares itself a snapshot; an affordance's rest state is never fully invisible | |
| Forms | Fit one screen; objects with a lifecycle are rows, not repeated fields; illegal combinations unrepresentable; one primary entry point per page and a second input or New button folds into a dialog or menu; secondary and destructive actions in one overflow menu; every destructive action through one confirm dialog, irreversible ones with typed confirmation | |
| Kit and reuse | Never hand roll a control, overlay, badge, table, or empty state the kit has; the kit's composition rule (on Base UI the `render` prop, never `asChild`); a third-party component's default box model, toolbar, palette, and animation are overridden to the contract before it ships; shared components are mandatory; one format module and one labels module | |

## Writing it

The contract lands under a `## Design contract` heading in the app's AGENTS.md: a precedence line first, then one bullet per row of the table above in table order, each naming the kit file or test that proves it, then the chart grammar bullets `plan-charts` produced. Run `python3 "$HOME/.agents/skills/normalize-agents-md/scripts/measure.py" <app-path> --strict` afterwards and cut prose, never a rule, to fit the caps.

## Precedence

The repository's own contract outranks the organization's law on density and grammar; the organization's law outranks this file on identity; this file outranks nothing that exists. A contract this skill writes carries the same precedence line so the next agent knows what to read first.
