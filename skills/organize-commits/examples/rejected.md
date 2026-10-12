# A run that gets stopped by the user (illustrative)

Each fault below breaks a rule of this skill, and the ones tagged seen were measured in real runs. Compare your run against it.

````
8 init checkpoints ahead of master; regrouping them.
git reset --soft $(git merge-base HEAD master)
git commit -m "feat: recap activity and other fixes"
git add skills/diagnose-root/SKILL.md
git commit -m "feat(diagnose-root): count a remote failure's recorded log as its observation"
git push --force origin feat/recap-activity
Reorganized into 2 commits. Done.
````

Why each line fails:

- The reset comes before any plan or question: the plan is printed first with its files, and the reset waits for a yes; 3 of the 8 commits were already pushed, and the call-out "rewriting 3 pushed commit(s); publishing requires force-push" never came.
- No `git branch _backup/<branch>` and no `ORIGINAL_TREE`: the recovery ref and the content identity are recorded before any `git reset`.
- `git commit` straight after `git reset --soft`: the whole range was still staged, so the first commit holds all 10 paths and the later groups have nothing left to take (seen: a soft reset left the whole range staged, so the first group's commit swallowed everything).
- `git add skills/diagnose-root/SKILL.md` from the session's directory while the branch lives in a worktree named only in prose: pass `--cwd <path>` and run every git command there (seen: a repository or worktree path was passed without `--cwd`).
- `git push --force`: never without the user's explicit permission; state the situation and let the user run it.
- `Done.` with no `git status`, no log, and no tree comparison: the run is verified only when the content is shown unchanged against `ORIGINAL_TREE`.
