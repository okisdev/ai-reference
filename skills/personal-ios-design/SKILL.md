---
name: personal-ios-design
description: "The maintainer's personal iOS design system (taste, exact values, components, and reject rules for iPhone and iPad apps in SwiftUI or React Native), read before building, reviewing, or redesigning an iOS UI whose DESIGN.md extends skill:personal-ios-design or when the user asks for an iOS UI in the maintainer's style."
argument-hint: "[build|review|learn] [surface or path]"
metadata:
  requires: "design-system"
---

## Context

Product design file: !`out=$(git ls-files 2>/dev/null | grep -iE '(^|/)DESIGN\.md$' | xargs grep -lE '^extends:.*skill:personal-ios-design' 2>/dev/null | head -4 | tr '\n' ' '); echo "${out:-(no DESIGN.md extends this skill)}"`

Sibling products: !`out=$(find .. -maxdepth 2 -name DESIGN.md -not -path "../$(basename "$PWD")/*" 2>/dev/null | xargs grep -lE '^extends:.*skill:personal-ios-design' 2>/dev/null | xargs ls -t 2>/dev/null | head -4 | tr '\n' ' '); echo "${out:-(none beside this checkout)}"`

Source files: !`out=$(git ls-files 2>/dev/null | grep -cE '\.(swift|tsx)$'); echo "${out:-0} matching files"`

## Instructions

**The one rule: an iOS surface in the maintainer's products follows this personal system and the product's own `DESIGN.md`, read in that order and applied in the reverse order of precedence, so the agent never falls back on its own taste or asks for a reference the system answers.** A great run names the product file it read, applies the exact values of [references/taste.md](references/taste.md), [references/swift.md](references/swift.md) for a SwiftUI app, then [references/ios.md](references/ios.md), which wins over taste.md on iOS wherever the product file is silent, takes each component from the product's exemplars, and says which rule decided each choice the user might question. Open [examples/applied.md](examples/applied.md) before reporting and check the run against [examples/rejected.md](examples/rejected.md).

### Process

1. Parse `$ARGUMENTS`: `build` a surface, `review` one, or `learn` from a correction; with no mode, take it from the conversation.
2. Read the product's `DESIGN.md` from the Context (the nearest one to the touched files when several exist): its scope, its token source, its overrides, its exemplars, and its checks. A repository with no such file is a new product: say so, read the sibling products from the Context (most recently changed first) or the one the user names, and apply this system.
3. Read [references/taste.md](references/taste.md), [references/swift.md](references/swift.md) for a SwiftUI app, then [references/ios.md](references/ios.md) whole; ios.md wins over taste.md on iOS. The product file overrides them rule by rule; everything it does not state comes from them, with their exact values.
4. Build or review with the system resolved: `build-ui` when installed builds from it, `review-ui` when installed reviews against it, and [references/checks.md](references/checks.md) gives the patterns a review runs over the diff when the product has not built them as checks yet. Without those skills, apply the registers and every "Before calling a surface done" list directly.
5. `learn`: a correction that holds for every product changes this skill's references (an edit to the maintainer's ai-reference checkout, shipped as a release; a change to taste.md is made in every personal design skill that carries it), one that holds for one product changes that product's `DESIGN.md`, through `design-system`'s learn mode; never write a correction into memory or a conversation note.
6. Report the product file and the references read, the rules that decided each visible choice, the code that breaks the system with the rule it breaks, and any correction routed in step 5.

### Rules

- Never apply a value from memory or another product: the value comes from this system or the product file, and a product's exemplars are read in place.
- Never write a product's own name, path, or token file into this skill; those belong in the product's `DESIGN.md`.
- Code that breaks the system is reported as a deviation with the rule it breaks, never copied as precedent.
