# Personal design taste: checks

Rules of taste.md and the platform file a match on code can enforce. A product that builds one lists it under its `DESIGN.md` Checks; until then a review runs the pattern by hand.

| Where | Pattern | Rule |
| --- | --- | --- |
| SwiftUI outside `Ink.swift` and `Measure.swift` | `.font(.system(`, `Color(`, `NSColor(`, `.cornerRadius(`, `.shadow(`, gradients, materials, raw animation durations | Roles, tokens, scales, flat |
| every product string | ` — `, ` – `, ` - ` | Copy: no dash punctuation |
