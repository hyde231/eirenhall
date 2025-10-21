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

## Neutral Core Distribution
- Stock system bundles only generic components plus minimal capability panels
  for core item types (document/task/wiki/correspondence/project/contact).
- Personal or domain-specific experiences ship as optional plugins (e.g.,
  storytelling bundle, finance dashboards). They register additional schemas,
  ingestors, surfaces, and editors without changing defaults.
- Installers can choose plugin sets during setup; mutual exclusion rules ensure
  personal bundles never leak into deployments meant for friends/family unless
  explicitly enabled.

## Testing Considerations
- UI smoke tests render each core type with only generic components enabled.
- Plugin integration tests ensure overrides respect fallback contracts.
- Regression tests validate that disabling a plugin reinstates generic
  behaviour without data loss.

## Roadmap
- **Phase 1:** Implement surface registry, generic list/detail/edit pages,
  capability panel loading, and plugin discovery.
- **Phase 2:** Add query builder and action slot APIs, plus override priority
  controls.
- **Phase 3:** Deliver sample plugins (e.g., storytelling bundle) to validate
  isolation, packaging, and deployment flows.
