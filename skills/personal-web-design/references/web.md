# Personal design taste: web

What the web adds to [taste.md](taste.md). A product's `DESIGN.md` overrides both. Values are stated for any styling stack; the Tailwind lines say how they bind on Tailwind, and a product on plain CSS variables binds the same values in its own token file.

## Tokens
- One token stylesheet holds light in `:root` and dark under `prefers-color-scheme` or `.dark`, as semantic variables (`--background`, `--foreground`, `--muted`, `--border`, `--chart-1` to `--chart-8`, `--chart-seq-1` to `--chart-seq-7`); a component reads the semantic variable, never a raw palette step or hex.
- Lines and fills are the ink mixed with transparency (`color-mix(in srgb, var(--foreground) 7%, transparent)` or an oklch alpha), so one definition stays right in both themes and on stacked surfaces.
- Tailwind: the variables map to colors through `@theme inline`, so a component writes `bg-muted` or `ring-border`.

## Registers
- Type sizes add 16 and 18 to the taste scale; Tailwind's scale is remapped so `text-xs` 12, `text-sm` 13 (the body), `text-base` 14, `text-lg` 16, `text-xl` 18, `text-2xl` 24, and nothing larger or arbitrary (`text-[13px]`).
- Top bar 48 with its controls centred; the sidebar header takes the same height and continues the top bar's hairline; page gutter 24, 16 under 760 wide.
- Sidebar rows 28 (`h-7`) inset 8 from the sidebar edge; controls 28 in every size of a button, input, or select.
- A page grid with wide gutters narrows them in a container query (24 under 900, 8 under 640), because eleven fixed 40 gaps alone are wider than a phone.
- Ease `cubic-bezier(0.23, 1, 0.32, 1)`; a transition names its properties, because Tailwind v4 compiles `translate-*` and `scale-*` to standalone properties that `transition-transform` misses.
- Radius 8 on controls, rows and cards and 12 on floating surfaces (Tailwind: `--radius-md` 8 and `--radius-lg` 12, so `rounded-md` and `rounded-lg` carry them, never the default 6); badges 5; fully round only for dots, avatars, radios and tracks.
- An interactive surface's edge is a 1 pixel ring or border in `--border`, so a focus ring replaces it without shifting layout; focus shows only on `:focus-visible`.
- The page never moves on its own while scrolling: the root takes `overscroll-behavior: none` so the window does not rubber band past its top or bottom and drag the sidebar and top bar with it, and `scrollbar-gutter: stable` so content does not shift sideways when a page grows long enough to scroll.
- A sticky top bar may be translucent (the background at 80 to 88 percent with a backdrop blur); nothing else blurs.
- Scrollbars are thin and drawn in the ink at low alpha (`scrollbar-width: thin`, `scrollbar-color`); a horizontal strip of tabs or chips hides its scrollbar, and a scrolling pane keeps a stable gutter so content never shifts when the bar appears.

## Components
- Primitives live in one layer every page imports (Base UI composed with the `render` prop on React, the product's own components elsewhere), and a shared folder holds what every page must reuse (confirm dialog, empty and error state, copy to clipboard).
- A native `<select>`, `window.confirm`, `alert()`, or a browser default menu never ships; the kit's select, confirm, and menu do.
- A select always receives its options so it renders the chosen label, never the raw value.
- The data hook keeps the previous result while a changed parameter loads (stale while revalidate) and reports that it is updating, so a view can dim instead of blanking; clearing data on every parameter change is what makes a switch flash.
- A text input shows a small clear control once filled, and a secret field has a reveal toggle.
- Popups (menu, popover, tooltip, dialog) share one motion definition: opacity and scale from 95 percent over 150 ms.
- Charts render through one shared chart frame and theme reading `var(--chart-N)`; entrance animation off.

## Before calling a surface done
- Both themes, a 390 wide and a 1440 wide viewport with no horizontal page scroll, keyboard focus order, and the empty, loading and error states were looked at in a browser.
