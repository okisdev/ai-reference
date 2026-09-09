# The blueprint

The blueprint is the design deliverable: a published artifact the user reads before any code changes, and the document the implementation packages are cut from. Its shape is fixed so that a blueprint written a year from now reads like the last one. Wireframes in it are drawn from real data, never lorem rows.

## Sections, in order

1. **Verdict.** Three short paragraphs: what is wrong in one sentence, what the direction is, what most of the return costs. A redesign that changed the right thing the wrong way says so ("right about density, wrong about form").
2. **Diagnosis in measurements.** The density audit table (body size, radius, control and row heights, hand-styled panels, content and shell widths, rules per panel, shadows, transition-all), the five layers, and the existence review, each defect cited `file:line`. Dead chart code and discarded query results are named here.
3. **What each reference contributes.** One row per reference project: what is taken, what is deliberately not taken, and why. A reference's recent direction is stated with dates from its git history.
4. **Interaction grammar.** The rules every screen obeys: every dimension is clickable and a click is a filtered navigation whose URL is shareable; one inspector container for detail when the list must stay in view; state color by semantics; the empty state ladder (skeleton with the real footprint, no data with one cause, unreachable stats annotated in the column, a global banner when the source is down); the command palette as second navigation.
5. **Data plane.** Where each screen's data comes from, what is fetched and discarded today, which seams do not exist yet, and the transport (push, poll, request scoped cache). A screen drawn against a seam that does not exist carries one visible not-yet-real marker on every affected column, and the seam itself is designed per the capture reference of `plan-charts` (a standard-defined shape or the product's own, with compatibility for clients that do not upgrade).
6. **Component system, now to target.** One row per layer (frame, tokens, primitives, charts, large tables, stat tiles, states): what exists, what replaces it, from which reference.
7. **Screen by module map.** One row per sidebar entry, modules listed top to bottom with new, kept, and dropped marked, and the question each module answers.
8. **Chart vocabulary.** The few forms chosen, each with its job; a form without a job does not enter. Composed with `plan-charts`, including its vocabulary expansion when a question has no form in the kit.
9. **Fork decisions.** Every fork the research exposed, decided on the spot with its basis: font, ground, kit port versus vendor, sidebar resizable or fixed, drawer versus page, rendering engine (the kit's own rows, the installed charting library, the organization's library; an unfinished internal package never enters production until its owner says so), time range scope. No row says either is fine.
10. **Implementation waves.** Core first (tokens, kit exemplars, primitives, contract), then the shell, then pages by breadth, detail and trace last, verification last; each wave names what it is parallel with and what it waits on.
11. **Quantified gain.** Rows per screen before and after, content width before and after, tiles that carry a trend, charts that answer a question a table cannot, hairlines per panel.
12. **Open decisions.** Product decisions the user owns, batched in one numbered list with a recommendation each, so one reply approves or delegates all of them.

## Wireframes

- Drawn from real series read read-only from production or staging; table bodies may be layout only.
- Each wireframe carries a caption stating the viewport and the count of ruled objects on the page.
- A tile shows its window and comparison; a chart shows its trailing sentence; a strip shows a selected day.
- Marks for data that does not exist yet are visible in the wireframe, not in a footnote.

## Density audit

`scripts/density.mjs <app-path>` prints the mechanical part as a table and as JSON with `--json`: type classes and the root size, radius classes and the radius token, control and row height classes, hand-styled panel patterns, shadow and transition-all counts, max width and sidebar width values, rule classes, pill badges, chart entrance animation, shared component inventory, and route counts. The judgment part is added by hand: rows per screen at 1440 wide on the busiest list, hairlines in the busiest panel, the number of distinct type sizes actually rendered, and which of the stacked defaults each page inherits.

## Publication

Publish through the harness's artifact surface when one exists, revised in place at the same link as the design moves; otherwise write the blueprint as markdown in the scratchpad and name its path in the handoff. Wireframes are monospace or CSS mock blocks inside it, one per page at the stated viewport. A repository gets a docs file only when the user asks. The link goes to project memory with the date and the branch.
