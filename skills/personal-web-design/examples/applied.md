# A run that clears the bar

The bar: every visible choice traces to a rule in the product file or the system, and the product's exemplars are read instead of asked for.

> Ask: add a "Delete workspace" action to the workspace settings page.
>
> Read `apps/web/DESIGN.md` (extends `skill:personal-web-design`), then `references/taste.md` and `references/web.md`. The product file says nothing about destructive actions, so the system decides:
>
> - The action lives in the settings section it affects, as a text button in the danger tone (Principle 2, one command in one place; Button weights: `ink` is for finishing only).
> - It opens the shared confirm component, never `window.confirm`; the destructive button is not ink and focus starts on Cancel (Components, Dialog and sheet). The exemplar the product file names, `components/shared/confirm-dialog.tsx`, is reused as is.
> - The confirmation is one sentence on what is lost: "Delete Acme and its 12 projects? This cannot be undone." No dash as punctuation (Copy).
> - Sheet width 460 for a confirmation (Layout, Columns); 250 ms entering from 95 percent scale (Motion).
>
> Deviation found while reading: the settings page's section headers sit in bordered boxes, which breaks Principle 3 (whitespace over lines); reported, not copied.

Why it clears the bar:
- It names the product file and each reference it read.
- Each choice cites its rule, with the exact value.
- It reuses the product's exemplar instead of asking for a reference.
- Code that breaks the system is reported as a deviation, not followed.
