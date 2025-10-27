# Naming Conventions

This guide aligns the terminology used across primitives, item types, schema
files, field identifiers, derived values, and capability metadata. Follow these
conventions when introducing new artifacts or renaming existing ones.

## Item Types & Manifests
- **Type keys** are singular nouns written in `lower_snake_case` (e.g. `document`,
  `reading_list`). Avoid plurals and acronyms; expand them into readable words.
- **Manifest filenames** mirror the type key: `schema/types/<type_key>.yaml`.
- **Derived definition filenames** also mirror the type key:
  `schema/derived/<type_key>.yaml`.
- **Capability entries** inside each manifest list verbs or verb phrases in
  lowercase (e.g. `read`, `write`, `manage`, `configure`). Prefixes are
  discouraged—use the shortest actionable word that communicates the affordance.

## Primitive Field Schemas
- Store reusable field definitions under `schema/fields` using filenames that
  match the canonical field identifier in `lower_snake_case`
  (e.g. `realm_descriptor.json`, `progress_summary.json`).
- Titles inside the schema documents should be human-readable Title Case.
- When a primitive has multiple variations, include a qualifier suffix such as
  `_summary`, `_descriptor`, or `_entry` to clarify its intent.
- See [Field Library](field_library.md) for semantic and validation guidance
  when choosing or extending field definitions.

## Field Identifiers
- Keys inside the `fields` object of an item use `lower_snake_case`.
  - Singular nouns represent single-value fields (`status`, `summary`).
  - Plural nouns represent collections (`assignees`, `links`, `tags`).
- Boolean fields prefer an `is_` or `has_` prefix (e.g. `is_pinned`, `has_body`).
  Avoid legacy flags like `inherited` in sensitivity; the session-level model
  does not use inheritance for sensitivity.
- Refer to nested properties using dot notation with snake_case segments
  (`fields.body.ops`, `metadata.sys.owner_team`).

## Derived Metrics & Stored Values
- Derived metric keys defined under `schema/derived` use `lower_snake_case`.
- Computed values stored under an item's `derived` object reuse the metric key
  when a one-to-one mapping exists (e.g. `completion_ratio`).
- Composite derived outputs that rely on a reusable field schema adopt that
  schema name as the key (e.g. `progress_summary` for the
  `progress_summary.json` shape).
- Boolean derived values follow the same `is_` / `has_` prefix guidance.

## Capability Identifiers & Metadata Namespaces
- Capability identifiers use dot-separated namespaces in lowercase
  (`editor.collab`, `tasks.board`). The segment before the dot names the
  capability family; the segment after the dot names the feature. Add
  subsequent segments only when a capability has sub-modes (see
  [Capability Contracts](capability_contracts.md) for contract details).
- Capability metadata stored in `metadata` mirrors the capability identifier and
  appends a specific attribute: `cap.<capability_key>.<attribute>`
  (e.g. `cap.editor.collab.autosave`). See
  [Metadata Governance](metadata_governance.md) for lifecycle policies.
- System metadata uses `sys.<category>` (e.g. `sys.owner_team`),
  temporary caches use `tmp.<category>`, and integrations use
  `ext.<vendor_slug>.<attribute>` where `vendor_slug` is lowercase with dashes or
  underscores.

## Identifiers & External References
- Item identifiers adopt the `<type_key>_<unique_suffix>` pattern
  (e.g. `document_20250101`, `task_abcd1234`).
- Checklist items, attachments, and other embedded records follow the same rule
  with a qualifier that reflects their container (`chk_<suffix>`, `att_<suffix>`).
- URLs and external keys remain lowercase unless the integration requires a
  specific format. Mirror the integration’s casing only when necessary.

## Applying the Conventions
When updating legacy names, rename the schema file (if required), adjust every
reference (tests, fixtures, docs, code), and regenerate manifests as needed.
Commit the renames atomically so downstream tooling does not observe mixed
conventions. Consult this document before introducing any new schema or item
types to avoid drift.
