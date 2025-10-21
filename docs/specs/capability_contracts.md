# Capability Contracts

Defines how mix-in capabilities are declared, validated, and consumed across
kernel services. Complements the type bootstrap logic in
`src/kernel/types/base.py` and informs schema authors when extending item types.

## Objectives
- Provide a canonical capability data model covering identification, versioning,
  configuration, and supported affordances.
- Describe registration and lifecycle rules so capabilities remain compatible
  across releases.
- Outline validation responsibilities (schema vs. runtime) and default behaviors
  for clients that do not understand a capability.

## Capability Definition Model
Each capability is identified by a dot-delimited key following the naming rules
in `docs/specs/naming_conventions.md` (e.g. `editor.collab`, `tasks.board`). A
capability contract consists of:

| Field | Description |
| --- | --- |
| `key` | Capability identifier (`family.feature` or `family.feature.mode`). |
| `version` | Semantic version indicating contract compatibility. Clients may gate features on major/minor versions. |
| `summary` | Human-readable description of the behavior the capability unlocks. |
| `configuration_schema` | `$id` of the JSON Schema validating the capability's `config` payload. |
| `affordances` | Declares UI/workflow surfaces the capability enables (e.g. `list`, `detail`, `kanban`, `timeline`, `map`, `dashboard_widget`). |
| `dependencies` | Optional list of other capability keys required for this capability to function. |
| `events` | Optional list of domain events the capability emits or consumes (e.g. `task.completed`). |
| `metadata_namespace` | Root metadata namespace reserved for the capability (e.g. `cap.editor.collab`). |

Capability definitions live under `schema/capabilities/<key>.yaml` (directory to
be introduced) and are registered during bootstrap alongside type manifests.

## Declaring Capabilities on Item Types
- Type manifests (`schema/types/<type_key>.yaml`) list required capability keys
  in `capabilities: []`. Ordering is preserved for deterministic tooling output.
- During bootstrap, `kernel.types.bootstrap_types` verifies that every declared
  capability is registered and that dependencies are satisfied.
- Item payloads store capability activation under `capabilities.<key>` with
  these fields:
  - `enabled`: boolean gate; defaults to `false` when absent.
  - `version`: capability contract version the item expects.
  - `config`: object validated via the capability's configuration schema.
- Payloads may omit `config` when the capability contract marks it as optional.

## Lifecycle & Versioning
- Capability contracts follow semantic versioning:
  - **MAJOR**: incompatible behavioral or schema changes; requires migration
    path and version bump in all manifests.
  - **MINOR**: additive features; clients should tolerate absence.
  - **PATCH**: documentation or bugfix-level clarifications with no schema
    change.
- Type manifests pin the contract version. Automated tooling highlights when a
  newer major version exists so maintainers can schedule migrations.
- Deprecating a capability requires:
  1. Marking the contract as deprecated (`deprecated: true`, `replacement`).
  2. Updating type manifests to drop the capability.
  3. Providing data migrations to remove the capability's metadata/config.

## Validation & Testing
- JSON Schema validation ensures `config` payloads conform to the declared
  shape. Schemas reside in `schema/fields` or a dedicated
  `schema/capabilities/<key>_config.json` file.
- Runtime checks assert version compatibility and dependency satisfaction during
  ingestion/update.
- Automated tests should cover:
  - Bootstrapping types with and without the capability.
  - CLI flows (e.g. `scripts/run_poc.py`) invoking derived views or actions
    unlocked by the capability.
  - Serialization/parsing of the capability `config`.

## Client Expectations
- Clients must treat unknown capabilities as disabled. Absence of a capability
  entry is not equivalent to `enabled = false` (it may be unauthorized or not
  provisioned in the current realm).
- When `enabled = false`, clients should hide or disable the affordances while
  preserving configuration for future reactivation.
- Affordance declarations inform client feature toggles; e.g., a capability
  listing `kanban` allows rendering the task board view without additional
  custom wiring.

## Governance & Extensions
- New capability proposals include: use cases, expected affordances, config
  schema outline, metadata needs, and interaction with existing capabilities.
- Reviewers ensure naming, namespace reservations, and dependency chains abide
  by this spec.
- Capability owners maintain documentation under `docs/specs/capabilities/<key>.md`
  detailing user-facing behavior, default config, and sample payloads.

Adhering to this contract keeps capability-driven behavior predictable and lets
types inherit powerful UX features without bespoke code.

## Initial Capability Catalog
- `projects.workspace` (`schema/capabilities/projects.workspace.yaml`) - enables project rollups, dashboard widgets, and saved-search integrations for `project` items.
- `conversations.timeline` (`schema/capabilities/conversations.timeline.yaml`) - provides transcript timeline rendering, search facets, and excerpt linking for `conversation_thread` items.
- `correspondence.archive` (`schema/capabilities/correspondence.archive.yaml`) - unlocks ingestion, retention controls, and export workflows for `correspondence` items.
