---
name: upload-testflight
description: Archive an Xcode app, upload the build to App Store Connect, and add it to TestFlight testing, when asked to send a TestFlight build, bump the build and upload, or find out why an upload never arrived.
argument-hint: "[scheme] [--version <x.y.z>] [--group <name>] [--submit]"
---

## Context

Xcode projects: !`out=$(git ls-files 2>/dev/null | grep -E '\.(xcodeproj|xcworkspace)/' | sed -E 's#(\.xcodeproj|\.xcworkspace)/.*#\1#' | sort -u | head -5); echo "${out:-(none)}"`
Archive entry points: !`out=""; test -f fastlane/Fastfile && out="$out fastlane"; grep -qE '^(testflight|archive|release-ios|upload)[a-z-]*:' Makefile 2>/dev/null && out="$out make"; s=$(ls scripts 2>/dev/null | grep -iE 'archive|testflight|upload' | head -3 | tr '\n' ' '); test -n "$s" && out="$out scripts: $s"; echo "${out:-(none)}"`
Xcode: !`out=$(xcodebuild -version 2>/dev/null | head -1); echo "${out:-(not installed)}"`

## Instructions

**The one rule: a build counts as sent only when App Store Connect shows it, and only the number the user asked to change was changed.** A great run uses the repository's own archive path, bumps the build number alone unless told to change the version, confirms the upload landed and finished processing, and reports the version, build number, processing state, and the testing group it joined. Open [examples/upload.md](examples/upload.md) before reporting and check it against [examples/rejected.md](examples/rejected.md).

### Process

1. Parse `$ARGUMENTS`: the scheme (default: the one the repository's archive path uses), `--version` to change the marketing version (without it, only the build number moves; seen: the user repeated "bump the build, not the version" across one session's uploads), `--group` for the TestFlight group, and `--submit` to also submit the build for external beta review. Refuse a dirty tree, because the archive must match a commit.
2. Use the repository's own path first: a `fastlane` lane, a `Makefile` target, or an archive script the repository ships, read end to end so you know whether it already bumps, uploads, or waits; only without one, build the path yourself in step 4. A path that archives but never uploads is a finding to fix in the report, not a step to repeat (seen: a make target that archived successfully and was assumed to upload).
3. Read the current numbers from the build settings (`agvtool what-version` and `agvtool what-marketing-version`, or `MARKETING_VERSION` and `CURRENT_PROJECT_VERSION` in `project.pbxproj` or the xcconfig that sets them), read the latest build App Store Connect already has for that version (`fastlane`'s `latest_testflight_build_number`, or the App Store Connect API's `GET /v1/builds?filter[app]=<app id>&filter[preReleaseVersion.version]=<version>&sort=-version&limit=1` with the machine's existing key; `altool --list-apps` lists apps, not builds), and set the new build number above both. Change the version only on `--version`. Commit the bump when the repository tracks these files, so the uploaded build maps to a commit.
4. Without a repository path: `xcodebuild -scheme <scheme> -configuration Release -destination 'generic/platform=iOS' -archivePath "$SCRATCH/<scheme>.xcarchive" archive`, then `xcodebuild -exportArchive -archivePath ... -exportOptionsPlist <plist> -exportPath "$SCRATCH/export"` with `method` `app-store-connect` and `destination` `upload`, so the export uploads; signing uses the account and profiles already configured on the machine, and a signing error is reported with the identity it wanted, never worked around by changing the team or bundle id.
5. Confirm the upload landed: the export or upload log names the delivery, then App Store Connect lists the build (`fastlane pilot builds`, or the App Store Connect API with the machine's existing key); poll its processing state under a bounded wait (about 30 minutes, a status line per check) until it is valid or failed. A build missing after the upload reported success is a failed upload, and the report says which step lost it.
6. Add the processed build to the requested internal group, or to the group the repository's path names, with "what to test" notes drawn from the commit subjects since the previous uploaded build; on `--submit`, submit it for external beta review.
7. Report the version, build number, commit, processing state, group, and anything in the repository's path that needed a manual step, so it can be fixed there.

### Rules

- Never change signing settings, the team, or the bundle identifier to make an archive pass.
- Never reuse a build number App Store Connect already has for the version.
- Credentials stay in the machine's keychain or the repository's configured key; none is printed or written to a file.
