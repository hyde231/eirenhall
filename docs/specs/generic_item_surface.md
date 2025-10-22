# Generic Item Surface Specification

Defines the baseline web surfaces (browse, query, view, edit) that every item
type enjoys by default. The goal is to ship a neutral UI shell that renders
any schema-driven type while allowing optional plugins to override or extend
behaviour for specialized deployments.

## Objectives
- Provide consistent list/detail/edit/pivot experiences driven solely by item
  schemas and capability metadata—no hand-written widgets required for new
  types.
- Keep the default UI neutral so a stock installation suits any operator,
  while enabling custom plugins to introduce richer views/editors without
  patching core code.
- Support capability-based affordances (timeline, dashboard, analytics) by
  loading optional components when the capability is present.
- Ensure plugin overrides can be disabled per realm or installation without
  affecting the generic shell.
- Ship curated starter layouts, saved queries, and optional plugin bundles that
  showcase value on day one while remaining entirely schema-driven and removable.

## Core Surfaces
1. **Browse View**
   - Paginated list/grid controlled by query parameters (type, realm, tag,
     capability). Columns derive from schema field metadata (`display`, `search` flags).
   - Supports quick filters, saved searches, and direct navigation to details.
2. **Query Builder**
   - Visual composer for filters/aggregations built from schema descriptors.
   - Exports queries as JSON for reuse (dashboards, automations).
3. **Detail View**
   - Presents item envelope (title, realm, sensitivity, capabilities) and fields
     grouped by schema hints (`section`, `order`).
   - For capabilities with registered view components (e.g., `conversations.timeline`),
     loads plugin-provided panels; otherwise renders metadata inspectors.
4. **Edit Mode**
   - Auto-generates forms for primitive/composite fields using schema types.
   - Supports inline diff preview and undo buffer before persisting.
   - Plugins may replace the editor for specific fields/capabilities via override hooks.

## Onboarding Bundles
- **Realm starter kits:** Provide optional presets that register schema combinations, saved searches, dashboards, and preconfigured surfaces for common scenarios (household command center, research notebook) without mutating the neutral core.
- **Template manifests:** Starter kits ship as signed manifests so operators can diff, audit, and roll back bundles; installation toggles occur per realm.
- **Capture shortcuts:** Offer quick actions and guided tours that call manifest-compliant ingestion scripts so operators store their first artifacts within minutes.

## Architecture
- **Surface Registry:** Core component that maps item types + capabilities to
  view/edit components. Defaults to generic renderer; plugin bundles register
  overrides with priority flags.
- **Schema Introspection:** Uses `schema/fields` metadata (`fieldType`,
  `capabilities`, `constraints`, localization hints) to pick renderers.
- **Plugin Loader:** Discovers packages declaring `surface.overrides` entries
  with dependency metadata; supports enabling/disabling per installation.
- **Isolation:** Overrides run inside sandboxed modules; missing plugins fall
  back to generic components automatically.

### Surface Registry Interfaces
- `register_surface(component, *, type=None, capability=None, priority=0)` –
  plugins call this to supply custom components. `type=None` targets all types,
  `capability=None` targets base views. Higher priority wins; ties fall back to
  generic component.
- `resolve_surface(type_key, capability, mode)` – returns the component chain
  (generic first, overrides layered) for a given item type, capability, and
  mode (`list`, `detail`, `edit`, `analytics`).
- `register_field_renderer(field_type, renderer)` – maps schema field metadata
  (`fieldType`, `dataType`, optional `ui.widget`) to reusable field widgets.
- `get_field_renderer(field_schema)` – selects renderer by inspecting schema
  metadata and capability hints; falls back to generic inspector/editor pairs.

Registry state lives in memory with hot-reload support when plugins change. The
CLI/UI expose `surface:list` and `surface:inspect` commands to audit active
overrides per installation.

### CRUD Workflow
1. **Create:** Generic editor builds an empty payload from schema defaults,
   validates client-side using JSON Schema, emits `create_item` API call, and
   refreshes list/detail view upon success. Plugins can hook `before_create`
   and `after_create` events.
2. **Read:** Browse/query surfaces call the item API with filters; detail view
   hydrates the full payload plus capability metadata. Optional capability
   panels fetch additional data on demand.
3. **Update:** Edit mode reflects current values, tracks field-level diffs, and
   submits patch payloads respecting `fields`, `metadata`, and capability
   config. Validators ensure derived fields remain read-only. Plugins can inject
   custom validation steps before commit.
4. **Delete/Archive:** Generic action menu includes archive/delete operations
   gated by capability checks (`manage`). Operators confirm via modal; audit log
   records actor, realm, and summary. Plugins can add soft-delete policies or
   override confirmation UX.

All CRUD flows pass through the same API layer, so new item types gain full
functionality once their schemas are registered—no bespoke UI work required.

## Extensibility Hooks
- **Component Override API:** Plugins can register custom components for:
  - Full item view/edit
  - Specific field types
  - Capability panels (e.g., timeline, dashboard widget)
- **Action Slots:** Generic views expose action slots (top bar, sidebar,
  contextual menus). Plugins contribute actions with declarative permissions
  and realm checks.
- **Theme Layer:** Base UI uses neutral theme tokens; plugins can supply custom
  palettes without altering layout logic.

## Rich Text Authoring Strategy
- **Adopt delta-native editor:** Embed an off-the-shelf rich text editor that speaks Quill-style delta operations so `fields.body` continues to persist the `std.rich_text` payload without lossy Markdown<->delta conversions.
- **Generic knowledge plugin:** Provide one extensible plugin that understands wiki links, `kki://` URIs, include directives, and Markdown export tokens. It consults the registered item types/capabilities at runtime, so new schemas appear automatically in link pickers and validation routines.
- **Plugin contract:** The core plugin supplies insertion menus, hover previews, and validation hooks. Type manifests (and future capability metadata) can contribute optional affordance hints via declarative descriptors rather than bespoke code.
- **Extension slots:** Specialized bundles can extend the generic plugin by registering additional resolvers (e.g., for capability panels or embeds) using the same surface registry, avoiding one-off editor forks.
- **Roadmap alignment:** Initial phase ships the editor shell and generic plugin focused on wiki/document authoring; later phases add collaborative cursors, comment tracks, and capability-aware embeds once the registry exposes richer metadata.

## Neutral Core Distribution
- Stock system bundles only generic components plus minimal capability panels
  for core item types (document/task/wiki/correspondence/project/contact).
- Personal or domain-specific experiences ship as optional plugins (e.g.,
  storytelling bundle, finance dashboards). They register additional schemas,
  ingestors, surfaces, and editors without changing defaults.
- Installers can choose plugin sets during setup; mutual exclusion rules ensure
  personal bundles never leak into deployments meant for friends/family unless
  explicitly enabled.

## Plugin Governance & Telemetry
- **Versioned manifests:** Every surface override and field renderer declares compatibility ranges, required capabilities, and migration hooks to prevent drift.
- **Health signals:** Collect heartbeat metrics (load success, render errors, degraded fallbacks) and expose them through the surface inspector plus exportable logs.
- **Automatic fallback:** When an override fails validation, the registry reverts to the generic renderer, flags the plugin, and prompts operators with remediation guidance.

## Testing Considerations
- UI smoke tests render each core type with only generic components enabled.
- Plugin integration tests ensure overrides respect fallback contracts.
- Regression tests validate that disabling a plugin reinstates generic
  behaviour without data loss.

## Roadmap
- Detailed milestone activities live in [editor_milestone_plan.md](editor_milestone_plan.md).
- **M2 Walking Skeleton:** Wire in the delta-native editor shell, support single-item editing for document/wiki types, persist rich-text deltas end-to-end, and land registry APIs so surfaces can query type manifests and capability hints.
- **M3 Alpha:** Ship the generic knowledge plugin with wiki link parsing, include directive handling, outbound link metadata capture, and editor affordances seeded from the registry; add action slot overrides and query builder needed for richer authoring flows. Bundle the first optional realm starter kit (household operations) with saved queries and dashboards to validate the onboarding story.
- **M4 Beta:** Deliver collaborative editing hooks, inline comment threads, capability-aware embeds, and the sample webcomic plugin to validate the extension story while exercising sandbox, packaging, and deployment steps. Introduce automated compatibility checks and health telemetry dashboards so plugin bundles remain trustworthy in production.
- **M5 GA:** Harden accessibility, localization, and offline fallbacks, complete regression coverage (surface registry, plugin contract, export round-trip), and polish admin tooling so operators can audit or disable editor plugins per realm.

## Sample Plugin: Webcomic Knowledge Bundle
- **Schema fields:** Title, base_url, availability, status, synopsis (rich text), artists (role-tagged list), cover_image, starting_date, end_date, last_update, pages, images, thumbnails, language, tags, comment, rating.
- **Operational metadata:** Optional technical block registering scraping_method, scraping_parameters, and health signals that default to hidden from the generic detail view unless the operator enables diagnostics mode.
- **Editor affordances:** Generic plugin surfaces autocomplete for artist roles, availability/status toggles, synopsis editor with preview, and collection widgets for pages/images/thumbnails; link pickers stay registry-driven so the plugin inherits future item types without new code.
- **Automation hooks:** Background jobs monitor base_url reachability to flip availability, refresh last_update from scraping results, and emit alerts when the scraping_method reports failures.
