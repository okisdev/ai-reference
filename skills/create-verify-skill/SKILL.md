---
name: create-verify-skill
description: Generate a project-local verify skill with a feature map so the repository gains a scripted, rerunnable way to prove its app's behavior, proven once end to end before handover.
argument-hint: "[app-or-package]"
---

## Context

Existing project verify skill: !`out=$(ls .claude/skills/ 2>/dev/null | grep -i verify); echo "${out:-(none)}"`

Runnable surfaces: !`out=$(jq -r '.scripts | to_entries[] | select(.key | test("dev|start|serve")) | .key + ": " + .value' package.json 2>/dev/null | head -3); echo "${out:-(no package.json)}"`

## Instructions

Interview the repository, write a project-local verify skill whose commands actually run, and prove it on one feature before handing it over.

### Process

1. Parse `$ARGUMENTS` (the app or package to cover; default the repository's primary runnable app). When a project verify skill already exists, update it in place instead of writing a second one.
2. Interview the repository, citing files: the launch command and its env, the readiness signal (port, log line, health route), the driving surface (a browser app drives like `verify-ui`, a terminal app like `verify-cli`, an API via direct requests), the evidence each feature can produce, and the teardown.
3. Write the skill at `.claude/skills/verify-<app>/SKILL.md` (symlink into `.agents/skills/` when the project also uses harnesses that scan it) with sections Launch, Ready, Drive, Evidence, Cleanup, each carrying the exact commands, plus `references/feature-map.md` listing every shipped user-visible feature with its entry point, the driving steps, and the assertion that proves it works.
4. Prove it once end to end: run the generated launch, drive one mapped feature, capture the evidence, and tear down. A generated skill that has never run is a draft, not a deliverable.
5. Hand over: report where the skill landed, the feature it was proven on, and the maintenance contract written into the generated skill itself: a change to app behavior updates the feature map in the same change.

### Rules

- The generated skill drives the real app; mocked or asserted-from-source evidence disqualifies a feature-map entry.
- The feature map lists shipped user-visible behavior only, never internals.
- One verify skill per app; a second app gets its own skill, not a fork of the first.
