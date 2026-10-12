# Fix PR (merged as #32)

The bar for a fix: the summary leads with the defect and its mechanism, each later bullet says what changed and why, every verified item names the exact command with the result it showed, and the reviewer step is one concrete reproduction.

Title: `fix(ship-pr): bound watches with sigterm, which gh does not ignore`

## summary

- ship-pr's watch bound never fired: `perl -e 'alarm 540; exec @ARGV' gh ...` delivers SIGALRM, and gh's Go runtime catches SIGALRM and keeps running. a `gh run watch` on a run that sat queued for 23 minutes outlived its 540 second alarm, the shell tool timed out and moved it to the background, and only an API EOF ended it.
- step 3 now forks gh and sends SIGTERM at the bound, exiting 124 on expiry so a bound hit reads as a heartbeat tick rather than a result; other exit codes pass through.
- AUTHORING's waits convention gains the same rule, so the next skill that bounds a gh call does not reach for `alarm; exec`; plugin version bumps to 0.0.40.

## test plan

### already verified

- [x] gh itself, blocked reading its query from a stdin pipe held open 10 seconds: under the old `alarm 2; exec` it exits after 11 seconds, under the new wrapper it exits 124 after 2 seconds
- [x] the wrapper extracted verbatim from the new step 3, bound shortened to 2 seconds, around a child that ignores SIGALRM and sleeps 6 seconds: exits 124 after 2 seconds, while the old `alarm 2; exec` form lets the child run the full 6 seconds
- [x] the same wrapper around `sh -c 'exit 3'` exits 3
- [x] `node scripts/validate-skills.mjs` prints `All skills validated.` and `python3 scripts/test-memory-scripts.py` passes
- [x] `npx skills@latest add <this checkout> -l` finds 28 skills, ship-pr among them

### reviewer should verify

- [ ] a ship-pr run on a PR whose checks outlast the bound returns at 540 seconds with exit 124 and re-enters the watch after its status line
