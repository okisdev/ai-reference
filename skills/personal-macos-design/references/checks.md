# Personal design taste: checks

Rules of taste.md and the platform file a match on code can enforce. A product that builds one lists it under its `DESIGN.md` Checks; until then a review runs the pattern by hand.

| Where | Pattern | Rule |
| --- | --- | --- |
| desktop `*.module.css` | gradients, `backdrop-filter`, `box-shadow` not `var(--shadow-`, transitions not `var(--motion-`, radii and font sizes off the scale | Flat, motion, scales |
| SwiftUI pages outside the UI module | `.font(.system(`, `Color(`, `NSColor(`, `.cornerRadius(`, `.shadow(`, gradients, materials, raw animation durations | Roles, tokens, scales, flat |
| SwiftUI on macOS | `.font(.title3)` on names or sidebar rows, `.animation(` beside a disclosure's state, `NavigationSplitView` with an empty detail | Sized like the system, motion carries neighbours, drill in |
| every product string | ` — `, ` – `, ` - ` | Copy: no dash punctuation |
