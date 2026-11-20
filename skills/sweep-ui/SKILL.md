---
name: sweep-ui
description: Find every screen, sheet, dialog, popover, window, and state a redesign or design system has not reached yet, including the ones hidden behind a button, a menu, an error, or a first run, and list or migrate each one.
argument-hint: "[app | path] [--fix]"
---

## Context

Design system: !`out=$(find . -maxdepth 2 -name AGENTS.md -not -path './node_modules/*' -exec grep -hiE '^(- )?design system:' {} + 2>/dev/null | head -2); d=$(git ls-files 2>/dev/null | grep -iE '(^|/)DESIGN\.md$' | head -4 | tr '\n' ' '); echo "${out:-(no pointer)} ${d:-(no DESIGN.md)}"`

UI stack: !`out=$(git ls-files 2>/dev/null | grep -oE '\.(swift|tsx|jsx|vue|svelte|kt|dart)$' | sort | uniq -c | sort -rn | head -4 | tr '\n' ' '); echo "${out:-(none)}"`

## Instructions

**The one rule: a sweep inventories surfaces from the code, never from what the navigation shows, so a sheet behind a button, a dialog behind an error, or a window behind a menu item is found before the user finds it.** A great sweep names the system and its component inventory, lists every presenter and state the code can reach with how to reach it, marks each one on system, partial, or off system with the rule it breaks, groups the stragglers by the one shared component that fixes them, and says which surfaces it opened and which it judged from code alone. Open [examples/sweep.md](examples/sweep.md) before reporting and check it against [examples/rejected.md](examples/rejected.md).

### Process

1. Parse `$ARGUMENTS`: the scope (the whole app by default, or a path) and `--fix` to migrate what the sweep finds; without it the sweep only reports.
2. Resolve the governing design system the way `build-ui` does (the nearest `DESIGN.md` or the `AGENTS.md` pointer, then its `extends:` chain), and list its component inventory from the code: the public views, styles, and modifiers of the UI module or design package, each with the pattern it owns (form sheet, viewer sheet, menu picker, toast, empty state). With no system, say so and sweep for consistency between surfaces instead.
3. Inventory every surface from the code with the stack's presenter patterns in [references/surfaces.md](references/surfaces.md): pages and routes with each tab; every sheet, popover, alert, confirmation, inspector, panel, window scene, menu bar window, context menu, and toast; and each surface's branches (empty, loading, error, permission denied, offline, first run, a record that no longer exists, a feature the build cannot offer). Record for each one the file and line that presents it and the path a person takes to reach it.
4. Classify each surface: **on system** when built from the inventory's components; **partial** when it mixes them with the signals in [references/surfaces.md](references/surfaces.md); **off system** when it draws its own header, footer, buttons, pickers, fields, or layout values, or carries a second implementation of a pattern the system owns (seen: a project log sheet was redesigned while the build log sheet beside it kept the old header and blue Done).
5. Open what can be opened in the running app (`verify-ui` when installed, or the platform's accessibility actions and window captures): trigger each presenter, force each branch with a fixture, a flag, or a stopped dependency, and capture it; a surface that cannot be reached stays in the report as judged from code.
6. Report one table per group: surface, how to reach it, status, the rule it breaks, and the fix named as a component. Group stragglers by shared fix, so one new or extended component covers many surfaces, and list a component the system is missing as its own finding.
7. With `--fix`: author or extend each missing component in the UI module first (`build-ui` when installed), migrate one surface as the exemplar and verify it by capture, then migrate the rest in batches with disjoint files, verify each batch in the running app, and sweep again until no off system surface remains.
8. Turn each signal that a match can catch into a check for the system (`design-system` when installed), so the next sweep starts from a failing check instead of a screenshot.

### Rules

- Never stop at the surfaces the sidebar, tabs, or routes show; a presenter found in code and not reported is a missed finding.
- Never mark a surface on system from its code alone when it could be opened; say which were captured.
- Leave the tree uncommitted.
