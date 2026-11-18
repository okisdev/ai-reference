---
name: build-ui
description: Build, redesign, or restyle a UI surface or component so it follows the repository's design system, reading the system's exemplars across the user's projects instead of asking for references, comparing variants when the direction is open, and covering every state.
argument-hint: "<surface, route, or component> [--variants <n>]"
---

## Context

Design system: !`out=$(find . -maxdepth 2 -name AGENTS.md -not -path './node_modules/*' -exec grep -hiE '^(- )?design system:' {} + 2>/dev/null | head -2); d=$(git ls-files 2>/dev/null | grep -iE '(^|/)DESIGN\.md$' | head -4 | tr '\n' ' '); echo "${out:-(no pointer)} ${d:-(no DESIGN.md)}"`

UI primitives: !`out=$(git ls-files 2>/dev/null | grep -E '(^|/)components/ui/|packages/(ui|design)/src/' | sed -E 's#/[^/]+$##' | sort -u | head -5); echo "${out:-(none)}"`

## Instructions

**The one rule: the surface is built from the governing design system and its exemplars, never from the agent's own taste or a reference the user has to hand over again.** A great run names the system it followed, the exemplar it read for each component, builds only with the repository's tokens and primitives, decides an open direction by showing variants rather than guessing, and proves every state before handing over. Open [examples/build.md](examples/build.md) before reporting and check the run against [examples/rejected.md](examples/rejected.md).

### Process

1. Parse `$ARGUMENTS`: the surface, route, or component, the platform it ships on, and `--variants <n>` to compare directions. A screenshot, a picked DOM element, or a sketch the user pasted is a locator for what to change, resolved to its file and line.
2. Resolve the governing design system: the nearest `DESIGN.md` from the touched files up to the repository root, or the system the repository's `AGENTS.md` names (`Design system: <owner>/<repo>:<path>`), then each `extends:` line in order, a `skill:<name>` read from that installed skill's references and an `<owner>/<repo>:<path>` read from a local checkout beside this repository or through `gh api` at the default branch. Read its principles, registers, components, reject list, and the platform entry for this platform. With no system, say so, build from the repository's nearest siblings, and offer `design-system` to write one once the user has corrected the result.
3. Read the exemplar for every component the surface uses before writing it: the file the system's Exemplars section names, in whichever of the user's repositories it lives, plus the repository's own primitive for it; reuse the primitive, follow the exemplar's composition, and never hand-roll a component the library or an exemplar already provides (seen: the user pasted the same sibling repository paths as design references in about twenty sessions). An outside reference the user points at goes through `mirror-reference` when installed.
4. When the direction is open (a new surface, a redesign, the user unsure between options, or `--variants`), build two or three genuinely different variants behind a temporary switcher in the running app, each named by its idea, and let the user pick before promoting one into the real code and deleting the rest.
5. Build with tokens only: no raw color, size, radius, shadow, or duration where a token exists, and every value on the system's scale; layout, density, and motion follow the registers, and copy follows the Copy register and the repository's voice.
6. Cover every state the surface can reach: empty, loading (in the system's loading pattern, never a stock spinner the system rejects), error, partial data, overflow with worst-case data (long names, unbroken strings, huge counts, an empty list, a single item, non-Latin text), disabled and permission-limited, light and dark, and the narrowest and widest supported widths.
7. Render it and look: `verify-ui` when installed, walking each state above; then review the result against the system (`review-ui` when installed) and fix every blocking finding before handing over.
8. Report the system and the exemplars used, the variants shown and the one chosen, the states verified with their evidence, and any correction the user made during the run, offered to `design-system`'s learn mode when installed so the next session starts from it.

### Rules

- Never ask the user for a design reference the governing system's exemplars already answer.
- Never add a new primitive, token, or dependency while one in the repository or the system covers the need; a new one states what it replaces and why.
- Leave the tree uncommitted; committing composes `commit-changes` when installed.
