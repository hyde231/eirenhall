# Item Schema Overview

This document summarizes the structure of the baseline item schema defined in
`schema/item_base.json`. The schema establishes a consistent envelope for all
knowledge items - documents, tasks, wiki entries, or other entities - so that downstream
services can rely on predictable metadata and capability contracts.

## Required Envelope Fields

All item payloads **must** include the following top-level members:

| Field | Type | Purpose |
| --- | --- | --- |
| `id` | string | Stable unique identifier that never reflows between realms. |
| `item_type` | string | Machine readable type discriminator (e.g. `document`, `task`, `wiki_entry`). |
| `title` | string | Human friendly title that appears in navigation and search results. |
| `realm` | object | Organizational context (GTD-style area/project path). |
| `sensitivity` | object | Item classification used for session-level filtering. |
| `capabilities` | object | Feature flags and hooks used by capability aware clients. |
| `fields` | object | Item specific field payloads keyed by schema field identifiers. |
| `metadata` | object | Namespaced metadata bag reserved for integrations. |
| `derived` | object | Calculated values that should not be user editable. |

The schema disallows undeclared top-level properties to keep the envelope
stable. Optional envelope members must be explicitly whitelisted in
`schema/item_base.json`.

Metadata namespace and capability naming follow the rules outlined in
[Naming Conventions](naming_conventions.md) and the governance practices in
[Metadata Governance](metadata_governance.md). Reusable field definitions live
in the [Field Library](field_library.md) and should be referenced rather than
duplicated in item schemas; link-related fields must follow the
[Linking & Backlink Specification](linking_and_backlinks.md).

Field payloads SHOULD reuse the cataloged composites. The base item schema now
accepts both singular and array forms of `std.object_ref`, enabling items to
point at related tasks, wiki entries, datasets, or other registry members without custom
ad hoc objects. Every item type MAY expose an optional `fields.notes` using the
standard rich-text field (`schema/fields/rich_text.json`) to capture ad-hoc comments,
migration breadcrumbs, or future schema candidates. Because notes reuse the rich-text
primitive, any embedded `kki://` URIs or wiki links participate in the canonical
linking/backlink pipeline without extra work.

## Levels & Session Filtering

This specification adopts a simplified security model focused on session-level
gating while keeping realms strictly organizational (GTD) rather than
authorization-bearing.

- Realms: represent areas/projects. The descriptor carries an `id` and a
  `path` of ancestor ids. Realms do not impose sensitivity floors.
- Sensitivity: each item declares a single classification used for filtering.
  Recommended ordered scale: `public < family < partner < personal < private < intimate`.
- Sessions: every interactive session declares a `max_level`. All reads, search
  results, and conversational surfaces MUST filter items where
  `item.level <= session.max_level`.

Implications for the envelope:
- `realm` remains the organizational locator for browsing, storage paths, and
  defaulting UX only.
- `sensitivity` is the item’s classification. Clients SHOULD default new items
  to the current session’s `max_level` and allow explicit upgrades. Downgrades
  require explicit confirmation and an audit event.

Compatibility notes:
- Existing schema artifacts include `realm.sensitivity_floor` and a
  `sensitivity` descriptor with an `inherited` flag. Under this model,
  `sensitivity_floor` MUST NOT be used and `inherited` SHOULD be treated as
  `false` by default. Schema updates will remove/deprecate these fields in a
  future change.

## Capability Hooks

The `capabilities` object gives client applications a consistent surface for
extending item behavior. Capabilities are arranged as namespaced keys to avoid
collisions and to support gradual rollout. Each capability entry is an object
with the following shape:

* `enabled`: boolean gate.
* `version`: semantic version string used by clients to select compatible
  contract shapes.
* `config`: arbitrary JSON data validated using capability-specific schemas.

The base schema only validates the envelope (`enabled` and `version`) while the
`config` payload is validated by capability-specific tooling. Custom capability
schemas can be referenced via `$ref` within `schema/fields` when tighter
validation is needed.

Clients must treat unknown capabilities as disabled and should not assume that a
capability being absent is equivalent to `enabled = false`; availability can
depend on item type or session level.
