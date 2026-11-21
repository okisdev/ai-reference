# Craft rules

Generic craft rules for judging UI when the design system is silent. A design system's rules outrank these: its brand grays, radius, density, type scale, and motion curves win wherever it states them. Cite a rule here only for what the system leaves open, and never read a rule as a demand for a particular look.

Each rule gives a value or a test, then the failure it prevents.

## Layout

- Put every spacing, size, and gap on a 4 point scale (4, 8, 12, 16, 24, 32, 48, 64); test by listing the distinct spacing values in the diff, any off the scale is a finding. Prevents drift where near-identical gaps (13, 15, 18) make a page look unfinished.
- Group by proximity before lines or boxes: the gap inside a group is at most half the gap between groups. Prevents borders and cards used to repair spacing that never separated the groups.
- Set nested radius to outer radius minus the padding between them (outer 16 with 6 padding gives inner 10); clamp at 0. Prevents corners that look pinched or fat where a child sits inside a rounded parent.
- Size every interactive target to at least 40 by 40 points (44 on touch only surfaces); a smaller visual may extend its hit area with padding or a pseudo element. Prevents missed taps and misclicks.
- Keep 8 points or more between adjacent interactive targets. Prevents a tap landing on the wrong neighbor.
- Align on shared edges: left edges of stacked labels, inputs, and text start at one x; test by overlaying a vertical line at the container padding. Prevents ragged columns that read as accident.
- Align an icon to the text baseline or its optical center, not its box center; a play triangle or arrow shifts toward its visual mass. Prevents icons that look a pixel or two off beside text.
- Put the primary action where the eye ends: bottom end of a form or dialog, one primary per view. Prevents several equal buttons competing and users hesitating.
- Order DOM, tab order, and reading order identically; test by tabbing the page and reading the focus path aloud. Prevents focus that jumps around the screen.
- Cap prose containers at 45 to 75 characters per line (about 65ch); tables and code may run wider. Prevents long lines that lose the reader at each line return.
- Use fluid or breakpoint layout that holds at 320 points wide with no horizontal scroll and no clipped controls; test by resizing to 320 and to 200 percent zoom. Prevents unusable phone, split screen, and zoomed views.
- Reserve space for anything that loads later (images, ads, embeds) with an aspect ratio or fixed height. Prevents content jumping under the pointer as media arrives.
- Allow 30 to 40 percent extra width for translated labels and give controls min widths, never fixed widths; test with a pseudo localized string. Prevents truncated buttons in German, Finnish, and similar languages.
- Use logical properties (start, end, inline, block) instead of left and right; test by setting the root to right to left. Prevents mirrored layouts with icons and padding on the wrong side.
- Respect safe areas and the on screen keyboard: sticky bars sit inside insets and scroll fields into view. Prevents controls hidden under a notch, home indicator, or keyboard.

## Color

- Reserve color for meaning: one accent for the primary action and current selection, plus fixed status colors (error, warning, success, info). Test by squinting; if everything is colored nothing is. Prevents decoration diluting signals.
- Use tokens or variables only; a raw hex, rgb, or named color in component code is a finding. Prevents themes that cannot change and one off shades that drift.
- Reach 4.5 to 1 contrast for body text, 3 to 1 for large text (24 points, or 19 bold), icons that carry meaning, and control borders; measure rendered pairs, not the token alone. Prevents text lost in sunlight or for low vision users.
- Convey state by more than color: pair red or green with an icon, label, or pattern. Prevents the 1 in 12 men with color vision deficiency missing the state.
- Build dark theme as its own palette: lower surface lightness for depth (raised surfaces lighter), desaturate accents, never invert or reuse light shadows; test every screen in both. Prevents glaring accents, muddy elevation, and white boxes inside dark pages.
- Pass both themes for contrast and for images, charts, and logos with baked in backgrounds. Prevents unreadable assets after a theme switch.
- Tint neutrals toward the brand hue lightly rather than using pure black on pure white. Prevents harsh contrast and a flat, sterile look.
- Remove a control that can never apply here; one disabled only for now still passes 3 to 1 against its surface when the label matters and says why nearby. Prevents invisible controls, silent dead ends, and explanations for affordances that should not exist.

## Type

- Draw sizes from one modular scale of at most 6 to 8 steps, with a ratio between 1.125 and 1.25; test by counting distinct font sizes in the diff. Prevents arbitrary sizes that flatten hierarchy.
- Set body text at 16 px or larger on the web (17 points on iOS) and nothing meant to be read below 12. Prevents squinting and forced zoom, and the mobile browser zoom on focus for inputs under 16.
- Set body line height 1.4 to 1.6, headings 1.1 to 1.3, tightening as size grows. Prevents airy headlines and cramped paragraphs.
- Limit weights to 2 or 3 per surface (regular, medium or semibold, bold); hierarchy comes from size, weight, and color together, not weight alone. Prevents a page that shouts everywhere.
- Use tabular numbers in tables, prices, timers, counters, and anything that updates in place; test by watching a changing value for width shift. Prevents columns that wobble and totals that do not line up.
- Right align numeric columns on the decimal and left align text columns; header alignment matches its column. Prevents unreadable magnitude comparison.
- Prefer sentence case for labels, buttons, and headings; reserve all caps for short tags. Prevents slow reading of long capitalized strings.
- Wrap headings with balanced wrapping and paragraphs with pretty wrapping where supported; avoid single word last lines. Prevents orphans in headlines and short cards.
- Load fonts with a metric matched fallback and swap behavior; test with throttled network. Prevents invisible text and layout shift when the font arrives.
- Never size type in fixed pixels inside a container that must follow user text size; test at 200 percent text size. Prevents clipped copy for users who scale text.
- Truncate with an ellipsis only where full text is reachable (tooltip, detail view, expand); wrap by default. Prevents lost information that cannot be recovered.

## Motion

- Animate only to explain a change (entry, exit, reorder, cause and effect), never on high frequency or keyboard driven actions; test by asking what the user would miss with motion removed. Prevents decoration that slows repeat work.
- Time UI feedback at 100 to 200 ms for small elements (buttons, toggles, tooltips), 200 to 300 ms for panels and menus, 300 to 500 ms only for full screen or large distance moves; never above 500 ms for feedback. Prevents sluggish interfaces and abrupt jumps.
- Scale duration with distance and size: a larger or farther move gets the longer duration. Prevents small things dragging and big things snapping.
- Enter with ease out (fast start, soft landing) and exit with ease in or ease out at about 60 to 70 percent of the enter duration. Prevents entries that feel late and exits that hold the user up.
- Use ease in out for on screen movement between two resting points, and never plain linear except for progress and continuous loops. Prevents robotic motion.
- Start entries from a scaled origin near the trigger (scale 0.95 or above, plus opacity), never from scale 0; popovers grow from their anchor, modals from the center. Prevents elements appearing from nowhere.
- Make motion interruptible: a new input retargets from the current value, with transitions rather than keyframes for state that can reverse. Prevents jumps and queued animations after rapid input.
- Animate only transform, opacity, and clip or filter properties; never width, height, top, left, or margin on busy pages. Prevents dropped frames and layout thrash.
- Keep motion from shifting layout unasked: loaded content swaps into reserved space, and content opened in place by the person moves its siblings in the same animation while it is revealed inside its own clipped bounds, never fading in over neighbours that have not moved yet. Prevents jumping content, overlap and mis clicks.
- Judge a transition from frames captured mid change, not from its resting states, because overlap and jumps exist only between them.
- Honor the reduced motion preference: replace movement with an instant change or a short fade, keep essential progress indication; test by enabling the setting. Prevents nausea and vestibular triggers.
- Press feedback appears within 100 ms (scale 0.97 to 0.98 or a tonal change) and hover effects apply only where hover exists. Prevents laggy taps and stuck hover states on touch.

## Copy

- Label a control with what happens (Save changes, Delete project, Send invite), never OK, Submit, or Yes; test by reading only the button. Prevents the wrong click and confirmation dialogs nobody understands.
- Start errors with what happened and what to do next in plain words, never a code or blame (Could not save. Check your connection and try again). Prevents dead ends and users thinking they erred.
- Write one term per concept across the product (do not alternate delete, remove, and discard); test by searching the diff for synonyms. Prevents users wondering whether two words mean two things.
- Lead with the action or outcome, front load the key word, and keep a button to 1 to 3 words and a heading to one line. Prevents scanning that loses the point.
- Use sentence case, active voice, and present tense; no exclamation marks except real celebration. Prevents a tone that feels pushy or noisy.
- Put destructive confirmations in the object's name and consequence (Delete Q3 report? This cannot be undone), with a button that repeats the verb. Prevents accidental data loss.
- Format dates, numbers, plurals, and lists through the locale API and plural rules; never concatenate strings (3 item, 1 items). Prevents broken grammar and wrong formats abroad.
- Delete explanatory text before shortening it: a hint, footer, or row note survives only when the user would decide or act differently without it; test by removing each one and asking what the user loses. Prevents interfaces that explain themselves on every visit to users who stopped reading after the first.
- Show the exception, not the norm: a fact that is the same or normal on most rows (a current version, an active state, a unit after each number, a label prefix) is left out and appears as a word only on the row where it differs. Prevents rows that wrap into three lines of facts nobody compares.
- Make empty states state what belongs here and offer the next step; make success messages short and place them where the user looked. Prevents blank screens and missed confirmations.

## Accessibility

- Use native elements first (button, a, input, select, dialog); a div with a click handler needs role, name, key handling, and focus, so replace it. Prevents controls that mouse works on and nothing else does.
- Show a focus ring on keyboard focus only (focus visible), at least 2 points thick with 3 to 1 contrast against both surfaces, never removed without a replacement; test by tabbing the whole page. Prevents lost position for keyboard users, and rings on every mouse click.
- Make every function reachable by keyboard in a logical order, with no trap; modals trap focus while open, restore it to the trigger on close, and close on Escape. Prevents blocked users and lost context.
- Give every control an accessible name matching its visible label; icon only buttons get an aria label or visually hidden text. Prevents announcements of just button.
- Associate every input with a visible label and tie errors and hints through described by; test with a screen reader or the accessibility tree. Prevents fields heard as edit text.
- Announce dynamic changes (toasts, validation, async results) in a polite live region, and move focus to new page level content. Prevents silent updates.
- Give images alt text that conveys purpose, and empty alt for decoration; never repeat adjacent text. Prevents noise and missing meaning.
- Meet 4.5 to 1 and 3 to 1 contrast in every theme and state (hover, pressed, selected, disabled, placeholder). Prevents states legible only in the default.
- Support 200 percent zoom and text resize with no loss of content, and never block pinch zoom. Prevents low vision users being locked out.

## States

- Design every data view for loading, empty, error, partial, and full; test by forcing each in the browser or story. Prevents screens that only work on the happy path.
- Show loading as a skeleton or inline spinner shaped like the final layout, only after 200 to 300 ms delay, held for at least 400 ms once shown. Prevents flashes on fast loads and layout jumps.
- Prefer optimistic updates for reversible actions, and roll back with a message on failure; disable a submit only while it is in flight and show progress. Prevents laggy feel and double submits.
- Make errors recoverable in place: keep user input, offer retry, and mark the field and the summary. Prevents lost work after a failure.
- Test worst case data: names of 100+ characters, a single unbroken string (a long URL or hash), counts in the millions (abbreviate or wrap, never overflow), zero, one, and thousands of items, and right to left and non Latin text (CJK, Arabic, Thai) with taller line heights. Prevents overlap, clipped content, and broken layouts that only real data exposes.
- Handle long content with a deliberate policy per slot: wrap, truncate with access to the full text, or scroll; set min width zero on flex children that must shrink. Prevents containers blown open by one value.
- Check the dark theme, high contrast mode, and the narrow widths at 320, 375, and 768 points for every new surface. Prevents layouts that hold only in the developer's setup.
- Handle offline, slow network, permission denied, and expired session with their own message and exit. Prevents infinite spinners and blank panels.
- Give every action a confirmed outcome: disabled while pending, a success signal, and an undo for destructive or bulk changes where feasible. Prevents users repeating an action to check it worked.
