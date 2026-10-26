# A render check that clears the bar (illustrative)

The bar for a verification report: each claim sits beside the evidence that decides it, the browser tool, URL, port, and viewport are the ones measured, a fix claim is shown on both sides, every page that renders the shared component is re-asserted, and a read-only caller gets the finding back without an edit. The repository, PR, and numbers are invented; the shape is the bar.

---

**Caller**: verify-pr, read-only, reviewing PR #212 `fix(settings): keep the save button visible on phones`. Claim under test: the Save button is no longer clipped at 390x844. Pasted fragment: `[<button class="btn-primary"> in SaveBar in SettingsForm (at src/settings/SaveBar.tsx:41:6)]`.

**Setup.** `AGENTS.md` leaves visual review to the agent, so the loop ran. The ports probe showed something on 3000 whose page title is another app's, so I cleared `.next/dev` and started `pnpm dev` from the review worktree (PID 48213, log in the scratch directory). The log printed `Port 3000 is in use, using 3001 instead`, so every URL below is `http://localhost:3001`. `curl --retry 15 --retry-connrefused` returned 200 after 4 s. The session exposed Chrome DevTools MCP and Claude in Chrome; DevTools ran the loop because it emulates a phone viewport and a color scheme, which Claude in Chrome's window resize cannot. Each assertion waited 1.5 s for hydration inside the same script call. The merge base was rendered first, then the head, in the same worktree with the same URL, viewport, and steps.

| Claim | Evidence | Result |
|-------|----------|--------|
| Base clips Save at 390x844 | `/settings` emulated at 390x844 (mobile, touch); Save rect `left 336, right 432` against a 390 wide viewport; screenshot looked at: the right 42 px of the button is cut off | reproduced |
| Head fits Save at 390x844 | same URL, viewport, and steps; rect `left 278, right 374`; screenshot looked at: label and border intact | fixed on `/settings` |
| Head leaves desktop unchanged | emulated at 1440x900; rect `left 1180, right 1276` on both commits | unchanged |
| Every page that renders `SaveBar` fits at 390x844 | `/team`: `right 374`; `/billing`: `right 432` | `/billing` still clips |

**Finding.** The PR fixes `/settings` and misses `/billing`: `src/billing/BillingForm.tsx:77` passes `summaryClassName="min-w-[320px]"` to the same `SaveBar`, which overrides the `min-w-0` default the PR sets on `Summary` (`SaveBar.tsx:40`). Suggested change, not applied because the caller is read-only: drop the override at `BillingForm.tsx:77` or move the width into a prop.

**Teardown.** Closed the two pages the run opened and killed PID 48213 only; `lsof -nP -iTCP:3001 -sTCP:LISTEN` printed nothing. The app on 3000 is not this skill's server and was left running.

**States the change touches.** Viewports: 390x844 and 1440x900 checked. Theme: light checked; dark not checked, because the review build pins the light theme and ignores the emulated dark color scheme. Empty and loading: not applicable, `SaveBar` renders only with a loaded form. Error: the save failure banner renders inside `SaveBar` and was not checked, since producing it needs a failing API the read-only caller cannot arrange. Flags: none gate `SaveBar`.

**Not checked.** Dark mode, the save error state, a keyboard focus pass, and engines other than Chrome's emulation.
