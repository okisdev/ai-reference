# Personal design taste: web

What the web adds to [taste.md](taste.md). A product's `DESIGN.md` overrides both.

## Tokens
- One token stylesheet holds light in `:root` and dark in `.dark`, as semantic oklch variables (`--background`, `--foreground`, `--muted`, `--border`, `--chart-1` to `--chart-8`, `--chart-seq-1` to `--chart-seq-7`) mapped to Tailwind colors through `@theme inline`; a component writes `bg-muted` or `ring-border`, never a raw palette step or hex.

## Registers
- Type sizes add 16 and 18 to the taste scale; Tailwind's scale is remapped so `text-xs` 12, `text-sm` 13 (the body), `text-base` 14, `text-lg` 16, `text-xl` 18, `text-2xl` 24, and nothing larger or arbitrary (`text-[13px]`).
- Sidebar rows 28 (`h-7`); controls 28 in every size of a button, input, or select.
- Ease `cubic-bezier(0.23, 1, 0.32, 1)`; a `transition-[...]` names its properties, because Tailwind v4 compiles `translate-*` and `scale-*` to standalone properties that `transition-transform` misses.
- Radius 8 on controls, rows and cards and 12 on floating surfaces, through the theme (`--radius-md` 8 and `--radius-lg` 12, so `rounded-md` and `rounded-lg` carry them, never Tailwind's default 6); badges 5; `rounded-full` only for dots, avatars, radios and tracks.
- An interactive surface's edge is `ring-1 ring-border`, so a focus ring replaces it without shifting layout; focus shows only on `:focus-visible`.
- A sticky top bar may be translucent (`bg-background/80` with a backdrop blur); nothing else blurs.

## Components
- Primitives are Base UI in `components/ui`, styled with cva and composed with the `render` prop; `components/shared` holds what every page must reuse (confirm dialog, empty and error state, copy to clipboard).
- A native `<select>`, `window.confirm`, `alert()`, or a browser default menu never ships; the kit's select, confirm, and menu do.
- A select always receives its options so it renders the chosen label, never the raw value.
- Popups (menu, popover, tooltip, dialog) share one motion definition: opacity and scale from 95 percent over 150 ms.
- Charts render through one shared chart frame and theme reading `var(--chart-N)`; entrance animation off.

## Before calling a surface done
- Both themes, a 375 wide and a 1440 wide viewport, keyboard focus order, and the empty, loading and error states were looked at in a browser.
