# 0. Document Meta$1
---

## Table of Contents (mini)
1. Vision & Goals
2. Stakeholders
3. Scope
3.1 Privacy Realms & Access Control
4. User & Use Cases
5. Functional Requirements (FR)
6. Non-Functional Requirements (NFR)
7. Data & Information Architecture (incl. Tagging, Collectable Content, Health, GTD)
8. Interfaces & Integrations
9. UX Principles & Views
10. Governance & Safety Rails
11. Risks & Mitigations
12. Roadmap & Releases
13. Requirement Backlog
14. Acceptance Criteria Patterns
15. Glossary
16. References

# 1. Vision & Goals
**Problem statement.** Build a privacy-respecting, local-first platform that captures and normalizes information, runs code and automations on LAN-only hardware, and smartly orchestrates compute to minimize power usage.

**Product vision (1‑liner).** _A self-hosted, realm-aware personal knowledge & automation substrate that privately understands, writes, and runs code, preserves online/offline content, and wakes the right machine to get work done._

**Goals / outcomes (SMART):**
- **G1 Locality:** ≥95% of use cases run fully local (no cloud egress) by GA.
- **G2 Code throughput:** Typical code task (≤150 LOC + tests) completes in ≤5 minutes p95 when GPU node available.
- **G3 Power:** Orchestrator wakes nodes on demand and auto-sleeps idle; 24/7 baseline power ≤ 15W on average.
- **G4 Memory:** Persistent, queryable long-term memory; <1s p95 retrieval for top‑k context.

**Non-goals (current phase):** No cloud LLMs/SaaS telemetry; no multi-tenant IAM beyond a single household.

**Success metrics & guardrails:** Task completion rate; p95 time-to-result; baseline power; **privacy incidents = 0**; default‑deny egress; encrypted at rest & in transit; idle auto-sleep on heavy nodes.

## 1.1 Vision Clarification Table (Decided Directions)
| # | Theme | Decided Direction | Implications |
|---|---|---|---|
| 1 | Primary Identity | **Platform-first** substrate for data/automation/AI | Open formats & modular automation outlive individual models/UIs |
| 2 | AI’s Role | **Meta-layer advisor** | AI proposes/assists; deterministic automation executes |
| 3 | System Evolution | **Advisory evolution** | Human approval gates; sandbox proposals; no unsupervised self-modifying behavior |
| 4 | Data Cohesion | **Unified substrate, modular interfaces** | Common data core; per-type plugins |
| 5 | User Scope / Realms | **Single-user privacy hierarchy** | Visibility/encryption scopes; simple sharing later |
| 6 | Extensibility Target | **AI-assisted, human-approved** | Schema evolution is auditable |
| 7 | Knowledge vs Action | **Action-driven foundation** | Deterministic core under flexible reasoning layer |
| 8 | Longevity | **Strict openness** | Human-readable, portable formats |

## 1.2 Living Schema & AI-Assisted Integration
Principles: (1) ingest first, model later; (2) AI proposes structures/relations; (3) schemas/workflows are **data** (JSON/YAML) with versions and diffs; (4) reflective loop with dry-runs; (5) iterative, human-approved evolution.

## 1.3 AI Personas (Contexts & Boundaries)
Roles are logical contexts with scoped permissions/tools. All personas are **local-only** and **realm-aware**.

| Persona | Purpose | Scope | Capabilities | Constraints |
|---|---|---|---|---|
| Librarian | Archival, retrieval, curation | Archives, indexes, metadata (R/O except tagging & collections) | Search, summarize, cross-reference | Strict realm caps; provenance for changes |
| System Advisor | Evolve workflows, schema, infra | Schemas, configs, manifests, metrics | Introspection, simulation, proposals | Sandbox; proposals only; human approval to apply |
| Assistant | GTD/tasks/projects, reflective notes | Personal/Household realms | Conversation, planning, scheduling | Undo/redo; non-destructive edits |
| Coding Assistant | Local dev support | Repos, docs, tests | Code gen, refactor, tests, PRs | No direct writes to prod data; PRs + tests required |

---

# 2. Stakeholders
Single-tenant home lab: Owner/Sponsor, Engineer/Operator, Household end users, Security/Privacy steward (you).

---

# 3. Scope
**In-scope:** Local-only models; file/repo ops; code execution in isolated runtimes; Git ops (Gitea/LAN); long-term memory with summarization/vector search; privacy **realms**; orchestrated agent containers; power-aware WoL/auto-sleep; secure remote intake (VPN/SSH/bot); capture/archival of web/media with **versioned time-stamped captures**; extensible plugin SDK; unified query & collections; GTD workflows.

**Out of scope (now):** Cloud LLMs/embeddings; multi-tenant SaaS; mobile beyond VPN + CLI/web.

**Assumptions:** Nodes reachable via LAN; WoL supported; sufficient local storage; legal local models/quantizations.

**Constraints:** End-to-end encryption; open formats (Markdown/CSV/JSON/YAML; optional WARC/MAFF/PDF); verifiable backups; offline usability.

---

## 3.1 Privacy Realms & Access Control (Genericized)
**Realms (configurable, examples):** `Shared`, `Household`, `Personal`, `Intimate`.

**Semantics:**
- Each **Artifact/Item** has exactly one **realm**. Sessions have an **active realm cap**; retrieval includes only items with realm ≤ cap.
- **Selective sharing:** time-boxed read-only sessions for `Shared`; never includes `Intimate`.
- **Break-glass (Personal only):** quorum + escrowed key; immutable audit; drills. `Intimate` excluded.
- Credentials, cookies, headless routes, and storage prefixes are scoped per realm.

---

# 4. User & Use Cases
Primary persona: privacy-first power user/developer running a home lab.

Top use cases: code tasks/PRs; repo maintenance; file ops; knowledge recall; remote quick tasks; GPU jobs; GTD; **link capture**; **archival + enrichment**; extensible plugins; unified query; bulk ops; **versioned captures per URL**; offline exports.

Sample stories: paste URL → offline archived Item (with timestamped local copy); saved search for “updates this week”; export Household-safe Markdown bundle.

---

# 5. Functional Requirements (FR)

## 5.1 Platform & Security
| ID | Title | Description | Priority | Acceptance Criteria |
|---|---|---|---|---|
| FR-001 | Local-only execution | All inference/tools run on LAN/local hosts only | Must | Egress monitor: 0 external connections in core flows |
| FR-002 | Open data formats | Store as Markdown/CSV/JSON/YAML (no lock-in) | Must | Round-trip tests; external readability |
| FR-003 | Realm tagging & scoping | Every artifact carries a realm tag; tools respect active cap | Must | Zero cross-realm leakage in tests |
| FR-004 | Encrypted backup/restore | One-command encrypted backup; selective restore | Must | Nightly job; restore drills pass |
| FR-005 | Capability/type registry | Types declare schema, capabilities, facets, actions, migrations | Must | New types auto-gain generic views; migrations pass tests |

## 5.2 Orchestration & Power
| ID | Title | Description | Priority | Acceptance Criteria |
|---|---|---|---|---|
| FR-006 | Power-aware scheduling | WoL heavy nodes; auto-sleep idle | Must | Verified by metrics/tests |
| FR-007 | Orchestrated agents | Spawn/stop containers across nodes | Must | Policy-based placement works |
| FR-008 | Secure remote intake | VPN/SSH/bot with authZ | Should | Key-based auth; rate-limited; audited |

## 5.3 Capture, Archival & Enrichment
| ID | Title | Description | Priority | Acceptance Criteria |
|---|---|---|---|---|
| FR-014 | Link capture & normalization | Ingest URLs; assign realm; create **time-stamped local copy** | Must | Paste URL → archived artifact with canonical URL + capture timestamp |
| FR-015 | Offline archiving | Store snapshots/media; maintain **version history** per URL | Must | Items render offline; checksums saved; captures listed chronologically |
| FR-016 | Plugin processors | Extensible item-type plugins | Must | Hooks: identify/fetch/enrich/render/schedule |
| FR-017 | AI enrichment | Optional local LLM summaries/tags/entities/quotes | Should | Realm-aware; skippable; provenance recorded |

## 5.4 Search, Collections & Bulk Ops
| ID | Title | Description | Priority | Acceptance Criteria |
|---|---|---|---|---|
| FR-018 | Unified query | Full-text + facets (type, realm, tags, date, **capture version/time**) | Must | p95 < 800ms; facet counts consistent |
| FR-019 | Bulk operations | Mass-tagging, realm move (down-scope by default), export static sets | Should | Dry-run; audited; undo |
| FR-020 | Dynamic & static collections | Saved dynamic (query-backed) and static (snapshot/export) | Must | Views auto-refresh; exports reproducible |

## 5.5 Extensibility & Evolution
| ID | Title | Description | Priority | Acceptance Criteria |
|---|---|---|---|---|
| FR-021 | Capability framework | Items = base fields + declared capabilities | Must | New types gain list/detail/query/export without custom code |
| FR-022 | Schema evolution & migrations | Versioned schemas; plugin-provided migrations | Must | Additive changes seamless; breaking changes migrate in tests |
| FR-023 | Assistant-led evolution | Expose registry/schemas so assistant can propose/apply changes | Should | Draft type+actions, run sandbox tests, produce report; human gate |
| FR-024 | Type-specific actions | Plugins declare actions (e.g., read_mode, download_media) | Must | Actions visible in UI/CLI; param validation; audited |
| FR-025 | Automation rules | If-this-then-that across types | Should | Rule engine evaluates on ingest/update; dry-run; audit |

## 5.6 Large Binaries & Caching
| ID | Title | Description | Priority | Acceptance Criteria |
|---|---|---|---|---|
| FR-026 | Large-binary handling | Multi-TB photos/media without Git cloning | Must | Manifests reference files; integrity via checksums |
| FR-027 | Tiered caching | Mini PC edge cache by policy (realm/recency/favorites/saved searches) | Must | Cache metrics; offline manifests enable browsing without full media |

---

# 6. Non-Functional Requirements (NFR)
**Reliability:** Orchestrator uptime ≥99.5%; durable queues.

**Performance:** Capture enqueue <300ms; p95 query <800ms; page snapshot <30s; videos at download wall-clock.

**Security & Privacy:** E2E encryption; realm-scoped tokens; immutable audits; default-deny egress.

**Operability:** Metrics for capture rate, success/failure, retries, storage growth, **captures per URL (version count)**, dedupe hit rate, query latency, realm scope violations (must be 0).

**Formats & Compatibility:** Archives in open formats (Markdown + assets; optional PDF/WARC/MAFF); yt-dlp sidecars; import/export CSV/JSON; **preserve capture timestamps**.

**Maintainability:** Plugin SDK with semver hooks; e2e tests for core plugins; sandboxed execution.

---

# 7. Data & Information Architecture
**Extensibility-first content model.** Items = base fields + capabilities.

**Base fields:** `id, type, realm, sensitivity, title, description, created_at, updated_at, tags[], source_url?, canonical_url?, captures[], attachments[], links[], checksum, size, metadata{}`

**Capabilities (mix-ins):** Viewable, Listable, Queryable, Storable, Importable/Exportable, Versioned, Scrapeable, Downloadable, Readable, Playable, Workflown, Schedulable, Annotatable.

**Type registry:** `{type_key, version, capabilities[], schema.json, facets[], actions[], migrations[]}`.

**Captures:** `capture_id, captured_at, paths, hashes, size, tool_versions` (multiple per Item).

**Storage layout (illustrative):** `/data/archive/<realm>/<type>/<YYYY>/<MM>/<id>/<captured_at-ISO8601>/` with `meta.json`, normalized content (`.md/.html/.cbz/.pdf`), assets, optional `snapshot.pdf`/`page.warc`.

**Indexing & search:** Full-text over normalized text + fields (incl. **captured_at**); optional vector index; plugin facets (e.g., series/episode/author/duration/language).

**Retention & deletion:** Realm defaults; quarantine then purge; per-capture pruning; `Scrapeable` may pin.

## 7.1 Storage & Data Sinks (Decisions & Options)
- **Metadata/docs/code → Git** (great for text, diffs, ADRs). Avoid huge binaries in repos.
- **Large binaries → raw FS/object store** with open **manifests** (JSON/YAML), checksums, optional CAS/dedup.
- **git-annex/Git LFS (optional)** if repo-centric workflows benefit; keep plain-file exportability.
- **Tiered caching** across Mini PC/Desktop/Server with realm/recency/favorites/saved searches policies.

**Open questions:**
- SQ‑1: Cache priority by realm vs. recency/favorites?
- SQ‑2: Any Git-centric mandate for photos/media or is manifest-first OK?
- SQ‑3: Comfort with optional local S3-compatible store if we preserve plain export?

---

# 8. Interfaces & Integrations
**Local systems:** Gitea, NFS/Samba, WireGuard, Prometheus/Grafana.

**Capture/Archive:** readability extractors → Markdown; OCR; yt-dlp; headless (Playwright) → PDF/HTML; optional WARC/MAFF; RSS/Atom.

**Plugin SDK:**
- **Manifest:** `type_key, display_name, version, capabilities[], schema, facets[], actions[]`
- **Hooks:** `identify(url|path)`, `ingest(input)`, `fetch(item)`, `enrich(item,capture)`, `render(item,mode)`, `actions()`, `schedule(item)`, `migrate(item,from,to)`

**APIs:** Content (CRUD Items/Captures, query, bulk, export/import); Registry (types/schemas/validation); Actions (invoke with realm checks & audit).

**Network policy:** Default‑deny egress; realm-scoped proxies/identities; explicit consent per outbound call.

---

# 9. UX Principles & Views
- **Generic views auto-derived from capabilities:** list/table (facets), detail, history (captures), reader mode (stories/threads), media panel (downloads/subtitles), workflow boards (tasks/projects), annotations.
- **Inputs:** paste box, watched folders, browser extension/bookmarklet, CLI (`kki capture <url> --realm R --tags a,b`).
- **Collections:** saved searches (dynamic) and snapshots (static exports with manifests).
- **Exports:** realm banners, redaction profiles, Markdown/CSV bundles + assets; masters untouched.

## 9.1 Saved Searches & Collections Spec
**Saved Search (dynamic):** `id, name, owner, realm_cap, query_dsl, sort, limit?, schedule?`
- DSL: boolean over fields (`type, realm, tags, captured_at/published_at, plugin, duration, author, status`), operators (`=, !=, in, contains, regex?, range`).
- Example: `type=webcomic AND captured_at>=2025-10-01`.

**Static Collection (snapshot):** `id, name, realm, item_ids[], manifest` (checksums, capture ids, paths). Export: Markdown/CSV + assets.

---

# 10. Governance & Safety Rails
- Personas operate under **realm/sensitivity** with default‑deny egress.
- **Sandboxed proposals:** Advisor/Coder output ADRs/PRs with tests; no direct live mutations.
- **Promotion gates:** human approval, semver bump, migration+rollback plan.
- **Audit:** immutable provenance for schema/tag/realm changes, exports, rules.

---

# 11. Risks & Mitigations
| ID | Risk | Impact | Likelihood | Mitigation |
|---|---|---|---|---|
| R‑01 | Model/code assist quality insufficient | High | Med | Escalate model size; tests; human review gates |
| R‑02 | Power mgmt flakiness (WoL/sleep) | Med | Med | Health checks; conservative timers; manual override |
| R‑03 | Data leakage via misconfig | High | Med | Realm-scoped stores; default‑deny egress; leakage tests in CI |
| R‑04 | Key/backup failure | High | Low | Offline encrypted backups; restore drills; escrow policy (not for Intimate) |
| R‑05 | Vector/index bloat | Med | Med | Distillation/compaction; tiered storage; cache |

---

# 12. Roadmap & Releases (indicative)
- **M1 Discovery:** finalize realm model; type registry skeleton; capture schema/storage layout; persona scaffolding.
- **M2 Walking Skeleton:** paste URL → archived Markdown; realm enforcement; search; basic Librarian flows; Public demo session.
- **M3 Alpha:** adapters (web page, YouTube, Instagram); mass tagging; saved searches; backups; GTD board.
- **M4 Beta:** headless snapshots (Playwright), WARC export, enrichment pipeline, export bundles, ingestion scheduling; Advisor proposals.
- **M5 GA:** hardening, dashboards, restore drills, full docs & ADRs.

**Dependencies:** WoL; VPN; storage planning; per-realm key management.

---

# 13. Requirement Backlog (Living Table)
| Key | Type | Title | Priority | Acceptance Criteria | Owner | Status |
|---|---|---|---|---|---|---|
| FR‑001 | FR | Local‑only execution | Must | No external egress; tests verify | You | Draft |
| FR‑002 | FR | Open data formats | Must | Readable externally; round-trip tests | You | Draft |
| FR‑003 | FR | Realm tagging & scoping | Must | Zero cross‑realm retrievals in tests | You | Draft |
| FR‑006 | FR | Power-aware scheduling | Must | WoL + idle sleep verified | You | Draft |
| FR‑014 | FR | Link capture & normalization | Must | URL → archived item with metadata + timestamped copy | You | Draft |
| FR‑015 | FR | Offline archiving (versioned) | Must | Items render offline; checksums saved; captures listed | You | Draft |
| FR‑016 | FR | Plugin processors | Must | Identify/fetch/enrich/render hooks pass tests | You | Draft |
| FR‑018 | FR | Unified query | Must | p95 < 800ms; saved searches work | You | Draft |
| FR‑019 | FR | Bulk operations | Should | Mass‑tag/move/export with audit | You | Draft |
| FR‑020 | FR | Dynamic & static collections | Must | Views auto‑refresh; exports reproducible | You | Draft |
| FR‑026 | FR | Large-binary handling | Must | Manifests; integrity via checksums | You | Draft |
| FR‑027 | FR | Tiered caching | Must | Cache metrics; offline manifests enable browsing | You | Draft |
| NFR‑SEC | NFR | E2E encryption & egress block | Must | WG/mTLS + firewall verified | You | Draft |
| NFR‑PERF | NFR | Capture/search performance | Must | Enqueue <300ms; query p95 <800ms | You | Draft |

---

# 14. Acceptance Criteria Patterns
- **Gherkin:** Given <context> When <action> Then <outcome>.
- **Quality bar:** objective evidence (tests, demo scripts, metrics deltas).
- **Negative cases:** auth failures, timeouts, invalid inputs, realm violations.

---

# 15. Glossary (selected)
- **Item**: typed, realm-scoped content entity.  
- **Capture**: time-stamped snapshot/version of an Item.  
- **Realm**: privacy boundary (configurable names).  
- **Sensitivity**: visibility control (configurable levels).  
- **Tag**: first-class classification entity (ID, aliases, hierarchy, lineage).  
- **Manifest**: open JSON/YAML index of Items & file references.  
- **Persona**: bounded AI role with scoped tools and realm caps.

---

# 16. Reconciliation Notes (What was lost in earlier merges and is now preserved)
- **Generic realm naming** (no personal names baked into models/paths/UI).  
- **Assistant personas** (Librarian, System Advisor, Assistant, Coding Assistant) with clear scopes.  
- **Versioned captures per URL** with **time-stamped local copies** and visible history.  
- **Data sinks separation**: Git for metadata/docs/code; raw FS/object store for large binaries; optional git-annex/LFS; manifests tie all together.  
- **Tiered caching** for Mini PC/Desktop/Server with policy knobs and metrics.  
- **Series/completeness detection** for archival subtypes → tasks.  
- **Redaction/export profiles** ensuring realm-safe sharing; masters remain immutable.  
- **Watched sources & ingestion scheduling** producing due/overdue tasks.  
- **Provenance** across captures, tagging, automation, personas, and exports.

---

# 17. References

---

## Change Log (v0.5)
- Merged vNext addendum into primary structure: Documents & Records now §7.5 (detailed); Collectable Content as §7.6.1; Tagging extended in §7.4.1; Health workspace §7.7.1; GTD workflows §7.8.1.
- Standardized realm name to **Intimate** (replacing “Private-Restricted”).
- Added mini Table of Contents for navigability.
- Clarified sensitivity labels `{low, normal, high, secret}` as canonical set.
- Cross-referenced FR sections to detailed narratives.


Consolidated from: System X working draft; Combined Requirements (vNext); archival/GTD addenda; internal notes.



---

# 7.5 Document & Record Archival — Detailed Spec

> Scope: Codifies vision‑level, implementation‑agnostic requirements for managing scanned correspondence, financial statements, contracts/policies, memberships, health/pet/property records, and extends adjacent areas (collectable online content; taxonomy; health workspace; GTD workflows). Examples name realms like “Kai, KaGa, LuMaPa, Intimate” to illustrate **user‑defined realm sets**; the system MUST remain **generic** and allow any realm names.

## 7.5.1 Concepts & Item Types (Documents & Records)
- Represent personal records as **typed Items** under a **Document/Record** umbrella.
- **Minimum subtypes** (extensible):
  - `FinancialStatement` (bank/broker/credit‑card statements)
  - `Contract/Policy` (contracts, policies, cancellations/renewals)
  - `MembershipRecord` (associations, clubs, unions)
  - `HealthRecord` (letters, findings, referrals, vaccination proofs)
  - `PetRecord` (vet letters, vaccination proofs)
  - `PropertyRecord` (ownership, warranties, deeds)
  - `GenericDocument` (fallback)
- Future subtypes may be added **without breaking existing data**; treat schemas as semver‑versioned with migrations (see FR‑022).

## 7.5.2 Realms & Sensitivity (Generic, User‑Defined)
- Support arbitrary **user‑defined realm sets** (e.g., *Kai*, *KaGa*, *LuMaPa*, and a separate encrypted *Intimate* realm). 
- Every Item belongs to **exactly one realm** and carries a **sensitivity label** in `{low, normal, high, secret}` (configurable enumerations). 
- Session modes (e.g., lightweight/public) MUST honor realm + sensitivity to **hide, degrade, or exclude** items accordingly.

## 7.5.3 Capture, Preservation & Integrity
- Preserve the **immutable master** of each upload/ingest (e.g., scanned PDF). 
- Track **capture_time** and **document_date** independently.
- Record **integrity checksums** per stored file; provide on‑demand integrity verification.
- Where available, record **digital signature** presence/validity and **PDF/A** conformance (best‑effort; tooling not mandated).

## 7.5.4 Indexing & Discoverability
- Make archived documents searchable by issuer/sender, title, tags, subtype, document_date, capture_time, realm, sensitivity; provide **full‑text** over OCR/embedded text.
- Optionally map **folder path segments → tags** to aid discovery; do **not** require renaming existing folders.
- Support **saved collections/filters** (e.g., “all KaGa bank statements 2020–2024”) respecting current realm cap.

## 7.5.5 Periodic Series & Completeness
- For periodic Items (e.g., monthly statements), support **series awareness** (year/sequence/month) and detect **gaps**.
- Surface gaps as reviewable **tasks/alerts** with links to the relevant Account/Series where available.

## 7.5.6 Relationships to Durable Entities (Vision Level)
- Permit linking documents to **Durable Entities** (e.g., `Account`, `Policy`, `Membership`, `Property`) to enable richer queries and completeness checks.
- Creation of Durable Entities is **optional and incremental**; absence must not block filing or discovery.

## 7.5.7 Automation (Lightweight, Rule‑Based)
- Allow **non‑destructive ingestion rules**: categorize by path/filename patterns; auto‑tag by issuer/year; optional post‑ingest actions.
- Support **watched locations** per realm; renaming of existing files is **not required**.

## 7.5.8 Redaction & Export Profiles
- Provide **export profiles** that define default redactions (e.g., mask IBAN/address) when sharing outside the owning realm.
- Exports must be **reproducible** (same inputs → same outputs) and must **not modify** archived masters.

## 7.5.9 Access Transparency (Privacy‑Preserving)
- Maintain optional, minimal **access logs** per Item (e.g., last opened/exported, actor within household context); scope and retention are **per realm/sensitivity** policy.

## 7.5.10 Storage Strategy (Documents & Records)
- Large binaries reside in bulk storage suited for long‑term retention.
- The **catalog/manifest** stores lightweight metadata and references to files; avoid unnecessary duplication.
- Support **deduplication by checksum** across user‑visible folders **without forcing physical relocations**.

## 7.5.11 Migration & Existing Structure Tolerance
- Ingest and index documents **in place**; no forced canonical names.
- Any normalization/renaming is **optional, reversible, and user‑driven**.

## 7.5.12 NFRs (Scope‑Specific)
- **Local‑first** and offline‑capable search/retrieval within a realm.
- **No‑regret**: adding subtypes/entities never invalidates earlier archives.
- **Safety**: operations that may reveal sensitive content are gated by explicit action and realm/sensitivity policy.

## 7.5.13 Success Criteria (Documents & Records)
- File/find/retrieve a target document in **≤3 actions** via issuer + year (+ optional free text).
- Periodic series exhibit **no unnoticed gaps**.
- Sensitive items from a realm do **not** appear in lightweight/public sessions unless explicitly allowed.
- One‑click **export bundles** (e.g., tax/insurance) follow a redaction profile.
- **Originals preserved**; integrity demonstrable via checksums (and signature status where present).

---

### 7.6.1 Collectable Online Content — Extended Requirements
> Extends Section 7.6 with vision‑level requirements subsuming the Personal Content Archival Assistant. 

### 7.6.1.1 Concepts & Item Types
- Support typed Items under **Collectable Content**: `Story`, `Game`, `Webcomic`, `Thread` (extensible).
- Types may declare normalized artifacts (e.g., Story→Markdown chapters, Webcomic→CBZ) without mandating internal tool choices.

### 7.6.1.2 Source & Adapter Model
- Provide **Source Adapters** (per site/API) and **Scraping Methods** (HTTP, cookie‑backed, headless). 
- Adapter selection is **rule‑based** (by URL + type) and discoverable at runtime.
- Adapters declare **capabilities/requirements** (login, JS rendering, anti‑bot, rate limits).

### 7.6.1.3 Ethics, Consent & Compliance
- Per‑site **rules**: respect robots/TOS, throttling, allow/deny lists.
- **Credentials/cookies** are stored **per realm** with consent, scope, and expiry controls.

### 7.6.1.4 Capture, Versioning & Provenance
- Each capture/update records: source URLs, timestamps, adapter/method IDs, input hashes, change reason.
- Preserve originals (HTML/images/zips); normalized outputs are additional derivatives.
- Aim for **reproducible normalization** (same inputs → same outputs).

### 7.6.1.5 Update Semantics & Scheduling
- Support scheduled/on‑demand **update checks**; “update” = any significant content/metadata delta per type.
- Ensure **idempotent** updates; avoid duplicates.

### 7.6.1.6 Media Preservation & Packaging
- Support **lossless** media archival; deterministic packaging for reader outputs (e.g., CBZ page order guarantees).

### 7.6.1.7 Relationships & Series
- Support cross‑links (e.g., Game ↔ Forum Thread ↔ Patch Notes) and **series** constructs (chapters/issues with order/completeness checks).

### 7.6.1.8 Indexing & Queries
- Minimum filters: title/author/site, tags, language, completion status (Stories), version (Games), chapter/issue ranges, forum/board (Threads), update status, **last_checked**.
- Provide offline **full‑text** over normalized text and key metadata.

### 7.6.1.9 Automation & Failure Handling
- Declarative pipelines: on new URL → classify → select adapter → capture → normalize → tag → file.
- Failures (captchas, paywalls, consent prompts) create **review tasks** with retry/backoff policies.

### 7.6.1.10 Realms, Safety & Isolation
- Isolate network/proxy/cookie context **per realm**; sandbox headless/browser methods.
- Flag downloaded executables/archives for user review before execution.

### 7.6.1.11 Migration Guarantees
- Import existing catalogs/folder layouts without renaming; preserve prior IDs where feasible.
- Schema evolution is **no‑regret**; additive changes must not invalidate earlier captures.

### 7.6.1.12 Licensing & Attribution
- When known, store **license/usage/attribution** metadata and surface in exports.

### 7.6.1.13 Success Criteria
- Adding a URL yields a correctly classified Item, captured and viewable offline in **≤2 actions**.
- Update checks detect/apply changes without duplication; normalized outputs deterministic; originals preserved.
- Migration maintains identities/folder structure without forced re‑downloads.

---

### 7.4.1 Tagging & Flexible Taxonomy — Extended Requirements
> Complements Sections 7 & 11 with first‑class Tag Items and governance.

### 7.4.1.1 Principles
- **First‑class Tags** as Items with identity, metadata, and history (not mere strings).
- **Schema‑evolution friendly**; tolerate add/rename/merge/split/hierarchy changes without breaking Items.
- **Type‑aware but optional** vocabularies; cross‑type tags permitted; ontology‑light.

### 7.4.1.2 Tag Item (conceptual fields)
- `id` (stable), `name`, `slug`, `description?`
- `scope` (global | realm | type‑specific)
- `applies_to_types[]`, `parents[]`, `aliases[]`, `status` (active|deprecated|merged|split)
- `lineage`, `created_at`, `updated_at`, `governance`

### 7.4.1.3 Operations & Governance
- Support **rename, merge, split, deprecate, move, alias add/remove** with lineage and redirects.
- Realm/role‑scoped edit rights; global tags may require elevated permission.

### 7.4.1.4 Attaching Tags to Items
- Multi‑vocabulary tagging (e.g., `story:romance`, `game:RPG`, `finance:issuer/bankX`).
- Record `who/when/source` and optional `confidence` for human‑in‑the‑loop review.
- Queries may **expand hierarchy** (configurable) and support boolean logic.

### 7.4.1.5 Automation & Mass Tagging
- **Rule‑based tagging** (patterns, metadata, OCR/ML hints) with **dry‑run** and **review queues**.
- Bulk attach/detach/replace with filters, pagination, and **undo**; record provenance and confidence.

### 7.4.1.6 Per‑Type Vocabularies & Namespaces
- Allow **type‑specific vocabularies** (e.g., Story vs Game vs Financial) alongside global tags.
- Namespaces (e.g., `story:character/*`, `game:platform/*`, `finance:issuer/*`).

### 7.4.1.7 Query & Indexing Semantics
- Exact tag, hierarchical expansion, boolean combos, alias resolution, **as‑of** historical evaluation.
- Facets with counts by tag and hierarchy level, scoped by realm/type.

### 7.4.1.8 Versioning & Snapshots
- **Tag catalog snapshots** for reproducible exports and longitudinal analysis.
- **Time‑versioned** Item‑tag links for historical views.

### 7.4.1.9 Migration & Compatibility
- Import free‑form tags as Tag Items; consolidate duplicates via aliasing.
- Import legacy category trees as hierarchical tags without enforcing 1:1 mapping.

### 7.4.1.10 Success Criteria
- Rename/merge/split tags without breaking queries or losing history.
- Human‑in‑the‑loop mass tagging achieves high recall with controlled precision.
- Distinct vocabularies per type coexist with cross‑type discovery; historical queries remain stable.

---

### 7.7.1 Personal Health & Metrics Workspace — Extended
> Adds health data organization/analysis requirements.

### 7.7.1.1 Concepts & Item Types
- **Measurement**, **Series/Dataset**, **Device/Source**, **Analysis Artifact**, **Visualization Artifact** as first‑class Items.

### 7.7.1.2 Realms, Sensitivity & Privacy
- Health data defaults to most restrictive sensitivity; may use an **Intimate** realm; sharing/export is **opt‑in** with redaction/anonymization profiles.

### 7.7.1.3 Capture & Ingestion
- Ingest device/lab exports (CSV/XLS/XLSX/ZIP); preserve **immutable masters**.
- Support **schema mapping**, **unit normalization**, and **time‑zone handling**; record provenance and non‑destructive transforms.
- Optional watched locations per realm; rule‑based routing to Datasets.

### 7.7.1.4 Reproducibility & Provenance
- Analysis/Visualization Artifacts record inputs, execution time, and parameters to enable **re‑runs**; allow short **method notes**.

### 7.7.1.5 Data Quality & Validation
- Validate required fields, ranges, units, duplicates, missingness; allow **calibration offsets** with rationale.

### 7.7.1.6 Query, Review & Exploration
- Filters and charts by time range, tags, context, device/source, medication periods, and events; support saved **views/collections**.

### 7.7.1.7 Automation & Alerts (Optional)
- Threshold‑based alerts and **review tasks** for anomalies; schedulable periodic imports/checks.

### 7.7.1.8 Tagging & Classification
- Use first‑class Tagging with health namespaces (e.g., `health:metric/bloodpressure`, `health:lab/lipid_panel`).

### 7.7.1.9 Export & Sharing
- **Anonymized exports** and **doctor‑friendly summaries**; reproducible; masters untouched.

### 7.7.1.10 Migration & Existing Structure
- Index existing mixed folders (raw data, scripts, notebooks, notes) **in place**; normalization is optional/non‑destructive.
- Import legacy CSV/XLS via mapping rules; no forced column renames.

### 7.7.1.11 NFRs & Success
- Local‑first processing; treat identifying data per sensitivity/realm policy.
- **Success:** import → normalized charts in ≤2 actions; raw/normalized/analysis artifacts traceably linked; reruns deterministic; one‑action anonymized exports from profiles.

---

### 7.8.1 Personal Workflow & GTD‑Inspired Automation — Extended
> Adds inbox, tasks/projects, routines, ingestion scheduling, and rules.

### 7.8.1.1 Core Entities
- **Task** (title, notes, status, priority A–E, due/start, snooze, estimate/actual, assignee, contexts, tags, links, attachments, timestamps)
- **Project** (goal, status, owner, deadline?, children)
- **Checklist / Template** (reusable lists; instantiable)
- **Routine** (recurring Tasks; cadence; streak/counter)
- **Journal Entry** (daily notes; links)

### 7.8.1.2 States & Transitions
- GTD states: **Inbox, Next, Waiting For, Scheduled, Recurring, Someday, Blocked, Done, Obsolete**; track provenance/history on changes.

### 7.8.1.3 Dates, Recurrence & Counters
- Support `due`/`start`, windows, **RRULEs**, and behaviors (**skip/snooze/catch‑up**); support counters (e.g., `0/3` per period).

### 7.8.1.4 Contexts, Tags & Relations
- Use first‑class Tags and **Contexts** (e.g., `@home`, `@money`); link Tasks to Items (Documents, Datasets, Content) for task‑centric navigation.

### 7.8.1.5 Inbox & Capture
- Frictionless **Inbox** (notes/links/files/voice/text) across devices; triage to Task/Project/Journal or link to existing Items **non‑destructively**.

### 7.8.1.6 Workflow Templates (Illustrative)
- Examples like “Process Incoming Mail”, “Start/End of Day” are supported via user‑editable templates instantiable on demand/schedule.

### 7.8.1.7 Document/Data Ingestion Scheduling
- Maintain **ingestion sources** with frequencies (e.g., monthly payslips, yearly policies, weekly trading exports) and realm association.
- Surface **due/overdue** ingestion checks as Tasks; record completion with links to resulting Items.

### 7.8.1.8 Automation & Rules
- Declarative rules: auto‑tagging, inbox routing, follow‑up Task creation, and capture triggers (e.g., “when BP export appears, append to Dataset”).
- Rules are versioned, auditable, and realm‑scoped; risky actions require confirmation.

### 7.8.1.9 Views & Queries
- Filters: list/state, due/start windows, priority, context, realm, tag, linked Item types, overdue; support saved **perspectives** (e.g., “Next @home this week”).

### 7.8.1.10 Realms & Sensitivity
- Tasks/Projects/Journals belong to a realm; inherit sensitivity policies; cross‑realm linking requires explicit consent.

### 7.8.1.11 Migration & Compatibility
- Import legacy text/markdown/CSV; preserve IDs where feasible; map contexts/tags.

### 7.8.1.12 Success Criteria
- Inbox triage in **≤2 actions**; routines show streaks/counters with easy catch‑up.
- Ingestion sources → actionable reminders linked to resulting archives.
- One‑click from Task to related document/dataset/thread.

