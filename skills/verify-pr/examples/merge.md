# Merge as-is (PR #32)

The bar for a clean pass: necessity argued from the failure that happened, the fix proven on both sides with the same command, every row pinned to evidence, and the binding pair at the end. The report's language follows the user; this structure and density do not change.

---

**PR summary**: #32 `fix(ship-pr): bound watches with sigterm, which gh does not ignore`, head `5f15daa`, MERGEABLE / CLEAN, no linked issue. Scope: the whole patch (3 files, +3 / -3).

| Dimension | Verdict | One-line note |
|-----------|---------|---------------|
| Necessity | OK | A `gh run watch` outlived its 540 s bound by 23 minutes in a real ship-pr run; no open or merged PR touches the wrapper |
| Correctness | OK | The old `alarm; exec` form lets a SIGALRM-ignoring child run on; the new fork-and-SIGTERM wrapper stops it at the bound and exits 124 |
| Test quality | OK | No test harness covers skill text; the PR carries reproducible command checks instead, rerun below |
| Conventions / paradigm | OK | Matches the existing wait convention in `AUTHORING.md` and states the rule there too, so the next bounded call inherits it |
| Side effects | OK | Non-timeout exit codes pass through unchanged (`sh -c 'exit 3'` exits 3) |
| CI | green | `validate` and GitGuardian pass |

**Correctness, both sides.** Claim: a watch bounded at N seconds returns by N seconds even when the child ignores SIGALRM. On the base, `perl -e 'alarm 2; exec @ARGV' sh -c 'trap "" ALRM; sleep 6'` returns after 6 s. On the head, the wrapper from `skills/ship-pr/SKILL.md` step 3, bound shortened to 2 s, returns after 2 s with exit 124. Same child, same inputs, symptom present on the base and gone on the head.

**Final recommendation**: Merge as-is.

**Merge readiness**: nothing pending; no review threads; no required approvals.

**Optional follow-ups**: none.

**Verified head**: `5f15daaa352054d6afceac89117d0f631f91a05d` against base `0ff1f9ef49b2de9e50ebd8b8cdce1e82e7b60977`.
