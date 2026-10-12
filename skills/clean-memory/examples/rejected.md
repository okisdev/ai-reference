# Rejected report

A pass that reads as thorough and gets overturned. Compare yours against it before reporting.

````
Cleaned up the project memory.
Verifier 3 checked the clipboard manager claim with pbpaste and then pbcopy to put the contents back; the clipboard did not come back.
The pass hit an API error at topic 9 of 12, so I started it over from the beginning.
Removed the stale topics (anything older than 60 days) and trimmed the long ones.
Everything is consistent now and the store is much smaller. Let me know if something is missing.
````

Why each part fails:

- `Cleaned up` with no sizing line and no counts: the user is told the size and a time estimate before the pass starts, and the report shows the audit's before and after numbers instead of asserting that the store is smaller.
- `pbpaste` and `pbcopy`: a verifier reads files and never touches user state; a claim about the machine comes back `unverifiable` (seen: a verifier subagent cleared the user's clipboard and could not restore it).
- `started it over from the beginning`: each settled row is recorded in the ledger beside the snapshot, and a dead pass resumes from the last one (seen: a pass that crashed on an API error lost 52 minutes and 154 subagent calls and restarted from zero).
- `anything older than 60 days`: age alone demotes; only evidence disproves or derives a topic.
- `trimmed the long ones`: a compaction keeps every claim that holds with its citation, and the report names what it dropped and which PR or issue carries it.
- `Everything is consistent`: a bare verdict is rerun; every disposition carries the locator that earned it (`file:line`, a SHA, an issue or PR state).
- No snapshot path, no escalations, no next cleanup date: memory lives outside git, so the snapshot is the only undo, and an unresolved conflict between a topic and the tree goes to the user with both sides' evidence.
