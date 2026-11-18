# Rejected reply

A draft the user overturns. The stance was "close it, we are not adding this", and the thread was a chat reply to a teammate plus a closing comment on a pull request. Compare yours against it before showing it.

````
## Update on your PR

Hi there! Thank you so much for this wonderful contribution. We really appreciate the effort.

Unfortunately we are not able to merge this at the moment, but maybe later once things settle down. Feel free to open a new PR with a smaller scope and we would be happy to take a look!

Best regards,
The maintainers

Posted with Claude Code.
````

Posted to the thread with `gh pr comment 212 --body "..."`, then `gh pr close 212`, before the user saw it.

Why each part fails:

- Posting before the user saw it: the one rule is that nothing is sent until the user approved this exact draft; show the draft and the command, then wait.
- `maybe later once things settle down`: the user said close, not planned, so a softer version changes the decision the user made; keep the stance and give the reason.
- `Feel free to open a new PR with a smaller scope and we would be happy to take a look`: a salvage invitation the user did not make, and a maintainer's invitation is a commitment others act on.
- A heading, a greeting, and a sign-off on a short reply: a chat reply reads like a person talking, short and unheaded, and a closing comment leads with the verdict in lowercase casual register.
- No mention of the author's two earlier issues: the earlier exchanges had answers, and a reply that ignores them reads as not listening; read the author's other issues and pull requests first.
- `as we discussed in the maintainers channel`: quotes another private conversation; a reply never reveals one.
- `Posted with Claude Code.`: a trace of tooling in an outbound message; nothing that leaves the machine carries one.
- No check of the asks against the code: one of the two asks had already shipped in a merged PR, which the verdict should have named as the reason.
