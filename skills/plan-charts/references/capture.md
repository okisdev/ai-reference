# When the data does not exist

A question with no source is a capture design, not a chart. Design it before the catalog row; only then does it earn tier C.

## The standards test

- Per field or channel, one criterion: does an upstream-implemented standard shape already exist (a semantic convention, a wire format, an id format)? If yes, take its names and semantics; if no, keep the product's own.
- Separate what the standard says, what the system accepts, what it stores, and what it renders into distinct rows before judging compliance; the gaps live in different layers.
- Gate the judgment on real production fill rates read-only (which optional fields are ever non-empty, what the free-form bag holds); a spec comparison alone decides nothing.
- Deliver the design as adopt, keep, and do not adopt with a reason each, a field mapping table, an interface contract, and waves; the first wave fixes the current channel's holes and is worth shipping even when the rest is deferred.

## User-supplied and unknown data

- Unknown keys land in an attributes bag with a length cap, never rejected and never silently dropped; the bag is the standard answer to data users put in the request, not a bespoke hook.
- Rendering is a key/value ledger, never a raw JSON block; known keys become facets backed by an index or a reserved key list; an external id becomes a configurable link template to the customer's own backend; a facet that would scan the base table gets its column in the rollup.
- A field the system validates and then discards is a defect; every accepted field has a column or the bag.

## Backward compatibility

- Public surfaces stay append-only: every shape today's clients send keeps working, and new fields are optional.
- An old field name stays accepted on write and returned on read as an alias of the new one; stored rows migrate once so the dashboard renders one shape.
- Two sources of the same record (a client report and a server span) merge by explicit per-field precedence, keyed on the standard id.
- Compatibility is proven by golden payloads built from the current client's real types, so client and server ship on their own schedules; fixtures for a new wire format are recorded from a real client, never synthesized.

## Synthetic and demo data

- Demo and seeded data fills new columns forward from the change, is labelled as example, and is never backfilled into history; a view whose demo cannot reach back far enough says so.
