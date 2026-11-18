# Bot signature reference

| Bot | Typical shape | What's signal |
|-----|---------------|---------------|
| `claude[bot]` | Long structured review with sections like "Issues found", "Suggestions". Often inline + summary. | Section headings under "Issues" / "Critical"; suggestion blocks. |
| `cubic-dev-ai[bot]` | Either "**No issues found**" or specific findings, each with severity. Always carries a `<!-- cubic:attribution -->` marker (ignore the marker text). | Findings with `file:line`; ignore boilerplate and attribution. |
| `coderabbit-ai[bot]` / `coderabbitai[bot]` | Verbose walkthrough + an "Actionable comments" section + inline nitpicks. | The "Actionable comments posted" count and inline comments. Ignore the walkthrough summary. |
| `greptile-apps` | Short status comment plus separate inline comments. Summary often contains only `<!-- greptile_other_comments_section -->`. | Inline comments only; the summary is metadata. |
| `changeset-bot` | "🦋 Changeset detected" or a warning if missing. | Whether a changeset exists; nothing else. |
| `vercel[bot]` / `vercel` | Deployment URL or build status. | Always noise. |
| Human reviewer | Free-form prose, sometimes inline. | Take seriously; outweighs bots on disagreement. |
