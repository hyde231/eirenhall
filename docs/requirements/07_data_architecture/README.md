# Data & Information Architecture

## Extensibility-First Content Model
Items = base fields + capabilities.

### Base Fields
`id, type, realm_id, realm_access_level, sensitivity, title, description, created_at, updated_at, tags[], source_url?, canonical_url?, captures[], attachments[], links[], notes?, checksum, size, metadata{}`

Session context assigns the default `realm_id` + `realm_access_level` pair; overrides are expressed through dedicated share relation items so that scoping changes remain auditable and composable. Realm records capture lineage (`parent_realm_id?`, `origin_access_level`, `clone_of?`) to support split/merge history and policy inheritance checks. Optional `fields.notes` (rich text) gives every item a scratchpad for interim context, migration breadcrumbs, or commentary; because it uses the standard rich-text field, embedded `kki://` URIs or wiki links flow through the existing linking/backlink pipeline.

### Capabilities (Mix-ins)
Viewable, Listable, Queryable, Storable, Importable/Exportable, Versioned, Scrapeable, Downloadable, Readable, Playable, Workflown, Schedulable, Annotatable, Geocoded.

Capability declarations drive derived UX: `Workflown` surfaces Kanban boards, `Schedulable` emits calendar and timeline views, and `Geocoded` enables map/heatmap visualizations. Removing the capability retracts the view without schema churn.

### Type Registry
`{type_key, version, capabilities[], schema.json, facets[], actions[], migrations[], relations[]?}`.

Plugins bundle data definitions, named relations, view descriptors, workflows, and automations. Core plugins ship reusable relation item types (e.g., tags, sharing links) that downstream plugins compose rather than duplicating or introducing deep inheritance chains.

### Starter Kits & Templates
- **Realm manifests:** Opinionated bundles combine schema sets, saved queries, dashboards, and automation defaults as signed manifests so operators can diff, audit, and roll back installations per realm.
- **Gradual enablement:** Starter kits install without mutating core definitions and include migration guides plus capture presets for household operations, research notebooks, and archival projects.

### Compatibility & Health Telemetry
- **Version fences:** Every plugin, capability mix-in, and starter kit declares supported schema/capability ranges and migration hooks so upgrades fail safe instead of drifting silently.
- **Manifest audits:** Scheduled checks validate bundle manifests against the registry, flagging fallbacks, skipped fields, or checksum mismatches before they reach production realms.
- **Operator dashboards:** Admin surfaces expose compatibility status, recent failures, and remediation playbooks, with exportable reports for offline audit trails.

### Project & Conversation Item Shapes
- **Project (`project`)** items act as organizing workspaces that aggregate tasks, documents, dashboards, and automation runs under a shared lifecycle. The schema captures summary status, stage, outcome metrics, canonical roadmap links, and rollups sourced from related items through `fields.summary` (`std.project.summary`) plus optional narratives (`fields.objectives` rich text) and curated relations. Declaring the dedicated `projects.workspace` capability exposes cross-linked boards, progress summaries, and saved-search widgets without per-project wiring.
- **Conversation Transcript (`conversation_thread`)** items persist assistant/operator dialog as ordered message arrays with speaker roles, timestamps, realm tags, topic labels, referenced item URIs, and optional excerpt tokens using `fields.timeline` (`std.conversation.timeline`). Conversation items inherit the same export guarantees as other content types so transcript snippets can rehydrate into Markdown bundles, dashboards, or follow-up tasks. Threads can aggregate related correspondence items and GTD tasks to represent long-running exchanges (e.g., medical billing disputes or insurance claims) without duplicating underlying artifacts while the `conversations.timeline` capability powers timeline rendering and search facets.
- **Correspondence (`correspondence`)** items store normalized mail/email metadata via `fields.entry` (`std.correspondence.entry`) plus party lists, attachments, and retention descriptors. The `correspondence.archive` capability unlocks ingestion dashboards, retention controls, and export tooling tailored to archival workflows.

## Primitive & Structured Data Types

The registry defines a standard library of primitives so plugins and importers speak a common language.

| Type | Description | Example | Notes |
| --- | --- | --- | --- |
| **Text** | Plain or formatted string | "Annual checkup" | Optional Markdown, HTML, or BBCode markup |
| **Integer** | Whole number | `12` | Supports signed/unsigned, min/max constraints |
| **Float / Decimal** | Floating-point or high-precision value | `3.1415` | Distinct type for monetary or scientific accuracy |
| **Boolean** | True/false (optional null) | `true` | Shown as switch or checkbox |
| **Date** | Calendar date | `2025-10-20` | ISO format internally |
| **Time** | Time of day | `13:45:00` | Timezone support optional |
| **DateTime** | Full timestamp | `2025-10-20T13:45:00+01:00` | Always stored UTC with local display |
| **Duration** | Time span | `PT1H30M` | ISO-8601 or numeric seconds |
| **Measurement** | Numeric value + physical unit | `{value: 7.2, unit: "mmol/L"}` | Validated via unit registry; auto-convertible |
| **Percentage** | Fraction of 100 | `12.5%` | Displayed as percent or slider input |
| **Currency** | Monetary value + currency code | `{value: 199.99, currency: "EUR"}` | Conversion via rate table, precision rules |
| **Enum** | One-of predefined list | `"Open"` | Editable or fixed options, scope aware |
| **Tag (multi)** | Dynamic keyword list | `["finance", "2025"]` | Searchable, sortable, user-extendable |
| **List<Primitive>** | Ordered set of same-typed primitives | `["red", "blue"]` | Enforces element type; optionally de-duplicates |
| **List<ItemRef>** | Ordered collection of typed object references | `[{type: "LabResult", id: "abc"}]` | Carries per-entry metadata (`order`, `role?`, `annotation?`, `inline_create?`) |
| **Markdown / HTML / BBCode** | Formatted text | Markdown content | Optional, depending on context |
| **JSON** | Structured data | `{...}` | Schema-aware editor |
| **CSV** | Tabular data | Comma or tab-separated | Header and type inference supported |
| **URL** | Valid link | `https://example.com` | Metadata enrichment optional |
| **Image** | Still media | File ref | Preview, EXIF stripping optional |
| **Video** | Moving media | File ref | Thumbnail, duration metadata |
| **File** | Arbitrary file ref | Path or blob ID | Checksum dedupe supported |
| **Folder** | Folder ref | Path | Local or remote scope |
| **Password / Secret** | Secure string | (masked) | Encrypted at rest, never logged |
| **GeoPoint** | Lat/long coordinate | `{lat: 50.1, lon: 8.7}` | Accuracy metadata optional |
| **Rating** | Normalized score within defined scale | `{value: 4, scale: {min: 1, max: 5, step: 1}}` | Supports star/thumb/likert renderings; optional weighting |
| **Ref<T>** | Reference to another object | Object ID | Single-directional |
| **Relation<T↔U>** | Typed link between objects | Edge in graph | Bidirectional semantics |
| **Note / Annotation** | Rich-text comment scoped to item or field | `{body_md, authored_by, authored_at, scope}` | Threaded replies, resolves, provenance |

Lists inherit validation from their element types: a `List<Measurement>` enforces unit declarations per entry, while `List<Tag>` maps to the multi-select taxonomy helper. Item reference lists include ordering and role metadata so playlists, reading lists, or source citations remain explicit, and they advertise whether inline creation is allowed so a parent schema can instantiate new child items (e.g., create a concert while editing a festival) without leaving context. Notes/annotations exist as first-class primitives that plugins can embed within schemas or as capability-provided related items when collaboration is optional.

### Schema Behavior

- **Extensibility:** Schemas can evolve on the fly when new fields are discovered.
- **Validation:** Type-aware validation (e.g., currency requires numeric value + valid ISO code).
- **Constraint Levels:** Hard (block save) or soft (warn only).
- **Versioning:** Schema versions tracked and diffable.
- **Cardinality:** Fields declare whether they hold a single value or a `List<T>`; list cardinality inherits validation, defaulting, and auditing rules from the underlying primitive or structured type.
- **Derived formulas:** Schemas declare derived fields as expressions (`derived[]{id, label, source_fields[], expression, unit?}`) that operate on canonicalized source data and emit read-only facets persisted alongside metadata with provenance (`computed_at, inputs, formula_id`).

### Derived & Calculated Values

- **Canonical units:** Measurement and duration primitives normalize into registry-defined base units (e.g., meters, kilograms, seconds) before any derived formula runs; currency amounts convert to configured base currency when the expression requests it.
- **Execution location:** Plugins own the evaluators/transforms for their data types, but the registry keeps the declarative formula definitions so orchestration, auditing, and UI can reason about them.
- **Invalidation & refresh:** Derived values recompute whenever a source field changes, when conversion tables update (e.g., currency rates), or on scheduled maintenance runs; failures surface as validation warnings rather than silently serving stale data.
- **Exposure:** Derived outputs live under a reserved `metadata.derived` namespace, are queryable like other fields, and carry explanatory strings/tooltips so downstream clients can present the formula and units used.

### Notes, Annotations & Review Trails

- **Storage model:** Notes can live inline as `Note / Annotation` primitives on a field (e.g., a measurement with technician remark) or as related items through the `Annotatable` capability when collaboration is optional.
- **Scoping:** Each note declares its scope (`item`, `field`, `relation`) and inherits the parent realm/sensitivity tags to prevent leaks across compartments.
- **Lifecycle:** Notes support reply threads, resolution state, and provenance metadata (`authored_by`, `authored_at`, `resolved_at?`, `resolution_note?`) so that audits and collaboration timelines remain reconstructable.

### Conversion & Mapping

#### Intelligent Conversion
- AI-assisted parsing of unstructured inputs (e.g., OCR from a photo or PDF).
- Pattern recognition for currencies (€, $, etc.), units (mg/dL), percentages (%), and dates.
- Auto-suggestion of field types and relations.

#### Guided Mapping UI
- **Left panel:** Detected fields and inferred types.
- **Right panel:** Target schema with required fields.
- **Connections:** Drawn as splines, colored by confidence and type compatibility.
- **Conversion Recipes:** Saved, editable, reusable across similar imports.

### Captures
`capture_id, captured_at, paths, hashes, size, tool_versions` (multiple per Item).

Complex traversals across relation items should be served through composable queries and, when needed, cached as saved searches or materialized lists to keep unified query performance predictable.

### Storage Layout (Illustrative)
`/data/archive/<realm>/<type>/<YYYY>/<MM>/<id>/<captured_at-ISO8601>/` with `meta.json`, normalized content (`.md/.html/.cbz/.pdf`), assets, optional `snapshot.pdf`/`page.warc`.

> POC-oriented example: hardware roles may consolidate into VMs/containers as long as required capabilities (e.g., GPU passthrough) are preserved.

### Indexing & Search
Full-text over normalized text + fields (including **captured_at**); optional vector index; plugin facets (e.g., series/episode/author/duration/language).

### Retention & Deletion
Deferred. Treat storage as fixed for now and plan cleanup workflows after functional feasibility is proven.

### Human-Readable Archival Path
- Canonical persistence remains JSON (per `schema/item_base.json`) for validation, automation, and capability contracts.
- Nightly export job emits Markdown bundles for each realm/type via the `kki_markdown_export` pipeline so archives stay readable even if the app is offline.
- Bundles are stored under `/backups/<date>/markdown/` alongside regular snapshots, following the standard retention window (30 daily / 12 monthly / 5 yearly).
- Each bundle keeps its `objects.json` metadata and checksums; restores can rehydrate JSON through the importer, while operators can reference Markdown directly when needed.

## 7.1 Storage & Data Sinks (Decisions & Options)
- **Metadata/docs/code → Git** (great for text, diffs, ADRs). Avoid huge binaries in repos.
- **Large binaries → raw FS/object store** with open **manifests** (JSON/YAML), checksums, optional CAS/dedup.
- **git-annex/Git LFS (optional)** if repo-centric workflows benefit; keep plain-file exportability.
- **Tiered caching** across Mini PC/Desktop/Server with realm/recency/favorites/saved searches policies.

### Open Questions (Working Positions)
- **SQ‑1:** Prioritize cache by recency and favorites (with realm awareness as already modeled).
- **SQ‑2:** “Manifest-first” = sidecar metadata files that travel with content; preferred default.
- **SQ‑3:** Favor plain filesystem storage for compatibility; consider S3-compatible layers only with clear benefits on homelab hardware.
