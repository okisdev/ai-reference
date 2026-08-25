---
name: verify-cli
description: Drive and verify a CLI or TUI change in a scripted terminal harness with captured transcripts as evidence, when asked to verify terminal behavior, check an interactive flow, or reproduce a terminal bug.
argument-hint: "[command] [--session <name>]"
---

## Context

tmux: !`command -v tmux >/dev/null 2>&1 && tmux -V || echo "(none)"`

Repo-native harness hints: !`out=$(jq -r '.scripts | keys[]' package.json 2>/dev/null | grep -iE 'e2e|smoke|demo|tui|cli' | head -5); echo "${out:-(none)}"`

## Instructions

Verify the claimed terminal behavior by driving the real CLI in a scripted, isolated session, with captured screens and transcripts as the evidence, never by reading the code alone.

### Process

1. Parse `$ARGUMENTS` (the command under test; `--session <name>` names the harness session; with no arguments, take the failing command or flow from the conversation). Pin the smallest deterministic workspace and inputs that exercise the claim.
2. Reuse the repository's own harness first: checked-in expect scripts, PTY helpers, e2e suites, or demo recorders know the app's startup, env, and prompts. Hand-roll a session only when none exists.
3. Launch isolated: start the command in a detached tmux session with a fixed size and deterministic env, record the session name, and capture the initial screen before any input. Follow [references/harness-loop.md](references/harness-loop.md) for the exact commands and the PTY fallback when tmux is unavailable.
4. Drive one action at a time: send a single keystroke or line, poll for a concrete screen pattern instead of sleeping a fixed interval, and capture the pane into the scratch transcript after each step. Every poll is bounded (default 30 seconds per step); on expiry, capture the screen as failure evidence, kill the owned session, and report instead of retrying past the budget.
5. Assert the specific claim against captures: the text, layout, prompt, or exit behavior under test, on the screen where a user would see it. A reported bug counts as reproduced when the discriminating screen appears twice from a reset session, not once. When verifying a fix, capture the baseline from the pre-change state first, then run the identical scripted sequence on the changed state and diff the transcripts.
6. Iterate: apply the edit, re-run the same sequence at the same size, re-capture, and report with the before and after evidence.
7. Tear down: kill only the session this skill created, by its recorded name, and delete any transcript that had to live inside the repo.

### Rules

- Never `pkill`, `killall`, or kill by process name; only the recorded session or PID this skill started.
- Never send credentials or destructive commands into the harness session; a flow that needs either stops and reports instead.
- A clean exit code proves liveness, not behavior; every behavioral claim carries a captured transcript or screen diff.
- Resize, interrupt (Ctrl-C), and empty-input paths count as surfaces when the change touches layout or input handling; verify the ones the change could regress.
