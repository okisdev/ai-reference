# Rejected review body

A body that fills a template and gets rewritten by the user. Compare yours against it before showing it.

````
## review

LGTM as `patch`.

### shortcomings of the original implementation
- coderabbit flagged that `parseRange` crashes on empty input
- the bot also noted the missing negative number test
- `src/range.ts` has a confusing name

### what we modified
- renames `parseRange` to `parseNumericRange`
- adds a guard for empty input
- adds tests for negative numbers

### potential further fixes
- none
````

Why each part fails:

- `## review`: GitHub labels the review state, so the heading spends the opening saying nothing.
- `LGTM as patch.` with no reason: the verdict comes with the one reason it holds.
- Three fixed groups: steps 4 to 6 are an order to think in, never sections to emit (seen: 75 of 79 bodies came out in one rigid three-part template).
- `coderabbit flagged`, `the bot also noted`: frame each shortcoming as critique of the code and never name the bots.
- `what we modified`: narrates the diff to the person who wrote it; cut anything the patch already shows.
- `crashes on empty input` with no command: a runtime claim that was only read is a suspicion; name what you ran and what it printed.
- `none` under further fixes: an empty section filled to fit the template; do not pad.
- No `file:line` in the baseline for the one concrete shortcoming.
