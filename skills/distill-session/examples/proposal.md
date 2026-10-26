# A proposal table that clears the bar (illustrative)

The bar for a proposal: a few rows, each pinned to a verbatim quote with its file and line and to a named home (for a skill edit, the section and the sentence to change), and every dropped candidate accounted for. The skills, sessions, and quotes are invented, and locators read `<session id prefix>.jsonl:<line>` in this repository's transcript directory. The report's language follows the user; quotes stay verbatim in the language they were typed.

---

**Sizing**: told at the start as 9 transcripts (7 days, 14 MB), 2 reader batches, about 10 minutes. Took 8.

**Scope**: 9 Claude transcripts from the last 7 days, so the inventory cap of 20 was not reached; no Codex or Grok store is present. The readers returned 14 candidates and 4 passed the gates.

| Target | Proposed change | Evidence |
|---|---|---|
| `skills/release-notes/SKILL.md`, Process step 2, the sentence "Collect the merged PRs since the last release." | Replace "since the last release" with "since the last tag (`git describe --tags --abbrev=0`), because a draft release has no tag". Anti-pattern: the notes started at a draft release and covered the wrong range | `"wrong range, it should start from v2.3.1"` (`4f1c9a02.jsonl:312`) |
| `skills/triage-issues/SKILL.md`, Rules, after the bullet "Reply before you close." | Add the bullet "Comment the canonical issue's link before closing a duplicate." Win: the reporter did not reopen | `"right, closing duplicates this way keeps them closed"` (`b7e3d518.jsonl:241`) |
| New-skill candidate (an issue in the skills repository) | `bump-changelog`: the same three-step edit (read the unreleased section, move it under the version heading, add the compare link) was done by hand in 3 sessions | `"editing the CHANGELOG by hand again"` (`2d80a6ce.jsonl:58`), `"same again, update the CHANGELOG"` (`b7e3d518.jsonl:402`) |
| Standing rule (suggested line, not written) | "Run `pnpm typecheck` before saying a UI change works." | `"you said it was done, but typecheck fails"` (`91ac07d4.jsonl:204`); the agent's own "typecheck passes" at `:199` was re-run on `main` at `a1b2c3d` and exits 2 |

**Dropped at the gates**: 10 of 14. 5 not durable (paths from one task), 3 not decision-changing ("be careful with dates"), 1 not encodable (no home), 1 already recorded (`AGENTS.md:14` already says to run the unit tests before a commit). No quote carries a secret.

Nothing is applied. Reply with the rows to apply.
