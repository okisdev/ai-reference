# A run that clears the bar

The bar: every visible choice traces to a rule in the product file, taste.md, swift.md, or macos.md, and the product's exemplars are read instead of asked for.

> Ask: add a menu bar item that shows how many builds are running.
>
> Read `DESIGN.md` (extends `skill:personal-macos-design`, token drawn), then `references/taste.md`, `references/swift.md` and `references/macos.md`. The product file names `Sources/AppUI/Popover.swift` as the popover exemplar.
>
> - The item is one figure, the running count in tabular digits; it rolls its digits when the count changes (taste, Motion; macOS, Components).
> - A click opens a 320 wide popover on 16 padding built from the exemplar; a right click opens a menu with Open and Quit; the popover holds no switches (macOS, Registers and Components).
> - Each build in the popover is one row: name over one meta line joined by ` · `, a live tone dot of 6 beside the word Running, one VoiceOver element (swift.md, Principles 1 and 3; Status dot).
> - No shadow beyond the popover's own; color only for the live state (taste, Principles 8 and 10).
>
> Deviation found while reading: the existing preferences window uses the system `Picker` menu style, which breaks the macOS rule that menus and selects come from the product's own components; reported, not copied.

Why it clears the bar:
- It names the product file and each reference read.
- Each choice cites its rule with the exact value.
- It reuses the product's exemplar instead of asking for a reference.
- Code that breaks the system is reported, not followed.
