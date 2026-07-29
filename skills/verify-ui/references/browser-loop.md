# Browser verification loop

Exact commands and shapes for the server lifecycle, feedback parsing, and assertions referenced from SKILL.md steps 3 onward. Prove readiness and hydration before asserting; never guess a port or a selector.

## Server lifecycle

Detect the dev script and framework marker from the Context probes; both decide the start command and the stale lock to clear.

Stale lock cleanup, run before starting a new server:

| Framework | Cleanup |
| --- | --- |
| Next.js | `rm -rf .next/dev` |
| Vite | none needed |

Start command shape, run from the repository root:
```
nohup <pm> dev > "$SCRATCH/dev.log" 2>&1 &
echo $!
```
Record the printed PID; it is the only PID this skill may ever kill.

Readiness poll against the expected port:
```
curl -sf --retry 15 --retry-connrefused --retry-delay 1 http://localhost:<port> >/dev/null
```

The retry budget above is the whole wait (about 15 seconds; raise it only for known-slow apps, never past 90 seconds). If it expires, the server did not come up: capture `tail -40 "$SCRATCH/dev.log"`, kill the recorded PID, and report the failure with the log tail rather than polling on.

Port drift detection: grep the log for the printed local URL and use that port instead of the expected one. Next.js prints a line shaped like `Port 3000 is in use, using 3001 instead` when the default port is taken.

## Feedback ingestion

A pasted DOM fragment has the shape `[<tag class="..."> in ComponentA in ComponentB (at /abs/path/file.tsx:LINE:COL)]`. The `(at ...)` pair is the edit target: open that exact file at that line rather than searching for the component by name.

Class strings inside the fragment are Tailwind output, not stable selectors. Prefer data attributes, ids, or role and text queries when writing assertions.

## Assertion shape

Wait for hydration inside the same `evaluate_script` call that queries the node:
```js
() => new Promise(r => setTimeout(r, 1500)).then(() => {
  const n = document.querySelector('<sel>');
  return n ? { found: true, rect: n.getBoundingClientRect(), text: n.textContent } : { found: false };
})
```

## Viewport

| Context | Size | Call |
| --- | --- | --- |
| Desktop (default) | 1440x900 | `resize_page` |
| Mobile (`--mobile` or a phone screenshot as reference) | 390x844 | `emulate` |

Match the medium the feedback arrived in; a phone screenshot pasted as the reference means the mobile row even without `--mobile`.

## Evidence

Call `take_screenshot`, then Read the resulting file; a screenshot that is never read is not evidence. Compare it against the pasted reference image when one exists.

## Teardown

```
kill "$PID"
lsof -nP -iTCP:<port> -sTCP:LISTEN
```
The `lsof` call after the kill must return nothing; an empty result confirms the port is free. Never touch a PID other than the one recorded at start.
