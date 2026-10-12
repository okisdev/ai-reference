# A delivery that clears the bar (illustrative)

The bar for a delivery: every target names the source it was found in and the identifier verified there, the form follows the repository's own icon pattern, and the typecheck proves the imports resolve. The repository is invented; the registry paths are real.

---

Probes: `components/icons/` holds three vendored marks and `lucide-react` 1.x is installed, so brand exports are absent and brand marks are vendored.

| Target | Kind | Source | Identifier | Delivery |
|--------|------|--------|------------|----------|
| GitHub | brand | svgl | `static/library/github_light.svg` | `components/icons/github.tsx`; the mark is mono, so the fixed fill became `fill="currentColor"` and the `_dark` variant is not needed |
| OpenAI | AI brand | lobe-icons | `packages/static-svg/icons/openai.svg` | `components/icons/openai.tsx`; mono, already `currentColor` |
| settings entry | UI concept | lucide | `Settings` (`icons/settings.svg`) | `import { Settings } from "lucide-react"`; a gear is the settings convention |
| `.csv` attachment | UI concept (file type) | lucide | `FileSpreadsheet` (`icons/file-spreadsheet.svg`) | `import { FileSpreadsheet } from "lucide-react"`; rows and columns read as tabular data |
| Acme Relay | brand | none | no entry in svgl or simple-icons, and the vendor repository ships no logo file | reused the parent glyph in `components/icons/acme.tsx`; no canonical mark exists |

Existence: each candidate was found in a source listing, then probed by path; each lucide pick was confirmed against the installed version with `node -e "const l=require('lucide-react');process.exit(['Settings','FileSpreadsheet'].every(n=>Object.hasOwn(l,n))?0:1)"`. Both vendored marks were fetched with `gh api ... -H "Accept: application/vnd.github.raw"` and their path data extracted by script, never retyped. The `providers` slot is typed `React.ComponentType<{ className?: string }>` so vendored marks and lucide icons interchange.

Verified: `npx tsc --noEmit` and the build pass, and `/login` rendered in both themes shows the GitHub mark following the text color.
