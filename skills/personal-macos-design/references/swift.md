# Personal design taste: Swift layer

What the Swift apps share beyond [taste.md](taste.md): a native row and control contract, and two ways to draw a surface, by the system or by tokens. A product's own `DESIGN.md` names which way it draws and its exemplars.

## Principles
1. **A row is one element.** A row of a name, facts and marks is combined into one accessibility element, because VoiceOver otherwise reads each fragment as a separate stop.
2. **A glyph control says its name.** An icon only control carries a `.help` tag and an accessibility label with the same words, because a glyph alone names nothing to the pointer or to VoiceOver.
3. **A row's facts are one meta line.** Facts follow the name on one line in the meta style, joined by ` · `, never commas or stacked lines, because the middle dot keeps one fact from reading as a clause of the next.
4. **A confirmation names the loss.** A command that deletes or ends work asks first through the platform's confirmation, in one sentence on what is lost, with the destructive role on its button and Cancel as the default, because a bare "Are you sure?" leaves the person guessing what the answer costs.
5. **No literal color in a view.** A view takes color from its app's token file, its asset catalog or a system semantic color; a literal hex or RGB lives only where the color is the content (a copied swatch, rich text), because a literal in a view cannot follow light, dark or the person's accent.
6. **The system font, nothing else.** Text is SF through the platform's text styles or an app's role table; monospace only for code and copyable identifiers, because a second family breaks Dynamic Type and the platform's own bars.
7. **A surface is drawn one way.** A surface is either system drawn (platform lists, forms, text styles and semantic colors) or token drawn (`Ink`, `Measure`, `TypeRole`), never a mix inside one pane, because the two disagree on row height, radius and ink.

## Tokens
- token drawn: the app's color, measure, and type role tables (`Ink`, `Tone`, `Measure`, `TypeRole`, `Motion`) holding the values taste.md names, reached only through `.role(_:tone:)` and those types.
- system drawn: no token file; text styles (`.body`, `.subheadline`, `.footnote`, `.caption`), semantic colors (`.primary`, `.secondary`, `.tertiary`, `Color.accentColor`) and the app's `AccentColor` asset, with any fixed lengths in one metrics type.

## Registers
### Layout
- A system drawn row is an `HStack` with 12 between its leading mark and its text, `.padding(.vertical, 3)`, and a `VStack` of the name over one meta line spaced 2 or 3; its trailing marks are one value, then at most one control.
- A row with a name over a meta line is at least 44 high; the platform file sets any compact row and the window or screen frame around the rows.

### Color
- A state is a filled dot or symbol in a state tone beside its word, never hue alone; a token drawn app uses `Tone`, a system drawn app uses the system green, orange, red and blue for ok, warning, danger and live.
- Fills and lines in a system drawn pane are `Color.primary` at low opacity (fill 4.5 percent, hairline 7 percent), matching the alpha lines of taste.md; never a gray step.

### Type
- A system drawn app sets text in the system styles: body for names, the platform file's meta style for meta lines, subheadline for secondary words, footnote for captions under a group, caption only inside dense marks; numbers that change use `.monospacedDigit()`.

### Mechanics
- Content that opens in place is driven by an animated binding or `withAnimation` on the state change, never a scoped `.animation(_:value:)`, because a scoped animation leaves the ancestors and siblings to jump; the opening view is clipped with `.clipShape` to its own bounds.
- A row that is focusable for the keyboard uses `.focusable(interactions: .activate)`, so a mouse click leaves no focus fill behind.
- Tabs keep their views alive in a `ZStack` of visited views shown by opacity, hit testing and accessibility hiding, never a `switch` that rebuilds them.
- A card's inset hairlines come from `Group(subviews:)` over its rows, so callers never draw dividers.
- An app on both iPhone and Mac draws its shared pages through one file of small views that each pick the platform's way (a page stack, a link to a route, page commands, a choice picker, a working indicator, the finishing and soft button styles), so a shared page names one view and never branches per control.

## Components
- **Row**: the name over one meta line, a trailing detail in the tabular meta style, at most one trailing control; secondary moves in the context menu.
- **Confirmation**: platform `confirmationDialog` for a system drawn app, `ConfirmSheet` for a token drawn app; the message is one sentence.
- **Empty state**: `ContentUnavailableView` with one label, one sentence and at most one action in a system drawn app; one meta line where rows would be in a token drawn app.
- **Status dot**: 6 in a token drawn app; a system drawn app uses a 9 point `circle.fill` symbol hidden from VoiceOver, because the word beside it is what is read.
## Reject
- Facts joined by commas or on separate lines → one meta line joined by ` · `.
- An icon only button without `.help` → add the tag and an accessibility label.
- `Color(red:green:blue:)` or a hex in a view → a token, an asset or a system semantic color.
- A custom font or a rounded or serif design in chrome → the system font; design variants only where the person chooses a typeface for their own text.
- A fixed `.font(.system(size:))` in a system drawn view → a text style, so Dynamic Type applies.
- A confirmation that asks "Are you sure?" → one sentence on what is lost.
- `.animation(_:value:)` on a disclosure → an animated binding on the state change and a clipped reveal.
- A `switch` over tabs that rebuilds each view → kept views in a `ZStack`.

## Platforms
- **SwiftUI**: one Swift package per app; a token drawn app takes its token tables, a system drawn app takes only system styles and its `AccentColor`; localized strings go through `LocalizedStringResource` in a package.
- **iOS**: native navigation and system controls replace principles 4 and 13 of taste.md; a fixed length beside text scales with `@ScaledMetric`.

## Before calling a surface done
- It is drawn one way, system or tokens, and names which.
- Every row reads as one VoiceOver element and every glyph control has a help tag.
- No literal color sits in a view.
- Light and dark, the smallest and largest Dynamic Type or the narrowest pane, and the empty, loading and error states have been looked at.
