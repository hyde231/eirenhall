# Capability: projects.workspace

Enables project workspaces to surface progress rollups, dashboard widgets, and saved-search integrations without custom wiring.

## Purpose
- Provide a canonical capability contract for `project` items.
- Advertise UI affordances (list/detail/dashboard) unlocked by the capability.
- Define metadata namespaces and expected configuration payloads (currently none).
- Describe integration points with related item types (tasks, correspondence, dashboards).

## Affordances
The capability declares the following surfaces:
- `list` – allows project items to appear in generic lists with progress indicators.
- `detail` – detail pages render project summary metrics, saved-search widgets, and related artifact panels.
- `dashboard` – enables placement of project KPIs and saved search widgets on dashboards.

## Metadata Namespace
`cap.projects.workspace.*` – reserved for capability-specific settings, such as:
- `cap.projects.workspace.widget_layout` – persisted layout configuration for project dashboard sections.
- `cap.projects.workspace.progress_overrides` – optional overrides for derived progress when manual adjustments are needed (future use).

## Events
- `project.progress.updated` – emitted when derived progress metrics change. Consumers can refresh dashboards or notify operators.

## Configuration
`configuration_schema: null` – no structured config is required initially. Future revisions may introduce widget layout definitions or default saved searches.

## Usage
1. Project item manifest (`schema/types/project.yaml`) includes `projects.workspace`.
2. UI reads `fields.summary` and related saved searches to populate widgets.
3. Derived metrics (progress summary, risk counts) feed the capability events.

## Future Considerations
- Introduce optional configuration schema for widget presets.
- Provide automation hooks to recompute progress from linked tasks periodically.
- Extend event set with budget or risk updates once metrics exist.
