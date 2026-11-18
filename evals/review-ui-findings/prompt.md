---
description: review-ui reports each finding with severity, the rule, and an exact fix, ranks the system rule and the missing state as blocking, and does not approve.
tags: [quality, review-ui]
runs: 2
max_turns: 10
timeout_seconds: 300
allowed_tools: [Skill, Read, Bash]
---

Use the review-ui skill to review this diff. Everything you need is below; do not run commands and do not change files. You cannot open a browser, so review in code.

System: `Design system: design-systems:acme/DESIGN.md`. Relevant rules: Color "no raw color where a token exists; tokens live in `tokens.css`, the success green is `--green-9`"; Reject "a gradient fill, use a flat token fill (`--gray-2`)"; Motion "enter 180ms `cubic-bezier(0.2, 0, 0, 1)`"; principle "every list has empty, loading, and error states".

```diff
--- a/src/ui/badge.tsx
+++ b/src/ui/badge.tsx
@@ -20,3 +20,3 @@
-  background: var(--gray-3);
+  background: #16a34a;
   color: white;
--- a/src/ui/drawer.tsx
+++ b/src/ui/drawer.tsx
@@ -55,3 +55,3 @@
-  transition: transform 180ms cubic-bezier(0.2, 0, 0, 1);
+  transition: transform 300ms ease-in;
--- a/src/routes/orders.tsx
+++ b/src/routes/orders.tsx
@@ -78,2 +78,6 @@
+  return (
+    <ul>
+      {orders.map((o) => <OrderRow key={o.id} order={o} />)}
+    </ul>
+  );
--- a/src/routes/orders.css
+++ b/src/routes/orders.css
@@ -46,2 +46,3 @@
+.hero { background: linear-gradient(90deg, #ffffff, #eeeeff); }
```

Reply in English with your review.
