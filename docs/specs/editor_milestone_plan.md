# Rich Text Editor & Knowledge Plugin Milestone Plan

Outlines the execution roadmap for embedding the delta-native rich-text editor, layering the generic knowledge plugin, and delivering the webcomic sample bundle. Aligns work with the programme milestones defined in `docs/requirements/12_roadmap`.

## Overview
- **Objective:** Provide a future-proof authoring surface that persists `std.rich_text` deltas, understands canonical link syntaxes, and exposes extension hooks for item-type specific plugins.
- **Scope:** Core editor integration, generic knowledge plugin, collaborative features, plugin packaging, and the exemplar webcomic bundle.
- **Not in scope (yet):** Mobile editing, AI-assisted authoring, or cloud sync of editor state; these feed later roadmap discussions once GA stabilises.

## Milestone Alignment

### Milestone M2 – Walking Skeleton
- **Goals**
  - Embed the delta-native editor shell into the generic item surface (`docs/specs/generic_item_surface.md`), covering basic create/edit for `document` and `wiki_entry`.
  - Expose registry APIs that surface type manifests, capability hints, and field metadata to the editor runtime.
  - Persist `std.rich_text` payloads end-to-end via the existing API, including backlink extraction on save.
- **Backlog links**
  - FR-046 (Generic item shell), FR-031 (Hierarchical browsing), FR-039 (Multi-value & annotation support, foundation).
- **Workstreams**
  1. Component integration: evaluate Quill, Slate+delta, TipTap adapters; choose one that emits Quill deltas.
  2. Registry service: extend `src/kernel/types` to expose schema-derived editor hints (sections, default widgets).
  3. Save pipeline: ensure ingestion/backlink jobs accept editor payloads, update tests under `tests/derived`.
  4. QA: smoke tests for editing docs/wiki, accessibility baseline (keyboard navigation, ARIA landmarks).
- **Exit criteria**
  - Editing flows for document/wiki validated locally with regression tests.
  - Registry API documented and consumed by editor to render dynamic field palettes.
  - No data regressions in existing PoC metrics (`scripts/run_poc.py`).

### Milestone M3 – Alpha
- **Goals**
  - Deliver the generic knowledge plugin handling wiki links, `kki://` URIs, include directives, Markdown export tokens.
  - Add action slot API + query builder integration for authoring flows.
  - Capture outbound link metadata and feed backlink engine.
- **Backlog links**
  - FR-046, FR-047 (Plugin-isolated extensions), FR-018 (Saved searches & query surfaces).
- **Workstreams**
  1. Parser/serializer: implement normaliser that converts inline syntaxes into canonical URIs.
  2. UI affordances: link insertion dialogs, include directive picker, hover previews.
  3. Metadata pipeline: update `metadata.sys.links.*` extraction jobs; add fixtures under `tests/fixtures/items`.
  4. Documentation: expand `docs/specs/generic_item_surface.md` and update export spec examples.
- **Exit criteria**
  - Round-trip tests for wiki links and includes within the editor.
  - Metadata capture verified in automated tests.
  - Action slots available for plugins; query builder interacts with editor context.

### Milestone M4 – Beta
- **Goals**
  - Introduce collaborative editing hooks (presence API, comment threads) tied to capability contracts.
  - Add capability-aware embeds (e.g., task summary cards) via plugin extension slots.
  - Ship the sample webcomic bundle to validate plugin packaging, sandbox boundaries, and deployment flow.
- **Backlog links**
  - FR-039 (Annotations), FR-047 (Plugin isolation), FR-019 (Automation hooks), FR-020 (Dashboards & embeds).
- **Workstreams**
  1. Collaboration core: integrate presence service, comment threads stored under `metadata.cap.*`.
  2. Embed framework: define registry contract for embed resolvers; build sample for tasks/projects.
  3. Webcomic bundle: author schema, derived metrics, ingestion routine, seed fixtures.
  4. Packaging: update `docs/specs/plugin_packaging.md` with editor-specific guidance; run sandbox tests.
- **Exit criteria**
  - Two-user collaborative editing demo with audit log.
  - Embed registry documented and used by sample plugin.
  - Webcomic plugin passes validation + sample ingestion script round-trips content.

### Milestone M5 – GA
- **Goals**
  - Harden accessibility, localisation, offline fallback for editor/plugins.
  - Finalise testing matrix, automation, and admin controls for enabling/disabling plugins per realm.
  - Conduct export/import regression for editor content and plugin-specific data.
- **Backlog links**
  - NFR-SEC (governance/audit), FR-018 (Exports), Operability objectives.
- **Workstreams**
  1. Accessibility audit: WCAG 2.1 AA sweep, localisation hooks for editor chrome.
  2. Admin tooling: surfaces to list active editor plugins, realm policy toggles, health diagnostics.
  3. Export fidelity: round-trip tests across `docs/specs/exports/kki_markdown_export.md` for editor tokens.
  4. Playbooks: author runbooks for enabling/disabling bundles, scaling collaboration services.
- **Exit criteria**
  - Accessibility sign-off, localisation strings externalised.
  - Admin UI/CLI controlling plugin availability in production.
  - Export/import tests green; documentation published in knowledge base.

## Webcomic Sample Plugin Blueprint
- **Item type:** `webcomic` (inherits `item_base.json`).
- **Primary fields**
  | Field | Schema | Notes |
  | --- | --- | --- |
  | `fields.base_url` | `schema/fields/url.json` | Canonical landing page. |
  | `fields.availability` | enum (`online`, `offline`) | Derived from reachability checks. |
  | `fields.status` | enum (`active`, `completed`, `abandoned`, `unknown`) | Manual/automated updates. |
  | `fields.synopsis` | `schema/fields/rich_text.json` | Markdown-like authoring via editor. |
  | `fields.artists[]` | composite (name, role, optional remark) leveraging `schema/fields/user_reference.json` or dedicated `artist_role` composite. |
  | `fields.cover_image` | `schema/fields/image_reference.json` | Stores media metadata. |
  | `fields.starting_date` / `fields.end_date` | `schema/fields/calendar_date.json` | End optional. |
  | `fields.last_update` | `schema/fields/timestamp.json` | Synced from scraper. |
  | `fields.pages[]` | `schema/fields/object_reference.json` | Links to page items if tracked individually. |
  | `fields.images[]` / `fields.thumbnails[]` | `schema/fields/file_reference.json` | Distinguish full-res vs thumbnail. |
  | `fields.language` | `schema/fields/locale.json` | IETF tag. |
  | `fields.tags[]` | `schema/fields/tag_list.json` | Topical categories. |
  | `fields.comment` | `schema/fields/rich_text.json` | Optional notes. |
  | `fields.rating` | `schema/fields/percentage.json` or custom rating. |
  | `fields.scraping` | composite { method, parameters } stored under capability namespace `cap.webcomic.scraper`. |
- **Capabilities**
  - `webcomic.library`: enables browse widgets and availability monitoring dashboards.
  - `webcomic.scraper`: governs scraping config visibility, diagnostics toggles, and automation hooks.
  - `alerts.subscribe`: optional for fans/operators to receive update notifications.
- **Derived metrics**
  - `chapter_count`, `page_count`, `days_since_update`, `uptime_ratio`.
  - Provenance captured to highlight data sources (scraper vs manual edits).
- **Automation hooks**
  - Scheduled scraper refresh producing events (`status_changed`, `new_page_detected`).
  - Availability monitoring raising alerts when `base_url` unreachable for N intervals.
- **Authoring experience**
  - Generic plugin surfaces role autocomplete for artists, availability/status toggles, media gallery management, and inline synopsis editing.
  - Diagnostics panel (opt-in) reveals scraping parameters—hidden by default.
- **Packaging**
  - Bundle ships with schema YAML, derived metrics definition, fixtures under `tests/fixtures/items/webcomic*.json`, ingestion script scaffolds, and UI extension manifest referencing editor affordances.

## Open Questions & Follow-ups
- Artist roles remain local to the webcomic bundle; no shared enum required for other media types.
- Scraped assets inherit the owning item's retention (default infinite) and link in the same relations block.
- Availability changes do not auto-create timeline entries; auditing is lightweight for this self-hosted deployment.
- Scraping configurations and rate limits are item/target-specific, while credentials are managed per realm.

## Next Actions
1. **Design Spike (M2):** Prototype editor integration with two candidate libraries and document trade-offs.
2. **Schema Draft (M3 prep):** Author initial `schema/types/webcomic.yaml` + field composites.
3. **Testing Plan:** Extend `tests/types/test_core_types.py` once the webcomic type registers.
4. **Operations Alignment:** Engage reliability team to plan scraper scheduling infrastructure for M4.
