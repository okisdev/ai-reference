# A merge that clears the bar (illustrative)

What the user sees from a good merge: the principles two products repeated move into one shared system, each product file keeps `extends:` and only its differences, exact values replace adjectives, exemplars are chosen with a stale repository named and excluded, rules the user never stated are marked as proposals with an inferred why, and the enforceable rules come back as proposed checks. Products, repositories, and values are invented; the shape is the bar.

````
Merged `harbor-web` and `kiln-app` into one shared system, `loom-design:DESIGN.md`. Uncommitted in both repositories.

Shared file, `loom-design:DESIGN.md`:

# Loom design system

Governs every Loom product. Where the code breaks a rule here, the code is fixed.

## Principles
1. **One accent per screen.** Exactly one `--accent` fill is visible at a time, because two competing primaries make the user hunt for the next step.
2. **Motion explains, never decorates.** Every transition shows where something came from or went, because ornamental motion on frequent actions reads as lag.
3. **Every list has three states.** Empty, loading, and error are designed before the populated row, because the unhappy states are what users meet first.
4. **Numbers align.** Figures in columns use `tabular-nums` and right alignment, because proportional digits make a column unscannable. (proposal, inferred why)
5. **Labels name the outcome.** Buttons say what happens ("Save changes", "Delete project"), never "OK" or "Submit". (proposal, inferred why: a vague label makes the user guess what the click commits)

## Tokens
- web: `packages/tokens/src/tokens.css` in `loom-design`; components read CSS variables.
- SwiftUI: `Sources/LoomTokens/Tokens.swift`; components read the `Loom` enum.

## Registers
### Layout
- Spacing scale 4, 8, 12, 16, 24, 32; row height 40 (compact 32); page gutter 24, 16 under 640 wide.
- Radius scale 4 (inputs), 8 (cards, menus), 999 (pills); nothing else.
### Color
- Neutrals `--gray-1` to `--gray-12`; text `--gray-12`, secondary `--gray-11`, borders `--gray-5`; accent `--accent`, danger `--red-9`.
- Contrast at least 4.5 to 1 for body text in light and dark.
### Type
- Sizes 12, 14, 16, 20, 28; weights 400 and 600 only; line height 1.5 for body, 1.25 for headings.
### Motion
- Enter 180ms `cubic-bezier(0.2, 0, 0, 1)`; exit 120ms ease-out; nothing over 240ms; honor `prefers-reduced-motion` by dropping to opacity only.
### Copy
- Sentence case; no exclamation marks; errors say what failed and what to do next.

## Components
- **Dropdown menu**: opens from the trigger edge, 8 radius, items 32 high, arrow keys and type-ahead; states: closed, open, item focused, item disabled, empty results.
- **Data table**: 40 row height, sticky header, tabular numbers, a designed empty row and a skeleton of 5 rows for loading.

## Reject
- A spinner on a list or table → the 5 row skeleton.
- A color or size not in `tokens.css` → the nearest token, or a proposal to add one.
- `transition: all` → name the properties.
- A gradient fill → a flat token fill. (kiln-app only, see its file)

## Exemplars
- **Dropdown menu**: `harbor-web:src/ui/menu.tsx`, current (changed 3 weeks ago), tokens only, covered by `menu.test.tsx`.
- **Data table**: `harbor-web:src/ui/table.tsx`, same reasons, and the only one with the loading skeleton.
- **SwiftUI list row**: `kiln-app:Sources/Kiln/Views/RowView.swift`, current and on `Loom` tokens.
- Not exemplars: `legacy-console` (last design change 2 years ago, raw hex throughout) and `kiln-app` web views under `Sources/Kiln/WebFallback/` (bypass the tokens).

## Platforms
- **web**: React with `harbor-web:src/ui/`; registers map to CSS variables.
- **SwiftUI**: `kiln-app:Sources/Kiln/Views/`; registers map to the `Loom` enum.

## Checks
- Proposed, not yet written: `no-raw-color` (stylelint, flags `#[0-9a-fA-F]{3,8}` and `rgb(` in `**/*.css` and `**/*.tsx` outside `tokens.css`) asserts the Color register.
- Proposed, not yet written: `no-transition-all` (stylelint `declaration-property-value-disallowed-list`, `transition: all`) asserts the Motion register.

`harbor-web/DESIGN.md`:

extends: loom-design:DESIGN.md
Differences only.
- Page gutter 32 above 1280 wide.
- Body size 16 on marketing pages, 14 in the app.

`kiln-app/DESIGN.md`:

extends: loom-design:DESIGN.md
Differences only.
- Row height 44 for touch; hit areas at least 44 by 44.
- Principle 2 differs in substance: motion may also confirm a gesture (a 60ms scale to 0.97 on press), kept here and not averaged into the shared file.
- Gradient fills are allowed on the onboarding hero only; everywhere else flat.

Pointers: one `Design system: loom-design:DESIGN.md` line added to each `AGENTS.md`.

Awaiting you:
- Principle 4, `tabular-nums` and right alignment. Inferred why: proportional digits misalign columns. Both products already do it in two tables; you never said it.
- Principle 5, outcome labels. Inferred why: a vague label hides what the click commits. 9 of 11 buttons already follow it.
Everything else came from your two docs or your edits (harbor-web `DESIGN.md` and the 180ms change in `menu.tsx`).
````

Why it clears the bar:

- The three principles both products repeated are written once in the shared file, and each product file holds only `extends:` and what differs, so a copy can no longer drift.
- A principle that differs in substance (motion confirming a gesture) stays in the product that needs it, never averaged into the shared file.
- Every register states a value (180ms, 40 high, 4.5 to 1) where an adjective would have been, and token values live in the token files the system points at.
- The two rules the user never stated are marked as proposals with an inferred why and listed under what awaits the user, so no invented taste reads as the user's.
- Exemplars name the implementation, the reason it is current, and the repositories excluded as stale or token-bypassing, so no agent is ever handed a path again.
- Enforceable rules come back as two proposed checks with their file and pattern, listed as not yet written.
- The run stops at an uncommitted tree and reports each rule's source.
