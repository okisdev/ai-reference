# A run that clears the bar

The bar: every visible choice traces to a rule in the product file, taste.md, swift.md, or ios.md, with ios.md winning on iOS, and the product's exemplars are read instead of asked for.

> Ask: add a notifications settings screen.
>
> Read `DESIGN.md` (extends `skill:personal-ios-design`, system drawn), then `references/taste.md`, `references/swift.md` and `references/ios.md`.
>
> - The screen is a platform grouped list under the native navigation bar titled Notifications; no custom top bar (ios.md, Registers, which replace taste principle 4).
> - Each setting is a platform row at least 44 tall with a `Toggle`; the footer under a group is one sentence on what the person gets (ios.md, Components; taste, Copy).
> - Text uses Dynamic Type styles only: body for labels, footnote for the footers (ios.md, Registers).
> - Turning off all notifications asks through a confirmation dialog in one sentence on what is lost, the destructive role on its button (swift.md, Principle 4; ios.md, Components).
> - Loading shows the navigation bar's one indicator and placeholder rows, never a centered spinner (ios.md, Registers).
>
> Deviation found while reading: the existing account screen sets `.font(.system(size: 15))`, which breaks Dynamic Type; reported, not copied.

Why it clears the bar:
- It names the product file and each reference read.
- Each choice cites its rule with the exact value.
- Platform rules that replace taste are applied as ios.md says, not argued away.
- Code that breaks the system is reported, not followed.
