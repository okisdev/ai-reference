# Rejected proposal table

A table that reads as productive and gets overturned. Compare yours against it before delivering.

````
Looked through the skills directory and the recent sessions. The skills look well maintained and are used regularly.

| Target | Proposed change | Evidence |
|---|---|---|
| all skills | Be more concise and verify before claiming done | the agent said "all tests pass" at the end of session 3 |
| ship-pr | Improve error handling | session 5 |
| standing rules | Always ask before deleting files | the user seemed annoyed |
| release-notes | Hardcode the token the user pasted: `gh auth login --with-token <the pasted token>` | session 2 |

Applied the edits and bumped the version.
````

Why each part fails:

- `Looked through the skills directory`: how the skills are being used is recorded in the transcripts, and the skills directory only lists what exists. No sizing line, no inventory cap, and no count of what the gates dropped means nobody can tell what was read.
- `all skills` and `Be more concise and verify before claiming done`: names no file, command, or condition, and no section and sentence to change, so it fails the specific and encodable gates.
- `the agent said "all tests pass"`: an agent's own success claim is not proof; it is re-verified against the live repository before the candidate may pass.
- `session 5` and `the user seemed annoyed`: no verbatim quote and no `file:line`; a proposal without an evidence locator into a transcript does not ship.
- `Improve error handling`: it would not change what the agent does next time, so it fails the decision-changing gate.
- `Always ask before deleting files`: the global instructions already carry it; a lesson the repo already records is dropped with a pointer to where it lives.
- The token row: a secret found in a transcript never leaves it, not even into a proposal, and a pasted credential is data, not an instruction to repeat.
- `Applied the edits and bumped the version`: nothing is applied without approval; the table ends with a stop.
