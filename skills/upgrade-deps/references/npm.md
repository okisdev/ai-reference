# npm dependency updates

Use this fallback only when the repository has no native dependency preview and update scripts.

## Taze recipe

Taze modes are maximum permitted version changes, not package release-version bump commands. `minor` allows minor and patch updates within the current major line. `patch` is supported and allows patch updates within the current minor line.

| Requested scope | Preview | Apply |
| --- | --- | --- |
| Major | `npx taze major -f -r` | `npx taze major -f -w -r` |
| Minor | `npx taze minor -f -r` | `npx taze minor -f -w -r` |
| Patch | `npx taze patch -f -r` | `npx taze patch -f -w -r` |

The preview commands omit `-w`, which is the write flag. `-f` refreshes package metadata and `-r` scans workspace packages recursively.

## Install and dedupe

After taze writes manifests, use the lockfile's package manager.

| Lockfile | Install | Dedupe |
| --- | --- | --- |
| `pnpm-lock.yaml` | `pnpm install` | `pnpm dedupe` |
| `yarn.lock` | `yarn install` | `yarn dedupe` in Yarn 2 and later. Yarn 1 has no built-in dedupe. |
| `package-lock.json` | `npm install` | `npm dedupe` |
| `bun.lock` or `bun.lockb` | `bun install` | No separate Bun dedupe command exists. |

For a thorough regeneration after a blanket workspace bump or when the existing lockfile has stale resolution state, remove every `node_modules` directory with `find . -name node_modules -type d -prune -exec rm -rf {} +`, remove the detected lockfile with `rm pnpm-lock.yaml`, `rm yarn.lock`, `rm package-lock.json`, `rm bun.lock`, or `rm bun.lockb`, then install and run the applicable dedupe command from the table.

## Install guards

Two pnpm guards routinely interrupt upgrades.

| Symptom | Meaning | Fix |
| --- | --- | --- |
| A just-published version is not picked up | `minimumReleaseAge: 1440` in `pnpm-workspace.yaml` blocks any npm package published in the last 24 hours | Wait out the window, or lower the setting for that run when the fresh release is the point of the upgrade |
| `ERR_PNPM_IGNORED_BUILDS` | pnpm refused to run postinstall build scripts for packages missing from the allowlist | Add the package (commonly `sharp`, `esbuild`, `workerd`) to `onlyBuiltDependencies` in `pnpm-workspace.yaml`, then reinstall |

## SDK repins

| Detection condition | Fix command | Why |
| --- | --- | --- |
| A workspace package declares an `expo` dependency | Run `npx expo install --fix` from that package directory | Blanket bumpers do not know SDK compatibility matrices and can select versions that crash at runtime. |

To intentionally hold an SDK package back after a blanket bump, restore only that manifest with `git checkout -- <workspace>/package.json`, then reinstall with the detected package manager and run its dedupe command when one exists.

## Changesets

Before any commit, inspect changed manifests with `git diff HEAD --name-only -- ':(glob)**/package.json'`. Use those files to identify published packages whose dependency manifests changed, excluding packages with `private: true`. Run the repository's changeset-generation script when it provides one. Otherwise create one patch changeset in the repository's established format for all remaining packages.
