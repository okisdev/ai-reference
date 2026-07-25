---
name: diagnose-root
description: Diagnose a failure to its origin with a reproduction first, fix the cause rather than the symptom, and stop at the diagnosis when only an explanation was asked.
argument-hint: "<symptom-or-error>"
---

## Context

Dirty status: !`git status --short | head -5`
Recent commits: !`git log --oneline -5` (a fresh regression usually traces here)

## Instructions

Reproduce the failure before explaining it, trace it to the origin, name the mechanism in one sentence, and fix at the origin or stop at the diagnosis when the ask was a question.

### Process

1. Parse `$ARGUMENTS` (an error string, a failing behavior, or a why question; take it from the conversation when absent). Classify the ask: a why question or a problem description ends at the diagnosis report in step 4; only an explicit fix request continues past it.
2. Reproduce first: run the failing thing (the repro command, the failing test, the dev server route) and capture the actual output. A diagnosis without an observed reproduction is a guess. When the failure cannot be reproduced, say so and check the log history for a fixing commit before concluding anything.
3. Trace to the origin: follow the wrong value or behavior from the symptom site backward through the call path, configuration, data source, or generation step until the first place it is wrong. For third-party behavior, compose `read-source` at the pinned version. Name the origin as file and line.
4. State the mechanism in one sentence: explain why that origin produces this symptom. Report the symptom, the origin, the mechanism, and the evidence chain. This is the stopping point for a why question.
5. Reject the surface patch explicitly before fixing: state what the symptom-site workaround would be and why it loses (it hides recurrence, diverges siblings, or contradicts the repo's paradigm). When the root fix is genuinely disproportionate, report the tradeoff and let the owner choose instead of silently patching.
6. Fix at the origin, conforming to the repo's own paradigm, then sweep for the same root cause elsewhere in the repository and fix or list every other site.
7. Prove it: rerun the exact reproduction from step 2 and show the before and after, then run the repo's own checks for the touched packages.

### Rules

- No fix before an observed reproduction, and no diagnosis delivered as fact without one; label unreproduced hypotheses as hypotheses.
- A why question never turns into an edit; deliver the diagnosis and stop.
- A symptom-site workaround ships only with the rejected root fix and the reason recorded in the report.
