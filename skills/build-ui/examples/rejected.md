# A run that gets stopped by the user (illustrative)

Each line below is a failure a build run has shown. Compare your run against it.

````
Which existing page should I use as a design reference for the billing settings? Meanwhile I made it clean and modern.

I wrote my own dropdown for the plan picker. Styles:
  background: #f7f7f8; border-radius: 10px; padding: 14px; box-shadow: 0 4px 12px rgba(0,0,0,.15);
  transition: all 0.3s ease-in;
  <Spinner /> while invoices load.
Added `framer-motion` for the card hover and a new `--card-bg-2` token.

I took a screenshot of the page and it looks good. Done.
````

Why each line fails:

- `Which existing page should I use as a design reference`: the system's Exemplars section already answers it, in whichever of the user's repositories it lives; resolve the system and read them (seen: the user pasted the same sibling repository paths as design references in about twenty sessions).
- `I made it clean and modern`: the surface is built from the system and its exemplars, never from the agent's own taste, and an open direction is decided by showing variants.
- `I wrote my own dropdown`: the repository's primitive and the exemplar's composition are reused; a hand-rolled component the library already provides is a defect.
- `#f7f7f8`, `10px`, `14px`, the raw shadow: raw color, size, radius, and shadow where tokens exist; every value comes from a token on the system's scale.
- `transition: all 0.3s ease-in`: off the Motion register (180ms enter, a named property, the system's easing) and `all` animates properties nobody meant to.
- `<Spinner />`: the system's loading pattern is the skeleton and it rejects the stock spinner.
- `framer-motion` and `--card-bg-2`: a new dependency or token needs a statement of what it replaces and why, and the repository already covered the need.
- `a screenshot ... looks good`: one screenshot proves one state; empty, loading, error, partial, worst-case data, disabled, dark, and the narrowest and widest widths each need evidence.
- No variants, no system named, no review against the system, no correction offered: the report names the system and exemplars used, the variants shown, the states verified, and any correction offered to design-system.
