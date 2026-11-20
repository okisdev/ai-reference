# Surfaces and signals

Where hidden surfaces come from in each stack, and the code that marks a surface as off system. Search the whole scope for every pattern; a match is a surface to inventory, not yet a finding.

## Presenters

| Stack | Patterns |
| --- | --- |
| SwiftUI | `.sheet(`, `.fullScreenCover(`, `.popover(`, `.alert(`, `.confirmationDialog(`, `.inspector(`, `.fileImporter(`, `.fileExporter(`, `Window(`, `WindowGroup(`, `MenuBarExtra(`, `Settings {`, `.contextMenu`, `openWindow(`, `NavigationLink`, `.navigationDestination(` |
| AppKit | `NSAlert`, `NSPanel`, `NSOpenPanel`, `NSSavePanel`, `NSPopover`, `NSWindow(`, `NSMenu(`, `runModal`, `beginSheet` |
| React and web | `Dialog`, `Modal`, `Drawer`, `Sheet`, `Popover`, `Tooltip`, `DropdownMenu`, `Toast`, `toast(`, `window.confirm`, `window.alert`, route files, `createPortal`, `<dialog` |
| Android and Flutter | `AlertDialog`, `BottomSheet`, `ModalBottomSheet`, `DropdownMenu`, `Snackbar`, `showDialog(`, `showModalBottomSheet(` |

## Branches

Search each surface's body for the branches a person can land in: an `if let error`, `catch`, `failure`, `isEmpty`, `isLoading`, `!available`, `unauthorized`, `permission`, `offline`, `notFound`, and `#if` platform splits. Each is a state of that surface and is reported with how to force it.

## Signals of a surface off system

- Its own header or footer: a bold title `Text` at the top, an `HStack` of Cancel and Done at the bottom, `.padding(16)` or `.padding(20)` around it, a `Divider()` under the title.
- A platform default where the system has its own control: `.pickerStyle(.segmented)` or a menu style `Picker` in content, `.toggleStyle(.checkbox)`, `.textFieldStyle(.roundedBorder)`, a bordered or prominent system button style, `ProgressView` where the system has a progress line, `GroupBox`, `DisclosureGroup` where the system has a disclosure row; on the web, a bare `<select>`, `<input>`, `<button>`, or the browser's `confirm`.
- A fixed `.frame(width:height:)` on a sheet that leaves empty space or clips its content.
- Raw values where tokens exist: literal colors, font sizes, radii, durations, and paddings.
- A second implementation of a pattern the system owns, found by searching for the pattern's distinctive pieces (a title over a subtitle with a close button, a log line renderer, a copy to the pasteboard without the system's toast).
- An error shown as raw text from the layer below, repeated in more than one place, or offered a retry that cannot succeed.
- A destructive command (delete, kill, reset, discard, clear) that is not the system's destructive component, not in the last group after a separator, has no confirmation, or also sits as a glyph beside the menu that holds it; search every `role: .destructive` and every such verb, because a platform menu ignores the destructive role's color.
