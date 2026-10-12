# Grouped by purpose (PR #34)

The bar for a mixed tree: the index emptied first, one commit per purpose in dependency order (the probe rule and its validator first, the readme sync last), a scope only where the change stays inside one skill, and each commit holding exactly the paths planned for it. The seven commits are the real history of PR #34 before the squash; the staged start and the lines around them are reconstructed, so the shape is the bar, not the transcript.

````
Recorded 46 staged paths (create-branch had run git add -A): 36 modified, 4 new, 6 deleted. Then `git restore --staged :/`; the index is empty.
Read `git diff HEAD` and the 4 new files directly. Seven purposes:
1. fix: run context probes without positional parameters and keep their fallbacks (3 files)
2. fix: harden the pr pipeline skills against the failures usage measured (10 files)
3. fix: tighten the review skills where usage overturned their verdicts (6 files)
4. fix: admit fewer memory writes and judge only what a write introduced (7 files)
5. fix(upgrade-deps): recheck sdk holds and report exact pins (2 files)
6. feat: route skills by the user's own words and retire four unused ones (16 files, 6 deleted)
7. docs: sync the readme and bump to 0.0.42 (2 files)
Commit 5: `git add skills/upgrade-deps/SKILL.md skills/upgrade-deps/references/npm.md`. `git diff --cached --name-only --no-renames` lists exactly those 2 paths. `git commit`.
Commits 1 to 4, 6, and 7 the same way: stage the group's paths, compare the staged list with the group, commit.
`git status` is clean. `git log --oneline -7`:
73d2862 docs: sync the readme and bump to 0.0.42
a984776 feat: route skills by the user's own words and retire four unused ones
aca8322 fix(upgrade-deps): recheck sdk holds and report exact pins
c959041 fix: admit fewer memory writes and judge only what a write introduced
2703351 fix: tighten the review skills where usage overturned their verdicts
d07757d fix: harden the pr pipeline skills against the failures usage measured
6bafd6f fix: run context probes without positional parameters and keep their fallbacks
`commit.gpgsign` is true, so `git cat-file commit <sha> | grep -c '^gpgsig'` ran for each of the seven and printed 1.
````

Why it clears the bar:

- The index was emptied before any group was staged; with all 46 paths pre-staged by create-branch, the first commit would have taken every one of them.
- Each subject names a purpose, not a file type; the single-skill change carries a scope and the repo-wide ones do not, which is how the repo's own history reads.
- Order follows dependency: the probe rule and the validator that enforces it come first, the docs sync and version bump come last.
- The staged list is compared with the group's list before every commit, and neither `git add -A` nor `git add .` appears anywhere.
- Signing is proven with the one check from step 3 on every new commit; no hook and no signature was bypassed.
