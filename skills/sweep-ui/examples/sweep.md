# A sweep that clears the bar

The bar: every surface the code can present was measured on real data, fixed through shared components until a fresh pass came back clean, and the report shows the counts before and after, what was opened, and the one question left for the user.

> Scope: the web console. System: `apps/console/DESIGN.md` (extends `skill:personal-web-design`); UI module `src/ui` exports `Card`, `List`, `ListItem`, `Table`, `KeyValue`, `Segmented`, `Notice`, `Toast`.
>
> Inventory: 14 routes, 31 tabs, 9 drawers, 12 dialogs, 1 command palette, 40 empty, loading or error branches; 2 pages only a charger or a guard source unlocks, opened in the home that has them. Size: 106 surfaces by 2 viewports, about 90 minutes.
>
> **Component fixes** (one change, every surface follows)
>
> | Finding | Surfaces | Fix |
> | --- | --- | --- |
> | icon-off-centre, 2.5 px on every icon inside text | 11 | `.ui-text` with an icon lays out as an inline flex row |
> | wrapped-label, short cells stacked one character per line in narrow tables | 4 | table cells outside the growing column never wrap |
>
> **Pattern fixes** (one component, then the surfaces migrated)
>
> | Finding | Surfaces | Fix |
> | --- | --- | --- |
> | rows built by hand with their own leading widths, text starting at 58 and 89 px in one list | 8 | `ListItem` everywhere; a check-ui rule fails a hand built row |
> | uneven-siblings and control-drift on the proxy member cards, 44 to 62 px tall with the menu moving | 1 page, 2488 cells | members grouped by region in fixed 32 px cells; region and name prefix said once per row; the per card menu replaced by the cell's own select, with Details and Test kept in the hover hint |
>
> **Structure fixes**
>
> | Finding | Surfaces | Fix |
> | --- | --- | --- |
> | majority-caption, "health check failed" on 52 of 92 members | proxy groups | one line under the group; the latency tone marks each member |
> | the same timeline on the overview and the logs page | 2 | the overview keeps the open items, links to the timeline |
>
> **Surface fixes**
>
> | Surface | How to reach it | Finding | Fix |
> | --- | --- | --- | --- |
> | Home card (`Homes.tsx:290`) | Homes | layout-shift 57 px when the update status arrives; says-nothing "No timezone set" | outcome as a toast at the moment it happens, version in place; timezone only in the edit form |
> | Incident row (`Incidents.tsx:108`) | Logs, Incidents | internal-id in the meta line; repeated-in-row "Source error" | the detail as the meta line, the subject only when it is a name |
> | Proxy groups (`Groups.tsx:60`) | Proxy, Groups | disclosure-wall, 30 of 34 groups opened one at a time; uncounted-list; the same three hop path on 17 rows | each row shows its exit and the one group it follows; the count and its split in the toolbar with a search and one open all; actions to review every group's members 30 to 1 |
>
> Counts, first pass to last: layout-shift 6 to 0, wrapped-label 4 to 0, icon-off-centre 73 to 0, uneven-siblings 3 to 0, control-drift 27 to 0, majority-caption 31 to 1 (accepted: each group lists the same policy member by design), says-nothing 44 to 0, internal-id 5 to 0, disclosure-wall 1 to 0, uncounted-list 1 to 0.
>
> Opened in 1440 and 390 wide, light and dark: 98 of 106 surfaces. Judged from code: 8 error branches that need a failing upstream; each is measured again once it can be opened, and the loop ends when every audit is clean or a finding is accepted by name.
>
> Question for you: the per member speed test now lives only in the hover hint, and the group test runs every member. May I drop the per member test, or keep it?

Why it clears the bar:
- Every surface the code presents was counted and measured, including the ones behind a source only one home has.
- Findings come from measurements and named questions, each with the fix, grouped so one shared change closes many.
- It looped until the audit was clean and names the one finding it accepted and why.
- The only question is about a capability, asked once at the end, with the capability kept meanwhile.
