---
description: sweep-ui inventories surfaces from the code, finds the sheet and the error state hidden behind a menu, and names the component that fixes each.
tags: [quality, sweep-ui]
runs: 2
max_turns: 10
timeout_seconds: 300
allowed_tools: [Skill, Read, Bash]
---

Use the sweep-ui skill on this app. Everything you need is below; do not run commands and do not change files. You cannot open the app, so judge from code.

The design system's UI module exports `FormSheet(title:subtitle:action:finish:content:)` for sheets that create something, `ViewerSheet(title:subtitle:content:)` for sheets that only show output, `MenuPicker` for a choice among a few values, and `EmptyState(title:systemImage:message:)`. The sidebar shows two pages, Images and Builds; both pages were redesigned last week and look right.

```swift
// ImagesView.swift
struct ImagesView: View {
    @State private var pulling = false
    var body: some View {
        ImageList()
            .toolbar { Button("Pull Image", systemImage: "arrow.down.circle") { pulling = true } }
            .sheet(isPresented: $pulling) { PullImageSheet() }   // line 12
    }
}
private struct PullImageSheet: View {
    var body: some View {
        VStack {
            Text("Pull image").font(.headline)
            Form { TextField("Image", text: $reference); Picker("Platform", selection: $platform) { ... } }
            HStack { Spacer(); Button("Cancel") { dismiss() }; Button("Pull") { pull() }.keyboardShortcut(.defaultAction) }
        }.padding(20).frame(width: 520, height: 360)
    }
}

// BuildsView.swift
struct BuildsView: View {
    @State private var logs: BuildRecord?
    var body: some View {
        BuildList(openLogs: { logs = $0 })
            .sheet(item: $logs) { record in                       // line 30
                VStack { HStack { Text(record.title).font(.headline); Spacer(); Button("Done") { dismiss() } }; Divider(); LogPane(record) }
            }
    }
}
struct BuildDetail: View {
    var body: some View {
        if let failure = inspection.failure {                     // line 41
            Text(failure).foregroundStyle(.red)
            Button("Try Again") { retry() }
        } else { StepList() }
    }
}
```

Reply in English with your sweep.
