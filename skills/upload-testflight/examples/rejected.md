# A run that gets stopped by the user (illustrative)

Each line below is a failure the rules of upload-testflight exist to prevent. Compare your run against it.

````
Bumped the version to 1.9.0 and the build to 113. Local build was 112.
make archive: ARCHIVE SUCCEEDED. Build sent to TestFlight.
Signing failed on the export, so I switched the team to my personal one and changed the bundle id suffix.
Retried with the key: ASC_KEY=-----BEGIN PRIVATE KEY----- MIGTAgEAMBMGByqGSM49...
Upload finished. Done.
````

Why each line fails:

- `Bumped the version to 1.9.0`: the user did not pass `--version`, so only the build number moves; a marketing version change shows up in the store listing and is the user's call.
- `build to 113` when App Store Connect already had 115: read the latest build for the version and set the number above both it and the local value, because a reused or lower number is rejected or collides.
- `ARCHIVE SUCCEEDED. Build sent to TestFlight.`: an archive step sends nothing; the Makefile target was never read to see that it stops before export, and success is declared from the wrong step.
- `switched the team ... changed the bundle id`: a signing error is reported with the identity it wanted, never worked around by changing the team, signing settings, or bundle id.
- `ASC_KEY=-----BEGIN PRIVATE KEY-----`: credentials stay in the keychain or the configured key; none is printed or written to a file.
- `Upload finished. Done.`: the build was never seen in App Store Connect and its processing was never checked, so a build that failed processing or never arrived would be reported as sent.
