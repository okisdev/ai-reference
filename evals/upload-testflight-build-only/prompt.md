---
description: upload-testflight keeps the version, reads App Store Connect's latest build before choosing the number, and confirms the build there.
tags: [quality, upload-testflight, guard]
runs: 2
max_turns: 8
timeout_seconds: 240
allowed_tools: [Skill, Read, Bash]
---

Use the upload-testflight skill to plan sending a build of my app Lantern to TestFlight without changing the version. Answer from this state only; do not run anything, and say exactly what you would set and check.

- Local numbers: version 2.3.0, build 41.
- Teammates sometimes upload builds from their own machines; you have not looked at App Store Connect yet.
- The repository has a fastlane lane `beta` that runs `increment_version_number(bump_type: "minor")`, then `increment_build_number`, builds, and runs `upload_to_testflight`. Its log ends with "Successfully uploaded the new binary to App Store Connect".
- The working tree is clean.
