# Internal consoles: access, members, secrets, settings

An internal console is gated at login, usually by an email domain, and everything below is about what happens after that gate.

## Visibility versus access

- Count the rows before building an editor: an access rule with one constant row (one domain may log in) gets a read-only line on the members page, never a CRUD surface.
- "We do not need access management" usually hides a second need: who may log in is settled, what each member may see is not. Ship the members page first (login method, second factor, sessions, last sign-in), and defer per-member visibility until a role model exists.
- Capabilities are a fixed code enum and roles bundle them; only the role assignment is data. A per-user per-permission matrix is the anti-pattern; it is named and rejected before it is built.
- Authorization lives at one data-layer choke point (every read and write names its capability); a route map in a proxy covers neither server actions nor route handlers. Navigation, tabs, and badges filtered by role are a courtesy, never the guard.
- A missing role row means the least privilege; the first owner row is bootstrapped by hand before the access release ships, or everyone locks out at deploy. The role command locks owner rows and refuses to demote the last owner, and a role change is an audit event.
- After a capability system lands, audit every existing read that returns names or lists under the lowest capability.

## Admin actions and self-serve

- An admin action on customers (approve, reject, revoke) goes into the console that is already gated to staff, never into the customer product behind a new permission layer.
- A self-serve action that belongs to the customer (link a device, rotate a key, connect an integration) goes into the product's own org settings behind the org's existing manage permission.
- A grant is modeled as rows in one generic table keyed by subject and kind; a new case is a seed row, not a migration. Pin down whether the product gates per user or per org before building the approval flow.
- A gate is concentrated at one call site; before shipping it, look for a second path that produces the same protected result without passing through it.

## Secrets

- Reveal-on-demand behind its own action, with its own audit event and a logging exclusion, is the shape for a staff-only console; reveal-once is public SaaS hygiene applied to the wrong boundary.
- The reveal policy decides the storage model (a digest only for reveal-once, a digest plus a sealed copy written together for reveal-on-demand); decide it before the form exists, and list and detail reads omit the secret either way.
- A self-built secrets manager inside the console fails the trust-boundary and bootstrapping test; the store is the organization's secrets manager, organized by ownership (shared, then one folder per deployment unit), never by repository or product name, and values are verified against the live system before they move.

## Settings surfaces

- A value earns a settings surface only when editing it changes real downstream behavior; a value whose semantics another app's code defines ships as a shared constant instead. A hot-path value (a rate limit) stays a static constant rather than a per-request read.
- Rank what to move into the console by cost and benefit: an existing table with no UI, then code registries and allow-lists, then policy numbers, then copy last; verify each hardcoded claim at its source line, and compare a hardcoded allow-list against production before removing it.
- Shapes: full list and detail with row actions for registries with a lifecycle; switches for capability bits; server-side pagination for an existing large table; a plain constants module and no UI for low-churn display parameters.
- A field the console can edit but another app's code writes is unfinished until the real write path is closed. Options a settings page offers are verified against the live table; an option that never occurs in production is a mismatch to resolve.
- Cross-app data: writes are single-direction and narrow (one row, one direction); bulk reads use a read-only schema mirror named and annotated identically in every consumer; a field the owning app should still interpret is read through that app's API. Exactly one repository runs a schema's migrations.
