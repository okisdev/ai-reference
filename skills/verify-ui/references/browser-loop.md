# Browser verification loop

Exact commands and shapes for the server lifecycle, the browser tool map, feedback parsing, and assertions referenced from SKILL.md steps 3 onward. Prove readiness and hydration before asserting; never guess a port or a selector.

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

## Browser tools

Every step names an operation, and the session's browser tool performs it. The families seen so far map like this; another tool (Playwright MCP, a desktop app's built-in browser, Codex's browser) maps the same operations by name. An operation the tool lacks is a narrower check the report names, never a reason to install another tool.

| Operation | Chrome DevTools MCP | Claude in Chrome | Gode site tools |
| --- | --- | --- | --- |
| List open tabs | `list_pages` | `tabs_context_mcp` | `list_sites` |
| Open a page | `new_page`, `navigate_page` | `tabs_create_mcp`, `navigate` | `open_site` |
| Viewport and touch | `emulate` with `viewport: "390x844x3,mobile,touch"` | `resize_window`, the window size only | `emulate_site` with `viewport`, `mobile`, and `touch` |
| Color scheme | `emulate` with `colorScheme` | none; switch the app's own theme control | `emulate_site` with `colorScheme` |
| Script | `evaluate_script`, a function | `javascript_tool`, an expression with top-level `await` | `run_in_site`, an expression or a function body with `return` |
| Screenshot | `take_screenshot`, inline unless `filePath` is set | `computer` `screenshot`, with `save_to_disk` for a file | `capture_site`, inline (`full_page`, `target`) |
| Page snapshot | `take_snapshot` | `read_page`, `find` | `read_site` |
| Click and type | `click`, `type_text`, `press_key` | `computer` `left_click`, `type`, `key` | `act_on_site` `click`, `type`, `press` |
| Console and network | `list_console_messages`, `list_network_requests` | `read_console_messages`, `read_network_requests` | `read_site` with `logs`, `inspect_site` |
| Close | `close_page` | `tabs_close_mcp` | `close_site` |

Traps each family has shown:

- Chrome DevTools MCP refuses a `take_screenshot` `filePath` outside its workspace roots ("not within any of the configured workspace roots"); omit the path, or write inside the workspace.
- Claude in Chrome with several connected browsers and none chosen fails every call until the person picks one: list them with `list_connected_browsers` and ask by display name. Its tools act only on tabs in the session's group, and closing a tab can dissolve the group, so re-read `tabs_context_mcp` after a close.
- Gode's tools act only on tabs of the agent's group, so "is not in your group" means re-list with `list_sites`; an `act_on_site` wait is capped at 10 seconds; a script on a site that is not a local address waits for the person's approval.

## Unattended runs

A run another agent dispatched often has a sandbox that cannot bind a port (`listen EPERM`) or browser calls that need an approval nobody is there to give. A refused curl against a port `lsof` shows listening does not prove the server is down: a page snapshot of a tab already open on it is the readiness check. When opening, clicking, or scripting is refused, use the read-only calls on an open tab and report every state that needed a refused call as not checked; with no open tab either, start no server, and hand the browser pass back to the dispatcher with the states it must cover (seen: 24 dispatched runs loaded this skill and none produced a screenshot, most stopped by `listen EPERM`).

## Feedback ingestion

A pasted DOM fragment has the shape `[<tag class="..."> in ComponentA in ComponentB (at /abs/path/file.tsx:LINE:COL)]`. The `(at ...)` pair is the edit target: open that exact file at that line rather than searching for the component by name.

Class strings inside the fragment are Tailwind output, not stable selectors. Prefer data attributes, ids, or role and text queries when writing assertions.

## Assertion shape

Element handles and coordinates go stale on navigation and reflow: re-query after every navigation, and click by coordinates only when a screenshot taken immediately before supplied them.

After an action, assert on the target's own state (its label, value, or checked state) read back from the page; a success message proves that some action ran, not that it hit the control you meant (seen: a coordinate click after a failed named click changed the key beside the one asked for while the app reported "saved successfully").

A value set directly (a `fill` action) can leave a React-controlled field's state empty, which shows as a submit that stays disabled; click the field and type into it instead, because typing fires the input events React listens to.

A hover-only state (a tooltip, a popover) may not survive the next screenshot call, which can move the pointer; assert it from the DOM right after the hover and report it as DOM-verified rather than seen.

A console error belongs to the change only after an untouched page that shipped before it is checked the same way; the same error there makes it pre-existing.

Wait for hydration inside the same script call that queries the node. The body returns plain data, because some tools serialize a `DOMRect` as `{}` unless it goes through `toJSON()`:
```js
await new Promise(r => setTimeout(r, 1500));
const n = document.querySelector('<sel>');
return n ? { found: true, rect: n.getBoundingClientRect().toJSON(), text: n.textContent } : { found: false };
```
Pass it in the form the tool takes: `async () => { <body> }` for Chrome DevTools, the body as it is for Gode, and `await (async () => { <body> })()` for Claude in Chrome.

## Viewport

| Context | Size |
| --- | --- |
| Desktop (default) | 1440x900 |
| Mobile (`--mobile` or a phone screenshot as reference) | 390x844, mobile and touch |

Match the medium the feedback arrived in; a phone screenshot pasted as the reference means the mobile row even without `--mobile`. A tool that can only resize its window checks the width, not a phone: report it as a window width, not device emulation.

## Evidence

Take a screenshot and look at it: Read the file when the tool saves one, and look at the image when it comes back inline; a screenshot nobody looked at is not evidence. Compare it against the pasted reference image when one exists. For structure, labels, and focus order, the tool's page snapshot (an accessibility tree or page view) is first-class evidence beside the screenshot and often the cheaper assertion.

## Teardown

Close the tabs or pages the run opened with the tool's close operation, then stop the server this skill started:
```
kill "$PID"
lsof -nP -iTCP:<port> -sTCP:LISTEN
```
The `lsof` call after the kill must return nothing; an empty result confirms the port is free. Never touch a PID other than the one recorded at start.
