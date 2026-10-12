# A regroup that clears the bar (PR #33)

The bar for a history rewrite: the plan printed with its files before anything moves, the reset gated on a yes, a recovery ref and the content identity recorded first, each group staged against its planned list, and the tree compared at the end so only history changed. The four target commits are the real history of PR #33 before the squash; the eight `init` checkpoints they replace and the lines around them are illustrative, so the shape is the bar, not the transcript.

````
Scenario 3: existing commits, some already pushed. Branch feat/recap-activity has 8 `init` checkpoints ahead of master; Pushed commits in range 3; behind / ahead of upstream 0 5; nothing uncommitted.
Read `git diff $(git merge-base HEAD master)..HEAD`: 10 files in 4 purposes.
Plan:
fix(distill-session): include transcripts of sessions started in task worktrees (2 files)
  skills/distill-session/SKILL.md, skills/distill-session/references/stores.md
feat(diagnose-root): count a remote failure's recorded log as its observation (1 file)
  skills/diagnose-root/SKILL.md
feat(recap-activity): recap what a person, project, or this computer did over a window (5 files)
  skills/recap-activity/SKILL.md, skills/recap-activity/references/github.md, skills/recap-activity/references/machine.md, skills/recap-activity/references/vercel.md, skills/recap-activity/references/workspace.md
docs: sync the readme and bump to 0.0.41 (2 files)
  .claude-plugin/plugin.json, README.md
Rewriting 3 pushed commit(s); publishing requires force-push. Reset to the merge base and recommit as planned?
(the user answers yes)
Recovery ref: `git branch _backup/feat/recap-activity`. `ORIGINAL_TREE=$(git rev-parse HEAD^{tree})` is 173dadf.
`git reset --soft $(git merge-base HEAD master)` staged the whole range: 10 paths recorded, then `git restore --staged :/`.
Group 1: `git add skills/distill-session/SKILL.md skills/distill-session/references/stores.md`; the staged list equals the group's 2 paths; committed. Groups 2 to 4 the same way.
`git status` is clean. `git rev-parse HEAD^{tree}` is 173dadf, equal to ORIGINAL_TREE, so only history changed. `git log --oneline -4`:
6c41a94 docs: sync the readme and bump to 0.0.41
b3ba3f4 feat(recap-activity): recap what a person, project, or this computer did over a window
49d9cc7 feat(diagnose-root): count a remote failure's recorded log as its observation
ac0b77f fix(distill-session): include transcripts of sessions started in task worktrees
`node scripts/validate-skills.mjs` printed All skills validated.
Not pushed: the branch now differs from origin/feat/recap-activity, so publishing needs a force-push, which the user runs.
````

Why it clears the bar:

- The plan comes first in the skill's one-line-per-commit form with every commit's files listed, so the user confirms the grouping and not just the idea of one.
- The pushed commits are called out with the force-push consequence before the reset, and the reset waits for a yes.
- The recovery ref and the content identity are recorded before the reset, so a bad regroup is one command from undone.
- The soft reset staged the whole range; the run recorded it and emptied the index first, so group 1 held only its 2 paths.
- Each group's staged list is compared with the plan before its commit.
- The tree comparison proves the rewrite changed history and not content, and the force-push stays with the user.
