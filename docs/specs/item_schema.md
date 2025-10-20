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
| `realm` | object | Location descriptor tracking hierarchical containment. |
| `sensitivity` | object | Classification of the item itself after realm inheritance is applied. |
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
ad hoc objects.

## Realm & Sensitivity Inheritance

Realms provide hierarchical context and drive default sensitivity. The schema
encodes two cooperating structures:

* `realm` captures the item's position.
  * `id`: canonical realm identifier.
  * `path`: ordered list of ancestor realm ids from root to the item's realm.
  * `sensitivity_floor`: optional classification imposed by the realm.
* `sensitivity` reflects the item's final classification.
  * `classification`: enum value such as `public`, `internal`, `confidential`,
    or `secret`.
  * `inherited`: boolean indicating whether the value is purely inherited from
    the realm (`true`) or the item (`false`).
  * `override_reason`: optional short explanation required when
    `inherited = false` and the classification is stricter than the realm floor.

When consumers resolve an item's effective sensitivity they must:

1. Start with the realm's `sensitivity_floor` (if present) and treat it as the
   minimum allowable classification.
2. Apply the item's `sensitivity.classification`, ensuring it is not weaker than
   the realm floor.
3. Use `sensitivity.inherited` to differentiate policy driven items from user
   managed overrides.

The schema enforces these rules by constraining the sensitivity enum choices and
requiring an `override_reason` whenever inheritance is broken.

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
capability being absent is equivalent to `enabled = false`; the capability may
not be available in the current realm or sensitivity band.
