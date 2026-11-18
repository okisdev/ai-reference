---
type: llm
weight: 2
---

The review reports at least these four findings (other valid findings are fine): the raw hex color in `badge.tsx` where `--green-9` exists, the 300ms ease-in transition in `drawer.tsx`, the list in `orders.tsx` with no empty state (and no loading or error state), and the gradient in `orders.css`. Each carries a severity, and the gradient (a system rule) and the missing state are ranked blocking.
