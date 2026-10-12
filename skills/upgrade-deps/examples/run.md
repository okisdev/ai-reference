# An upgrade that clears the bar (illustrative)

The bar for the closing message of a run: every dependency that does not land on its latest release is named with the reason and the evidence from this run, each ecosystem has its own block, and the last line states the state of the tree. Package names, versions, and counts are invented; the shape is the bar.

````
npm (pnpm workspace, 9 packages): `npx taze major -f -r` previewed, then applied with `-w`, then `pnpm install` and `pnpm dedupe`. `apps/mobile` declares `expo`, so `npx expo install --fix` ran from that directory.
- Bumped 58 dependencies. Notable majors: `vite` 6 to 7, `zod` 3 to 4, `@acme/forms` 2 to 3 (release notes read; the `Form` default export became a named export and 4 call sites moved).
- Held: `@acme/camera` stays on 2 (an SDK package in `apps/mobile`). Blocker: `@acme/scanner`; `npm view @acme/scanner@latest peerDependencies` ran now and still lists `@acme/camera: ^2`, so the hold stands.
- Hold dropped: `@acme/maps` 5 was rejected by the installed `@acme/geo` 1. `npm view @acme/geo@latest peerDependencies` ran now and accepts `@acme/maps: ^5`, so `@acme/geo` moved to its latest release and `@acme/maps` stayed bumped.
- Exact pins with a newer release (taze skips them without `--include-locked`): `esbuild` 0.25.1 bumped to 0.25.9; `sharp` 0.33.5 held, because `npm view @acme/images@latest dependencies` ran now and still pins it exactly.
- Pinned back: `acme-jest` 4 to 3, because 6 suites failed on a matcher the new major removed.
- Validation: `pnpm build`, `pnpm lint`, and `pnpm test` pass (312 tests; none changed, skipped, or deleted).
- Changeset: `.changeset/` exists and the repo has no generator script, so one patch changeset covers the 3 published packages whose manifests changed; the 6 private packages are skipped.
python (`services/api`, `uv.lock`): `uv lock --upgrade && uv sync`; `uv run pytest` 87 passed. No changeset: the lock change is transitive, not the package's own version.
actions: skipped. `.github/dependabot.yml` exists and owns the workflow pins.
State: validated and uncommitted; the lockfile diff is large, which is expected after regeneration. Committing composes `commit-changes`.
````

Why it clears the bar:

- It accounts for every dependency short of its latest release: a hold that stands, a hold that was dropped, the exact pins, a pin back, each with its reason.
- Each hold cites the blocker's newest peer range read in this run, not a remembered one; that recheck is what turned the `@acme/maps` hold into a bump.
- Exact pins are listed as held or bumped with the taze caveat, so the user never has to ask whether pinned packages were upgraded.
- Skipped work carries its reason, and the missing Python changeset is explained.
- The closing line states that the tree is validated and uncommitted, and nothing was committed or weakened to get there.
