# Personal design taste: macOS

What a Mac app adds to [taste.md](taste.md) and [swift.md](swift.md), whether it is built in SwiftUI or as a desktop web stack styled with CSS modules. A product's `DESIGN.md` overrides all three.

## Tokens
- SwiftUI: color, measure, and type role tables (`Ink`, `Tone`, `Measure`, `TypeRole`, `Motion`) hold every value; text only through `.role(_:tone:)`.
- Desktop CSS: CSS custom properties (`--ink-*`, `--tone-*`, `--kind-1` to `--kind-8`, `--radius-*`, `--height-*`, `--motion-*`) read by CSS modules, no Tailwind; text only through the design package's components.

## Registers
- Ease `cubic-bezier(0.19, 1, 0.22, 1)`.
- Sidebar rows 30 in SwiftUI, 28 in CSS; table rows 36; menu bar popover 300 to 320 wide on 14 to 16 padding.
- Radii 3, 5, 6, 8, 12 from the radius table; badges 5, controls and rows 8, groups and floating surfaces 12.
- The window's own material, the traffic lights' title bar area, and the platform split view are chrome and may follow the system; content starts after the title bar inset (`env(titlebar-area-x)` on a desktop web stack).
- Focus rings show only for keyboard focus and are never clipped by their container.

## Components
- Dropdown, select, menu, scrollbar, and toast come from the product's own components, never the system or browser default, so they match the moment they open.
- A menu bar item is one glyph or figure; a click opens its popover window, a right click a menu with Open and Quit; a popover holds no settings.
- The top bar, sidebar top strip, and inspector top strip drag the window; popovers and sheets close when the window loses focus.
- Confirmations use the product's confirm sheet with Cancel as the default; a destructive action is never ink.

## Before calling a surface done
- Light and dark, the narrowest and widest window, keyboard only, and the empty, loading and error states were looked at in the running app.
