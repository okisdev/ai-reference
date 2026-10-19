# Digest (a week in an org)

The bar for a digest: the heading prints the absolute window with its offset, the answer comes first and says what was produced before it counts anything, the counts table holds numbers only and each one was computed from deduplicated records, themes are clustered by what the records share with their latest links, what is still open follows, and the coverage list says what was probed, which caps were met, where an aggregate disagrees, and what could not be reached. Condensed from a real run: three of nine theme lines are shown, and private repositories and projects are left out. The report's language follows the user; this structure and density do not change.

---

````
## me in acme, digest, 2026-10-05 00:00 to 2026-10-11 23:59 (+08:00)

Last week in the acme org you moved generative UI into its own package and gave it spec mode rendering and state for Vue and React Native; fixed the runtime's thread list, adapter switching, and seeded thread races and its stream chunk order; shared one logic layer across the UI flavors with React 18 and IME fixes; and made markdown rendering faster. Underneath that you opened 171 PRs and merged 165 (Tue 49, Fri 60, Sun 36), reviewed 175 PRs (797 reviews), opened 108 issues, and commented on 54 issues and PRs. The 165 default branch commits are those same 165 merges, since every subject ends in `(#N)`, so nothing bypassed a PR. 97 of the PRs trace to a Claude session.

| Metric | Count |
|---|---|
| PRs opened / merged / union | 171 / 165 / 172 |
| PRs closed unmerged / still open / merged after the window | 5 / 1 / 1 |
| PRs reviewed / reviews | 175 / 797 |
| Approved / commented / changes requested | 257 / 531 / 9 |
| Issues opened / still open | 108 / 33 |
| Items commented on / comments | 54 / 63 |
| Default branch commits / bypassing a PR | 165 / 0 |
| Unpushed commits | 0 |
| Claude / Codex / Grok sessions | 39 / 515 / 34 |
| Vercel team events, excluding deployments and aliases | 58 |

**PR themes** (172 PRs by conventional scope, type split in parentheses, links are the theme's latest merges)
- runtime 32 (fix 19, refactor 10, perf 2, test 1): thread list, adapter switching and seeded thread races, store scrolling, stream chunk order. [#9337](https://github.com/acme/web/pull/9337) [#9324](https://github.com/acme/web/pull/9324) [#9312](https://github.com/acme/web/pull/9312)
- generative-ui 30 (feat 11, fix 11, refactor 4, docs 2, chore 1, test 1): the move to a standalone package, spec mode rendering and state for Vue and React Native. [#9344](https://github.com/acme/web/pull/9344) [#9332](https://github.com/acme/web/pull/9332) [#9329](https://github.com/acme/web/pull/9329)
- ui and react packages 29 (fix 12, refactor 8, perf 4, feat 2, docs 1, chore 1, test 1): shared logic across flavors, React 18 and IME fixes, markdown performance. [#9351](https://github.com/acme/web/pull/9351) [#9331](https://github.com/acme/web/pull/9331) [#9323](https://github.com/acme/web/pull/9323)
- six smaller themes: framework integrations 25, docs and examples 18, repo tooling 16, unscoped 9, vue kit 8, other repos 5

**Claude session threads** (97 PRs link a session, 75 do not): "generative UI spec mode" 26, "open issues" 21, "codebase refactor analysis" 19, "acme issue 6475" 13, 11 other sessions 18.

**Vercel** (team acme, your 58 non-deployment events): one project's environment variables updated 39 times (10-08 19:10 to 19:19), another project had 10 added (10-05 01:08 to 01:13), `vc env ls` run 8 times, 1 AI Gateway key created (10-10 13:15). No variable name or value is quoted.

**Still open**
- PR [#9338](https://github.com/acme/web/pull/9338), opened 10-11 21:27: mergeStateStatus BLOCKED, no review decision; checks success 35, skipped 10, cancelled 8, neutral 2, action_required 1 (`review-tier`, which waits for an approval).
- 33 issues: runtime 9, generative-ui 10, ui and react packages 4, framework integrations 4, repo tooling 2, other repos 2, docs 1, unscoped 1.
- Unpushed: 0. Five local branches hold 28 commits, all in merged PRs; 3 files carry uncommitted changes across 3 clones as of now.

**Coverage**
- Window: GitHub, Vercel activity, and git log all use 2026-10-05T00:00:00+08:00 to 2026-10-11T23:59:59+08:00 (10-04T16:00:00Z to 10-11T15:59:59Z). Claude sessions by file mtime from the window start (2 were touched after it), Codex by first line timestamp, Grok by mtime.
- Caps: the searches returned 171, 165, and 108 records against the 1000 maximum; review and comment searches took 2 and 4 pages and never reached the inner 100; Vercel activity paged 42 times to a null cursor; one empty repository answered HTTP 409 and was skipped.
- Aggregates: reviewed PRs 175 against 172, exactly the 3 PRs with comment-only reviews, which the aggregate leaves out; commits 165 against 153, PRs opened 171 against 167, and issues 108 against 107 stay unexplained and were not chased.
- Skipped: Actions runs, releases (no author field; at least 85 in the window, 2 sampled were bot releases), Vercel deployments, logs, and alerts (a person digest takes only non-deployment events), the org member list.
- Not reachable: whether the 75 PRs without a session link came from Codex, Grok, or by hand, since only Claude sessions carry PR links; private repository work inside the aggregates; the uncommitted state of 24 task worktrees.
- Mapping: GitHub org acme to Vercel team acme (30 of 40 projects link to it) to 13 local clones.
````
