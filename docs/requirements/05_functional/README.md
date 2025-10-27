# Functional Requirements

## Companion Artifacts

- [Home Lab Infrastructure Requirements (v0.6 Draft)](home_lab_infrastructure.md)

## 5.1 Platform & Security

| ID | Title | Description | Priority | Acceptance Criteria |
| --- | --- | --- | --- | --- |
| FR-001 | Local-only execution | All inference/tools run on LAN/local hosts only | Must | Egress monitor: 0 external connections in core flows |
| FR-002 | Open data formats | Store as Markdown/CSV/JSON/YAML (no lock-in) | Must | Round-trip tests; external readability |
| FR-003 | Session level gating | Each item has a sensitivity level; sessions enforce a max level across all reads/search/conversations | Must | Zero cross-level leakage in tests |
| FR-040 | Level presets & quick switching | Provide presets (e.g., Public, Family, Personal, Private, Intimate) and a prominent session-level switch; sessions remember last-used level per device/profile. | Must | Switching level immediately filters views/search; audit records level changes when applicable |
| FR-004 | Encrypted backup/restore | One-command encrypted backup; selective restore | Must | Nightly job; restore drills pass |
| FR-005 | Capability/type registry | Types declare schema, capabilities, facets, actions, migrations | Must | New types auto-gain generic views; migrations pass tests |

## 5.2 Orchestration & Power

| ID | Title | Description | Priority | Acceptance Criteria |
| --- | --- | --- | --- | --- |
| FR-006 | Power-aware scheduling | WoL heavy nodes; auto-sleep idle; defer storage-heavy automation and GPU workloads to scheduled windows aligned with desktop/server availability | Must | Nightly report captures WoL success rate, idle-to-sleep latency, and % of deferred GPU/storage jobs per node; thresholds reviewed when outliers appear. Reports should be stored a "system report" data type, integrated into the system, not external logs |
| FR-007 | Orchestrated agents | Spawn/stop containers across nodes | Must | Placement policies enumerate node roles (desktop GPU, storage server, Raspberry Pi orchestrator) and hardware capabilities; tests assert workloads land on compatible, available hardware |
| FR-008 | Secure remote intake | VPN/SSH/bot with authZ | Should | Key-based auth; rate-limited; audited |

## 5.3 Capture, Archival & Enrichment

| ID | Title | Description | Priority | Acceptance Criteria |
| --- | --- | --- | --- | --- |
| FR-014 | Link capture & normalization | Ingest URLs; assign realm; create **time-stamped local copy**; follow pagination/linked assets automatically; manage secrets/cookies with minimal human intervention | Must | Paste URL → archived artifact with canonical URL + capture timestamp |
| FR-015 | Offline archiving | Store snapshots/media; maintain **version history** per URL | Must | Items render offline; checksums saved; captures listed chronologically |
| FR-016 | Plugin processors | Extensible item-type plugins | Must | Hooks: identify/fetch/enrich/render/schedule |
| FR-017 | AI enrichment | Optional local LLM summaries/tags/entities/quotes | Should | Session-level aware; skippable; provenance recorded |
| FR-045 | Correspondence management | Unify intake of scanned mail, email exports, digital letters, and attachments with domain/topic/source classification, retention cues, and cross-linking to related items. | Must | Drop folders, email ingest, and manual uploads all generate correspondence items with source/addressee metadata; operators can tag/link correspondence to projects or tasks; exports preserve originals plus normalized metadata manifests |

## 5.4 Search, Collections & Bulk Ops

| ID | Title | Description | Priority | Acceptance Criteria |
| --- | --- | --- | --- | --- |
| FR-018 | Unified query | Full-text + facets (type, realm, tags, date, **capture version/time**) | Must | p95 < 800ms (aspirational, non-binding during feasibility); facet counts consistent |
| FR-019 | Bulk operations | Mass-tagging, realm move (organizational only; no security impact), export static sets | Should | Dry-run; audited; undo |
| FR-020 | Dynamic & static collections | Saved dynamic (query-backed) and static (snapshot/export) | Must | Views auto-refresh; exports reproducible |
| FR-031 | Hierarchical browsing | Provide quick, navigable browsing of stored documents mirroring directory-style hierarchies; may leverage on-demand list generation or cached dynamic queries tied to hierarchy metadata. | Must | Users can traverse arbitrarily deep hierarchy fields (e.g., full path/wiki structure with Breadcrumbs) without search input; on-demand loading keeps desktop navigation snappy while mobile performance is best-effort |
| FR-041 | User-definable dashboards | Allow operators to build dashboard entry pages composed of saved searches, reports, quick links, and widgets surfaced from schema metadata. Ship with a default dashboard that presents a hierarchical browser for data, metadata, and schema exploration. | Must | User can create and edit dashboards, place widgets sourced from saved searches or reports, and set a default view; system boots with a stock dashboard exposing hierarchical navigation across data types and schemas |
| FR-046 | Standards export (vCard/ICS) | Export contacts to vCard 4.0 (.vcf) and events to iCalendar (.ics) with correct field mappings and timezone handling | Should | Batch and per-item exports work; generated .vcf and .ics validate with common tools (vdirsyncer/Thunderbird/Apple Calendar); round-trip tests preserve key fields |
| FR-047 | Source-specific ingestion plugins | Allow per-source ingestion plugins (site/service specific) that depend on a base type bundle and can be enabled per area | Should | Loader enforces dependencies; per-area enablement toggles; network allowlists and secrets integration; items carry provenance |
| FR-048 | Plugin dependencies & resolution | Support plugin `requires` with semver constraints, deterministic install/enable order, and clear diagnostics on conflicts or missing deps | Must | Dependency cycles rejected; enable fails with actionable error; CLI lists required installs |
| FR-049 | Local speech I/O | Provide local offline ASR (German primary) and optional local TTS for conversational capture | Must | No cloud calls; per-area enablement; transcript quality acceptable for example; provenance recorded |
| FR-050 | Conversational capture to items | From a voice memo, propose event/task drafts, resolve people and topics, append to conversation thread, and confirm before publish | Should | Example scenario yields accurate drafts; undo supported; links between items created |

## 5.5 Extensibility & Evolution

| ID | Title | Description | Priority | Acceptance Criteria |
| --- | --- | --- | --- | --- |
| FR-021 | Capability framework | Items = base fields + declared capabilities | Must | New types gain list/detail/query/export without custom code |
| FR-022 | Schema evolution & migrations | Versioned schemas; plugin-provided migrations | Must | Additive changes seamless; breaking changes migrate in tests |
| FR-023 | Assistant-led evolution | Expose registry/schemas so assistant can propose/apply changes | Should | Draft type+actions, run sandbox tests, produce report; human gate |
| FR-024 | Type-specific actions | Plugins declare actions (e.g., read_mode, download_media) | Must | Actions visible in UI/CLI; param validation; audited |
| FR-025 | Automation rules | If-this-then-that across types | Should | Rule engine evaluates on ingest/update; dry-run; audit |
| FR-042 | Project item type | Introduce a first-class `project` item backed by a dedicated capability so tasks, documents, dashboards, and GTD artifacts can anchor to a shared project workspace with rollups and status fields. | Must | `project` schema registered with capability contract; project detail view surfaces linked tasks/wiki/docs via saved relations; exports/imports retain project metadata and memberships without manual mapping |
| FR-043 | Conversational transcript archive | Persist assistant/operator conversations as structured items with searchable transcripts, message metadata, and linkable excerpts so ideas, follow-ups, and coding notes remain queryable. | Must | Conversation ingestion writes items tagged by realm/session with speaker roles and timestamps; saved searches can filter by speaker, topic tag, or referenced item; Markdown export restores transcript order and token references |
| FR-028 | Capability-driven derived views | Items that declare `Workflown`, `Schedulable`, or `Geocoded` capabilities automatically surface Kanban, calendar/timeline, or map heatmap views; plugins opt-in by adding the capability. | Must | Declaring capability exposes the matching view with no manual wiring; removing capability withdraws the view; default list/detail/card views remain available. |
| FR-029 | Session-aware defaults | Newly created items inherit the session's active realm (organizational) and session `max_level` as the default item level. | Must | Items record the session realm and default level; UI clearly shows current session level and allows upgrade/downgrade with confirmation/audit. |
| FR-030 | First-class relations & composable queries | Named relations (tags, sharing, links) are represented as items managed by core plugins; plugins extend via composition rather than deep inheritance, with expensive relation traversals cacheable as saved lists. | Should | Relations persist as items with source/target metadata; plugins reuse core relation types; heavy multi-hop queries can be materialized into saved searches without schema changes. |
| FR-038 | Derived value pipeline | Schema-declared formulas generate read-only fields (e.g., BMI, age) using canonicalized source data and register provenance for recalculation. | Should | Measurement values normalize to canonical units before evaluation; derived fields refresh whenever inputs change; API/UI flag derived status with traceable formula metadata. |
| FR-039 | Multi-value & annotation support | Schemas declare cardinality and supply list widgets, ratings, and note threads so repeated fields, reviews, and inline commentary remain first-class without custom plugins. | Should | List fields enforce element type validation; rating scales expose configurable bounds; notes/annotations capture scope, author, timestamps, and resolution metadata; list editors can spawn permitted child items inline so flows like "festival → add concert" never require leaving the parent form. |
| FR-046 | Generic item shell | Provide a default web browse/query/view/edit surface that renders any registered item type using schema metadata without bespoke widgets. | Must | Item manifests auto-render with field inspectors and inline editors generated from schema definitions; integration tests cover document/task/wiki/person/organization flows without type-specific code. |
| FR-047 | Plugin-isolated extensions | Allow optional bundles (schemas, ingest flows, views, editors) to register as plugins without modifying core distributions, ensuring the stock system remains neutral. | Must | Core ships with plugin loader enabling/disabling bundles per installation; baseline build passes tests with only stock plugins; personalized bundles install via plugin manifest without altering system defaults. |

### Plugin & Recipe Ecosystem

- **Importers:** OCR, CSV, JSON, HTML, and other structured/unstructured intake surfaces.
- **Transformers:** Unit converters, schema normalizers, parsers, and enrichment helpers.
- **Exporters:** CSV/JSON/PDF/HTML packages and webhook targets.
- **Widgets:** Additional field editors and visualizations that bind to primitive types.
- **Recipes:** Versioned conversion templates that can be reused and iterated across collections.

## 5.6 Large Binaries & Caching

| ID | Title | Description | Priority | Acceptance Criteria |
| --- | --- | --- | --- | --- |
| FR-026 | Large-binary handling | Multi-TB photos/media without Git cloning | Must | Manifests reference files; integrity via checksums |
| FR-027 | Tiered caching | Mini PC edge cache by policy (realm/recency/favorites/saved searches) | Must | Cache metrics; offline manifests enable browsing without full media |

## 5.7 Operations, Collaboration & Compliance

| ID | Title | Description | Priority | Acceptance Criteria |
| --- | --- | --- | --- | --- |
| FR-032 | Unified observability | Centralize logs, metrics, and traces across orchestrated agents with lightweight dashboards and alert thresholds tailored to solo-operator needs. | Should | Core services emit structured logs/metrics; single dashboard surfaces health; threshold breach triggers local notification |
| FR-033 | User lifecycle & session presets | Provide self-service onboarding/offboarding, role tiers, and audit trails. Allow configuring default session levels per user/device/profile. | Could | User creation/deactivation flows update audit log; default session level applies on login/device; audit records level changes when applicable |
| FR-034 | Collaboration cues | Offer lightweight commenting, tagging for follow-up, or notification hooks so future human collaborators can coordinate around artifacts and automations. | Could | Users can leave comments/flags; notification hook delivers summary to configured channel; history retained with artifact |
| FR-035 | Resilience drills | Automate periodic backup verification, dependency heartbeat checks, and runbooks for restoring critical services after failure. | Should | Scheduled job exercises restore on sample dataset; heartbeat alerts on dependency outage; runbook validated quarterly |
| FR-036 | Accessible client experience | Ensure UI components follow accessibility best practices (contrast, keyboard navigation) and remain usable on constrained or offline-first devices. | Could | Accessibility audit checklist passes; core flows keyboard-navigable; responsive layout renders on mobile |
| FR-037 | Data lifecycle policies | Define retention, legal hold, and export procedures that respect item sensitivity and session-level gating alongside personal compliance goals. | Should | Configurable retention per area/realm and type; legal hold prevents deletion; export produces auditable package |

### Tooling Expectations
- Core stack shared across personas: Python, Git, Docker, NFS/Samba-accessible storage, and vector databases backing long-term AI memory.
- Persona-specific tooling will be explored later; prefer alignment to the common stack wherever possible.

## 5.8 Data Operations & Provenance

- **Copy / Clone:** Duplicate objects or whole realms with optional relation preservation; item sensitivity levels are preserved.
- **Split / Merge:** Combine or separate records or realms with conflict resolution flows and explicit lineage tracking.
- **Duplicate Detection:** Normalize titles, hashes, and metadata similarity to surface collisions.
- **Similarity Search:** Support vector or heuristic comparisons to reveal related content.
- **Security & Provenance:** Encrypt sensitive values at rest, log every AI/conversion step with inputs/outputs, and require user confirmation before applying automated transformations.

## Traceability

| Requirement | Spec references | Automated coverage |
| --- | --- | --- |
| FR-001 | docs/specs/metadata_governance.md | tests/types/test_core_types.py |
| FR-002 | docs/specs/item_schema.md | scripts/validate_schema.py; tests/fixtures/items/*.json |
| FR-003 | docs/specs/metadata_governance.md; docs/specs/capture_storage_blueprint.md | tests/derived/test_project_metrics |
| FR-014 | docs/specs/capture_storage_blueprint.md; docs/adr/ADR-000-data-sinks-and-replication.md | tests/derived/test_evaluator.py::test_document_metrics_handle_delta_body |
| FR-015 | docs/adr/ADR-003-conflict-resolution-and-offline-policy.md | Acceptance scenario AC‑FR‑015 (manual) |
| FR-018 | docs/specs/generic_item_surface.md; docs/specs/spec_scaffold.md | tests/derived/test_project_metrics |
| FR-020 | docs/specs/project_workspace.md | tests/derived/test_project_metrics |
| FR-027 | docs/adr/ADR-003-conflict-resolution-and-offline-policy.md | Cache drill script (planned) |
| FR-032 | docs/requirements/06_non_functional/README.md; docs/specs/spec_scaffold.md | Observability stub (pending automation) |

| FR-046 | docs/specs/exports/contacts_calendar_export.md | Export validation script (planned) |

Keep this table in sync with `docs/specs/spec_scaffold.md` so requirement,
specification, and test mappings stay coherent.
