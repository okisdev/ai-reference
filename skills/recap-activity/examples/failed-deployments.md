# List (failed deployments, a month)

The bar for a list: failures are clustered by project, error code, and the first error line of the build log, never by an exit code message that hides the cause; each cluster carries its count, first and last seen, whether the latest deployment of the same project, target, and branch still fails, a sample link, and its cause in one line; and records that match the filter's wording but not its intent (blocked, canceled) get their own table grouped by the reason they carry. Condensed from a real run: project names other than the public ones are replaced and their links dropped. The report's language follows the user; this structure and density do not change.

---

````
## acme team deployments, list, 2026-10-01 00:00 to 2026-10-12 11:26 (+08:00)

This month the acme team had 34 failed deployments (state ERROR), all between 10-01 03:34 and 10-10 12:13, in 8 clusters by project, errorCode, and the first error line of the build log. 28 are `web` production builds on main, 5 belong to a docs project, 1 to `storefront`. The latest deployment of all three projects is READY, so no cluster is still failing. Another 56 BLOCKED and 69 CANCELED records matched the filter but are not failures; they are in the second table.

| # | Cluster | Count | First to last (+08:00) | Still failing | Sample | Cause |
|--:|---|--:|---|---|---|---|
| 1 | web, BUILD_UTILS_SPAWN_1, a runtime provider nested inside another | 9 | 10-10 11:24 to 12:13 | no, production READY 10-12 10:22 | `dpl_example1` | `Command "turbo run build" exited with 1`; prerendering `/docs/tools/runtime` threw `RuntimeProvider cannot be nested inside another RuntimeProvider` |
| 2 | web, BUILD_UTILS_SPAWN_1, `new Date()` | 7 | 10-09 16:43 to 17:29 | no, same | `dpl_example2` | same exit message; a Client Component on `/elements/[slug]` used `new Date()`, which Next.js rejects while prerendering |
| 3 | a docs project, BUILD_EXCEEDED_MAXIMUM_TIME | 5 | 10-01 03:34 to 10-08 13:52 | no, production READY 10-03 18:09, preview READY 10-10 06:05 | `dpl_example10` | `The build exceeded Vercel’s 45-minute limit.`; 1 production and 4 preview builds on 5 branches, and the latest log goes quiet right after `pnpm install` |
| 4 | web, BUILD_UTILS_SPAWN_1, TS2304 | 5 | 10-07 13:57 to 14:06 | no, same | `dpl_example3` | same exit message; `packages/react-generative-ui/src/a2ui/convert.ts(1249,30)` cannot find `decodePointer`, so type checking failed |
| 5 | web, BLOCKED_PACKAGE | 5 | 10-02 00:34 to 01:50 | no, same | `dpl_example4` | `Vulnerable TanStack Start package detected (@tanstack/react-start@1.168.59). Please update to a patched version.`; a build stopped for a vulnerable dependency, which is state ERROR and not state BLOCKED; versions 1.168.54 and 1.168.59 share the cluster because versions are normalized |
| 6 | web, out_of_memory | 1 | 10-08 19:08 | no, same | `dpl_example5` | `Command "turbo run build" exited with 137`; out of memory, which the errorCode settles without a log |
| 7 | storefront, ENOENT | 1 | 10-06 18:57 | no, preview READY 10-10 12:48 | `dpl_example6` | `Command "pnpm run build" exited with 1`; after the Nitro build finished, `finalize-static-website.mjs:68` hit ENOENT on a docs content file (preview, dependabot branch) |
| 8 | web, BUILD_UTILS_SPAWN_1, `/learn` | 1 | 10-03 21:15 | no, same | `dpl_example7` | same exit message; `/learn` read uncached or runtime data outside `<Suspense>` while prerendering |

Not failures, grouped by the reason the record carries:

| State | Count | Projects | First to last (+08:00) | Reason on the record | Sample |
|---|--:|---|---|---|---|
| BLOCKED | 56 | 4 | 10-02 03:13 to 10-08 06:28 | the commit author has no access to the team (3 outside authors); never built, no log | 7jWcNc |
| CANCELED | 58 | 8 | 10-01 21:27 to 10-10 13:16 | `the commit didn’t affect this project`, a monorepo skip | `dpl_example8` |
| CANCELED | 8 | web | 10-01 17:48 to 10-12 07:58 | `Ignored Build Step command returned exit code 0` | `dpl_example9` |
| CANCELED | 3 | a docs project | 10-02 05:04 to 10-09 08:31 | no reason recorded; each has a later deployment of the same project and branch, so superseded | `dpl_example11` |

**Coverage**
- Vercel team acme, window 2026-10-01T00:00:00+08:00 to 2026-10-12T11:26:58+08:00 (1790784000000 to 1791775618000 ms).
- `state=ERROR` returned 90 rows (34 ERROR and 56 BLOCKED) in one page with `pagination.next` null, under the 100 row cap; `state=CANCELED` returned 69; an all states query returned 2688 rows (2529 READY) whose ERROR, BLOCKED, and CANCELED ids match the two filtered queries exactly.
- Build logs: 23 fetched (22 `turbo run build` exits and the `storefront` one) and split by each log's first error line; BUILD_EXCEEDED_MAXIMUM_TIME, BLOCKED_PACKAGE, and out_of_memory were settled by errorCode, plus the tail of the latest timeout log.
- Aggregates: none named for deployments, so nothing to compare.
- Skipped: GitHub (its records are PRs, issues, and runs, not deployments) and the local clones; Vercel runtime logs, activity, and alerts were not collected because the ask was about deployments.
- Not reached: the code fix behind each failure; the other 4 timeout logs; whether the preview branches in cluster 3 recovered, since only each project's latest deployment was checked.
- Mapping: the team has 40 projects, 30 linked to the GitHub org through `link.org`.
````
