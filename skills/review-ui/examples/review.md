# A review that clears the bar (illustrative)

What the user sees from a good review: the system it judged against, findings by register with a severity, `file:line`, the quoted rule from the system or the craft reference, the exact fix as a value or token, a plain split of what was checked in the browser and what only in code, a register named as not reviewed, and a repeated finding proposed as a check. Files, lines, and values are invented; the shape is the bar.

````
Reviewed the uncommitted diff (4 files) against `design-systems:acme/DESIGN.md` (extends `base`). Verdict: not approved, 3 blocking.

Color
- BLOCKING `src/ui/badge.tsx:22`, system rule "no raw color where a token exists": `background: '#16a34a'`. Fix: `var(--green-9)`.
- BLOCKING `src/routes/orders.css:48`, system Reject "a gradient fill → a flat token fill": `linear-gradient(90deg, #fff, #eef)`. Fix: `background: var(--gray-2)`.

Motion
- SHOULD-FIX `src/ui/drawer.tsx:57`, system Motion "enter 180ms cubic-bezier(0.2, 0, 0, 1)": `transition: transform 300ms ease-in`. Fix: `transition: transform 180ms cubic-bezier(0.2, 0, 0, 1)`. Craft: ease-in delays the first frame the user sees.

States
- BLOCKING `src/routes/orders.tsx:81`, system principle "every list has three states": the order list renders rows only, no empty or error state, and the loading state is the first render with no skeleton. Fix: add the empty row ("No orders yet. They appear here after checkout."), the error row with a retry, and the 5 row skeleton from `src/ui/table.tsx`.

Layout
- POLISH `src/routes/orders.tsx:94`, craft layout "figures in columns align": the total column is left aligned. Fix: `text-align: right; font-variant-numeric: tabular-nums`.

Copy (6 strings that are not labels or values; 2 kept)
- SHOULD-FIX `src/routes/orders.tsx:102`, craft copy "delete explanatory text before shortening it": every unpaid row carries "Payment syncs from Stripe every hour". Nobody acts on it per row. Fix: delete it; the one row whose payment failed shows the verb "Retry payment".
- SHOULD-FIX `src/routes/orders.tsx:96`, craft copy "show the exception, not the norm": each meta line reads "Created 3 May · v2 checkout · EUR". Fix: date only; "v1 checkout" appears on the rows still on it.

Accessibility: no findings. The drawer close button has `aria-label="Close order details"` and 44 by 44 hit area (`drawer.tsx:63`).

Checked in the browser (verify-ui, `localhost:3000/orders`, light, 1440 wide): layout, color, motion (recorded the drawer enter, measured 300ms), the populated state.
Checked in code only: dark theme, the 360 wide layout, the error state, keyboard focus order. Not reviewed: type, because the diff touches no text styles beyond the lines above and I did not render at a second size.

Repeated finding: raw hex colors appear at 4 sites (`badge.tsx:22`, `orders.css:31`, `orders.css:48`, `drawer.tsx:12`). Reported once. Proposed check `no-raw-color` for the system (stylelint, `#[0-9a-fA-F]{3,8}` outside `tokens.css`); awaiting your yes before it goes to design-system.

No files were changed.
````

Why it clears the bar:

- It names the system it judged against and ranks each finding blocking, should-fix, or polish, with the system rules outranking the craft ones.
- Each finding carries `file:line`, the rule quoted from the system or the craft reference, and a fix as a value or a token, never an adjective.
- It says what was checked in the browser and what only in code, and reports the unreviewed register as not reviewed instead of passing it.
- It does not approve while a blocking finding remains.
- The raw color repeated at four sites is reported once with every site and proposed as a check, not as four findings.
- It inventories the explanatory strings before judging wording, and a removable one is reported as delete with the design change that replaces it, never reworded or moved.
- It invents no taste: where the system is silent the finding cites the craft reference, and the review is read only.
