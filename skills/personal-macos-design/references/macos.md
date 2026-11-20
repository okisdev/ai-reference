# Personal design taste: macOS

What a Mac app adds to or replaces in [taste.md](taste.md) and [swift.md](swift.md), whether it is built in SwiftUI or as a desktop web stack styled with CSS modules. A product's `DESIGN.md` overrides all three.

## Principles
1. **Quiet chrome, bright sheet.** The sidebar sits on the window's own translucent material and the selected page sits on an opaque sheet inset from the window edge, so what the person works on is the brightest thing in the window; this replaces taste.md's chrome bands on the Mac.
2. **The page owns its header.** There is no toolbar band: the page title, its count, its commands and its search are drawn on the sheet in one header row, and a tab's own controls sit at the right end of its tab row, because a second bar inside the content splits one place into two.
3. **Opening a row drills in.** A row opens in place of its list, the header turns into the path back (page name, then the row's name), and Escape or Command [ returns, because a split pane halves the room of both the list and the detail.
4. **Sized like the system.** Running text uses the platform's text styles at the sizes the system's own windows use, and the sidebar follows the Sidebar icon size the person chose, because a Mac app set larger than Finder reads as a port.
5. **Round controls.** Glyph commands are circles, text commands, tabs and search are capsules, and cards are soft rounded fills, because round controls on a quiet ground read as touchable without borders.

## Tokens
- SwiftUI: one product-agnostic UI module (its own package target, no product names) holds the metrics, grounds, type roles and every component; pages compose it and never define a look inline.
- Desktop CSS: CSS custom properties (`--ink-*`, `--tone-*`, `--kind-1` to `--kind-8`, `--radius-*`, `--height-*`, `--motion-*`) read by CSS modules, no Tailwind; text only through the design package's components.

## Registers
### Window
- Sidebar ground: the behind-window material (`underWindowBackground` in SwiftUI, the under-window vibrancy in a desktop shell) under a veil, white at 62 percent in light and the window background at 45 percent in dark, so it reads as light as the system's own sidebars; never the `sidebar` material or a glass effect, which read dark.
- Sheet: opaque text background, inset 8 from the window, radius 14, a hairline border.
- Title bar hidden and transparent; the traffic lights are centred vertically in the sidebar's top strip (46 high) and as far from the leading edge as from the top, placed again whenever the system lays the title bar out, including after a title change; a desktop shell sets the same position through its traffic light offset.
- Sidebar 220 wide; its top strip drags the window; the window opens at 1180 by 760, at least 860 by 560.
- An app with a menu bar item follows its windows: a regular app while any titled window is open, menu bar only when all are closed.

### Layout
- Page inset 28 from the sheet's sides; the header is 32 high and placed so its 30 point controls sit 28 below the sheet's top, the same as from its side; a sheet's close button sits 28 from both edges with its title and controls centred on it; card edges line up with the header's text.
- Lists, details, settings and info tabs fill the sheet; the 640 column is for sheets only.
- Section gap 20; 8 from a group title to its card; 12 between the header and the first group.

### Density
- List row at least 44 for a name over a meta line, 36 for a compact or nested row; settings row 42.
- Sidebar rows by the system Sidebar icon size: small 26 with 11 point text, medium 32 with 13, large 38 with 15; a desktop shell that cannot read the setting uses medium.
- Controls 30, controls inside a row 26.

### Type
- Navigation and row names `.body` (13); meta `.subheadline` (11); page title `.title2` semibold with its count in secondary `.body`; group and section titles `.headline`; never `.title3` for running text. A desktop CSS app sets the same sizes through its type roles: names 13, meta 11, page title 17 semibold, group titles 13 semibold.
- Numbers that change are tabular and roll their digits.

### Shape and color
- Radii: card 14, hovered or selected row 10, sidebar row 9; circles and capsules for controls; pills are allowed for controls, never for badges.
- Fills on the sheet are the text color at low opacity: card 3.5 percent, hover 4.5, selected sidebar row 8, hairline 7; the selected sidebar row is neutral, never the accent.

### Motion
- Hover fills 120 to 150 ms; page switches fade in on insertion only, never cross fading two headers; press scales controls to 0.94.

### SwiftUI mechanics
- A tab's controls travel to its tab row through a preference the row reads with `overlayPreferenceValue`, with a fallback that draws them above the view when no tab row hosts it.
- The traffic lights are placed by hand and placed again on the views' frame change notifications, because the system resets them on every title bar layout.
- The sidebar reads `NSTableViewDefaultSizeMode` from the global defaults to size its rows like the system's.

## Components
- **Sidebar**: navigation rows parted by space, no headers; arrow keys move the selection; its foot holds the app level places such as Settings, and an app that runs a background service shows its state as a dot at the end of one of those rows.
- **Page header**: title or capsule tabs, a secondary count (`3 running · 12 total`), round glyph commands, then a capsule search that Command F focuses and Escape clears.
- **Detail**: the path as the header, at most two glyph commands, one More menu with delete last; its views are capsule tabs with each tab's controls at the right end of the tab row; the views are kept once built.
- **Grouped list**: every list is groups of rows on soft cards with inset hairlines between rows, under the group's name and count; a row shows a state dot, the name over one meta line, one trailing value, and its commands slide in after the value on hover or keyboard focus.
- **Settings form**: sections as soft cards, header above and footer below on the card's edge, label icons in a 22 wide column, a text setting as one row with its field trailing and Apply only after an edit.
- **Menus**: the system menu behind a round or capsule trigger is the product's menu on the Mac; never a system pop up button or bordered picker in content.
- **Empty state**: a glyph, one title, one sentence and at most one capsule action, centred where the rows would be.
- **Menu bar item**: one glyph or figure; a click opens its popover window, a right click a menu with Open and Quit; a popover holds no settings, 300 to 320 wide on 14 to 16 padding.
- **Viewer sheet**: a sheet that shows rather than completes (logs, output) has its title over a one line subtitle, its controls, then a round close button bound to Escape; never a blue Done.
- **Confirmation**: the platform confirmation with the loss in one sentence, Cancel the default, the destructive role on its button.

## Reject
- A toolbar band or a second control row inside the content → the page header and the tab row's end.
- A split view with an empty detail pane → drill in.
- `.title3` names in rows or the sidebar → `.body`, meta in `.subheadline`.
- A dark sidebar from the `sidebar` material or a glass view → the behind-window material under its veil.
- Traffic lights that jump after navigation → place them again on every title bar layout.
- A Finder style column table for files → the grouped file browser.

## Before calling a surface done
- Light and dark, the narrowest and widest window, every Sidebar icon size, keyboard only, and the empty, loading and error states were looked at in the running app.
- The traffic lights were measured at their inset on more than one page.
