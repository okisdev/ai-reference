---
name: mirror-reference
description: Adapt a design, interaction, or API from a URL, repository, or sibling path the user points at into this project's own components, never a copy (参考, 借鉴, 照着做, 不要照抄).
argument-hint: "<url-or-path>... [target-area]"
---

## Context

Current branch and status: !`git branch --show-current; git status --short | head`

UI or primitives directories: !`out=$(find . -name node_modules -type d -prune -o -type d \( -iname ui -o -iname primitives \) -print 2>/dev/null | head -5); echo "${out:-(none)}"`

## Instructions

**The one rule: take the pattern and leave the skin.** The result reads as native to this repository and untraceable to the reference in class strings, tokens, colors, and names, and the report says where it diverges and why. The bar is a deviation report with one take and not-take per reference, every adopted pattern attributed, and every deviation argued from this repository's idiom: open [examples/deviation.md](examples/deviation.md) before reporting, and check the draft against [examples/rejected.md](examples/rejected.md).

Study the reference until the pattern separates from its styling, implement the pattern in this repository's own primitives and conventions, and report where and why the result deviates from the reference.

### Process

1. Parse `$ARGUMENTS` (one or more references: a URL, an owner/repo, or a local sibling path; an optional target area names where in this codebase the pattern lands; with no arguments, infer both from the conversation instead).
2. Study each reference with the tool that matches its shape: a repository through `gh` (shallow clone or fetch files via the API) rather than scraping its rendered site, a docs or marketing page through a web fetch, a local sibling path by reading it directly. Identify the load-bearing pattern, the structure, API shape, interaction, or behavior that makes the reference work, and separate it from the reference's styling, naming, and tokens; the pattern transfers, the skin does not. When what makes the reference worth following is how it presents information (what it shows, how it groups and orders it, and the marks that let a person scan it, such as flags, badges, or status dots), that presentation is the pattern and transfers too, drawn in this repository's own components; "不必完全照抄" leaves out the reference's styling, never its information layout (seen: a diagnostics page that kept only the reference's behavior drew "我感觉我们现在一点排版都没有，也没有对应的，比如说国旗之类的").
3. Read the target area's own idiom before writing: nearest siblings decide naming, placement, and import style, and the repository's own primitives and helpers are the building blocks. Read the repository's `AGENTS.md` and README first when the codebase is unfamiliar.
4. Implement the pattern expressed entirely in this repository's conventions and primitives. Search for an existing primitive before writing a new one; a new parallel implementation states what existing thing was rejected and why.
5. Write the deviation report as part of the result: where the implementation intentionally diverges from the reference and why (this repository's idiom, its constraints, its design system), where it matches, and which reference each adopted pattern came from when more than one reference was studied.
6. Verify with the repository's own checks; compose `verify-ui` for render evidence when the result is UI.

### Rules

- Never copy class strings, design tokens, colors, or naming verbatim from a reference; every borrowed pattern is re-expressed in this repository's own primitives (seen: asks to follow a reference without copying it, as in 参考 X，不要照抄, went ad hoc).
- More than one reference means attribution per adopted pattern, not a blend nobody can trace.
- With several references, each contributes one named pattern class (language, density, page skeleton, interaction grammar), stated as take and not-take per reference; a reference's recent direction is read from its dated git history, not its current file state.
- A reference the task says to study without implementing produces the pattern analysis and deviation notes only, with zero edits.
