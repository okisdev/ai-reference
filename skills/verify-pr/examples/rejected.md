# Rejected report

A report that reads fine and gets overturned. Compare yours against it before posting.

````
Looks good overall! The change is small and CI is green, so it should be safe.

Necessity: seems useful.
Correctness: the logic looks right to me.
Tests: there are tests.

Waiting for the remaining checks to finish... done, all green.

Recommendation: merge after small fixes, though closing it would also be fine.
````

Why each part fails:

- `CI is green, so it should be safe`: green proves the tree builds; it says nothing about necessity or whether the bug is gone.
- `Necessity: seems useful`: necessity is argued from evidence (the failure, the duplicates searched, what already covers it), or the dimension was not checked (seen: claim-only reviews passed redundant PRs before necessity became the gate).
- `the logic looks right to me`: correctness is a falsifiable claim measured on both sides with the same command, and it says whether the cause is removed or a symptom is patched (seen: four verdicts the user overturned by asking whether the fix really reached the root).
- `there are tests`: test quality is judged against the repo's own test patterns, not presence.
- `Waiting for the remaining checks`: this skill never waits on CI; a pending check is reported as pending (seen: reviews blocked in a CI watch after the user had already merged).
- `merge after small fixes, though closing it would also be fine`: exactly one recommendation, and Merge after small fixes lists each blocking item with `file:line` (seen: a hedged recommendation left the decision to the user).
- No `file:line` anywhere, no Merge readiness, no Verified head: without the binding pair, the next push silently inherits a verdict it never earned.
