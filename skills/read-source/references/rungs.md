# Source ladder rungs

Exact commands for each rung, referenced from SKILL.md step 2 onward. Prove the answer in real source at an exact version before reporting it; stop at the first rung that answers the question.

## L0 installed

Read the exact installed version:
```
cat node_modules/<pkg>/package.json | jq -r .version
```
List the shipped type declarations:
```
find node_modules/<pkg> -maxdepth 3 -name '*.d.ts' | head
```
Grep the symbol across those declarations:
```
find node_modules/<pkg> -maxdepth 3 -name '*.d.ts' -print0 | xargs -0 grep -n '<symbol>'
```
Check for a local patch of the pin; a hit makes the patched output the behavior authority for this project:
```
jq -r '.pnpm.patchedDependencies // empty' package.json; ls patches/ 2>/dev/null
```
An installed CLI with no `node_modules` entry: its version, its resolved binary, and an npx cache copy when there is one:
```
<bin> --version; realpath "$(command -v <bin>)"
ls -d ~/.npm/_npx/*/node_modules/<pkg> 2>/dev/null
```
Bound a run of the binary with a SIGTERM wrapper, since macOS ships no `timeout`: `perl -e '$p=fork or exec @ARGV; $SIG{ALRM}=sub{kill TERM=>$p}; alarm 60; waitpid $p,0; exit($? & 127 ? 124 : $? >> 8)' <bin> <args>`.

A task worktree with no `node_modules`: the pin comes from the worktree's lockfile (a scoped `@scope/pkg` sits in pnpm's store directory as `@scope+pkg`), the files from the main checkout's pnpm layout or the pnpm store, never from scratch scripts resolving `./node_modules` in the worktree:
```
grep -n '<pkg>@' pnpm-lock.yaml | head -3
main=$(git worktree list --porcelain | sed -n '1s/^worktree //p'); ls -d "$main"/node_modules/.pnpm/<pkg with / as +>@<ver>*/node_modules/<pkg>
ls -d ~/Library/pnpm/store/v*/links/*/<pkg>/<ver>* 2>/dev/null
```
A Rust crate: the pin from `Cargo.lock`, the source from the registry cache, fetched into a scratch `CARGO_HOME` when the sandbox makes `~/.cargo/registry` read-only or empty:
```
grep -A1 'name = "<crate>"' Cargo.lock
ls -d ~/.cargo/registry/src/*/<crate>-<ver>/src || CARGO_HOME="$SCRATCH/cargo" cargo fetch
```
A Maven or AAR artifact without published source: extract `classes.jar` from the Gradle cache and read the bytecode, citing the class and method since there are no source lines:
```
find ~/.gradle/caches/modules-2/files-2.1/<group>/<artifact>/<ver> -name '*.aar' -o -name '*.jar'
unzip -o <artifact>.aar classes.jar -d "$SCRATCH/aar" && javap -c -p -classpath "$SCRATCH/aar/classes.jar" <fully.qualified.Class>
```

## L1 published artifact

Pack and extract the exact version in a scratch directory outside the repository, then search it:
```
mkdir -p "$SCRATCH/pkg-probe" && cd "$SCRATCH/pkg-probe" && npm pack <pkg>@<ver> --ignore-scripts && tar -xzf <pkg>-<ver>.tgz && rg -n '<symbol>' package/
```
The tarball always extracts to a `package/` root directory regardless of the package's own name.

Bisect a behavior change by packing a short list of versions:
```
for v in 1.2.0 1.2.1 1.3.0; do npm pack <pkg>@$v --ignore-scripts; done
```
Extract each tarball to its own directory, then diff or grep across them. This rung answers what actually shipped, which docs regularly get wrong.

## L2 upstream source

Resolve the repository without needing an install:
```
npm view <pkg> repository.url
```
The result is usually a `git+https://github.com/<owner>/<repo>.git` URL; strip the `git+` prefix and the `.git` suffix to get `<owner>/<repo>`.

Read the tag naming from the latest release, since it varies (`v16.4.3`, `rust-v0.164.0`, `@changesets/cli@3.0.3`), then probe the target version in that form before the `v` prefixed and bare forms:
```
gh release view -R <owner>/<repo> --json tagName -q .tagName
gh api repos/<owner>/<repo>/git/ref/tags/<prefix><ver> || gh api repos/<owner>/<repo>/git/ref/tags/v<ver> || gh api repos/<owner>/<repo>/git/ref/tags/<ver>
```
Fetch a single file at that resolved ref:
```
gh api "repos/<owner>/<repo>/contents/<path>?ref=<tag>" -H "Accept: application/vnd.github.raw"
```
Shallow clone into scratch for cross-file tracing:
```
gh repo clone <owner>/<repo> "$SCRATCH/<repo>-ref" -- --depth=1 --branch <tag>
```

When `gh api` answers `error connecting to api.github.com` or the host does not resolve, the sandbox has no network: stop retrying this rung, return to the local copies at the pinned version (L0 above), and when none holds the answer report the claim as unverified, naming the blocked command (seen: all six upstream reads in sandboxed runs failed to connect at least once).
