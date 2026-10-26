# Body format (when no repo template was found)

```
closes #<n>

## summary

- <2 to 4 bullets, lead with user-visible change, then implementation>

## breaking changes

- <removed/renamed APIs, changed defaults, migration steps; OMIT this whole section if none>

## test plan

### already verified

- [x] <exact command + observable outcome, e.g. `pnpm --filter @x/y test` -> 42/42 green>

### reviewer should verify

- [ ] <concrete reproduction step naming the UI path / flag / API call and the expected observable outcome>

## notes

- <follow-ups, known limitations, attribution; OMIT this whole section if none>
```

Body rules:

- `closes #<n>`: very first line, no heading, lowercase keyword, only when the merge resolves the whole issue; a PR that delivers part of it opens with `part of #<n>` instead and says in `## notes` what remains. Repeat on its own line per issue (`closes #10` then `closes #11`); cross-repo is `closes owner/repo#<n>`. Omit when no issue is referenced. Issue numbers come from explicit user mention, branch name patterns like `fix/4005-foo`, or commit subjects mentioning `#<n>`.
- When the diff mixes hand-written and generated or mechanical files (lockfiles, snapshots, codemod output), say so in the summary and name which files carry the reviewable logic.
- When the change needs a rollout or migration order (deploy X before Y, run the migration first), state it in `## notes`; the diff cannot show sequencing.
- All section headings are lowercase.
- Pre-check `[x]` only for items actually verified before the push. Leave `[ ]` for things the reviewer needs to do.
- Skip the entire `## test plan` section for docs-only, types-only, or changeset-only PRs. Replace it with a single line: `no test plan, <one-clause reason>` (e.g. `no test plan, docs only`).
- Omit `## breaking changes` and `## notes` sections entirely when they have no content. No empty headings.
