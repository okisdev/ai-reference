# Workspace

## Identity and scope

The clones root is the directory holding the current repository's main worktree: `dirname "$(git rev-parse --path-format=absolute --git-common-dir | sed 's#/\.git$##')"`. Outside a repository, use a path the user names or skip local sources with that reason.

Clones of a GitHub org; without an org, drop the `case` filter and keep every directory that answers:

```
find <root> -mindepth 1 -maxdepth 1 -type d | while read -r d; do r=$(git -C "$d" remote get-url origin 2>/dev/null) || continue; case "$r" in *[:/]<org>/*) echo "$d $r";; esac; done
```

## Unpushed work

Per clone, filtered to the subject's commit email (for `me`, that clone's `git config user.email`; for a team, drop `--author` and group by `%ae`):

```
GIT_OPTIONAL_LOCKS=0 git -C <clone> log --branches --not --remotes --since=<start> --until=<end> --author=<email> --format='%h %ad %ae %S %s' --date=iso-strict-local
git -C <clone> worktree list --porcelain
GIT_OPTIONAL_LOCKS=0 git -C <worktree> status --short
```

Run `status` in every worktree the list names and report uncommitted changes, which carry no time, as of now and apart from unpushed commits. A squash-merged branch keeps commits no remote holds, so drop a branch (`%S`) when a merged PR's head is its tip: `gh pr list -R <owner>/<name> --head <branch> --state merged --json headRefOid --jq '.[].headRefOid'` prints `git -C <clone> rev-parse <branch>`.

## Agent sessions

Store layouts, including how a path is encoded into `<encoded>`, are in [distill-session's stores.md](../../distill-session/references/stores.md). Index sessions by default; read one only when the ask is about the work itself rather than its outputs, and then through distill-session's reader brief.

Claude sessions of a clone, including its task worktrees' `<encoded>--claude-worktrees-*` directories, with each session's latest title and the PRs it linked (opened or worked on):

```
find ~/.claude/projects -mindepth 2 -maxdepth 2 -name '*.jsonl' \( -path "$HOME/.claude/projects/<encoded>/*" -o -path "$HOME/.claude/projects/<encoded>--claude-worktrees-*/*" \) -newermt '<start in local time, YYYY-MM-DD HH:MM:SS>' | while read -r f; do grep -h -E '"type":"(ai-title|pr-link)"' "$f" | jq -s -c --arg f "$f" '{file: $f, title: (map(select(.type == "ai-title")) | last | .aiTitle), prs: (map(select(.type == "pr-link") | .prUrl) | unique)}'; done > sessions.jsonl
```

The lower bound alone is deliberate: a session active in the window may have been touched since, and joining the `prs` URLs to the window's GitHub records keeps only the window's work, grouping the PRs one session linked into one thread. A session started in a subdirectory of the clone gets an `<encoded>-<subpath>` directory, which a prefix cannot tell apart from a sibling clone whose name extends this one; include it only after its transcript's `cwd` field shows the clone. For the whole machine, drop the two `-path` tests; a session without PR links belongs to the window when the span from its first `timestamp` (`grep -m1 -o '"timestamp":"[^"]*"' <file>`) to its last (the final match in `tail -n 50 <file>`) overlaps it.

Codex runs sit in `~/.codex/sessions/YYYY/MM/DD/`, dated in the machine's local time when each run started. Scan from the day before the window to the day after it, keep runs whose first-line timestamp falls inside, and tie a run to a clone when its `cwd` is the clone path or starts with it plus `/`:

```
head -1 <file> | jq -c '{cwd: .payload.cwd, originator: .payload.originator, at: .payload.timestamp}'
```

`originator: codex_exec` marks a run dispatched by another agent rather than an interactive session; count runs per clone.

Grok sessions are `~/.grok/sessions/<url-encoded-cwd>/<uuid>/chat_history.jsonl`, with the cwd encoded by `python3 -c 'import sys,urllib.parse;print(urllib.parse.quote(sys.argv[1],safe=""))' <clone>`; a session belongs to the clone when its directory is that encoding or starts with it plus `%2F`, and its file's modification time places it in the window.
