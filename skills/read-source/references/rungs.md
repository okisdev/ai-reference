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

This rung is the compatibility authority for what the project can actually import or typecheck; no later rung overrides it for that question.

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
Always pin `<tag>` to the resolved ref. The default branch describes a future version, not the one installed.

## L3 docs

Fetch the documentation site only after the earlier rungs cannot answer the question, or to confirm intended usage and find examples. Docs answer intent and examples only; they never prove an API exists or behaves as described.

## Choosing the entry rung

| Question type | Entry rung |
| --- | --- |
| Import or typecheck question (does this exist in our version, why does the build fail) | L0 |
| Shipped artifact or regression question (what shipped in version V, when did behavior change) | L1 |
| Behavior, internals, or history question (how or why it behaves, maintainer intent, unreleased work) | L2 |
