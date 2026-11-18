---
description: normalize-md deletes a markdown file nobody reads and proposes, rather than deletes, one a person may still open.
tags: [quality, normalize-md]
runs: 2
max_turns: 8
timeout_seconds: 300
allowed_tools: [Skill, Read, Bash]
---

Use the normalize-md skill's file challenge on these three markdown files of my repository and tell me what happens to each and why. Nothing here is on disk; answer from these facts and do not run anything.

- `docs/plans/2025-q3-migration.md`: the plan for a storage migration that finished in 2025. No instruction file names it, no markdown file links to it, no script or build step loads it, and it holds no rule.
- `docs/guides/self-host.md`: a setup guide the project website links to from outside the repository. Its steps name the Docker image `relay/server:1`, which the README says was retired in March; the current image is `relay/server:2`. It holds no rule an agent follows.
- `features/invoices.md`: one of 96 files that `scripts/check-features.mjs` loads with `readdirSync('features/')`. It has front matter, a Rules section with "An invoice total is rounded once, at issue time.", and an Interactions section saying "The list shows twelve rows per page with a gray header."
