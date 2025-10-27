# UX Principles & Views

## UX Tenets
- **Generic views auto-derived from capabilities:** list/table (facets), detail, history (captures), reader mode (stories/threads), media panel (downloads/subtitles), card views, and annotations for all items; `Workflown` adds Kanban boards, `Schedulable` adds calendar/timeline views, and `Geocoded` adds map/heatmap visualizations.
- **Inputs:** paste box, watched folders, browser extension/bookmarklet, push-to-talk voice capture (local ASR), CLI (`eirenhall capture <url> --realm R --tags a,b`).
- **Collections:** saved searches (dynamic, first-class data type) and snapshots (static exports with manifests); curated primarily on desktop UI, viewable on mobile.
- **Exports:** handled via automation/maintenance flows; UX ensures discoverability of export status but not authoring.
- **APIs:** ingestion and automation endpoints expose the same collection/saved-search surfaces for tooling.
 - **Voice:** local TTS playback for confirmations and summaries when the conversations.voice capability is enabled.

## Interaction Design Principles

- **Uniform operability:** Every operation in the system is accessible via keyboard, mouse, and (future) conversational input.
- **Keyboard navigation:** Global shortcuts (`Ctrl+K`, `Alt+/`, `Esc`, `Ctrl+S`), focus cycling with arrows/tab, in-line editing, bulk selection, and undo/redo.
- **Mouse operation:** Drag & drop for objects/relations/file uploads, visual connectors (splines) in conversion views, context menus, tooltips, and gesture-based multi-selection.
- **Conversational mode (planned):** Natural-language data entry and updates, AI-assisted parsing of structured data from text/photos/PDFs/screenshots, and suggestions surfaced as diffs before confirmation.

## Widgets by Primitive Type

Each primitive data type maps to an interactive widget for desktop and mobile clients.

| Type | Widget | Key Features |
| --- | --- | --- |
| **Text** | Text field / textarea | Auto-grow, inline formatting, markdown preview |
| **Boolean** | Switch / checkbox | Keyboard toggle (Space), optional tri-state |
| **Date / Time / DateTime** | Calendar / time picker | Keyboard and quick-entry presets (e.g. "+1d") |
| **Duration** | Input with units | Supports relative format (e.g. "3h 15m") |
| **Measurement** | Numeric + unit selector | Auto unit conversion, unit search, grouping (mass, length, etc.) |
| **Percentage** | Numeric input or slider | Range 0–100%, fractional support |
| **Currency** | Numeric field + currency code dropdown | Exchange-rate lookup, symbol preview |
| **Enum / Tag** | Searchable dropdown / chip list | Scoped values, add new if permitted |
| **List / Multi-value** | Tokenized chips / sortable list editor | Drag-reorder, bulk add via paste/import, per-entry badges, inline creation for child records when schema permits |
| **Markdown / HTML** | Editor with preview | Optional syntax highlighting |
| **JSON / CSV** | Structured editor | Validation, schema hints, import/export |
| **URL** | Text field with metadata preview | Favicon, title lookup |
| **Image / Video / File / Folder** | Upload or picker | Drag-drop, thumbnail, hash dedupe |
| **Password** | Masked input | Strength indicator, generate button |
| **GeoPoint** | Map picker / coordinate input | Privacy level selector |
| **Ref / Relation** | Searchable reference field | Inline creation, relation visualization, stay-in-context editing |
| **Rating** | Star/slider/likert control | Configurable scale, half-step support, keyboard nudging |
| **Note / Annotation** | Rich-text comment thread | Mentions, resolve state, context breadcrumb |

## Conversion & Mapping Experience

- **AI assistance:** Parse unstructured inputs (OCR on photos/PDFs) and suggest field types and relations based on detected patterns (currencies, units, percentages, dates).
- **Guided mapping UI:** Left panel lists detected fields and inferred types; right panel shows the target schema; connections render as confidence-colored splines; saved "conversion recipes" remain editable and reusable.

## Presentation of Derived Values

- Derived fields display as read-only chips, inline cards, or secondary table columns that include hover/click explanations of the contributing source fields and formula.
- Tooltips and inspector panels surface the normalized units/currency used in the calculation and show when the value was last recomputed.
- UI affords quick navigation from a derived value back to its editable source fields (e.g., jump from BMI to height/weight) while preventing direct edits to the computed value itself.

## Accessibility & Internationalization

- WCAG 2.2 AA compliance with full ARIA labeling and screen-reader support.
- Locale-aware formatting for dates, numbers, units, and currencies.
- Multi-language labels and enum values with user-selectable display language.

## Extensible UI Plugins & Recipes

- Plugin system admits new field editors, visualizations, import/export widgets, and transformers.
- Conversion recipes are versioned artifacts that can be reused across collections and refined over time.

## 9.1 Saved Searches & Collections Specification

### Saved Search (Dynamic)
`id, name, owner, max_level, query_dsl, sort, limit?, schedule?`

- DSL: boolean over fields (`type, realm, tags, captured_at/published_at, plugin, duration, author, status`), operators (`=, !=, in, contains, regex?, range`). Session `max_level` is enforced implicitly; queries may still facet by `realm` for organization.
- Example: `type=webcomic AND captured_at>=2025-10-01`.

### Static Collection (Snapshot)
`id, name, realm, item_ids[], manifest` (checksums, capture ids, paths). Export: Markdown/CSV + assets.

## 9.2 Dashboards & Entry Pages

- **User-defined layouts:** Dashboards are composable canvases where operators place widgets sourced from saved searches, reports, quick links, session level switches, and pinned automations. Layout changes persist per user and can be duplicated or shared as templates.
- **Widget palette:** Provide widgets for saved search result lists, metric callouts, embedded documents/wiki sections, shortcut groups, and automation status cards. Widgets pull metadata hints from schemas (e.g., recommended fields, realm filters) to speed configuration.
- **Default experience:** Ship an initial dashboard that highlights a hierarchical browser spanning data items, metadata facets, and the schema registry, giving new operators an immediate overview without building a custom layout first.
- **Navigation parity with wikis:** Dashboards support inline editing, drag-and-drop reordering, and link previews so they function as living entry pages comparable to wiki home screens.
