# Rejected report

A mirror that gets rewritten. Compare yours against it before reporting.

````
Matched the reference. Copied its Toolbar and FilterChip components, class strings and color tokens included (rounded-xl bg-zinc-900/60 text-[13px]), and renamed them to ours. Took the filter bar from the first reference and the page layout from the second and merged them. Read the references' current files. Looks identical to the reference now.
````

Why each part fails:

- `class strings and color tokens included (rounded-xl bg-zinc-900/60 text-[13px])`: class strings, tokens, colors, and names are never copied verbatim, and a rename leaves the skin intact; the pattern transfers, the skin does not (seen: asks to follow a reference without copying it, as in 参考 X，不要照抄, went ad hoc).
- `Copied its Toolbar and FilterChip components`: no search for an existing primitive; this repository already has `components/ui/toolbar.tsx`, and a parallel implementation must state what existing thing it rejected and why.
- `merged them`: with several references each contributes one named pattern class as a take and a not-take, and each adopted pattern is attributed, not blended into something nobody can trace.
- `Read the references' current files`: a reference's recent direction comes from its dated git history; current files cannot tell a direction from a leftover.
- `Looks identical to the reference now`: sameness is the failure, not the goal; the report states where the result diverges and why, and where it matches.
- No verification: the repository's own checks and a `verify-ui` render never ran for a UI result.
