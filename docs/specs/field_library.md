# Field Library Specification

Defines the structure, semantics, and lifecycle of reusable field schemas stored
under `schema/fields`. Complements `item_base.json`, the naming conventions, and
the metadata/capability governance specs.

## Goals
- Establish a canonical catalogue of primitive and composite field types that
  item schemas can reference.
- Describe validation and typing constraints so schema authors know when to
  reuse an existing field vs. introduce a new one.
- Capture UI/rendering hints that downstream clients can use to present data
  consistently.
- Provide extension rules for adding new field definitions, ensuring
  compatibility with registries, importers, and validation tooling.

## Field Taxonomy
Fields fall into four categories. Each entry corresponds to a JSON Schema file
in `schema/fields`.

| Category | Field Schema | Purpose & Notes |
| --- | --- | --- |
| **Core Identifiers** | `identifier.json` | Canonical string identifier with length and pattern constraints. |
|  | `title.json` | Human-facing title; enforces min/max length. |
| **Descriptors** | `realm_descriptor.json` | Realm path, hierarchy, and sensitivity floor metadata. |
|  | `sensitivity_descriptor.json` | Classification + override metadata. |
|  | `user_reference.json` | Lightweight user handle (id + display name + optional email). |
|  | `geo_point.json` | Latitude/longitude (+ optional altitude) for geospatial tagging. |
|  | `object_reference.json` | Generic reference envelope for any registry object (type/id/uri/relationship metadata). |
| **Interaction & Content** | `rich_text.json` | Delta-style rich text payload. |
|  | `tag_list.json` | Ordered list of strings for tagging. |
|  | `timestamp.json` | ISO-8601 timestamp (UTC). |
|  | `measurement.json` | Numeric value paired with UCUM unit and optional uncertainty/timestamp. |
|  | `link.json` | Link object with title/url/kind aligned with the [Linking & Backlink Specification](linking_and_backlinks.md). |
|  | `checklist_item.json` | Itemized task entry with id/label/checked. |
|  | `capabilities.json` / `capability_entry.json` | Capability map + entry structure for item payloads. |
| **Derived & Aggregates** | `progress_summary.json` | Composite derived structure (total/completed/percent). |
| **Domain Composites** | `weather_observation.json` | Standardized weather observation payload using measurement, geo point, and object reference primitives. |
|  | `correspondence_party.json` | Party/contact descriptor for correspondence and conversation participants. |
|  | `correspondence_retention.json` | Retention/hold metadata applied to correspondence artifacts. |
|  | `correspondence_entry.json` | Normalized metadata envelope for letters, emails, and related documents. |
|  | `conversation_message.json` | Single timeline message with speaker metadata, body, and references. |
|  | `conversation_timeline.json` | Ordered collection of conversation messages with optional summary. |
|  | `project_summary.json` | Project status, health, and timeline descriptor with progress rollup. |

Future categories may introduce measurement fields, media descriptors, or
relation definitions. Additions must follow the rules below.

## Schema Requirements
All field definitions must:

1. Declare a unique `$id` anchored under `https://kki.example.com/schema/fields/`.
2. Specify `$schema` (Draft-07 currently).
3. Provide a `title` (Title Case) and, when helpful, a `description` field.
4. Use `additionalProperties: false` unless extensibility is intentional.
5. Reference other field schemas via relative paths (`./identifier.json`) to
   promote reuse.
6. Follow naming rules from `docs/specs/naming_conventions.md` (filenames,
   property names, enums).

When a field requires enums or constant lists, document their semantics and
required migration strategy in comments or the accompanying spec.

## Validation Semantics
- **Lengths & Patterns:** Numeric fields use `minimum`/`maximum`. Strings specify
  `minLength`, `maxLength`, and `pattern` when needed.
- **Timestamps:** Enforce `format: "date-time"` and ensure values are stored in
  UTC. Derived/localized variants should be separate fields if required.
- **Lists:** Use `type: "array"` with `items` referencing another field schema.
  Add `minItems`/`maxItems` and `uniqueItems` as appropriate.
- **Optional vs. Required:** Express required keys using the `required` array in
  JSON Schema. Optional keys either omit `required` entries or use defaults in
  consuming schemas.
- **Nullability:** Express nullable fields using `type: ["string", "null"]` etc.
  Avoid implicit null acceptance.

## UI & Rendering Hints
Field schemas may include the following optional metadata to guide clients:

- `ui:component`: Suggested input type (`text`, `textarea`, `rich_text_editor`,
  `tag_select`, etc.).
- `ui:format`: Display formatting instructions (`currency`, `percentage`,
  `duration`).
- `ui:ordering`: Default column or form ordering when multiple fields render.

UI hints live under a namespaced `x-ui` object to avoid clashing with standard
JSON Schema keywords. Example:

```json
{
  "title": "Progress Summary",
  "type": "object",
  "x-ui": {
    "component": "progress_bar",
    "read_only": true
  }
}
```

Tooling should ignore unknown `x-` prefixed members by default.

## Extension Workflow
1. **Proposal:** Document motivation, data shape, and rendering expectations in
   an ADR or issue referencing this spec.
2. **Design:** Draft the JSON Schema and, if necessary, a companion doc under
   `docs/specs/fields/<field_name>.md` describing context and usage examples.
3. **Validation:** Update unit tests or add new ones to ensure fixtures using the
   field validate correctly. Run `scripts/run_poc.py` or other schema validation
   tooling to confirm the new field integrates with the registry.
4. **Registration:** Ensure the schema loader captures the new file (no manifest
   updates needed if it lives under `schema/fields`). Update type or capability
   manifests that consume the field.
5. **Documentation:** Reflect the new field in this spec’s taxonomy table and in
   relevant user-facing docs (data architecture, UX, etc.).

## Reuse Guidelines
- Prefer extending existing composite schemas by composition rather than
  duplicating similar structures. For example, a `subtask_summary` should reuse
  `progress_summary.json` instead of creating a near-identical shape.
- When custom metadata is required, consider namespacing inside the field
  object (`{ value, annotations: [] }`) with clear validation.
- Avoid embedding capability-specific configuration in general-purpose fields;
  keep capability metadata under `metadata.cap.*`.

## Deprecation Strategy
- Mark deprecated schemas with an `x-status: deprecated` field and document the
  replacement. Leave the file in place until all references migrate.
- Update tests and fixtures to avoid creating new items with deprecated fields.
- Communicate the deprecation in release notes and the field taxonomy table.

By formalizing the field library in this way, schema authors and plugin
developers share a consistent vocabulary, reducing duplication and simplifying
validation across the PoC and future milestone work.
