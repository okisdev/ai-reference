# Personal design taste

The maintainer's taste on every platform: dense, flat, achromatic chrome with color only where it carries meaning. The platform file beside this one adds or replaces values for its platform, and a product's own `DESIGN.md` holds its differences, token files, and exemplars and overrides both rule by rule. Where the code breaks a rule here, the code is fixed.

## Principles
1. **One name, one place.** The top bar says where the pane is (a breadcrumb counts), and no page title or header repeats it, because a repeated name is noise the eye must skip on every visit.
2. **One command, one place.** A command on the whole surface lives in the top bar, on part of it in that row or section, and one that needs input in a sheet, because a command shown twice makes people wonder whether the two differ.
3. **Whitespace over lines.** Separate groups with the section gap before adding a hairline or a box, and never box a box, because every extra line and layer competes with the content.
4. **Chrome is bands.** A pane stacks top bar, tab bar, toolbar, strips and content, each full width with one job and a hairline between band and content, because nothing should float in a padded box.
5. **Tools run edge to edge, documents sit in a column.** A surface the person works in fills its pane from the 16 point line; one the person reads or fills in sits centered, because width helps scanning rows and hurts reading.
6. **One grid.** Every band starts and ends 16 points from its pane's edges, because bands that disagree on the margin read as misalignment.
7. **Weight follows finality.** Ink fills only the button that completes what the person is composing; everything else is bordered, a word or a glyph, because several filled buttons leave no way to tell which one finishes the task.
8. **Hue is meaning.** Chrome is black, white and very light gray; color marks a state, the person's accent, or a series in a chart, never decoration or a button's rank, because color that decorates cannot also mean something.
9. **Dense by default.** Rows, controls and cards take the smallest size on the scale below, because large elements leave too little information on screen.
10. **Flat.** No gradients, glows, glass or material in content; a shadow only under what floats, because depth on resting surfaces reads as heavy and dirty. Chrome may carry the platform's window material or a translucent sticky top bar.
11. **Charts are varied and colored.** Show data as the chart form that fits the question, in the categorical palette, never as text or only plain lines, because text and uniform lines hide the shape of the data.
12. **Motion is slight and never moves content.** Motion shows where a change came from and never makes the person wait or shifts layout, because jumping content breaks reading.
13. **Controls are drawn by the product, not the platform default.** Where the platform file says so, a dropdown, select, menu, scrollbar and toast come from the product's own components, because the defaults break the look the moment they open.
14. **Terse copy.** Say what the person gets in one sentence and no more, because every clause is read on every visit.
15. **A surface shows its subject.** What belongs to the subject is on screen and the rest is one command away, because repeating what another page owns buries the answer.

## Registers
### Layout
- Spacing scale 2, 4, 6, 8, 12, 16, 20, 24, 28, 32; 28 between sections, 12 from a section header to its content, 16 pane gutter.
- Columns: forms 720, dashboards and tables 1440; sheets 460 for confirmations, 560 for a thing's details or a picker, 640 for lists and sectioned settings.
- Bars: pane bar 40, tab bar 36, list toolbar 44; controls 28, text buttons 22. Top bar height is per product.
- Density: table row 36 and 44 for two lines, form row 52, card padding 16, on every platform.
- Lines: a hairline is 1 device pixel, only between bands and inside a bordered group; two neighbouring parts share at most one hairline, and groups parted by the 28 gap carry none.

### Color
- Grounds and inks are achromatic; lines and fills are the text color at low opacity: border 6 to 7.5 percent, fill 4.5 percent, hover 3.5 to 5 percent in light, and border 9 percent, fill 6.5 percent in dark, never solid gray steps, because alpha stays correct when surfaces stack.
- Very light gray means the fill and hover values above on a white ground; no tinted, blue or warm gray.
- State tones: ok, warning, danger, done (violet, finished work) and live blue, each as a dot, a text and a fill in the token files; a state is also said in words or shape, never hue alone.
- Accent is black by default (follows the text ink) and marks what can be acted on or was chosen; the chosen row stays the selected fill and a running state stays live blue whatever the accent.
- Charts: eight categorical hues and a seven step sequential blue, named in the token source; each series keeps its slot everywhere; a hardcoded hex in a chart is a bug.
- Shadows: popovers, menus and floating bars only, bordered; `0 12px 32px` at 14 percent in light and 45 percent in dark; a composer takes `0 1px 3px` at 4 percent.

### Type
- Sizes 12, 13, 14, 24 and 20 for a figure: body 13, meta and detail 12, navigation and section title 14, page title 24; the platform file adds or replaces sizes.
- Medium for titles and figures; numbers are tabular wherever they appear and can change; monospace only for code, hashes, addresses and copyable identifiers.
- Text is set through a role or a type-scale utility only, never a raw size.

### Motion
- Fast 150 ms for hover and press fills, switches and chevrons; fold 200 ms for content opening in place; sheet 250 ms entering from 95 percent scale; no UI transition over 300 ms except a digit roll, 500 ms.
- Ease out on the platform file's curve; transform, scale and opacity only, with scoped property lists and never `transition-all`.
- Under Reduce Motion every duration is zero, or as near zero as the platform allows.
- Live work is a dot matrix (5 by 5 grid, blink periods 0.9 to 1.4 s); a figure that changes as it is watched rolls its digits; a loading surface draws its frame and placeholders after 400 ms, with no stock spinner, no bouncing dots and no centered "Loading…".

### Copy
- Commands and menu items are title case, at most four words besides values; names of places, labels, descriptions and messages are sentence case; an ellipsis only when a command asks for more or opens a sheet.
- A subtitle, footer or empty state is one sentence on what the person gets, never how the product does it.
- No em dash, en dash or spaced hyphen as sentence punctuation in any product string; break with a period, comma or colon, and write ranges as `5 to 100`.

## Components
- **Sidebar**: navigation only, rows at the platform file's height, selected row on the selected fill, one trailing mark at most.
- **Top bar**: location on the left, at most two muted commands then an overflow, never an ink button.
- **Button**: weights `ink` (finishing only), `muted`, `popup`, `text`, `icon` (28 with a help tag), `glyph`; heights 28, text 22; radius 6 text buttons, 8 controls.
- **Dropdown and select**: the design system's own menu and select, 8 radius rows, destructive items last in the danger tone; a select always shows its chosen option's label, never its raw value.
- **Table and rows**: a row is the click target for its primary move, secondary moves in its menu and at most one trailing text button; no bordered or filled button in a row.
- **Dialog and sheet**: confirmations through the shared confirm component, never `window.confirm`; the destructive button is never ink and focus starts on Cancel.
- **Toast**: for a success whose result does not show where the person is; a failure is an alert, not a toast.
- **Empty state**: one meta line where content would be, or a title, a sentence and one next step.
- **Stat tile and figure**: label in meta, number in the figure role, at most one detail line, no box per figure.
- **Chart**: framed by one shared chart frame with shared theme, tooltip and legend; entrance animation off.
- **Badge**: 5 radius, never a pill.
- **Loading**: frame drawn at once, placeholders matched to the final footprint, dot matrix for live work.

## Reject
- A divider or box around every row or section → the 28 section gap and 12 inner gap, one hairline per band at most.
- A large row or oversized control → controls 28, table rows 36, card padding 16.
- Blue or tinted chrome, "gray gray" cards → white ground, fills at 4.5 percent, borders at 6 to 7.5 percent.
- A gradient background, glow or accent fill for decoration → none; hue only for state, accent and chart series.
- A shadow under a resting card → none; shadows only under popovers, menus and floating bars.
- A large radius → 8 on controls and rows, 12 on groups and floating surfaces, 5 on badges; pills only for dots, avatars and tracks.
- A hardcoded hex or palette step in a chart → the categorical slots, via the shared chart theme.
- A stock spinner or three bouncing gray dots → the dot matrix; layout that jumps while loading → a skeleton with the final footprint.
- A button that repeats a command already on screen → delete it; the command has one home.
- A wordy, formal or "AI" sounding sentence → one short plain sentence on what the person gets.

## Before calling a surface done
- Its type (tool, document or form) is named and decides padding, width and where status goes.
- No line, box or gradient was added that the content does not need.
- Every color is a token and every hue carries a state, the accent or a chart series.
- Light and dark, a narrow and a wide pane, and the empty, loading, error states have been looked at.
- Every command appears once and no ink button sits in a bar, row or header.
