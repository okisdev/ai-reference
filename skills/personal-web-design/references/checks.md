# Personal design taste: checks

Rules of taste.md and the platform file a match on code can enforce. A product that builds one lists it under its `DESIGN.md` Checks; until then a review runs the pattern by hand.

| Where | Pattern | Rule |
| --- | --- | --- |
| web `**/*.tsx` | `transition-all` | Motion: scoped property lists |
| web charts outside the chart theme | `#[0-9a-fA-F]{3,8}\b` | Color: no hardcoded chart hex |
| web `**/*.tsx` | `bg-(gradient\|linear)-`, `linear-gradient(`, `radial-gradient(` | Flat |
| web `**/*.tsx` | `rounded-(xl\|2xl\|3xl)` outside floating surfaces, `rounded-[Npx]` | Radius scale |
| web `**/*.tsx` | `text-[Npx]`, `text-(3xl\|4xl\|5xl\|6xl)` | Type scale |
| web `**/*.tsx` | `shadow-(md\|lg\|xl\|2xl)` outside popover, menu, sheet, toast | Shadows only under what floats |
| web `**/*.tsx` | `window.confirm`, `alert(` | Confirm through the shared component |
| web `**/*.tsx` | `<select` | The system's select |
| web `**/*.tsx` | `animate-spin` outside a button's busy state | No stock spinner |
| every product string | ` — `, ` – `, ` - ` | Copy: no dash punctuation |
