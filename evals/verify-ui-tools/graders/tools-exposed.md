---
type: llm
weight: 2
---

The plan drives the page only with tools the prompt lists, and it chooses Gode's site tools for the check because they can emulate a phone viewport and the dark color scheme (for example `emulate_site` with a mobile viewport near 390 by 844 and a dark `colorScheme`), where Claude in Chrome can only resize its window. It opens `http://localhost:3001`, not port 3000. It names no tool the prompt says is absent (`navigate_page`, `emulate`, `evaluate_script`, `take_screenshot`, `resize_page`, `take_snapshot`), and it does not call the check impossible or leave dark mode out because Chrome DevTools MCP is missing.
