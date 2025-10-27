# Capability: correspondence.archive

Unlocks ingestion dashboards, retention controls, and export workflows tailored to correspondence artifacts (letters, emails, portal downloads).

## Purpose
- Standardize how `correspondence` items expose archival and retention metadata.
- Advertise list/detail/archive affordances to UI and automation components.
- Define metadata namespace for retention status, ingestion provenance, and policy overrides.

## Affordances
- `list` – enables correspondence-specific list views (inbox, retention queue).
- `detail` – detail pages render normalized metadata (parties, timestamps, topics) and retention indicators.
- `archive` – surfaces archival operations such as export bundles, retention policy edits, and legal hold toggles.

## Metadata Namespace
`cap.correspondence.archive.*` – potential entries include:
- `cap.correspondence.archive.intake` – provenance of ingestion jobs (source folder, automation key).
- `cap.correspondence.archive.retention_status` – computed retention state (e.g., indefinite, legal_hold, scheduled_purge).
- `cap.correspondence.archive.review` – review queue metadata (assigned reviewer, due date).

## Events
- `correspondence.ingested` – emitted when a new correspondence item is registered.
- `correspondence.retention.updated` – signals changes to retention policy or legal hold.

## Configuration
`configuration_schema: null` – current workflow relies on global configuration. Future versions may introduce per-area (organizational) retention defaults or inbox routing rules.

## Usage
1. `correspondence` manifest includes `correspondence.archive`.
2. Ingestion pipeline populates `fields.entry` (`std.correspondence.entry`) and optional `fields.notes`.
3. UI components read capability metadata to display retention status and available actions.
4. Export tooling references capability events to schedule archival bundles.

## Future Considerations
- Formalize configuration schema for inbox routing or default retention policies.
- Add derived metrics for backlog counts, retention expiries, and review SLA tracking.
- Integrate automation hooks for remote intake or third-party connectors.
