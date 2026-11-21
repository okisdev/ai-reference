---
description: review-ui deletes explanatory copy the person never acts on and names the design change that replaces it, instead of rewording it or moving it to a footer.
tags: [quality, review-ui]
runs: 2
max_turns: 10
timeout_seconds: 300
allowed_tools: [Skill, Read, Bash]
---

Use the review-ui skill to review the copy and row layout of this settings screen of a notes app. Everything you need is below; do not run commands and do not change files. There is no design system in this repository and no browser, so review in code.

```swift
Section("Devices") {
  ForEach(devices) { device in
    HStack {
      Image(systemName: device.glyph)
      VStack(alignment: .leading) {
        Text(device.name)
        Text("Last active: \(device.lastSeen) · \(device.os) \(device.osVersion) · Notes \(device.appVersion) (\(device.build))")
          .font(.footnote).foregroundStyle(.secondary)
        if device.os == "iOS" {
          Text("Notes taken in the widget appear after opening the app")
            .font(.footnote).foregroundStyle(.secondary)
        }
      }
      Spacer()
      Text("\(device.noteCount) notes").font(.footnote)
    }
  }
} header: {
  Text("Synced devices: \(devices.count)")
}
Section {
  LabeledContent("Storage used", value: storage)
} footer: {
  Text("When this device is low on space, attachments unused for a day stay on the server and download when you open them.")
}
```

Sample data: five devices, four of them iOS; every device runs the same app version 2.4.0 with builds 61 to 64; one iOS device is the one in the person's hand.

Reply in English with your review.
