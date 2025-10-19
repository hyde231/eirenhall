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
| FR-006 | Power-aware scheduling | WoL heavy nodes; auto-sleep idle | Must | Verified by metrics/tests |
| FR-007 | Orchestrated agents | Spawn/stop containers across nodes | Must | Policy-based placement works |
| FR-008 | Secure remote intake | VPN/SSH/bot with authZ | Should | Key-based auth; rate-limited; audited |

## 5.3 Capture, Archival & Enrichment

| ID | Title | Description | Priority | Acceptance Criteria |
| --- | --- | --- | --- | --- |
| FR-014 | Link capture & normalization | Ingest URLs; assign realm; create **time-stamped local copy** | Must | Paste URL → archived artifact with canonical URL + capture timestamp |
| FR-015 | Offline archiving | Store snapshots/media; maintain **version history** per URL | Must | Items render offline; checksums saved; captures listed chronologically |
| FR-016 | Plugin processors | Extensible item-type plugins | Must | Hooks: identify/fetch/enrich/render/schedule |
| FR-017 | AI enrichment | Optional local LLM summaries/tags/entities/quotes | Should | Realm-aware; skippable; provenance recorded |

## 5.4 Search, Collections & Bulk Ops

| ID | Title | Description | Priority | Acceptance Criteria |
| --- | --- | --- | --- | --- |
| FR-018 | Unified query | Full-text + facets (type, realm, tags, date, **capture version/time**) | Must | p95 < 800ms; facet counts consistent |
| FR-019 | Bulk operations | Mass-tagging, realm move (down-scope by default), export static sets | Should | Dry-run; audited; undo |
| FR-020 | Dynamic & static collections | Saved dynamic (query-backed) and static (snapshot/export) | Must | Views auto-refresh; exports reproducible |

## 5.5 Extensibility & Evolution

| ID | Title | Description | Priority | Acceptance Criteria |
| --- | --- | --- | --- | --- |
| FR-021 | Capability framework | Items = base fields + declared capabilities | Must | New types gain list/detail/query/export without custom code |
| FR-022 | Schema evolution & migrations | Versioned schemas; plugin-provided migrations | Must | Additive changes seamless; breaking changes migrate in tests |
| FR-023 | Assistant-led evolution | Expose registry/schemas so assistant can propose/apply changes | Should | Draft type+actions, run sandbox tests, produce report; human gate |
| FR-024 | Type-specific actions | Plugins declare actions (e.g., read_mode, download_media) | Must | Actions visible in UI/CLI; param validation; audited |
| FR-025 | Automation rules | If-this-then-that across types | Should | Rule engine evaluates on ingest/update; dry-run; audit |

## 5.6 Large Binaries & Caching

| ID | Title | Description | Priority | Acceptance Criteria |
| --- | --- | --- | --- | --- |
| FR-026 | Large-binary handling | Multi-TB photos/media without Git cloning | Must | Manifests reference files; integrity via checksums |
| FR-027 | Tiered caching | Mini PC edge cache by policy (realm/recency/favorites/saved searches) | Must | Cache metrics; offline manifests enable browsing without full media |
