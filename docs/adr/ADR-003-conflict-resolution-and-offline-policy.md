# ADR-003: Conflict resolution & offline policy

- Status: Accepted
- Date: 2025-10-21
- Deciders: Eirenhall core maintainers
- Related work: docs/requirements/05_functional/README.md (FR-015, FR-027), docs/requirements/14_acceptance/README.md, docs/specs/capture_storage_blueprint.md

## Context

The platform must function across multiple devices and offline conditions.
Requirements call for offline archiving, tiered caches, and conflict-aware realm
operations, yet we lacked a documented resolution strategy. Without a clear
model, developers could implement incompatible sync logic, leading to lost data
or ambiguous merges when offline edits are reconciled.

## Decision

We adopt a deterministic, human-centred sync model:

1. **Authoritative record:** The canonical state for metadata and schemas lives
   in Git; item payloads are synchronised via manifests stored in the primary
   object store. Offline caches treat manifests as read-only until sync.
2. **Change capture:** Every mutation produces an append-only journal entry with
   `item_id`, `patch`, `author`, `timestamp`, and `persona`. Journals replicate
   alongside manifests.
3. **Conflict detection:** When syncing, we apply journal entries in timestamp
   order. If two patches touch overlapping JSON Pointer paths, we flag a
   conflict and queue the item for human resolution.
4. **Resolution semantics:**
   - Metadata with explicit priorities (realm policy overrides, retention flags)
     prefers the higher-sensitivity source.
   - Checklist-style data merges union unique entries keyed by `id`.
   - Rich-text or free-form fields fall back to manual review (generate diff).
5. **Merge tooling:** The sync engine produces a dry-run diff summarising merges
   and conflicts. Operators must approve the diff before committing changes.
6. **Cache freshness:** Hot cache (`/cache/primary`) publishes freshness markers
   per realm with `last_synced_at` timestamps. Clients treat data as stale once
   it exceeds the configured SLA (default 15 minutes for realm actives, 24 hours
   for cold realms).

Partial replication rules:

- Cache selection uses realm + recency + favorites. Operators define policies in
  `config/replication_policies.yaml` (to be added separately).
- Large binaries marked `retain_indefinitely` remain in hot cache until manually
  evicted, regardless of recency.

## Consequences

Positive:

- Deterministic rules keep sync tooling predictable and auditable.
- Human-in-the-loop conflict handling prevents silent data drops.
- Freshness markers give UX concrete values for “up to date” indicators.

Trade-offs:

- Manual conflict review slows down high-churn workflows; we accept this to
  preserve correctness.
- Journal replay requires additional storage and maintenance scripts.

Follow-up work:

- Implement journal writer/reader APIs and conflict detection helpers.
- Extend acceptance tests to cover offline edit scenarios per FR-015/FR-027.
