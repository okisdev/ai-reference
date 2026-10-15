# A read-path doc rewrite that clears the bar (illustrative)

The bar for a doc an instruction file orders agents to read: every rule stays as one bullet under the concern it governs, every description of what the app shows today goes with the file that records it, the orders to update the doc alongside code are gone, and the pointer names the section a change needs. The app, numbers, and files are invented; the shape is the bar.

Before, `apps/desktop/AGENTS.md` (excerpt):

````md
- Read `DESIGN.md` before any UI change.
````

Before, `apps/desktop/DESIGN.md` (excerpt; 41 KB in all):

````md
# Design

This file records what Harbor decided on purpose; where it and the code disagree, this file wins. A new color, size, or control style is a change to this file first.

## Badges

A badge is never a pill: it takes the smallest radius. Live state (a sync running) is the `Pulse` mark; a static state is a `StatusDot`.

## Inbox

The Inbox lists the threads of the selected account, newest first, at most 200 and 25 at a time: each row shows the sender's avatar, the subject in medium weight, the first line of the body in muted text, the time, and an unread dot.

## Drift found on 2026-08-02

- D7, rhythm (2026-08-02): Settings put 16 points between sections and Inbox 24, so the two pages read as different apps. Sections stand 24 points apart everywhere.

## Building

Build only from the components this file names; if one is missing, add it to `src/design` and to this file in the same change.
````

After, `apps/desktop/AGENTS.md`:

````md
- Read `DESIGN.md`'s Tokens before adding a color, size, or radius, and its Components before adding a control.
````

After, `apps/desktop/DESIGN.md` (excerpt; 9 KB in all):

````md
# Design

The rules every Harbor desktop surface follows; read Tokens before adding a color, size, or radius and Components before adding a control. Where the code breaks a rule here, the code is fixed.

## Tokens

- Sections stand 24 points apart on every page (`--section-gap`), because two spacings make two pages read as two apps.

## Components

- A badge takes the smallest radius and is never a pill.
- Live state is the `Pulse` mark and static state is a `StatusDot`.
- Build only from components in `src/design`; a missing one is added there.
````

Report, as the user reads it:

````
apps/desktop/DESIGN.md is a read-path doc (required: apps/desktop/AGENTS.md:4 orders it read before any UI change). 41 KB to 9 KB against the 16 KB target.
Kept: the badge radius and the Pulse and StatusDot rules, one bullet each under Components; the section rhythm as a token rule, without its story.
Dropped: the Inbox paragraph (as-built description; src/inbox/ThreadList.tsx records it, and no rule in it governs another surface); the drift log D1 to D9 (dates and incidents; git and the PRs carry them); "a change to this file first" and "to this file in the same change" (accretion orders; the editing contract's amendment triggers replace them).
Changed: the precedence line covers rules only; the AGENTS.md pointer names Tokens and Components instead of the whole file.
Loss check in a fresh subagent: no obligation of the old doc is missing. measure.py --strict: clean, no accretion order left.
````

Why it clears the bar:

- Every rule survives as one bullet under the concern it governs, and the one decision buried in the drift log, the section rhythm, stays as a rule without its date, its number, or its story.
- The Inbox paragraph goes with the file that records it, because a doc that restates what a surface shows today must change with every change to that surface.
- Both orders that made each code change a doc change are gone, and the precedence line says the code is fixed where it breaks a rule, so no description is written down to win.
- The pointer sends a UI change to the two sections it needs instead of the whole doc, and the report names the line that made the doc required reading.
