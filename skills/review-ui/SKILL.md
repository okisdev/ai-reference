---
name: review-ui
description: Review UI changes, a page, or a whole app against its design system and the craft of layout, color, type, motion, copy, accessibility, and states, reporting each finding with its severity, the rule it breaks, and the exact fix.
argument-hint: "[diff | path | route] [--register <layout|color|type|motion|copy|a11y|states>]"
---

## Context

Design system: !`out=$(find . -maxdepth 2 -name AGENTS.md -not -path './node_modules/*' -exec grep -hiE '^(- )?design system:' {} + 2>/dev/null | head -2); d=$(git ls-files 2>/dev/null | grep -iE '(^|/)DESIGN\.md$' | head -4 | tr '\n' ' '); echo "${out:-(no pointer)} ${d:-(no DESIGN.md)}"`

Changed UI files: !`out=$(git diff --name-only HEAD 2>/dev/null | grep -E '\.(tsx|jsx|vue|svelte|css|swift|kt)$' | head -10); echo "${out:-(none)}"`

## Instructions

**The one rule: approval is earned, so every finding cites the rule it breaks and the exact fix, and nothing passes because it looks fine at a glance.** A great review names the design system it judged against, walks each register, ranks findings blocking, should-fix, or polish with `file:line`, quotes the system rule or craft rule each one breaks, gives the fix as a value or a change rather than an adjective, and says plainly what it could not check. Open [examples/review.md](examples/review.md) before reporting and check it against [examples/rejected.md](examples/rejected.md).

### Process

1. Parse `$ARGUMENTS`: the scope (the uncommitted and branch diff by default, a path, or a route) and an optional `--register` to narrow the review.
2. Resolve the governing design system the way `build-ui` does: the nearest `DESIGN.md`, or the `AGENTS.md` pointer, then its `extends:` chain. Its rules outrank the craft references; with no system, judge against [references/craft.md](references/craft.md) alone and say so.
3. Walk each register over the scope, reading the code and, when a browser tool is available, the rendered result (`verify-ui` when installed): layout (grid, alignment, spacing on the scale, density, hierarchy, whitespace before lines and boxes), color (tokens only, contrast, color reserved for meaning), type (scale, weights, line length, tabular numbers), motion (purpose, duration, easing, interruption, layout shift, reduced motion), copy (voice, length, labels that say what happens), accessibility (focus, keyboard, names, hit areas, contrast), and states (empty, loading, error, overflow with worst-case data, dark theme, narrow widths).
4. Record each finding with its severity: **blocking** breaks a system rule, an accessibility requirement, or a state the user can reach; **should-fix** breaks a craft rule with a visible cost; **polish** is a refinement. Each finding gives `file:line`, the rule quoted from the system or [references/craft.md](references/craft.md), and the fix with its exact value or token.
5. Approve only when no blocking finding remains; say which registers and states were checked in the browser and which only in code.
6. A finding that repeats across files and that a match can catch (a raw color, a radius off the scale, a banned property) is reported once with every site and proposed as a check for the system (`design-system` when installed).

### Rules

- Never pass a register unchecked; one not reviewed is reported as not reviewed.
- Never invent a taste rule for the user's system; a preference the system does not state is a craft finding at most, cited to the craft reference.
- Read only: the review changes no files.
