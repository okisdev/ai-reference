# A review that gets stopped by the user (illustrative)

Each line below is a failure a review has shown. Compare your review against it.

````
I looked at the page and it looks great overall. The spacing feels a bit off and the colors could be more polished, and the animation seems a little slow. Maybe consider making the empty state nicer. I'd also say the design should feel more premium, so I switched the buttons to a pill shape and used a softer gray.

Everything else looks fine. LGTM, approved.
````

Why each line fails:

- `it looks great overall`: approval is earned; nothing passes because it looks fine at a glance, and a review that approves names no rule checked.
- `spacing feels a bit off`, `colors could be more polished`, `a little slow`: an adjective is not a finding; give `file:line`, the quoted rule, and the exact value (`gap: var(--space-3)`, `180ms`).
- No severity: every finding is ranked blocking, should-fix, or polish, and a broken system rule or a missing state is always blocking.
- `Maybe consider making the empty state nicer`: a missing state is a blocking finding with the exact fix, not a suggestion.
- `should feel more premium`, `pill shape`, `softer gray`: inventing taste the system does not state; a preference outside the system is a craft finding at most, cited to the craft reference, and a review never switches a style on its own.
- `I switched the buttons`: a review is read only and changes no files.
- `Everything else looks fine`: a register not reviewed is reported as not reviewed, and the review says which registers and states were checked in the browser and which only in code (dark theme, narrow width, error and loading states, and keyboard focus were never mentioned).
- `LGTM, approved`: approval only when no blocking finding remains, with the system named and the checked registers listed.
- A raw color that repeats at several sites was never reported once as a proposed check for the system.
