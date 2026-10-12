# Rejected report

A render check that reads fine and gets overturned, written for the same read-only review as `render-check.md`. Compare yours against it before reporting.

````
Started the dev server and opened http://localhost:3000/settings. It returns 200 and the page renders. Opened it with navigate_page, took a screenshot, and the Save button looks fine on mobile. To check the validation message I set the form to its error state from the console. The padding on the button was off, so I fixed it in SaveBar.tsx. Killed the servers with pkill -f next.
````

Why each part fails:

- `opened http://localhost:3000/settings` and `It returns 200`: a 200 proves liveness, not visual correctness, and the port was never read from the log; Next.js moves to 3001 when 3000 is busy, so this may be another app.
- `Opened it with navigate_page, took a screenshot`: the page was captured before hydration, the screenshot file was never read, and the loop's readiness poll and teardown were skipped (seen: browser checks in 82 sessions ran through raw browser tools without it).
- `looks fine on mobile`: no viewport named, no measured rect, and no merge base to compare, so it shows neither that the symptom existed nor that it is gone.
- `set the form to its error state from the console`: the state was injected instead of driven the way a user would; state inspection only confirms what was observed.
- `I fixed it in SaveBar.tsx`: the caller was read-only, so the finding goes back as a suggestion and no file changes (seen: a read-only caller's run was told to apply edits); the shared component was also never asserted on the other pages that render it.
- `pkill -f next`: kills by process name, including servers this check never started; only the PID recorded at startup may be killed, and `lsof` confirms the port is free.
- No `Not checked` line: dark mode and other engines are unstated, so the pass reads as complete.
