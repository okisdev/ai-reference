# Checkout paths

Invoked from ship-pr steps 1 and 5, only when Current branch is `gitbutler/workspace` or the change lives in another worktree; a plain single checkout never reads this file.

- **GitButler PR lookup.** On this path the current-branch Existing PR probe cannot see the virtual branch's PR, so look it up by virtual branch name (`gh pr list --head <virtual-branch> --json number,url`).
- **GitButler cleanup.** Stay on `gitbutler/workspace` and `but pull` instead of checking out the default branch.
- **Worktree removal.** When the shipped branch lived in its own worktree, that worktree has served its purpose: remove it by default (`git worktree remove <path>`, run from another worktree of the same repo), and keep it only when the user said further work is coming in that same worktree, naming it when you do.
- **No default checkout in a worktree.** Never `git checkout <default>` inside a worktree, because the default branch is normally checked out in the primary one and git refuses with `'<default>' is already used by worktree at ...`; that same collision makes `gh pr merge --delete-branch` print a failure after the merge itself succeeded, so confirm the outcome from `gh pr view <n> --json state,mergedAt` rather than the command's exit code.
