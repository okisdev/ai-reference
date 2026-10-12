# Feature PR (adapted from #33)

The bar for a feature: the first bullet says what the user can now do, the next bullets name the mechanisms in the order a reader meets them, verified items quote measured numbers, and notes state what was deliberately not done.

Title: `feat: add recap-activity, the activity and failure recap skill`

## summary

- add `recap-activity`: recaps what a person, team, project, or this computer did, or what failed, over a time window, from whatever records exist. it finds every store that can speak to the ask (playbooks first, then installed CLIs and connectors, then an app's own data on disk), and when no store holds records it says there is nothing to recap and lists where it looked; a refused owning store makes the answer provisional instead of empty
- four playbooks carry verified commands and traps: GitHub (offset ranges because a bare date is a UTC day, reviews in every state timed by submission, comments inside the window), Vercel (`vercel api` reads with `-X GET`, BLOCKED and CANCELED apart from failures, build logs split by their first error, runtime logs bisected under the CLI's 50 row cap), workspace (unpushed work without squash-merged leftovers, session transcripts joined to the PRs they linked), and machine (app usage, browser and shell history, opened files, downloads, each converted from its own epoch)
- `diagnose-root`: a remote failure that already happened counts as observed through its recorded log; the repeat is a second failed run or a cheap rerun at the failing sha in a disposable worktree, and a remote rerun waits for the user
- `distill-session`: sessions started in `.claude/worktrees/<topic>` live in their own project directory, so the probe and the store table now include them and resolve the main worktree first

## test plan

### already verified

- [x] `node scripts/validate-skills.mjs` -> all skills validated
- [x] the skill ran end to end on five real asks across three revisions: a weekly org digest (172 PRs, 175 reviewed, 108 issues, matching independent queries), a month of failed Vercel deployments (34 failures, with 56 blocked and 69 canceled set apart), a why on a day without failures (named the nearest failure with its distance and stopped at a labeled hypothesis), a week of computer usage, and a service with no reachable store (provisional nothing with the remedy)

### reviewer should verify

- [ ] `/recap-activity me in <org> last week` prints an absolute window with its offset, and its PR count matches `gh search prs --author=@me --owner=<org> --created=<range>`
- [ ] `/recap-activity why <project> failed yesterday` on a quiet day names the nearest failure and its distance instead of widening the window silently

## notes

- `npx skills add <repo> -l` was not run, to avoid installing the CLI; the validator parses the same frontmatter
- the machine playbook targets macOS; on Linux only shell history and browser profiles carry over
