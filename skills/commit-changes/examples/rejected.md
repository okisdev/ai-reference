# A run that gets stopped by the user (illustrative)

Each fault below breaks a rule of this skill, and the ones tagged seen were measured in real runs. Compare your run against it.

````
46 paths are staged already, so committing what is staged.
git commit -m "chore: update skills"
git add -A
git commit --no-verify -m "fix: misc"
Checking the signature with git log --show-signature -1.
The 1Password prompt failed on the last commit, so: git -c commit.gpgsign=false commit -m "docs: readme"
Done.
````

Why each line fails:

- `committing what is staged`: the first commit swallows every pre-staged path; record the staged paths, run `git restore --staged :/`, then stage per group (seen: a tree that create-branch staged collapsed into the first commit, and 23 percent of runs had to unstage first).
- `chore: update skills` and `fix: misc`: a subject that names a file type or nothing; one commit per purpose, with the purpose in the subject, in the repo's own conventional style.
- `git add -A`: stage by explicit paths and compare `git diff --cached --name-only --no-renames` with the group's list; a blanket add also takes files that belong to no group.
- `--no-verify`: a failing hook is fixed and the commit retried (seen: `--no-verify` appeared in 10 runs despite the rule).
- `git log --show-signature`: an improvised proof; the only check is `git cat-file commit <sha> | grep -c '^gpgsig'` printing 1, which reads the commit object and needs no key lookup (seen: 376 of 540 runs improvised their own signing proof).
- `commit.gpgsign=false`: a signing failure stops the run and is reported (seen: one run turned signing off when the 1Password prompt failed).
- `Done.` with no `git status` and no `git log --oneline`: the run is not verified until both are shown.
