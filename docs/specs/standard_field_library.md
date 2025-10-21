# Standard Field Library Specification

## Purpose and Scope
This specification defines the canonical field library for KKI items. It
extends the core item schema by enumerating the primitive fields the platform
must support, outlining compositional and derived field patterns, and defining
validation, localization, and governance expectations. The library is intended
for use across all capability surfaces (viewing, workflow, scheduling,
annotation) and ingestion pipelines described in the product requirements and
roadmap. All schema definitions derived from this specification MUST live under
`schema/fields/` and conform to JSON Schema Draft 2020-12.

## Design Principles
1. **Clarity and discoverability** – Field names, descriptions, and metadata
   must allow registry consumers to understand intent without reading
   implementation code.
2. **Interoperability** – Field structures align with relevant external
   standards (ISO 8601 dates, RFC 3339 timestamps, ISO 4217 currency codes,
   BCP 47 language tags) so that capture and export tooling can interoperate.
3. **Extensibility** – The library supports composition (embedding primitives
   inside higher-order types) and future capability extensions without schema
   rewrites.
4. **Governance and provenance** – Each field declares ownership, update
   semantics, and derivation rules to support lifecycle controls and derived
   value tracking.

## Field Classification
Fields fall into three categories:

- **Primitive fields** – atomic values with straightforward validation rules.
- **Composite fields** – aggregates of primitives that represent a single
  conceptual datum (e.g., address, money).
- **Derived fields** – values computed from other fields or external signals,
  defined with evaluator metadata and provenance requirements per the derived
  value framework.

### Metadata Envelope
Every field definition MUST include a metadata envelope that is consistent
across primitives, composites, and derived values:

| Property            | Description                                                                                     |
|---------------------|-------------------------------------------------------------------------------------------------|
| `id`                | Machine-readable identifier, namespaced by capability (e.g., `std.title`, `std.progress`).      |
| `name`              | Human-readable label in platform default locale.                                               |
| `description`       | Concise explanation of the field intent and usage.                                             |
| `fieldType`         | One of `primitive`, `composite`, `derived`.                                                     |
| `dataType`          | Primitive JSON type (`string`, `number`, `integer`, `boolean`, `object`, `array`).              |
| `version`           | Semantic version of the field definition.                                                       |
| `owner`             | Registry owner or team responsible for stewardship.                                            |
| `capabilities`      | List of capability hooks that expose or consume the field (Viewable, Workflown, etc.).          |
| `sensitivity`       | Sensitivity classification (e.g., `public`, `restricted`, `secret`) per sensitivity descriptor. |
| `constraints`       | Validation rules (regex, ranges, enumerations).                                                 |
| `localization`      | Localization policy (translatable content, locale-specific formatting rules).                  |
| `example`           | Canonical example for documentation and testing.                                               |
| `provenance`        | For derived fields, describes the source fields, evaluators, and refresh cadence.              |

### Primitive Field Catalog
The primitives below form the foundation of the standard library. Each entry
includes the canonical JSON Schema fragment and key validation rules.

1. **Identifier** (`std.identifier`)
   - Type: `string`
   - Format: UUID v4 (`^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-4[0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$`)
   - Use cases: Item identity, attachment manifests, evaluator IDs.

2. **Short Text** (`std.short_text`)
   - Type: `string`
   - Max length: 256 characters
   - Use cases: Titles, labels, display names.

3. **Rich Text** (`std.rich_text`)
   - Type: `object`
   - Structure: Portable text array with content blocks, annotations, and marks.
   - Use cases: Descriptions, narrative content, annotations.

4. **Boolean** (`std.boolean`)
   - Type: `boolean`
   - Use cases: Flags, toggles, workflow gates.

5. **Integer** (`std.integer`)
   - Type: `integer`
   - Range: 64-bit signed (`-9,223,372,036,854,775,808` to `9,223,372,036,854,775,807`).
   - Use cases: Counts, ordinal positions, version numbers.

6. **Decimal** (`std.decimal`)
   - Type: `string`
   - Format: decimal string complying with IEEE 754 decimal128 representation.
   - Use cases: Precise measurements, currency base units, ratios.

7. **Percentage** (`std.percentage`)
   - Type: `number`
   - Range: `0.0` to `1.0`
   - Use cases: Completion percentages, confidence scores.

8. **ISO Date** (`std.date`)
   - Type: `string`
   - Format: `date` per RFC 3339 (YYYY-MM-DD)
   - Use cases: Due dates, effective dates, audit dates.

9. **ISO Time** (`std.time`)
   - Type: `string`
   - Format: `time` with timezone offset or `Z` (HH:MM:SS.sssZ)
   - Use cases: Event start times, time-of-day thresholds.

10. **Timestamp** (`std.timestamp`)
    - Type: `string`
    - Format: `date-time` per RFC 3339.
    - Use cases: Creation, modification, capture ingestion times.

11. **Timezone Identifier** (`std.timezone`)
    - Type: `string`
    - Enum: IANA TZ database names (e.g., `America/New_York`).
    - Use cases: Scheduling, localization context.

12. **Locale Code** (`std.locale`)
    - Type: `string`
    - Format: BCP 47 language tag (`en-US`, `fr-CA`).
    - Use cases: Content localization, translation management.

13. **Email Address** (`std.email`)
    - Type: `string`
    - Format: `email`
    - Use cases: Contacts, notification routing.

14. **Phone Number** (`std.phone`)
    - Type: `string`
    - Format: E.164 (`+{country code}{subscriber number}`)
    - Use cases: Stakeholder contact, escalation routing.

15. **URL** (`std.url`)
    - Type: `string`
    - Format: `uri`
    - Use cases: External references, linkage to capture sources.

16. **Tag List** (`std.tag_list`)
    - Type: `array` of `string`
    - Constraints: 0-64 entries, each <= 64 characters, slug format.
    - Use cases: Faceted search, classification, ingestion mapping.

17. **Enumeration** (`std.enum`)
    - Type: `string`
    - Constraints: Enum values defined per field instance, optional default.
    - Use cases: Status fields, categorical attributes, risk levels.

18. **Binary Reference** (`std.binary_ref`)
    - Type: `object`
    - Properties: `blobId` (`std.identifier`), `mediaType` (`std.media_type`),
      `sizeBytes` (`integer` >= 0), `hash` (multihash string)
    - Use cases: Attachment manifests, capture payload references.

19. **Media Type** (`std.media_type`)
    - Type: `string`
    - Format: IANA media type (`type/subtype`)
    - Use cases: Attachment manifests, capability negotiation.

20. **Geo Coordinate** (`std.geo_point`)
    - Type: `object`
    - Properties: `latitude` (number, -90 to 90), `longitude` (number, -180 to 180), optional `altitude` (meters).
    - Use cases: Location tagging, routing, analytics.

21. **Structured Identifier** (`std.slug`)
    - Type: `string`
    - Pattern: `^[a-z0-9]+(?:-[a-z0-9]+)*$`
    - Use cases: Human-readable IDs, registry keys, ingestion mapping.

### Composite Field Catalog
Composites compose primitives to capture real-world constructs.

1. **Localized Text** (`std.localized_text`)
   - Structure: Object keyed by locale (`std.locale`) with `std.rich_text` or
     `std.short_text` values.
   - Policy: MUST include default locale; optional fallbacks per governance.
   - Use cases: Multilingual titles, descriptions, user-visible narratives.

2. **Person Name** (`std.person_name`)
   - Properties: `given`, `middle`, `family`, `suffix`, `prefix`, `display`.
   - Constraints: Each property `std.short_text`; `display` optional override.
   - Use cases: Stakeholder records, assignment lists, contact manifests.

3. **Postal Address** (`std.postal_address`)
   - Properties: `addressLines` (array of <=4 `std.short_text`), `locality`,
     `region`, `postalCode`, `country` (ISO 3166-1 alpha-2), optional `geo` (`std.geo_point`).
   - Use cases: Event venues, billing addresses, asset locations.

4. **Monetary Amount** (`std.money`)
   - Properties: `currency` (ISO 4217 code), `value` (`std.decimal`), optional
     `precision` (integer scale), `asOf` (`std.date`).
   - Use cases: Budgeting, cost baselines, spend tracking.

5. **Measurement** (`std.measurement`)
   - Properties: `value` (`std.decimal`), `unit` (UCUM code), optional
     `displayUnit`, `uncertainty` (`std.decimal`), `timestamp` (`std.timestamp`).
   - Use cases: Sensor readings, throughput metrics, SLA monitoring.

6. **Duration** (`std.duration`)
   - Type: `string`
   - Format: ISO 8601 duration (`PnYnMnDTnHnMnS`)
   - Use cases: Task durations, SLA windows, planned effort.

7. **Progress Summary** (`std.progress`)
   - Properties: `percentComplete` (`std.percentage`), `status` (`std.enum`),
     `updatedAt` (`std.timestamp`), optional `summary` (`std.rich_text`).
   - Use cases: Work tracking, milestone dashboards, SLA reporting.

8. **Checklist** (`std.checklist`)
   - Type: Array of `std.checklist_item`
   - Each item: `id` (`std.identifier`), `label` (`std.short_text`), `isDone`
     (`std.boolean`), optional `completedAt` (`std.timestamp`).
   - Use cases: Ingestion validation, QA checklists, compliance attestations.

9. **User Reference** (`std.user_ref`)
   - Properties: `userId` (`std.identifier`), `displayName` (`std.short_text`),
     `email` (`std.email`), optional `avatar` (`std.url`).
   - Use cases: Assignments, audit trails, comment authorship.

10. **Object Reference** (`std.object_ref`)
    - Properties: `object_type` (`std.slug` identifying the registry item or resource class),
      `object_id` (`std.identifier`), optional `uri` (`std.url` supporting `kki://` and
      external schemes), optional `display_name` (`std.short_text`), optional `relationship`
      (`std.slug` scoped to the field definition), optional `version` (`std.integer`), and
      optional `notes` (`std.rich_text` describing the linkage context).
    - Use cases: Cross-object linking, dependency tracking, referencing upstream datasets,
      embedding related incidents or assets in field payloads. Collections SHOULD be modeled
      as arrays of `std.object_ref` unless a domain-specific composite is required.

11. **Attachment Manifest** (`std.attachment_manifest`)
    - Properties: `attachmentId` (`std.identifier`), `label` (`std.short_text`),
      `binary` (`std.binary_ref`), `source` (`std.url`), `capturedAt`
      (`std.timestamp`), optional `checksum` (multihash), `capabilities`
      (`array` of `std.enum` describing view/annotate rights).
    - Use cases: Capture pipeline, archival metadata, compliance reviews.

12. **Capture Metadata** (`std.capture_metadata`)
    - Properties: `sourceSystem` (`std.short_text`), `ingestedAt` (`std.timestamp`),
      `ingestedBy` (`std.user_ref`), `pipeline` (`std.slug`), `quality`
      (`std.enum`), optional `notes` (`std.rich_text`).
    - Use cases: Ingestion recipes, audit reporting, data lineage.

13. **Lifecycle State** (`std.lifecycle_state`)
    - Properties: `state` (`std.enum`), `enteredAt` (`std.timestamp`),
      `enteredBy` (`std.user_ref`), optional `transitionReason`
      (`std.rich_text`).
    - Use cases: Workflow automation, governance reporting.

14. **Sensitivity Descriptor** (`std.sensitivity_descriptor`)
    - Aligns with existing schema definition, extends to include `justification`
      (`std.rich_text`) and `reviewDate` (`std.date`).
    - Use cases: Access control, compliance attestations.

15. **Realm Descriptor** (`std.realm_descriptor`)
    - Properties: `realmId` (`std.slug`), `displayName` (`std.short_text`),
      `type` (`std.enum`), `defaultSensitivity` (`std.enum`), optional `parent`
      (`std.slug`).
    - Use cases: Multi-tenant scoping, capture routing, capability defaulting.

16. **Capability Entry** (`std.capability_entry`)
    - Properties: `capabilityId` (`std.slug`), `version` (`std.integer`),
      `surface` (`std.enum` of `viewable`, `workflown`, `schedulable`,
      `annotatable`), `actions` (array of `std.slug`), optional `constraints`
      (`std.rich_text`).
    - Use cases: Registry catalogs, plugin negotiation.

#### Directory & CRM Composites
- **Contact Method** (`schema/fields/contact_method.json`) – single communication channel (email, phone, portal, messenger) with verification metadata for automation routing.
- **Person Profile** (`schema/fields/person_profile.json`) – individual identity, pronouns, roles, relationship stage, affiliations, and review cadence.
- **Organization Profile** (`schema/fields/organization_profile.json`) – institutional identity, legal metadata, roles, site addresses, and cadence expectations.

These composites extend the contact library introduced for correspondence to power the new directory capability. They share primitives (postal address, identifiers, contact methods) so ingestion pipelines and automations can reconcile contacts across correspondence, projects, and conversations.

### Derived Field Catalog
Derived fields MUST declare evaluator logic following the derived value
specification. Each derived field definition extends the metadata envelope with
`evaluation` metadata:

| Property          | Description                                                                  |
|-------------------|------------------------------------------------------------------------------|
| `inputs`          | Array of field IDs consumed by the evaluator.                               |
| `evaluator`       | Identifier of the evaluation module or formula.                             |
| `refresh`         | Policy string (`event`, `scheduled`, `manual`).                             |
| `quality`         | Expected data quality tier (`authoritative`, `best_effort`, `experimental`).|
| `lineage`         | Freeform explanation of derivation steps for audit.                         |

Key derived fields required for Milestone M1:

1. **Normalized Progress** (`std.progress.normalized`)
   - Inputs: `std.checklist`, `std.progress.percentComplete`
   - Evaluator: `progress.normalizer.v1`
   - Logic: Calculate blended completion percent (checklist ratio if available,
     else provided percentage), classify into status buckets (On Track, At Risk,
     Off Track).
   - Outputs: Object with `percent` (`std.percentage`), `status` (`std.enum`),
     `trend` (`std.enum` of `up`, `down`, `flat`).

2. **SLA Breach Forecast** (`std.sla.forecast`)
   - Inputs: `std.timestamp` (due date), `std.duration` (allowed slack),
     `std.progress.percentComplete`, historical completion durations.
   - Evaluator: `sla.forecaster.v1`
   - Outputs: Object with `breachProbability` (`std.percentage`),
     `expectedCompletion` (`std.timestamp`), `recommendation` (`std.rich_text`).

3. **Risk Score** (`std.risk.score`)
   - Inputs: `std.enum` (risk level), `std.measurement` (impact metrics),
     `std.checklist` (mitigation tasks).
   - Evaluator: `risk.scorer.v2`
   - Outputs: Object with `score` (`std.integer` 0-100), `category`
     (`std.enum`), `explanation` (`std.rich_text`).

4. **Engagement Heat** (`std.engagement.heat`)
   - Inputs: Capture metadata, user interaction metrics, annotation counts.
   - Evaluator: `engagement.heatmap.v1`
   - Outputs: Object with `level` (`std.enum`), `lastSignal`
     (`std.timestamp`), `signals` (array of signal descriptors).

### Validation and Testing Strategy
- **Schema Tests** – Every field JSON Schema must have automated tests under
  `tests/schema/fields/` covering valid and invalid payloads.
- **Example Fixtures** – Provide canonical examples in `schema/examples/fields/`
  for use in documentation and integration tests.
- **Backward Compatibility** – Version bumps to existing fields require
  compatibility review; breaking changes must increment the major version and
  include migration notes in `docs/specs/CHANGELOG.md` (to be created).

### Governance and Registry Integration
- Field definitions MUST be registered in the capability registry with their
  metadata envelope. The registry stores the canonical version and enforces
  sensitivity constraints when surfaces request field access.
- Capability contracts MUST reference field IDs from this library to ensure
  consistent semantics across view, workflow, scheduling, and annotation
  surfaces.
- Ingestion pipelines MUST map source system fields to these standard IDs.
  Capture blueprints should include mapping tables and validation rules.

### Implementation Roadmap
1. **Schema Authoring** – Create JSON Schema files for missing primitives and
   composites, ensuring consistent naming (`schema/fields/<name>.json`).
2. **Registry Bootstrapping** – Seed the registry with the field metadata
   envelope, linking to capability contracts.
3. **Tooling Support** – Extend schema linter scripts to validate metadata
   envelope completeness and enforce naming conventions.
4. **Documentation** – Add example usage snippets to `docs/specs/examples/` and
   reference the field IDs in capability and derived value specs.
5. **Migration Guidance** – Draft upgrade playbooks for converting legacy items
   to the standard field library, including mapping tables and remediation
   steps for deprecated fields.

### Open Questions
- Do we require localized validation messages for constraints, and if so,
  where do those live?
- How should binary references integrate with external object storage
  lifecycle policies?
- What governance body approves new standard field additions post-M1?

Resolving these questions is recommended before declaring the standard field
library complete, but the above specification provides the baseline structure
and required field catalog for Milestone M1.
