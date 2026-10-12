# Rejected report

An answer that is mostly right, cites nothing it read, and recommends something the project cannot import. Compare yours against it before replying.

````
`z.coerce.boolean()` is just `Boolean(value)`, so `"false"` becomes `true`. It has always worked that way, and if you want real string handling the newer `z.stringbool()` does it. Per the docs, it is safe to rely on.
````

Why each part fails:

- `is just Boolean(value)`: right from memory and still unproven; every claim names the rung, the exact version or ref, and the file and line that proved it, and a call that reading cannot settle is run in a scratch script instead of recalled.
- `It has always worked that way`: a history claim with no version behind it; bisect by packing a short list of versions (`npm pack <pkg>@<ver> --ignore-scripts`) and diffing, or report the history as unknown.
- `the newer z.stringbool()`: that API is on the default branch and absent from the pinned `3.23.8`; upstream reads pin a tag or commit, because the default branch describes a future version, and the installed copy decides what the project can import.
- `Per the docs`: docs answer intent and examples and never prove that an API exists or behaves as described; no link, no quote, no version.
- No unproven label: the reply never says which claims were read and which were recalled; a claim that cannot be proven is reported as unproven.
