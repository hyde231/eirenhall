# Derived Value Conventions

Derived values capture machine computed attributes that help clients render or
summarize items without re-running expensive computations. They live under the
`derived` object defined in `schema/item_base.json` and follow the conventions
below.

## Naming

Refer to the [Naming Conventions](naming_conventions.md) guide for the full
set of rules. In short:

* Use snake_case keys describing the computed artifact (`word_count`,
  `completion_ratio`, `last_activity_at`).
* Prefix boolean predicates with `is_` or `has_` (e.g. `is_overdue`, `has_body`).
* When a derived value emits a reusable composite schema, reuse that schema
  name directly (e.g. `progress_summary`).
* Nested derived collections adopt plural nouns (`subtask_rollups`).

## Typing

Each derived field must reference a schema in `schema/fields` to ensure it is
well typed. Primitive derived values (numbers, strings, booleans, timestamps)
can reuse the same field definitions as user editable data, while composite
values should point to dedicated composite field schemas (e.g.
`schema/fields/progress_summary.json`).

## Change Responsibility

Derived values are exclusively owned by the server or background processors.
Clients **must not** attempt to persist user supplied overrides. When derived
values depend on user modifiable state, the writers should recompute the derived
state during the same transaction to avoid race conditions.

## Reserved Metadata Namespaces

The `metadata` bag under each item is partitioned to reduce conflicts between
integrations. The following namespaces are reserved:

| Namespace | Description |
| --- | --- |
| `sys.*` | Internal system metadata. Clients should not rely on specific keys. |
| `cap.<capability_key>.<attribute>` | Capability-managed metadata tied to a specific capability and attribute (e.g. `cap.editor.collab.autosave`). |
| `ext.<vendor_slug>.<attribute>` | Third-party integration data, where `<vendor_slug>` matches the integration slug (e.g. `ext.crm.record_id`). |
| `tmp.*` | Short lived data with automatic expiration (e.g. preview caches). |

Integrations adding new namespaces must register a unique prefix to avoid
collisions. Namespaces are case insensitive and should be treated as reserved
regardless of capitalization. Keys inside a namespace may use nested objects but
must remain within the namespace boundary (e.g. `ext.crm.stage`).
