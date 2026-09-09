# Observability dashboards

For surfaces owned by a telemetry tool (Axiom, Grafana, PostHog, Better Stack) rather than product code. The catalog and the question to form table still apply; these mechanics replace the inventory and implementation steps.

## Learn the surface before building

- Fetch an existing dashboard's definition to learn the schema (chart kinds, grid, panel fields) instead of guessing the format; the tool's own MCP or API is the surface, the browser is the fallback for what the API does not expose (creating datasets, deleting seeded samples).
- Probe what data exists: count by service, by source, by kind over the last hour and the last week; find the noise (build logs, health checks, a sample dataset the vendor seeded) before proposing anything.
- Run every query standalone and read back row counts and percentile values before wiring it into a panel; never ship a broken or empty panel.
- Prove a delete works on a disposable probe object before concluding a stuck delete means the target is vendor protected.
- Check a dataset's declared kind before assuming a trace or waterfall view renders; an ingest target must exist before a pipeline is pointed at it; structured bodies may land as one JSON string field that needs parsing; the same metric can be double counted across parent and child spans.

## Organize by system, not by dataset

- A dashboard answers "how is X doing" for a system or product, mixing datasets per panel when the tool allows it (verify that it does); a dataset-shaped set cannot answer that once X spans several datasets.
- Name a dashboard for the question or the system, never for the dataset; name datasets by source where the vendor integration fixes the name and by signal type where sources are heterogeneous.
- When merging dashboards, drop a panel whose answer is already on the page (a stat beside its own series, a trend beside a table that ranks the same thing).
- A panel whose conclusion is never acted on ("safe to drop") is an ownership gap, not a reason to keep re-displaying the finding.
- Shared surfaces carry English labels.

## Monitors and datasets

- A monitor is an alert rule over data already flowing; a dataset is new ingestion for signals that exist nowhere yet. Say which one a proposal is.
- Outside-in (uptime probes, heartbeats, a status page) and inside-out (logs, traces, derived health) are complementary fault domains; state both explicitly so they do not read as redundant.
- Before proposing a monitor for a process failure, ask whether the failure can be removed structurally (automate the missed human step); a monitor is often a stopgap for a fixable cause.
- Every threshold comes from a measured baseline window and is scoped to the narrowest metric that isolates the failure (one call kind's p95, not the blended p95); a monitor's logic is re-derived from the event schema (cancelled is not failed).
- Stage a schema-risking pipeline change (a new drain, a new exporter, a filter at the source) in a throwaway parallel dataset and diff the fields before cutting a live, dashboard-backed dataset over.
- Cap retention early; an unbounded default compounds silently. Re-verify a cost judgment against per-source usage before acting; the expensive source is often not the one assumed.
- Never copy one service's log or sampling config onto a sibling with a different signal source; a config tuned for a service with one meaningful log line mutes a static asset worker entirely.

## Batches and verification

- One dashboard per batch. After creation, fetch it back by id and diff its panel list against the grammar artifact; rerun every panel query standalone and read back row counts.
- Fire each monitor against a probe window before trusting its threshold; a notifier is verified by one delivered test message.
- Labels on shared surfaces are English; probe objects are deleted; the handoff names every dataset with zero dashboards left and every monitor whose baseline was guessed rather than measured.
