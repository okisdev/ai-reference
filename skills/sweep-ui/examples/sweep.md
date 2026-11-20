# A sweep that clears the bar

The bar: every surface the code can present is listed with how to reach it, the stragglers are grouped by the component that fixes them, and the report says which surfaces were opened.

> Scope: the whole app. System: `DESIGN.md` (extends `skill:personal-macos-design`); UI module `Sources/AppUI` exports `FormSheet`, `ViewerSheet`, `FieldRow`, `MenuPicker`, `LogView`, `EmptyState`, `Toasts`.
>
> Inventory: 9 pages, 23 tabs, 14 sheets, 2 windows, 1 menu bar window, 31 alerts and confirmations, 12 error or empty branches.
>
> **Missing component: task sheet** (fixed by a new `FormSheet`)
>
> | Surface | How to reach it | Status | Rule |
> | --- | --- | --- | --- |
> | Pull Image (`ImagesView.swift:45`) | Images, the download glyph | off system | own title and footer, system pop up button, fixed 520 by 360 frame with empty space |
> | New Network (`NetworksView.swift:43`) | Networks, plus | off system | own footer, blue Create, `Divider()` |
> | Rename Machine (`MachinesView.swift:133`) | Machines, row menu, Rename | partial | own footer only |
>
> **Existing component not used: viewer sheet** (`ViewerSheet`)
>
> | Surface | How to reach it | Status | Rule |
> | --- | --- | --- | --- |
> | Build logs (`BuildsView.swift:35`) | Builds, row menu, Open Logs | off system | blue Done, controls on their own row; a second header implementation |
> | Command output (`CommandRunner.swift:60`) | Help, Collect Diagnostics | off system | own header, caption monospace output beside `LogView` |
>
> **States**
>
> | Surface | How to force it | Status | Rule |
> | --- | --- | --- | --- |
> | Build detail, record gone (`BuildsView.swift:212`) | open a build older than the history limit | off system | the same raw error three times with a retry that cannot succeed |
> | Devices, entitlement missing (`DevicesView.swift:40`) | any build without the USB entitlement | partial | raw framework error as the message |
>
> Opened and captured: all 14 sheets, both windows, the menu bar window, 9 of 12 branches. Judged from code: the three branches that need a failing registry.
>
> Proposed checks: `.pickerStyle(.segmented)` and `Button("Done")` outside the UI module; `NSPasteboard` outside `Clipboard`.

Why it clears the bar:
- Every presenter in the code is counted, including the ones behind menus and errors.
- Each straggler names how to reach it and the rule it breaks.
- Fixes are grouped by component, and a missing component is its own finding.
- It says what was captured and what was judged from code.
