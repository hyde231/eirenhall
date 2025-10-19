# Functional Requirements

## 5.1 Platform & Security

| ID | Title | Description | Priority | Acceptance Criteria |
| --- | --- | --- | --- | --- |
| FR-001 | Local-only execution | All inference/tools run on LAN/local hosts only | Must | Egress monitor: 0 external connections in core flows |
| FR-002 | Open data formats | Store as Markdown/CSV/JSON/YAML (no lock-in) | Must | Round-trip tests; external readability |
| FR-003 | Realm tagging & scoping | Every artifact carries a realm tag; tools respect active cap | Must | Zero cross-realm leakage in tests |
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
| FR-017 | AI enrichment | Optional local LLM summaries/tags/entities/quotes | Should | Realm-aware; skippable; provenance recorded |

## 5.4 Search, Collections & Bulk Ops

| ID | Title | Description | Priority | Acceptance Criteria |
| --- | --- | --- | --- | --- |
| FR-018 | Unified query | Full-text + facets (type, realm, tags, date, **capture version/time**) | Must | p95 < 800ms (aspirational, non-binding during feasibility); facet counts consistent |
| FR-019 | Bulk operations | Mass-tagging, realm move (down-scope by default), export static sets | Should | Dry-run; audited; undo |
| FR-020 | Dynamic & static collections | Saved dynamic (query-backed) and static (snapshot/export) | Must | Views auto-refresh; exports reproducible |
| FR-031 | Hierarchical browsing | Provide quick, navigable browsing of stored documents mirroring directory-style hierarchies; may leverage on-demand list generation or cached dynamic queries tied to hierarchy metadata. | Should | Users can traverse arbitrarily deep hierarchy fields (e.g., full path/wiki structure) without search input; on-demand loading keeps desktop navigation snappy while mobile performance is best-effort |

## 5.5 Extensibility & Evolution

| ID | Title | Description | Priority | Acceptance Criteria |
| --- | --- | --- | --- | --- |
| FR-021 | Capability framework | Items = base fields + declared capabilities | Must | New types gain list/detail/query/export without custom code |
| FR-022 | Schema evolution & migrations | Versioned schemas; plugin-provided migrations | Must | Additive changes seamless; breaking changes migrate in tests |
| FR-023 | Assistant-led evolution | Expose registry/schemas so assistant can propose/apply changes | Should | Draft type+actions, run sandbox tests, produce report; human gate |
| FR-024 | Type-specific actions | Plugins declare actions (e.g., read_mode, download_media) | Must | Actions visible in UI/CLI; param validation; audited |
| FR-025 | Automation rules | If-this-then-that across types | Should | Rule engine evaluates on ingest/update; dry-run; audit |
| FR-028 | Capability-driven derived views | Items that declare `Workflown`, `Schedulable`, or `Geocoded` capabilities automatically surface Kanban, calendar/timeline, or map heatmap views; plugins opt-in by adding the capability. | Must | Declaring capability exposes the matching view with no manual wiring; removing capability withdraws the view; default list/detail/card views remain available. |
| FR-029 | Realm-aware defaults & sharing overrides | Newly created items inherit the session's active realm; sharing overrides are modeled as first-class relation items that can supersede the default realm per target. | Must | Items record the session realm by default; share records specify target realm/scope and audit trail; UI exposes active realm & overrides. |
| FR-030 | First-class relations & composable queries | Named relations (tags, sharing, links) are represented as items managed by core plugins; plugins extend via composition rather than deep inheritance, with expensive relation traversals cacheable as saved lists. | Should | Relations persist as items with source/target metadata; plugins reuse core relation types; heavy multi-hop queries can be materialized into saved searches without schema changes. |

## 5.6 Large Binaries & Caching

| ID | Title | Description | Priority | Acceptance Criteria |
| --- | --- | --- | --- | --- |
| FR-026 | Large-binary handling | Multi-TB photos/media without Git cloning | Must | Manifests reference files; integrity via checksums |
| FR-027 | Tiered caching | Mini PC edge cache by policy (realm/recency/favorites/saved searches) | Must | Cache metrics; offline manifests enable browsing without full media |

## 5.7 Operations, Collaboration & Compliance

| ID | Title | Description | Priority | Acceptance Criteria |
| --- | --- | --- | --- | --- |
| FR-032 | Unified observability | Centralize logs, metrics, and traces across orchestrated agents with lightweight dashboards and alert thresholds tailored to solo-operator needs. | Should | Core services emit structured logs/metrics; single dashboard surfaces health; threshold breach triggers local notification |
| FR-033 | Realm-aware user lifecycle | Provide self-service onboarding/offboarding, role tiers, and audit trails scoped by realm, even if limited to a handful of trusted accounts. | Could | User creation/deactivation flows update audit log; roles enforce realm-scoped access in tests |
| FR-034 | Collaboration cues | Offer lightweight commenting, tagging for follow-up, or notification hooks so future human collaborators can coordinate around artifacts and automations. | Could | Users can leave comments/flags; notification hook delivers summary to configured channel; history retained with artifact |
| FR-035 | Resilience drills | Automate periodic backup verification, dependency heartbeat checks, and runbooks for restoring critical services after failure. | Should | Scheduled job exercises restore on sample dataset; heartbeat alerts on dependency outage; runbook validated quarterly |
| FR-036 | Accessible client experience | Ensure UI components follow accessibility best practices (contrast, keyboard navigation) and remain usable on constrained or offline-first devices. | Could | Accessibility audit checklist passes; core flows keyboard-navigable; responsive layout renders on mobile |
| FR-037 | Data lifecycle policies | Define retention, legal hold, and export procedures that respect realm boundaries and personal compliance goals. | Should | Configurable retention per realm/type; legal hold prevents deletion; export produces auditable package |

### Tooling Expectations
- Core stack shared across personas: Python, Git, Docker, NFS/Samba-accessible storage, and vector databases backing long-term AI memory.
- Persona-specific tooling will be explored later; prefer alignment to the common stack wherever possible.
