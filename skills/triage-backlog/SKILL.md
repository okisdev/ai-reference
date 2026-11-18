---
name: triage-backlog
description: Sort a repository's open issues and pull requests into batches (close now, fix now, needs a decision, follow-up), then work through the approved batches one by one, when asked to go through the whole backlog or to take the next batch.
argument-hint: "[issues|prs|all] [--label <name>] [--admin] [--approve] [next]"
---

## Context

Repository: !`gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null || echo "unknown"`
My login: !`gh api user --jq .login 2>/dev/null || echo "unknown"`
Open issues and PRs: !`out=$(gh api 'repos/{owner}/{repo}' --jq .open_issues_count 2>/dev/null); echo "${out:-unknown}"`

## Instructions

**The one rule: every open item lands in exactly one batch with the evidence that put it there, and a batch the user approved runs to its end without being asked about again.** A great run shows one plan the user can approve in a single reply, keeps that plan in a file so "next batch" resumes it after any amount of context loss, carries the flags the user gave once to every item, and reports each item's outcome with its link. Open [examples/plan.md](examples/plan.md) before presenting a plan and check it against [examples/rejected.md](examples/rejected.md).

### Process

1. Parse `$ARGUMENTS`: the scope (`issues`, `prs`, or `all`, the default), a `--label` filter, and the flags to carry to every merge (`--admin`, `--approve`, a merge method); a bare `next`, or an ask for the next batch, resumes from the plan file in step 7 instead of re-planning (seen: the user typed "what is the next batch" and "go, same as before" between every batch of a backlog). Flags or instructions the user gave once in this conversation ("same steps as before") stay in force for every later batch and are written into the plan file.
2. Read how the repository decides: `AGENTS.md`, `CONTRIBUTING.md`, the last 20 merged PRs and the maintainers' review comments on them, so a fix follows the repository's own patterns and a closure follows its stated scope.
3. List everything in scope in two calls: `gh issue list --state open --limit 500 --json number,title,labels,author,createdAt,updatedAt,comments` and `gh pr list --state open --limit 200 --json number,title,author,isDraft,headRefName,baseRefName,labels,mergeable,reviewDecision,isCrossRepository,maintainerCanModify,createdAt,updatedAt,closingIssuesReferences`. A list that returns exactly its limit was cut off: raise the limit until the lists together reach the Context count, or ask the user to narrow the scope by label or age, and never plan on a partial list. Link each issue to the PRs that claim it (closing references and `#N` mentions in PR bodies), so an issue and its PR are judged together.
4. Classify every item, in parallel read-only passes (`verify-issue` for an issue and `verify-pr` for a PR when installed; otherwise reproduce or read the code yourself), into exactly one disposition:
   - **close now**: already fixed (name the commit or PR), a duplicate (name the original), not reproducible on the current default branch, out of the repository's stated scope, or a PR superseded or abandoned; each carries a drafted reply.
   - **fix now**: the fix needs no product or API decision and fits one reviewable PR; for a contributor PR, it lands by fixing the contributor's branch when it is pushable.
   - **needs a decision**: a product, API, or naming choice only the owner can make; it carries one question with the options and a recommendation, and never runs.
   - **follow-up**: real but larger than one PR; it carries the scope a follow-up would need.
5. Batch the plan: batch 0 is every close now item; later batches group fix now items that touch the same files or subsystem into one PR, and keep independent items as separate PRs that can ship in parallel; order batches by value to users over risk. Size a batch so its PRs can all be verified and shipped in one sitting.
6. Write the plan to a file in the scratchpad (scope, carried flags, every item with its disposition, evidence, batch, and status) and present it: one table per batch, the drafted closure replies, and the decision questions together at the end. Stop for one approval of the plan; the user may move items between batches in that reply.
7. Run the approved batch without asking again, independent items in parallel in their own worktrees: a close now item posts its reply and closes (`draft-reply` when installed); a fix now issue is fixed in a task worktree and shipped (`ship-pr` when installed, with the carried flags); a fix now contributor PR is taken over on its branch (`adopt-pr` when installed), approved (`approve-pr` when installed), and shipped. Stop only for a real blocker (a red check the batch cannot fix, a reviewer requesting changes, a decision the plan did not foresee), and keep the rest of the batch moving.
8. After each batch, refresh both lists, because items merge, close, or appear between batches; update the plan file (status per item, newly opened items classified into the plan), report every item of the batch with its outcome and link, and present the next batch; a new item that needs a decision joins the decision list rather than the running batch.

### Rules

- Nothing is posted, closed, or merged before the user approved the batch that holds it; an approved batch needs no further confirmation per item.
- The plan file, not the conversation, is the state: read it at every resume, because the conversation may have been compacted.
- A needs a decision item never runs on a guess; it waits in the decision list until the user answers.
- Replies and PR text follow the repository's language and the user's writing rules.
