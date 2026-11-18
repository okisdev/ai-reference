# A run that clears the bar (illustrative)

What the user sees from a good run: the system and its `extends:` chain named, an exemplar read for every component from whichever sibling repository holds it, three genuinely different variants for an open redesign, tokens only, every state proven with evidence including worst-case data and dark, and a correction made during the run offered to the system. Names, paths, and values are invented; the shape is the bar.

````
Task: redo the billing settings page in `shop-web`, direction open.

System: `AGENTS.md` says `Design system: design-systems:acme/DESIGN.md`. Resolved from the sibling checkout `../design-systems`, then its `extends: design-systems:base/DESIGN.md`; `shop-web/DESIGN.md` overrides the gutter (32 above 1280). Read principles, Motion and Layout registers, Reject list, and the web platform entry.
Exemplars read: form section `shop-web:src/ui/form-section.tsx`; data table `admin-web:src/ui/table.tsx` (the system's exemplar, in a sibling repository; `legacy-admin` is excluded as stale); confirm dialog `shop-web:src/ui/confirm.tsx`. Primitives reused: `Button`, `Field`, `Table`, `Dialog` from `src/ui/`. Nothing hand-rolled and no reference asked of you.

Variants (the direction is open), behind a temporary `?variant=` switcher on `/settings/billing`:
- A, "ledger": invoices first as a table, plan summary in a right rail.
- B, "plan card": plan and payment method as two cards, invoices collapsed below.
- C, "single column": one form section per concern, invoices last.
You picked B. Promoted B into `settings/billing.tsx`; deleted A and C and the switcher.

Build: tokens only (`--space-4`, `--radius-2`, `--gray-5`, `--accent`), 180ms enter on the invoice disclosure per the Motion register, copy in sentence case ("Update payment method"). No new primitive, token, or dependency.

States verified in the browser (verify-ui, `localhost:3000/settings/billing`, light and dark, 360 and 1440 wide):
- Empty (no invoices): designed empty row with the "Download your first invoice after the next billing date" copy. Screenshot 1.
- Loading: the 5 row skeleton the system requires, no spinner. Screenshot 2.
- Error (invoices request 500): inline error with a retry button, plan card still shown.
- Partial: plan present, payment method missing; the card shows "Add payment method".
- Worst case: 214 invoices (virtualized), a 90 character company name that truncates with a title, a 48 character unbroken string that wraps with `overflow-wrap: anywhere`, a Japanese company name, a single invoice. Screenshots 3 to 5.
- Disabled: the plan change button is disabled for a member without the billing role, with a tooltip saying who can change it.
- Dark: every state above rechecked; borders `--gray-5` hold. Screenshots 6 and 7.
Review against the system (review-ui): 0 blocking, 1 polish (invoice date column left aligned; moved to the numeric alignment in the table exemplar), fixed.

Correction offered: you changed the plan card heading from 20 to 16 medium while we worked. That reads as a rule (card headings are 16 at weight 600 in settings). Offer to record it through design-system learn mode as a proposal. Awaiting your yes.

Tree is uncommitted.
````

Why it clears the bar:

- It names the system and walks the `extends:` chain to the file each value came from, so the user can see what governed the result.
- Exemplars come from the system's Exemplars section, including one in a sibling repository, and the stale repository is named as excluded; the user is never asked for a reference.
- An open redesign is decided by three named variants in the running app, one picked, the rest and the switcher deleted.
- Only tokens and the repository's primitives are used, and the report states that no primitive, token, or dependency was added.
- Every reachable state has evidence, including worst-case data, a single item, non-Latin text, disabled, dark, and both widths, and loading uses the system's skeleton and not a spinner.
- The review result is reported with its fix, and the user's correction during the run is offered to the system as a proposal instead of being lost.
