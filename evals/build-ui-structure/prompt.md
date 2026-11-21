---
description: build-ui challenges the structure of a redesign before styling it, merging pages that answer the same question and moving a command to the page that owns it, and asks for approval before deleting anything a person can reach.
tags: [quality, build-ui]
runs: 2
max_turns: 10
timeout_seconds: 300
allowed_tools: [Skill, Read, Bash]
---

Use the build-ui skill for this ask. Everything you need is below; do not run commands and do not write code, tell me your plan.

Ask: the `fleet-console` web app looks messy and nothing lines up; make it look clean and consistent.

Its `DESIGN.md` exists and is up to date; assume you have read it. The pages, from the code:
- Overview: `SpendByRegion` (calls `api.costByRegion()`), `BusiestVehicles` (calls `api.topVehicles()`), `AlertsPanel`.
- Analytics: `RegionCostChart` (calls `api.costByRegion()`), `TopVehicles` (calls `api.topVehicles()`), `WeeklyTrend`.
- Reports: `CostTable` (calls `api.costByRegion()`), `ExportButton`.
- Vehicles, Trips, Settings: one list or form each.
- The shared `TopBar` renders `TrackingToggle` on every page; it calls `trips.setPaused`.
