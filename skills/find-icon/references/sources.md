# Icon sources

Exact commands for each source in the routing ladder, referenced from SKILL.md step 3 onward. Prove a match with a listing or a direct probe before writing any code.

## Source ladder

| Target kind | Source | When it applies |
| --- | --- | --- |
| UI concept (action, state, object) | lucide | Default source for interface glyphs. |
| AI model, provider, or agent brand | lobe-icons | Purpose-built registry for AI brand marks. |
| General brand | svgl | Broad, actively maintained logo registry. |
| Brand missing from svgl | simple-icons | Large brand fallback; usually sparse on niche AI brands. |
| Still missing anywhere above | Vendor's own repository or official site | Last resort escalation. |

## lucide

Repository `lucide-icons/lucide`, files at `icons/<kebab-name>.svg`.

Probe one candidate name at a time and keep only confirmed hits:
```
gh api repos/lucide-icons/lucide/contents/icons/arrow-up.svg --jq '.content' >/dev/null 2>&1 && echo FOUND || echo missing
```
Loop a short list of candidate names through that probe before falling back to a broad search of the whole tree:
```
gh api 'repos/lucide-icons/lucide/git/trees/main?recursive=1' --jq '.tree[].path' | grep -i arrow
```
Fetch the confirmed file's content and decode it:
```
gh api repos/lucide-icons/lucide/contents/icons/arrow-up.svg --jq '.content' | base64 -d
```
Kebab-case file names map to PascalCase lucide-react exports (`arrow-up.svg` becomes the `ArrowUp` export). Confirm the export exists in the installed version before using it:
```
node -e "process.exit(Object.hasOwn(require('lucide-react'),'ArrowUp')?0:1)"
```
Or list `node_modules/lucide-react/dist/esm/icons/` and grep it for the kebab-case file name.

## lobe-icons

Repository `lobehub/lobe-icons`. The npm package is `@lobehub/icons` for components and `@lobehub/icons-static-svg` for flat SVG files; the bare name `lobe-icons` does not exist on npm.

Two layouts coexist. Component sources sit at `src/<Name>/components/Mono.tsx`, with `Color.tsx` and brand colors in `src/<Name>/style.ts` present for brands that have a color variant. Flat static files sit at `packages/static-svg/icons/<name>.svg` and `packages/static-svg/icons/<name>-color.svg`.

List a directory and filter it:
```
gh api repos/lobehub/lobe-icons/contents/packages/static-svg/icons --jq '.[].name' | grep -i openai
```
Search paths directly when a directory listing is too large to scan:
```
gh api 'search/code?q=openai+repo:lobehub/lobe-icons+in:path' --jq '.items[].path'
```
Fetch the chosen file's raw content:
```
gh api repos/lobehub/lobe-icons/contents/packages/static-svg/icons/openai.svg -H "Accept: application/vnd.github.raw"
```
Prefer extracting the SVG into a local component over adding either npm package as a dependency.

## svgl

Repository `pheralb/svgl`, files under `static/library/`.

List and filter:
```
gh api repos/pheralb/svgl/contents/static/library --jq '.[].name' | grep -i notion
```
Fetch the chosen file raw:
```
gh api repos/pheralb/svgl/contents/static/library/notion.svg -H "Accept: application/vnd.github.raw"
```

## simple-icons

Repository `simple-icons/simple-icons`, files under `icons/<slug>.svg`. The slug is the brand name lowercased with punctuation stripped.
```
gh api repos/simple-icons/simple-icons/contents/icons/notion.svg -H "Accept: application/vnd.github.raw"
```
Search the tree listing when a guessed slug misses:
```
BRANCH=$(gh api repos/simple-icons/simple-icons --jq .default_branch)
gh api "repos/simple-icons/simple-icons/git/trees/$BRANCH?recursive=1" --jq '.tree[].path' | grep -i notion
```
Niche AI brands are usually absent from this registry.

## Vendor escalation

Resolve the default branch, then grep the recursive tree for a likely icon path:
```
BRANCH=$(gh api repos/zed-industries/zed --jq .default_branch)
gh api "repos/zed-industries/zed/git/trees/$BRANCH?recursive=1" --jq '.tree[].path' | grep -iE 'logo|icon|brand|mark'
```
Two examples worth the pattern: `zed-industries/zed` keeps its mark at `assets/icons/ai_zed.svg`; `better-auth/better-auth` keeps its marks under `docs/public/branding/svg/`. When the repository itself has nothing, the vendor's marketing site press or brand page is the next step, and a general web search is the last resort.

## Extraction

Fetch the SVG to a file first, then pull the path data out with a script; a long path attribute retyped by hand is a known transcription failure.
```
gh api repos/<owner>/<repo>/contents/<path/to/icon.svg> -H "Accept: application/vnd.github.raw" > /tmp/icon.svg
node -e "console.log((require('fs').readFileSync('/tmp/icon.svg','utf8').match(/ d=\"[^\"]+\"/g) || []).join('\n'))"
```
Or with Python:
```
python3 -c "import re; print('\n'.join(re.findall(r' d=\"([^\"]+)\"', open('/tmp/icon.svg').read())))"
```
Paste the extracted output into the component programmatically, never by hand.

## Platform notes

- WeChat WXSS strips `mask` and `-webkit-mask`, so a themed icon there needs a per-theme base64 data URI `background-image` instead.
- ImageMagick's MSVG renderer drops stroked paths, so rasterize SVGs through a real browser engine instead.
