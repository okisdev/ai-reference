---
name: read-source
description: Answer how a dependency behaves, or whether it supports something, from its source at the pinned version, including asks to read a library's or upstream's source.
argument-hint: "<package> [symbol] [@version]"
---

## Context

JavaScript lockfile: !`for f in pnpm-lock.yaml yarn.lock package-lock.json bun.lock bun.lockb; do if test -f "$f"; then echo "$f"; exit 0; fi; done; echo "(none)"`

node_modules directory: !`test -d node_modules && echo "present" || echo "(none)"`

## Instructions

**The one rule: every claim about a dependency names the source that proved it.** Pick the ladder rung that matches the question, prove the answer in real source at an exact version, and report the answer first, then the rung, the exact version or ref, and the file and line that settle it; docs and memory never count as proof, and a behavior that reading cannot settle is run in a scratch script or reported as unproven. The bar is [examples/answer.md](examples/answer.md): open it before writing, and check the draft against [examples/rejected.md](examples/rejected.md).

### Process

1. Parse `$ARGUMENTS` (a package name, an optional symbol, and an optional `@version`; without a version, use the installed or lockfile-pinned one). Classify the question before touching anything: "does this exist in our version" or "why does our build fail" starts at rung L0; "what shipped in published version V" or "when did behavior change" starts at rung L1; "how or why does it behave", maintainer intent, or unreleased work starts at rung L2. Docs are never the starting rung.
2. L0 installed: read `node_modules/<pkg>/package.json` for the exact version, then the shipped type declarations and JS under its `dist`; an installed CLI without a `node_modules` entry reads its version from `<bin> --version` and its files from its install path (the npx cache, the Homebrew prefix). Check for a local patch of the pin (`pnpm.patchedDependencies` in package.json, a `patches/` directory); when one exists the patched file is the behavior authority and the published artifact no longer describes this project. This rung is the compatibility authority for what the project can actually import; no upstream read overrides it for import and typecheck questions. See [references/rungs.md](references/rungs.md) for the exact commands at this and every later rung.
3. L1 published artifact: in a scratch directory outside the repository, run `npm pack <pkg>@<ver> --ignore-scripts`, extract it, and search the extracted `package/`. This catches the case where docs claim an API the artifact does not ship. Loop over a short list of versions to bisect a behavior change.
4. L2 upstream source: resolve the repository from the package's `repository` field, resolve the release tag for the target version (naming varies, so read it from the latest release before probing), then fetch single files with `gh api` at that ref, or shallow clone into scratch for cross-file tracing. Always pin the ref; the default branch describes a future version, not the one installed. For an intent question (why it works this way), code shape is not its own explanation: read the commit messages, PRs, and issues that touched the lines at the pinned ref, and where they are silent report the intent as unknown rather than inferred from the code.
5. L3 docs last, to confirm intended usage or find examples, never as proof an API exists or behaves as described.
6. Stop at the first rung that answers the question. A behavior claim that reading cannot settle gets a scratch script that imports the installed package and runs the call, or for a CLI the installed binary driven through the project's own integration path, since a source read covers only the layer it read (seen: a source read settled a CLI's plugin loading while its installed version had renamed the database table the integration queried); when even that is unavailable, report the claim as unproven instead of settling it from prose. Report the answer with the rung, the exact version or ref, and the file that proved it.

### Rules

- An ask to read a library's or upstream's source in the user's own words, in any language, is this skill's ask: classify the question under it and start at that rung (seen: users asked to read a library's source in their own words and the skill never fired).
- Never assert an API exists or behaves a certain way from docs or from memory; every claim names the rung and version that proved it.
- `npm pack` always runs outside the repository tree and always with `--ignore-scripts`.
- Upstream reads always pin a tag or commit, never the default branch head.
