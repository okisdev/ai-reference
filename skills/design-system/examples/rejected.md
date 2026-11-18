# A merge that gets stopped by the user (illustrative)

Each line below is a failure a design system run has shown. Compare your run against it.

````
Merged both products into `DESIGN.md` in each repository.

## Principles
1. Keep the interface clean and modern.
2. Use subtle, tasteful animations.
3. Be dense but never cluttered.
4. Follow Material guidelines for elevation and shadows.
5. Prefer calm, muted colors.

## Registers
Spacing is generous. Radius is soft. Motion is quick. Text is highly readable.

## Exemplars
- Dropdown menu: ask the user to paste the one from the other project.
- Table: `legacy-console:src/table.tsx`

Both product files keep a full copy of the principles so each stays self-contained. Where the products disagreed on gutter width I used the average, 28. I also added a rule that every button uses title case, since that is common practice.
````

Why each line fails:

- `Keep the interface clean and modern`, `subtle`, `dense`, `calm`: an adjective gives every agent a different reading; a register states a duration, a radius, a gray step, or a row height.
- Principles with no because-clause: each principle names the failure it prevents, otherwise an agent cannot tell which cases it extends to.
- `Follow Material guidelines`: copying another organization's system into the user's is never the job; a pattern is re-expressed in the user's own tokens.
- `Spacing is generous. Radius is soft.`: no scale, no values, nothing a check or a reviewer can compare against.
- `ask the user to paste the one from the other project`: exemplars exist so the user never hands over a path again; choose the current implementation across the products.
- `legacy-console:src/table.tsx` as an exemplar: a repository that is stale or bypasses the tokens is never an exemplar, and the system names it as excluded with the reason.
- `each stays self-contained` with full copies: shared principles move into one file the products extend, or the copies drift (seen: two design docs carrying the same eight principles nearly word for word).
- `the average, 28`: a value that differs between products stays in each product's file, never averaged into a value neither one uses.
- `every button uses title case, since that is common practice`: good practice the user never expressed is not their taste; a rule the user did not say, edit, or confirm is a proposal with an inferred why, and the user decides.
- No Checks and no report of sources, proposals, or exclusions: every rule a match can enforce is proposed as a check with its file and pattern, and the report lists what awaits the user.
