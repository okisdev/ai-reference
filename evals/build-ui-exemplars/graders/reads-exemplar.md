---
type: llm
weight: 2
---

The answer resolves the design system through the `AGENTS.md` pointer, takes the exemplar the system names for the dropdown (`shop-web:src/ui/menu.tsx`) as what it builds from (the facts the prompt gives about these files count as read), and reuses the repository's `Menu` primitive rather than hand-rolling a dropdown. It does not ask the user for a design reference, a sibling project to copy, or a screenshot, and it does not take `legacy-console` as a reference.
