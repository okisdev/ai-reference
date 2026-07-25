---
name: find-icon
description: Locate a verified icon for a brand, product, or UI concept and deliver it as a lucide-react import or a vendored SVG component when asked to find or add icons.
argument-hint: "<brand|product|concept>..."
---

## Context

Existing icon registry directories: !`find . -name node_modules -type d -prune -o -type d -iname icons -print 2>/dev/null | head -5 || echo "(none)"`

Package.json files declaring lucide-react: !`find . -name node_modules -type d -prune -o -name package.json -print 2>/dev/null | xargs grep -l lucide-react 2>/dev/null | head -5 || echo "(none)"`

Installed lucide-react version: !`node -e "console.log(require('lucide-react/package.json').version)" 2>/dev/null || echo "(not installed)"`

## Instructions

Locate the correct icon for each target, prove it exists at its source, and deliver it in the form the repository already consumes icons, never writing an icon name or path data from memory.

### Process

1. Parse `$ARGUMENTS` (each target is a brand, product, AI model, or UI concept; with no arguments, take the targets from the conversation). Classify each target as a UI concept (action, state, object) or a brand mark (company, product, model, agent).
2. Read the probes: the existing icon registry directory and its component pattern decide where vendored icons go, and the installed lucide-react version is the compatibility authority, not upstream docs (lucide-react 1.0 removed all brand icons, so a brand export that older docs show may not exist locally).
3. Route each target down the source ladder: UI concept to lucide; AI model, provider, or agent brand to lobe-icons; other brand to svgl, then simple-icons; still missing, escalate to the vendor's own repository or official site. Follow [references/sources.md](references/sources.md) for the exact probes and commands for each source.
4. Prove existence before writing any code: search the source's listing rather than guessing paths (icon file names regularly differ from product names, for example stepfun, hermesagent, ai_zed), probe every candidate and keep only confirmed hits, and for a lucide pick confirm the export exists in the installed lucide-react version.
5. Fetch the confirmed SVG source with `gh` and extract long path data by script into the component, never by retyping.
6. Deliver each icon: a UI glyph as a lucide-react import; a brand mark vendored as a component in the detected registry (`components/icons/<name>.tsx` when none exists), mono marks with `fill="currentColor"` sized by `className` so they interchange with lucide icons, color marks with their official brand colors preserved. Where local and lucide icons must interchange, type the slot as `React.ComponentType<{ className?: string }>` rather than `LucideIcon`.
7. Verify with the repository's typecheck (`npx tsc --noEmit` when no narrower script exists; esbuild based builds skip type errors and let a phantom icon member render as nothing), then the build, then visually when a dev server and browser tooling are available.
8. Report a per-target table (target, source, icon identifier, delivery form) with a one line rationale for each UI concept pick; when no canonical mark exists anywhere, say so and reuse the closest parent brand glyph or a neutral placeholder.

### Rules

- Never substitute text or punctuation for an icon.
- Brand marks keep their official colors and UI glyphs follow `currentColor`; never flatten a color mark to a single color and never wrap an icon in a background chip.
- Prefer SVG over raster wherever the platform allows it.
