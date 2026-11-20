# Personal design taste: iOS

What an iPhone or iPad app adds to [taste.md](taste.md) and [swift.md](swift.md), whether it is built in SwiftUI or React Native. Where this file and taste.md disagree, this file wins on iOS; a product's `DESIGN.md` overrides all three.

## Registers
- Native navigation bars, tab bars, and system controls replace taste principles 4 (chrome is bands) and 13 (product drawn controls), because people expect the platform's bars and controls on a phone.
- Type is the platform's Dynamic Type text styles (body 17, callout 16, subheadline 15, footnote 13, caption 12, titles 20 to 28), never fixed sizes, so text follows the person's setting; meta lines are footnote; a fixed length beside text scales with it.
- Touch targets at least 44; a primary call to action 52 tall.
- Spacing scale 2 to 24; a screen gutter of 16 on small phones and 20 from 414 wide and on iPad.
- Glass and materials only on floating controls (a floating composer, a toolbar over content), never on content.
- One wordless activity indicator in the navigation bar while a screen loads; content uses placeholders shaped like the final rows.
- Haptics confirm a completed action or a threshold crossed, never every tap.

## Components
- Rows are the platform list rows, 44 minimum, one accessibility element each; secondary moves in a context menu or swipe actions.
- Confirmations are the platform confirmation dialog, one sentence on what is lost, the destructive role on its button.
- Sheets use the platform detents; a sheet that holds typed content asks before it is swiped away.

## Before calling a surface done
- The smallest and largest Dynamic Type sizes, light and dark, a small phone and an iPad, VoiceOver order, and the empty, loading and error states were looked at in the simulator.
