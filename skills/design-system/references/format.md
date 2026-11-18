# Design system format

One shape for every design system, so any skill can read any of them. A design system is a markdown file, `DESIGN.md` by default, owned by the repository it describes or by a shared design repository several products extend.

## Sections

```md
# <name> design system

extends: <owner>/<repo>:<path>
<One line: what it governs. Where the code breaks a rule here, the code is fixed.>

## Principles
1. **<Rule in a few words>.** <The rule>, because <the failure it prevents>.

## Tokens
- <platform>: `<path of the token source of truth>`; <how components reach them (CSS variables, a Swift enum, a theme object)>.

## Registers
### Layout
### Color
### Type
### Motion
### Copy

## Components
- **<component>**: <when it is used, its shape, its states, in one or two lines>.

## Reject
- <the mistake an agent makes> → <the fix, with the exact value>.

## Exemplars
- **<component>**: `<owner>/<repo>:<path>`, <why it is the one to read: current, follows the rules, tested>.

## Platforms
- **<web | SwiftUI | Compose | ...>**: <primitive library, where tokens live, how a register maps onto it>.

## Checks
- `<lint rule, test, or hook>` asserts <rule>; when this file and the check disagree, the check wins.

## Before calling a surface done
- <one checkable condition per line>
```

Empty sections are left out. A rule states an exact value whenever one exists (a duration, a radius, a gray step, a type size), because "subtle" and "dense" read differently to every agent.

## Inheritance

- `extends:` lines name the systems this one builds on, nearest last; a later system overrides an earlier one rule by rule, and a project file holds only what differs from what it extends.
- A reference is `<owner>/<repo>:<path>`, resolved against a local checkout of `<repo>` beside the current repository or under the same source root, and otherwise read through `gh api repos/<owner>/<repo>/contents/<path>` at the default branch; the owner may be left out only for a repository that has no remote, which then resolves from a local checkout alone.
- A repository names its system in its `AGENTS.md` with one line, `Design system: <owner>/<repo>:<path>`, or keeps a `DESIGN.md` at the root of the app it governs.

## Exemplars

An exemplar is the existing implementation an agent reads before building that component, chosen as the most current one that follows the rules: recently changed, consistent with the tokens, covered by a test where one exists. A repository whose design is stale, or that bypasses the tokens, is never an exemplar, and the system says so when it was once a reference. Exemplars are the reason an agent never has to be handed a path to another project.

## Platforms

One system can serve several platforms. The registers and principles are shared; each platform entry names where its tokens live and which primitives implement the components, so a SwiftUI app and a web app built on the same system read alike without sharing code.
