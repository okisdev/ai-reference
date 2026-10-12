# Already fixed in a later commit (issue #27)

The bar for an issue that was real when filed and is gone now: every claim gets its own row and the strongest check it needed, "already fixed" is proven by one fixture run on both sides of the fixing commit instead of by the commit message, and the one claim no check could reach says what blocked it instead of rounding to a verdict. Real: okisdev/ai-reference#27, judged at `5c88010`.

---

**Issue summary**: #27 (closed as completed) reports five defects in `skills/clean-memory/scripts/audit.py` that leave the flagged set noisy and incomplete together, plus one measurement: 7 of 16 unflagged control topics held a claim the tree or upstream contradicts.

**Method**: `audit.py` from the fix's parent `f776205` and from `54903c8` (byte-identical to `5c88010`), both run with `--json --gh` over one fixture: the anchor cases from `scripts/test-memory-scripts.py`, a bare `[[bob]]`, a topic holding only an `originSessionId`, 100 refs in one topic, and a stub `gh` on PATH that logs its calls.

| # | Claim | Result | Evidence |
|---|-------|--------|----------|
| 1 | `LINE_SUFFIX` strips only `:\d+`, so `path:14-63`, `path:246,251` and `path:symbol` count as dead | Already fixed in `54903c8` | `audit.py:15` on `f776205` is `:\d+$`. The fixture reports 7 dead anchors there, 3 of them the live `src/live.ts` cited those three ways; on `54903c8` all three resolve (`audit.py:18`). |
| 2 | Cross repo detection knows only local sibling checkouts | Already fixed in `54903c8` | `anchor_scope` consults `sibling_repositories` alone (`audit.py:129` and `:122`). `registry/foo.ts`, `lib/parse.ts` and `lib/tokens.ts`, each on a line naming `shadcn-ui/ui` or `vercel/streamdown`, are dead on `f776205` and `cross-repo` on `54903c8` (`:162`). The one anchor still dead, `src/missing.ts`, really is missing. |
| 3 | `SHA` matches the 8 and 12 hex fragments of `originSessionId`, so an uncited topic reads as cited | Already fixed in `54903c8` | A topic holding only the uuid: `shas` `['1a2b3c4d', '0e1f2a3b4c5d']` and `uncited: False` on `f776205`; `shas` `[]` and `uncited: True` on `54903c8` (`UUID` at `:20`, `topic_body` at `:248`). |
| 4 | `--gh` stops at 60 lookups, smallest number first, so recent refs are never checked | Already fixed in `54903c8` | 100 refs, #10 to #109: `f776205` makes 60 `gh issue view` calls (#10 to #69) and leaves 40 unchecked (`:189` sorts smallest first, `:190` and `:196` stop at 60); `54903c8` makes 2 calls (`gh issue list --state open`, `gh pr list --state open`) and resolves 100 of 100 (`:228`). |
| 5 | `WIKILINK` flags `[[...slug]]` and `[[alice]]` as broken links | Partial | `f776205` reports 4 broken links: `...slug` twice, `alice` in a code span, a bare `bob`. `54903c8` skips code spans and targets starting `...` (`:363` and `:367`), so only the bare `[[bob]]` remains; the contract test pins the code span form only. |
| 6 | 7 of 16 unflagged control topics hold a contradicted claim that no audit signal covers | Inconclusive | The count comes from a manual pass over the assistant-ui store (276 topics), which is not in this checkout, so nothing could run against it. Not rounded to Confirmed or Refuted. |

**Prior art**:
- PR #28, merged as `54903c8` (closes #27 and #29): the fix. Neither it nor #27 records a wontfix or by-design ruling.
- Issue #29, closed: asked for the contract test. `scripts/test-memory-scripts.py` pins claims 1 to 3 and the code span form of claim 5, and passes on `5c88010`. It never passes `--gh`, so claim 4 is pinned by nothing.

**Conclusion**: valid when filed, fixed now except one residue. The load-bearing claim is that these defects live in `audit.py` as described (claims 1 to 5); it was settled by running both versions over one fixture, not by reading the commit message. The issue's own figures (5 of 25 dead anchors, 7 of 16 controls) come from a store this checkout lacks and were not reproduced; the mechanisms they rest on were.

**Extra findings**: `audit.py:230` and `:231` cap each open listing at 1000, and `:246` reports every ref outside both lists as CLOSED, so a repo with more than 1000 open issues or PRs would mislabel some open refs. Read only, with no repo that large to run against, so a suspicion rather than a finding.

**Possible fix directions**: none for claims 1 to 4, since #28 removes each cause at its source (the regex, the scope function, the call pattern) instead of filtering the report; a merged PR needs no `/verify-pr`. Claim 5: decide whether a bare `[[name]]` that names no topic is a broken link (the code says yes) or a mention to skip, and if skip, extend the code span skip at `audit.py:367`. A contract test for claim 4 with a stub `gh` on PATH, as run here, would pin the two call pattern.
