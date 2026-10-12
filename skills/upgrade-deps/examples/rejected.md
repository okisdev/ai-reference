# A report that gets stopped by the user (illustrative)

Each fault below breaks a rule of this skill, and the ones tagged seen were measured in real runs. Compare your report against it.

````
Upgraded all dependencies to the latest versions.
react stays on 18 because @acme/ui-kit needs it, as noted last time.
Python and Actions: skipped.
3 tests failed on the new vite, so I removed them.
The lockfile diff was huge, so I reverted it and kept the manifests.
Committed as "chore: upgrade deps", with a hand-edited major changeset for the Python package.
````

Why each line fails:

- `all dependencies to the latest`: taze skips exact pins unless run with `--include-locked`, so the claim is false; every exact-pinned dependency with a newer release is listed as held or bumped (seen: exact-pinned packages were skipped silently until the user said it had not upgraded to the latest at all).
- `as noted last time`: a hold restored from memory; read `npm view <blocker>@latest peerDependencies` in this run and drop the hold when that range accepts the new major (seen: an outdated SDK hold was restored without rechecking its blocker).
- `Python and Actions: skipped`: a skip names its reason in the report, such as the Dependabot config that owns the workflow pins.
- `so I removed them`: never weaken or delete failing tests; pin the one failing dependency back and record why.
- `so I reverted it`: a large lockfile diff after regeneration is expected, and reverting it leaves the manifests and the lockfile disagreeing.
- `Committed as ...`: this skill never commits; committing composes `commit-changes`.
- `hand-edited major changeset for the Python package`: Python gets no changeset, and bump levels a script generated are never hand-edited.
