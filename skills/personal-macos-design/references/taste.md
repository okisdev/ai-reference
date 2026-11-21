# Personal design taste

The maintainer's taste on every platform: dense, flat, achromatic chrome with color only where it carries meaning. The platform file beside this one adds or replaces values for its platform, and a product's own `DESIGN.md` holds its differences, token files, and exemplars and overrides both rule by rule. Where the code breaks a rule here, the code is fixed.

## Principles
1. **One name, one place.** The top bar says where the pane is (a breadcrumb counts), and no page title or header repeats it, because a repeated name is noise the eye must skip on every visit.
2. **One command, one place.** A command on the whole surface lives in the top bar, on part of it in that row or section, and one that needs input in a sheet, because a command shown twice makes people wonder whether the two differ.
3. **Whitespace over lines, until sections sit side by side.** In a single column, separate groups with the section gap before adding a hairline or a box, and never box a box, because every extra line and layer competes with the content; where sections share a row of a grid, each takes one edge (a panel) so its title, its trailing status and its content read as one group, because whitespace alone cannot tell which far right status belongs to which title.
4. **Chrome is bands.** A pane stacks top bar, tab bar, toolbar, strips and content, each full width with one job and a hairline between band and content, because nothing should float in a padded box.
5. **Tools run edge to edge, documents sit in a column.** A surface the person works in fills its pane from the margin line, and so do the details, settings and info tabs inside it; only a standalone document or a sheet sits in a reading column, because a capped column inside a tool leaves a dead strip beside it.
6. **One grid.** Every band starts and ends on its pane's margin line, and a control in a corner sits as far from the top edge as from the side, with every control in that row centred on it, because bands or corners that disagree on the margin read as misalignment.
7. **Weight follows finality.** Ink fills only the button that completes what the person is composing; everything else is bordered, a word or a glyph, because several filled buttons leave no way to tell which one finishes the task.
8. **Hue is meaning.** Chrome is black, white and very light gray; color marks a state, the person's accent, or a series in a chart, never decoration or a button's rank, because color that decorates cannot also mean something.
9. **Dense by default.** Rows, controls and cards take the smallest size on the scale below, because large elements leave too little information on screen.
10. **Flat.** No gradients, glows, glass or material in content; a shadow only under what floats, because depth on resting surfaces reads as heavy and dirty. Chrome may carry the platform's window material or a translucent sticky top bar.
11. **Charts are varied and colored.** Show data as the chart form that fits the question, in the categorical palette, never as text or only plain lines, because text and uniform lines hide the shape of the data.
12. **Motion is slight and carries its neighbours.** Motion shows where a change came from and never makes the person wait; when content opens or closes in place, everything it pushes moves in the same animation and the new content is revealed inside its growing bounds, because content that fades in over neighbours that have not moved yet reads as overlap.
13. **Controls are drawn by the product, not the platform default.** Where the platform file says so, a dropdown, select, menu, scrollbar and toast come from the product's own components, because the defaults break the look the moment they open.
14. **Terse copy.** Say what the person gets in one sentence and no more, because every clause is read on every visit.
15. **A surface shows its subject.** What belongs to the subject is on screen and the rest is one command away, because repeating what another page owns buries the answer.
16. **Switching never reloads.** A tab or page keeps its state once built and a revisit shows its last result at once while it refreshes in place, because a blank frame or a lost search on every switch reads as a broken app.
17. **A row asks for one thing.** A row that needs the person shows only the verb that fixes it (Allow, Set Up); a row that is fine shows only its state; never a state word beside a button that opens somewhere else, because two marks for one fact double the reading.
18. **Safe and destructive never share a group.** What frees space or resets nothing the person would miss sits apart from what loses data, and each row that loses data says what it deletes in the row itself, because a mixed "danger zone" leaves the person to guess which button costs them.
19. **What cannot apply is not drawn.** A disclosure with nothing hidden, a tab, filter or toggle that cannot apply to this subject, a picker with one choice, and a column or row whose value is the same or empty for every item are absent rather than empty, disabled or a dash, because an affordance that leads nowhere misleads.
20. **Nothing appears by pushing.** A control, status line or title that shows only sometimes takes reserved space or overlays the content, because content that jumps when something appears reads as broken.
21. **A state never wears a control's shape.** A state is a word or a dot, never a bordered capsule, and anything that looks clickable is clickable; a reference the product can show (an id, a commit, a host) opens it there, because a state shaped like a button invites a click that does nothing.
22. **Structure before polish.** Before a surface is refined, its place in the product is challenged: every page, section and command is listed with the question it answers, and two that answer the same question merge, one that answers none goes, and a command shown on surfaces it does not own moves to the one that does, because polish on a redundant structure makes the redundancy permanent.
23. **Explanation is the last fix.** Before a footer, subtitle, row note, hint or popover explains something, the surface changes so it needs none: a clearer label, a better default, the state shown as data, or the limitation removed; a sentence stays only when the person would decide or act differently without it, sits where that decision is made and appears once, because text that explains the interface is read on the first visit and skipped on every one after.

## Registers
### Layout
- Spacing scale 2, 4, 6, 8, 12, 16, 20, 24, 28, 32; 28 between sections, 12 from a section header to its content, 16 pane gutter.
- Columns: forms 720, dashboards and tables 1440; sheets 460 for confirmations, 560 for a thing's details or a picker, 640 for lists and sectioned settings.
- Bars: pane bar 40, tab bar 36, list toolbar 44; controls 28, text buttons 22. Top bar height is per product.
- Density: table row 36 and 44 for two lines, form row 52, card padding 16, on every platform.
- Lines: a hairline is 1 device pixel, only between bands and inside a bordered group; two neighbouring parts share at most one hairline, and groups parted by the 28 gap carry none.
- Symmetry: a block's top and bottom insets are equal, and bars that face each other across columns (a sidebar header and the top bar) share one height and one hairline.
- Sections: a section is a one line header (title, its meta inline on the same baseline, trailing actions, control height) and its content 12 below; in a single column it is never a box, and side by side in a grid it is a panel (1 pixel border, radius 12, padding 16, 16 between panels, panels in one row stretched to one height); section headers in one grid row share a top edge.
- Row columns: leading marks (flag, swatch, icon, dot) sit in one reserved leading column and trailing values in a reserved right aligned column, so every title and number in a list starts on one line whatever a row carries.
- Row text: a row is its title and at most one meta line holding only what tells rows apart; a fact that is normal or the same on most rows (the current version, an "active" state, a unit after every count, a label prefix such as "Last active:") is not drawn and returns as a word on the row where it becomes the exception ("Needs update"), and a sentence that would repeat on two or more rows becomes the one row's verb where the person can fix it, or goes.
- Optical edge: a trailing glyph, icon or ghost button aligns its glyph, not its padded box, with the margin line, and a leading one does the same on the other side.

### Color
- Grounds and inks are achromatic; lines and fills are the text color at low opacity: border 6 to 7.5 percent, fill 4.5 percent, hover 3.5 to 5 percent in light, and border 9 percent, fill 6.5 percent in dark, never solid gray steps, because alpha stays correct when surfaces stack.
- Very light gray means the fill and hover values above on a white ground; no tinted, blue or warm gray.
- Hover is always lighter than selected (hover 3.5, selected 6 percent in light), and both fills are inset so the gap between rows survives, because a hovered row that matches the selected one shows two selections.
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
- Live work is a dot matrix (5 by 5 grid, blink periods 0.9 to 1.4 s); a figure that changes as it is watched rolls its digits; a loading surface draws its frame and placeholders after 400 ms, with no stock spinner, no bouncing dots and no centered "Loading…"; a surface seen before shows its cached result instead of placeholders.
- Content opening in place (a disclosure, an expanding row) uses the fold duration on a spring with no bounce, driven by the state change itself so every ancestor and sibling moves with it, and is clipped to its own bounds; closing fades without sliding back.
- A switched tab cross fades in the fast duration and its selection mark slides between tabs; the views behind it are kept, never rebuilt.
- A control that switches what a view shows (a segmented control, a range, a tab inside a section) keeps the last result on screen, dimmed to half opacity, until the next one arrives and then fades it back in the fast duration; its selection mark slides in 200 ms; a placeholder is only for the view's first load, and the view keeps its height across the switch (a legend stays one line), because a blank frame or a jump on every switch is the flash people notice first.

### Copy
- Commands and menu items are title case, at most four words besides values; names of places, labels, descriptions and messages are sentence case; an ellipsis only when a command asks for more or opens a sheet.
- A subtitle, footer or empty state is one sentence on what the person gets, never how the product does it, and exists only after principle 23: deleted, not shortened, when the person loses nothing without it; the one fact that changes a decision (what a backup leaves out, what a toggle also turns off) is said even where every other sentence goes.
- A footer holds one subject; a card summary or hub row never restates the place it opens; a row whose meaning lives in its footer takes the sentence as its own meta line; a credit or disclaimer that must ship sits once on the page that owns it (About, Privacy), never under each section.
- No em dash, en dash or spaced hyphen as sentence punctuation in any product string; break with a period, comma or colon, and write ranges as `5 to 100`.

## Components
- **Sidebar**: navigation only, rows at the platform file's height, selected row on the selected fill, one trailing mark at most.
- **Top bar**: location on the left, at most two muted commands then an overflow, never an ink button.
- **Button**: weights `ink` (finishing only), `muted`, `popup`, `text`, `icon` (28 with a help tag), `glyph`; heights 28, text 22; radius 6 text buttons, 8 controls.
- **Dropdown and select**: the design system's own menu and select, 8 radius rows; a select always shows its chosen option's label, never its raw value; the trigger keeps its pressed state while open, and the menu is as wide as its content.
- **Destructive command**: anything that deletes, kills, resets or discards sits in the last group of its menu after a separator, in the danger tone with an ellipsis, through one shared component, and always opens a confirmation that names what is lost; it has one home, never a row glyph beside a menu item that does the same.
- **Table and rows**: every row in the product is the one row component: a mark in the leading column, a title, at most one meta line with further facts joined by a middle dot, a trailing value or state, and its command at the row's end; a row is the click target for its primary move, secondary moves in its menu and at most one trailing text button; no bordered or filled button in a row, no third line, no command on a line of its own, because rows built per feature disagree on where their text starts and stack into tall, half empty blocks.
- **Dialog and sheet**: confirmations through the shared confirm component, never `window.confirm`; the destructive button is never ink and focus starts on Cancel.
- **Toast**: for a success whose result does not show where the person is; a failure is an alert, not a toast. Every action answers: either its result appears where the person looks or a toast says it happened, and every copy toasts. One at a time, a capsule at the bottom centre of the focused window or viewport with a glyph and at most four words, gone after 1.8 s, announced to the screen reader.
- **Ranked list**: a ranking on a dashboard shows its first ten rows and a toggle for the rest that appears only when rows are hidden; a scroll area nested in the page is for streams such as logs, never for a ranking, because a clipped half row reads as broken.
- **Log view**: monospace lines with the time muted, the source in its categorical color only when several sources share the view, and the message; a line is red or orange only when it states error or warning itself, never for the stream it came on; search marks matches in place; wrapped by default; it follows the newest line until the person scrolls up, then a capsule offers the way back with the count of new lines.
- **Empty state**: one meta line where content would be, or a title, a sentence and one next step.
- **Stat tile and figure**: label in meta, number in the figure role, at most one detail line, no box per figure.
- **Chart**: framed by one shared chart frame with shared theme, tooltip and legend; entrance animation off. A part of a whole shows at most eight slices, the rest as one neutral "other"; a mirrored chart sizes its two halves by their peaks, so a small side never leaves a blank half.
- **Chart tooltip**: floats above every surface beside the pointer (right of it, flipping left at the edge, never clipped by a sidebar or pane and never over the section header); it names the shared qualifier once in its title, lists only non-zero series in descending order, and shows at most eight rows with a count of the rest.
- **Badge**: 5 radius, never a pill.
- **Loading**: frame drawn at once, placeholders matched to the final footprint, dot matrix for live work.
- **Disclosure row**: a chevron at the leading edge that turns a quarter as it opens; children beneath in the compact row, indented so their marks line up with the parent's title, along a hairline guide that ends at the last child; siblings keep the chevron's column so every mark stays on one line; the open parent and its children share one faint fill.
- **Status**: the state of a subject (a service, a sync, a job) is one dot in a state tone at the end of a row that already exists, its details in the hover tag; the commands that change it live on the page that owns the subject, never in a capsule or banner of their own.
- **Capacity**: storage or quota is one bar parted by category in the categorical palette over its limit, then one row per category with its size; removals follow, grouped as principle 18 says.
- **File browser**: the path as a breadcrumb that is always shown, every folder but the last going back, beside a button to the enclosing folder; entries in the product's grouped rows, folders first, icon, name over size, kind and date, a chevron on folders that open in place; search and sort in the bar above, never a column table.

## Reject
- A divider or box around every row or section → the 28 section gap and 12 inner gap, one hairline per band at most.
- A section header whose description wraps to a second line beside a one line header → the description inline after the title, so neighbouring headers align.
- A hover fill equal to the selected fill → hover 3.5 percent, selected 6.
- A row showing the same moment twice ("21 days ago" and "15:44") → one of them, the other in the hover tag.
- An on and an off button for one state → a switch when the state is known, else both commands in the row's menu.
- A form field or its submit stretched across a wide pane → the form keeps a 560 column, so the label, the input and the button stay together.
- Unboxed sections side by side in a grid, with a status floating far from its title → a panel per section, 16 apart.
- A row that stacks a title, a detail, an evidence line and a link on four lines → one row: the title, one meta line, the link at its end.
- Two kinds of rows in one list with different leading marks (a dot beside an icon box) → the same row component, each mark centred in the same leading column.
- A view that blanks, shows a placeholder or changes height when its segmented control switches → the last result stays, dimmed, until the next arrives; the height is reserved.
- A tab bar with one tab, or a section of empty states and dashes for data the source cannot provide → no tab bar, no section, no row.
- A control split from what it acts on (a group by switch on its own row above a table, an export beside the filters) → on the header row of the section it acts on.
- A large row or oversized control → controls 28, table rows 36, card padding 16.
- Blue or tinted chrome, "gray gray" cards → white ground, fills at 4.5 percent, borders at 6 to 7.5 percent.
- A gradient background, glow or accent fill for decoration → none; hue only for state, accent and chart series.
- A shadow under a resting card → none; shadows only under popovers, menus and floating bars.
- A large radius → 8 on controls and rows, 12 on groups and floating surfaces, 5 on badges; pills only for dots, avatars and tracks.
- A hardcoded hex or palette step in a chart → the categorical slots, via the shared chart theme.
- A stock spinner or three bouncing gray dots → the dot matrix; layout that jumps while loading → a skeleton with the final footprint.
- A button that repeats a command already on screen → delete it; the command has one home.
- "Not allowed" beside "Open Settings" → one verb that does it, "Allow".
- One "Danger zone" holding cleanups and resets alike → a safe group and a group that names what each row deletes.
- Content that fades in over rows that have not moved yet → animate the state change for the whole layout and clip the reveal.
- A details or settings column capped and pinned left in a wide tool pane → fill the pane from the margin line.
- A wordy, formal or "AI" sounding sentence → one short plain sentence on what the person gets.
- A footer or hint rewritten shorter when deleting it loses nothing → delete it.
- A caveat repeated on every row of one kind, or moved into the footer instead → the verb that fixes it on the one row the person can act on, or nothing.
- Versions, build numbers, "active" or a unit on every row → the exception word on the row it applies to, the number alone in the trailing column.
- A status line that counts what the list below shows, or a requirement that can never read as met → delete it.
- A redesign that keeps every existing page and only restyles it → the structure pass first: the pages merged, deleted or moved, then the polish.

## Before calling a surface done
- Its type (tool, document or form) is named and decides padding, width and where status goes.
- No other page answers the question this one answers, and no command on it belongs to another page.
- No line, box or gradient was added that the content does not need.
- Every color is a token and every hue carries a state, the accent or a chart series.
- Light and dark, a narrow and a wide pane, and the empty, loading, error states have been looked at.
- Every command appears once and no ink button sits in a bar, row or header.
- Every footer, subtitle, meta fact, hint, popover and unit was deleted in turn and kept only where the person would decide or act differently without it, with the count before and after reported, and a test asserting deleted copy goes with it.
- Every transition was checked in frames captured mid change, not from the resting state, and alignment that matters was measured rather than judged by eye: the edges of section headers in one row, controls in one bar, and the insets on every side of a block, reported as numbers.
- A redesigned pattern lives in one shared component and every place a search finds the old pattern uses it, because fixing only the screen that was pointed at leaves its siblings in the old look.
