# Rejected approval

An approval run that compiles into a posted review and still gets stopped by the user. Compare yours against it before posting.

````
Posted a second approval with: gh pr review 4621 --approve -b "lgtm, `retry.ts` looks good"
Watching CI to make sure it stays green... lint pending... lint pending... all green.
The author pushed 5a7b8c9 while I waited, but it was a small change. Approved 9d1c3f7.

## Review

### Summary
This PR adds a RetryBudget class to retry.ts and calls it from runJob.

### Verdict
LGTM, great work!

This follows the pattern from #4702.
````

Why each part fails:

- `a second approval`: when your latest review is already APPROVED, refresh its body in place; a stacked duplicate leaves the old one on the PR.
- `-b "... `retry.ts` ..."`: the shell runs the backticks as a command; pass the body with `--body-file -` and a quoted heredoc.
- `Watching CI`: this skill never watches checks, since approval and merge are independent gates and `ship-pr` owns the wait (seen: it kept watching checks after posting until the user said CI was fine).
- `The author pushed 5a7b8c9 ... Approved 9d1c3f7`: re-read `headRefOid` before posting; a moved head sends you back to the gate, because an approval binds to the SHA verify-pr judged.
- `## Review` and `### Summary`: headings and a restatement of the diff to the person who wrote it; the note is prose that gives the verdict and the one reason it holds.
- `LGTM, great work!`: no reason, and nothing about what was run against what was only read.
- `follows the pattern from #4702`: #4702 merged after the maintainer's ruling in the #4388 thread; cite the comment that ruled, not the PR that followed it (seen: a later PR was cited as authority when an earlier maintainer comment ruled).
