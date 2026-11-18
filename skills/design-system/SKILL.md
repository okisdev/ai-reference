---
name: design-system
description: Create, extract, merge, or update a design system that agents read before UI work (principles, tokens, registers, components, reject rules, exemplars, platforms), including turning repeated design corrections into rules and sharing one system across several products.
argument-hint: "[create|extract|merge|learn|audit] [paths or repos...]"
---

## Context

Design docs here: !`out=$(git ls-files 2>/dev/null | grep -iE '(^|/)DESIGN\.md$' | head -8); echo "${out:-(none)}"`

Design system pointer: !`out=$(find . -maxdepth 2 -name AGENTS.md -not -path './node_modules/*' -exec grep -hiE '^(- )?design system:' {} + 2>/dev/null | head -3); echo "${out:-(none)}"`

Token files: !`out=$(git ls-files 2>/dev/null | grep -iE '(^|/)(tokens?|theme|globals)\.(css|ts|json|swift|kt)$' | head -8); echo "${out:-(none)}"`

## Instructions

**The one rule: a design system holds the user's taste as exact, checkable rules with their reasons, and every product that shares that taste reads one copy.** A great run leaves a system in the format of [references/format.md](references/format.md) where each principle names the failure it prevents, each register gives values instead of adjectives, each component points at the exemplar to read, duplicated principles across products have moved into one shared system the products extend, and every rule the user did not state is marked as a proposal. Open [examples/system.md](examples/system.md) before writing and check the draft against [examples/rejected.md](examples/rejected.md).

### Process

1. Parse `$ARGUMENTS` into one mode: `create` a new system from the user's direction, `extract` one from existing code and docs, `merge` several products' systems into a shared one plus per-product differences, `learn` rules from the corrections in a session or set of sessions, or `audit` an existing system's truth and exemplars. Paths or repositories name the evidence; without them, use this repository and the repositories its design docs and the conversation name.
2. Gather the evidence before writing a rule: every `DESIGN.md` and design section of an `AGENTS.md` in scope, the token files, the component library and its primitives, and the user's own words. For `learn`, read the corrections the way `distill-session` does when installed: explicit corrections, silent edits of files an agent wrote (their value is the rule), repeated nudges (record where they landed), reverts and rejected variants, and confirmed choices a fresh agent would not repeat (seen: about fifty sessions where the user called a design ugly or off-system and the rule was never written down).
3. Write each rule with an exact value and its reason: a duration, a radius, a gray step, a type size, a row height, never "subtle" or "dense" alone; a reason the user never gave is written as a proposal marked *inferred*, because a wrong why gets extended to cases it does not fit. A rule only the user's taste supports stays only when the user said, edited, or confirmed it; good practice the user never expressed belongs to the craft references of `review-ui`, not to their system.
4. Choose one exemplar per component across every product in scope: the implementation that is current (recent changes), follows the tokens, and is tested where tests exist; name the stale or token-bypassing repositories that are not exemplars, because a stale reference teaches the old design (seen: the user handed agents the same set of sibling repository paths in about twenty sessions, some of them stale).
5. In `merge`, move every principle and register value two or more products share into one shared system, and leave each product's file with `extends:` and only its differences; a principle that differs in substance between products stays in each product, never averaged into the shared file (seen: two products' design docs carried the same eight principles nearly word for word, each copy free to drift).
6. Turn every rule a match on code can enforce (a banned value or property, a raw literal where a token belongs, a radius or duration off the scale) into a proposed check with its file and pattern, and list it under Checks once it exists, because a check runs every time while a sentence is skipped once the context fills.
7. Write the system and its pointers: the shared file in the repository that owns it, each product's `DESIGN.md` with its `extends:` lines, and one `Design system: <owner>/<repo>:<path>` line in each product's `AGENTS.md`; a system shared by the user's private products is packaged as a skill (`extends: skill:<name>`) holding only the taste, and each product's exemplars, paths, and token files stay in that product's `DESIGN.md`, because a skill may be published while the products are private.
8. Report the rules written with their sources, the proposals awaiting the user (each with its inferred why), the exemplars chosen and the repositories excluded with the reason, the checks proposed, and what each product file kept as its own. Stop at an uncommitted tree.

### Rules

- Never invent taste: a rule the user did not say, edit, or confirm is a proposal, never a rule.
- Never copy another organization's design system into the user's; take a pattern through `mirror-reference` when installed and re-express it in the user's own tokens.
- Token values live in their source files; the system points at them and names only values the code does not hold.
