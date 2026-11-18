---
description: draft-reply drafts a closing reply that keeps the user's stance, cites the merged PR, and is shown unsent with the command that would post and close.
tags: [quality, draft-reply]
runs: 2
max_turns: 8
timeout_seconds: 240
allowed_tools: [Skill, Read, Bash]
---

Use the draft-reply skill to draft a reply to this issue. Everything you need is below; do not run commands and do not send anything.

Repository: acme/tally. My login: maintainer-a.
Issue #305, opened by `riverstone` (no other issues or pull requests by this author): "Add a `--sort` flag to `tally list`". The body asks for `tally list --sort name` and `--sort date`, and says there is no way to order the output today. One comment from another user: "+1, would use this".
What the code and history show: pull request #298, merged last week and released in v2.4.0, added `--sort <name|date>` to `tally list` (`list.ts:31`). The issue was opened against v2.3.0.
My stance: close it as done, thank them.

Reply with the findings for me in Chinese first, then the draft, then the exact command that would post it and the command that would close the issue, nothing else.
