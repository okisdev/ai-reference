# A run that clears the bar (illustrative)

This run clears the bar because the build number moved alone, above both the local value and App Store Connect's latest, and the build was seen in App Store Connect and processed before anything was reported. Names, numbers, and SHAs are invented; the shape is the bar.

````
Scheme Lantern (Lantern.xcodeproj), clean tree at 5d1e7a3. No fastlane; the Makefile has an `archive` target.
Read the Makefile: `archive` runs `xcodebuild archive` and stops. It never exports or uploads, so running it alone would not send anything. Using its archive step and adding the export with upload myself.
Numbers: local version 1.8.0 build 112; App Store Connect's latest for 1.8.0 is build 115. Version stays 1.8.0 (no --version). Build set to 116 with agvtool and committed as 9c40b2e (chore: bump build to 116).
make archive: ARCHIVE SUCCEEDED, Lantern.xcarchive built from 9c40b2e. Not sent yet.
xcodebuild -exportArchive with method app-store-connect and destination upload: upload log shows delivery 7f3b21aa accepted.
App Store Connect check 1 (0m): build 116 not listed yet.
App Store Connect check 2 (2m): build 116 listed, processing.
App Store Connect check 3 (6m): build 116 processing, 6m, still alive.
App Store Connect check 4 (11m): build 116 valid.
Added build 116 to internal group "Core Team". What to test, from the commit subjects since build 115: fix crash when opening an empty list; add pull to refresh on the home feed; update onboarding copy.
Report: Lantern 1.8.0 (116), commit 9c40b2e, processing valid, group Core Team. Gap in the repository's path: the Makefile `archive` target never exports or uploads; adding an `upload` target that runs the export step would let the next run use it as is.
````

Why it clears the bar:

- The Makefile was read end to end, so the report names that its target archives without uploading instead of assuming it sends.
- The version stayed 1.8.0 and only the build number moved, to 116, above both the local 112 and App Store Connect's 115.
- The export used `destination` `upload`, and the build was then seen in App Store Connect rather than trusting the upload log.
- Processing was polled under a bounded wait with a status line per check, until the build was valid.
- The group notes came from commit subjects since the previous uploaded build.
- The report names the version, build, commit, state, group, and the Makefile gap, so it can be fixed in the repository.
