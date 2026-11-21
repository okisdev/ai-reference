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
3. Walk each register over the scope, reading the code and, when a browser tool is available, the rendered result (`verify-ui` when installed): layout (grid, a row composed by hand instead of the system's row component, a row taller than two lines or with its command on its own line, side by side sections without a shared edge whose trailing status reads as orphaned, alignment measured from bounding boxes rather than judged by eye, equal top and bottom insets, leading marks and trailing values in reserved columns, conditional elements that reserve their space, spacing on the scale, density, hierarchy, whitespace before lines and boxes), color (tokens only, contrast, color reserved for meaning), type (scale, weights, line length, tabular numbers), motion (purpose, duration, easing, interruption, layout shift, a view that blanks or shows a placeholder when a control switches it, reduced motion), copy (first an inventory of every string that is not a label or a value: footers, subtitles, meta facts, hints, popovers, badges, units, card summaries; each one deleted in turn and kept only when the person would decide or act differently without it, a removable one reported as delete rather than rewritten shorter or moved to a footer, and a sentence repeated across rows or restating the list beside it reported as one finding; then voice, length, and labels that say what happens), accessibility (focus, keyboard, names, hit areas, contrast), states (empty, loading, error, overflow with worst-case data, dark theme, narrow widths), and structure (the same data or command on two surfaces, a page or tab that answers no question of its own, a command on a surface that does not own it), whose findings propose the merge or deletion instead of a restyle.
   An explanation is judged as a symptom before it is judged as copy: name the design change that makes it unnecessary (a clearer label, a better default, the state shown as data, a verb on the one row that can act), because shortening a sentence the person never needed keeps its cost (seen: a review kept 50 of 56 settings footers by rewording them, and moved a caveat repeated on every device row into a footer instead of asking whether it should exist).
   With a browser, run `<this skill's directory>/scripts/detail-audit.js` in each page under review once it shows real data, again after each switch or action, and in each viewport the product supports, and report its counts (layout shifts, wrapped labels, icons off centre, clipped text, internal ids, a row repeating its own words, sibling panels whose rows disagree, values that only say nothing is set) beside the screenshot, because these are the details a screenshot read by eye passes over and a measurement does not.
4. Record each finding with its severity: **blocking** breaks a system rule, an accessibility requirement, or a state the user can reach; **should-fix** breaks a craft rule with a visible cost; **polish** is a refinement. Each finding gives `file:line`, the rule quoted from the system or [references/craft.md](references/craft.md), and the fix with its exact value or token.
5. Approve only when no blocking finding remains; say which registers and states were checked in the browser and which only in code.
6. A finding that repeats across files and that a match can catch (a raw color, a radius off the scale, a banned property) is reported once with every site and proposed as a check for the system (`design-system` when installed).

### Rules

- Never pass a register unchecked; one not reviewed is reported as not reviewed.
- Never invent a taste rule for the user's system; a preference the system does not state is a craft finding at most, cited to the craft reference.
- Read only: the review changes no files.
