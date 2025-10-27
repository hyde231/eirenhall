# KKI Glossary

Comprehensive terminology reference for the Knowledge Kernel Initiative. Terms
are grouped alphabetically for quick lookup. Definitions stay in plain ASCII to
avoid rendering issues.

## A
- **Access Level** - Governance tier (for example `Intimate`, `Personal`) that
  defines default policies for realms created beneath it.
- **Actor** - User, system component, or automation that triggers auditable
  actions.
- **Affordance** - UI or workflow surface exposed by a capability (Kanban board,
  timeline view, dashboard widget).
- **Annotation** - Rich-text comment thread attached to an item or field; inherits
  the item's realm and sensitivity.
- **Archive Manifest** - Sidecar JSON or YAML document listing capture assets,
  checksums, and provenance metadata.
- **Attachment Manifest** - Structured listing of files linked to an item
  including hash, size, and storage path.

## B
- **Backlog Entry** - Requirement or feature card tracked against the roadmap.
- **Baseline Schema** - Canonical JSON Schema definition inherited by item types
  via `$ref`.
- **Backlink** - Derived record noting that another item links to the current
  item, stored under `metadata.sys.links.inbound` and via link relation items.

## C
- **Bootstrap Loader** - Initialization routine that populates the type registry
  from manifests on disk.
- **Bulk Operation** - Realm-scoped action that affects multiple items at once
  (tagging, realm move, export).
- **Capability** - Modular mix-in that unlocks behavior for an item type (for
  example `editor.collab`, `tasks.board`).
- **Capability Contract** - Specification describing capability key, version,
  configuration schema, dependencies, and affordances.
- **Capture** - Time-stamped snapshot or version of an item including archived
  assets and manifest metadata.
- **Capture Blueprint** - Operational plan detailing directory layout, hashing,
  and storage rules for captures.
- **Collection** - Saved grouping of items. Dynamic collections are saved searches;
  static collections are snapshot exports.
- **Conversion Recipe** - Versioned mapping aligning external source fields to
  registry schemas during ingestion.
- **Core Registry** - In-memory representation of all registered schemas and
  manifests.
- **Custom Field** - Schema-defined extension that is not part of the
  standardized field library.

## D
- **Dashboard** - User-configurable entry page composed of widgets, saved
  searches, and navigation aids.
- **Derived Metric** - Computed value stored under an item's `derived` object,
  accompanied by provenance data.
- **Derived Namespace** - Metadata prefix reserved for derived outputs such as
  `metadata.sys.derived.*`.
- **Discovery Sprint (M1)** - Initial milestone that establishes the data model,
  type registry, and storage foundations.

## E
- **Envelope** - Top-level structure of an item (`id`, `title`, `realm`, `fields`,
  `metadata`, `derived`, and so on).
- **Event Log** - Append-only record of significant system events used for
  auditing and alerting.
- **Export Package** - Bundle containing items, captures, manifests, and metadata
  prepared for egress from the system.

## F
- **Facet** - Queryable dimension (realm, tag, status) exposed by schemas to power
  search and filtering.
- **Field Library** - Collection of reusable field schemas stored under
  `schema/fields`.
- **Field Manifest** - Document describing which fields are available for a given
  item type together with constraints or UI hints.
- **Formula Source** - Input field or metric referenced by a derived expression.

## G
- **GTD Workflow** - Capture/clarify/organize/review/execute task management
  pattern supported by the system.
- **Guardian Node** - Infrastructure component responsible for data durability,
  such as a storage server or NAS.

## H
- **Hard Constraint** - Validation rule that blocks persistence when violated.
- **Hierarchy Browser** - UI component that renders nested realms, folders, or
  schema hierarchies.
- **Homelab** - Owner-operated infrastructure environment that hosts the KKI
  services.

## I
- **Import Pipeline** - Orchestrated flow that ingests external data into items
  while mapping fields to schemas.
- **Index Manifest** - Metadata file describing indexed fields, faceting
  configuration, and search tuning parameters.
- **Ingestion Blueprint** - Specification covering mapping UI, recipe storage,
  validations, and operator workflow.
- **Inclusion Directive** - Macro such as `{{include:item:...}}` or
  `{{value:item:...}}` that embeds live data or copies values from another item
  following the linking specification.
- **Item** - Typed, realm-scoped knowledge entity governed by the item envelope.

## J
- **JSON Schema** - Validation language used to describe item envelopes, field
  definitions, and capability configurations.

## K
- **Kernel** - Core services and registries that manage schemas, items, and
  capability lifecycles.
- **Keyring** - Secure store for encryption keys used during capture, archival,
  and backup operations. Under the session model, per-realm keys are optional.

## L
- **List View** - Default table-style presentation of item collections with
  configurable columns and sorting.
- **Local-only Execution** - Requirement (FR-001) ensuring inference and tooling
  run on LAN or controlled hosts only.
- **Lookup Table** - Reference dataset (for example unit registry, currency rates)
  used during validation or derived computations.

## M
- **Manifest** - Generic term for structured index files (type manifests,
  attachment manifests, registry manifests, and so on).
- **Metadata Namespace** - Prefix partitioning metadata keys such as `sys.*`,
  `cap.<capability>.*`, `ext.<vendor>.*`, or `tmp.*`.
- **Migration Hook** - Callback executed when a schema version upgrades to
  reconcile persisted data.
- **Mix-in** - Synonym for a capability module attached to an item type.

## N
- **Namespace Registry** - Governance record tracking approved metadata prefixes
  and capability identifiers.
- **Non-functional Requirement (NFR)** - System quality constraint, for example
  security posture or performance target.
- **Note Thread** - Sequence of annotations with status (open or resolved) and
  provenance markers.

## O
- **Operator** - Human responsible for managing organizational areas (realms),
  infrastructure, and automation across the system.
- **Override Reason** - Text explanation recorded when an item’s sensitivity is
  downgraded; used to drive confirmation and audit.

## P
- **Persona (AI)** - Automation persona limited by realm and capability scopes
  running inside sandboxed runtimes.
- **Persona (Human)** - Household member, steward, or collaborator interacting via
  UI or CLI with realm-defined permissions.
- **Pipeline** - Automated sequence (ingestion, derived evaluation, export)
  orchestrated by the kernel.
- **Playbook** - Runbook-style documentation guiding operational flows such as
  backup, restore, or ingestion.
- **Progress Summary** - Composite field tracking total work, completed work, and
  percentage completion.
- **Provenance** - Traceability metadata capturing inputs, computations, and
  authorship history.

## Q
- **Query DSL** - Structured language powering saved searches and dynamic
  collections.
- **Queue Intake** - Workflow that buffers remote capture requests before local
  archival completes.

## R
- **Realm** - Policy-bound workspace hosting items, metadata, and storage with a
  shared access level.
- **Reference Link** - Link entry classified as `reference` within the link field
  schema.
- **Registry Manifest** - Persisted checksum record for loaded schemas (for example
  `var/registry/schemas.json`).
- **Roadmap Milestone** - Time-boxed delivery objective (M1 Discovery, M2 Walking
  Skeleton, and onward).

## S
- **Schema Loader** - Utility that discovers, checksums, and registers JSON or
  YAML schemas into the registry.
- **Schema Version** - Incremental identifier used to track schema evolution and
  trigger migration hooks.
- **Sensitivity** - Classification label that dictates visibility and handling
  rules for items.
- **Soft Constraint** - Validation rule that emits warnings without blocking the
  operation.
- **Standard Field** - Approved field schema from the field library.
- **Storage Blueprint** - Plan covering directory layout, manifest structure,
  hashing, and retention strategy.
- **System Report** - Item type representing operational metrics (for example
  Wake-on-LAN success rate).

## T
- **Tag** - First-class classification item with hierarchy and lineage tracking.
- **Telemetry** - Operational metrics collected for uptime, performance, and
  reliability observability.
- **Type Manifest** - YAML document describing an item type, its schema reference,
  capabilities, and metadata.
- **Type Registry** - Ordered mapping of type manifests loaded into memory for
  runtime use.

## U
- **Unified Query** - Search service combining full-text, facets, and derived
  filters (requirement FR-018).
- **User-definable Dashboard** - FR-041 feature allowing operators to compose
  dashboard entry pages.
- **UUID** - Universally unique identifier used where global uniqueness is
  required.

## V
- **Vector Index** - Optional embedding-based search index referenced by the
  storage blueprint.
- **Version History** - Ordered capture record tracking revisions to an item over
  time.

## W
- **Wake-on-LAN (WoL)** - Infrastructure mechanism to power up nodes for scheduled
  jobs (deferred to milestone M2).
- **Widget** - Dashboard component rendering a saved search, metric callout, or
  shortcut group.
- **Workflown Capability** - Capability exposing Kanban or task board affordances.

## X
- **X-UI Metadata** - `x-ui` hints embedded in field schemas that inform client
  rendering choices.

## Y
- **YAML Manifest** - Schema or manifest file expressed in YAML rather than JSON.

## Z
- **Zero-trust Posture** - Security stance assuming every realm interaction
  requires explicit authorization and auditing.




