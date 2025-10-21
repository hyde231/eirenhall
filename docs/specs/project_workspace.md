# Project Workspace Specification

Defines the structure and behavior of the `project` item type introduced in FR-042.
Projects act as organizing hubs that align tasks, documents, correspondence, and
dashboards around a shared outcome.

## Objectives
- Provide a canonical place to track project status, stage, health, and timeline.
- Aggregate related artifacts (tasks, wiki entries, correspondence, dashboards,
  saved searches) via relations and curated widgets.
- Surface progress rollups and saved-search widgets automatically through the
  `projects.workspace` capability.
- Ensure exports/imports retain project metadata, linked artifacts, and derived
  progress values without manual mapping.

## Item Envelope
Projects reuse `item_base.json` with `item_type = "project"`. Core fields:

| Field                | Schema                               | Notes |
| -------------------- | ------------------------------------- | ----- |
| `fields.summary`     | `schema/fields/project_summary.json` | Status, stage, health, lead, dates, progress rollup, description. |
| `fields.objectives`  | `rich_text.json`                      | Optional narrative goals, constraints, or scope statements. |
| `fields.links`       | `link.json[]`                         | Curated external/internal references (standards, repos, docs). |
| `fields.related`     | `object_reference.json[]`             | Pinned related artifacts (primary datasets, automations, etc.). |
| `fields.notes`       | `rich_text.json`                      | Scratchpad for ad-hoc commentary, interim data, or future schema candidates (links normalize via the standard backlink pipeline). |
| `metadata.cap.projects.workspace` | Capability-specific metadata (e.g., widget layout presets). | Stored according to capability contract. |

Projects rely on the `projects.workspace` capability to unlock dashboard widgets,
saved search embedding, and automatic progress summaries. Removing the capability
collapses those affordances while preserving raw data.

## Suggested Relations
- **Tasks:** `object_reference` entries targeting task items, optionally filtered
  by status for progress rollups.
- **Correspondence:** Links to `correspondence` items that influence project scope
  (e.g., contracts, stakeholder letters).
- **Conversation Threads:** Links to `conversation_thread` items that capture
  ongoing discussions or decisions.
- **Dashboards & Saved Searches:** `related_saved_searches` within
  `project_summary` reference saved queries that populate widgets.

## Derived & Reporting
- `derived.progress_summary` should populate from linked tasks or manually
  provided metrics to keep UI tiles in sync.
- Additional derived metrics (budget burn, risk count) can be surfaced under
  `metadata.sys.project` namespaces once defined.

## Exports
Markdown exports include:
- `content.md` with the narrative fields (`summary.description`, `objectives`)
  and inline tokens for structured metrics.
- `objects.json` entries for `std.project.summary` and linked references so that
  round-trip imports restore relationships.
- Optional embedding of saved-search queries as tokens for downstream rebuild.

## Next Steps
- Implement capability-specific metadata schema (layout presets, widget configuration).
- Define derived evaluators that compute `progress_summary` from linked tasks.
- Extend dashboard defaults to render project widgets (rollup cards, timeline,
  open correspondence list).
