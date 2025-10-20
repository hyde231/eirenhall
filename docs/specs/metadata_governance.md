# Metadata Governance

Defines how metadata attached to kernel items is named, stored, evolved, and
validated. Complements the envelope description in `docs/specs/item_schema.md`
and the naming rules in `docs/specs/naming_conventions.md`.

## Scope & Objectives
- Provide a taxonomy for metadata namespaces (`sys.*`, `cap.<capability>.*`,
  `ext.<vendor>.*`, `tmp.*`) and guardrails for extending them.
- Describe lifecycle expectations: registration, review, deprecation, and audit.
- Specify storage and validation constraints applied by schemas and tooling.
- Outline how metadata is surfaced to clients and how sensitive content is
  protected across realms and sensitivities.

## Namespace Taxonomy
Metadata keys must conform to the pattern enforced by `item_base.json`. The
top-level namespace conveys ownership and lifecycle:

| Namespace | Owner | Characteristics | Typical Examples |
| --- | --- | --- | --- |
| `sys.<category>` | Core platform | Stable, versioned by platform; breaking changes require migration plan. | `sys.last_indexed_at`, `sys.owner_team` |
| `cap.<capability_key>.<attribute>` | Capability plugin declaring the feature | Changes track capability versioning; values scoped to capability configuration. | `cap.editor.collab.autosave`, `cap.tasks.board.wip_limit` |
| `ext.<vendor_slug>.<attribute>` | External integration maintainer | Namespaced per integration; additions require integration ADR; removal requires migration/export plan. | `ext.crm.record_id`, `ext.jira.issue_key` |
| `tmp.<category>` | Ephemeral processors & caches | Expire automatically; must tolerate eviction and realm purges; never relied upon by persistence flows. | `tmp.previewer.session`, `tmp.import.draft_id` |

### Naming Conventions
- `<category>` and `<attribute>` components use `lower_snake_case` or
  hyphen-separated slugs. Avoid camelCase and uppercase acronyms.
- Capability keys mirror the identifiers defined in the capability manifest
  (e.g. `editor.collab`). Additional segments describe nested settings.
- Vendor slugs are registered once per integration and reused across schemas,
  scripts, and docs.

## Registration & Change Control
1. **Proposal:** Authors document new metadata keys in a short RFC or ADR,
   including purpose, value shape, retention expectations, and realm impact.
2. **Review:** Core maintainers validate naming, namespace choice, data
   sensitivity, and cross-schema reuse. Capability metadata requires approval
   from the corresponding capability owner.
3. **Schema Update:** `item_base.json` or capability-specific schemas are
   updated if new shapes or validation rules are required.
4. **Change Log:** Additions and deprecations are logged in
   `docs/specs/metadata_registry.md` (to be introduced) or the relevant
   integration/capability documentation.
5. **Deprecation:** Mark legacy keys with `sys.deprecated_at` metadata and
   publish migration steps before removal. Keep readers tolerant for at least
   one release cycle.

## Storage & Validation Rules
- Metadata values can be primitives, objects, or arrays but must stay within the
  namespace boundary (`cap.tasks.board.{...}` may contain nested objects).
- Sensitive metadata inherits the item's realm/sensitivity. Plugins must not
  down-scope metadata without authorization checks.
- Link tracking metadata (`metadata.sys.links`) follows the schema described in
  the [Linking & Backlink Specification](linking_and_backlinks.md).
- Inclusion metadata (`metadata.sys.includes.*`) records dynamic value embeds,
  static copies, and destination contexts as defined in the linking spec.
- Validation:
  - Platform metadata is enforced via JSON Schema refs.
  - Capability metadata is validated by the capability contract (see
    `docs/specs/capability_contracts.md` once available).
  - Integrations provide schema snippets or runtime validators that run during
    ingestion/sync.
- Metadata keys should be present only when values are meaningful; omit keys
  rather than storing nulls, unless a capability explicitly requires a null to
  signal tri-state behavior.

## Access & Auditing
- Access policies mirror those of the parent item; realm crossings require
  explicit permission grants.
- Mutations to `sys.*` and `cap.*` namespaces are logged with actor, timestamp,
  and change summary. Integrations must surface their own audit trail in
  addition to core logging.
- Derived values referencing metadata must record provenance (via
  `metadata.sys.provenance[*]`) to facilitate traceability.

## Tooling & Automation
- Registry loader checks enforce namespace compliance when loading schema field
  definitions or capability manifests.
- Lint commands (to be added) will scan for unregistered metadata keys in code,
  fixtures, and tests.
- Import/export tooling must preserve metadata verbatim, retaining namespace
  structure. External exports may redact `tmp.*` keys by default.

## Extension Checklist
When adding metadata:
1. Verify the namespace selection against this document.
2. Register or reuse the capability/vendor slug as required.
3. Update schemas or validators to enforce value shape.
4. Document the key (purpose, data type, retention) in integration or capability
   docs.
5. Ensure tests/fixtures cover the new key and respect the naming pattern.

Following this governance keeps metadata predictable across the PoC and future
milestones, enabling automation, auditing, and consistent UX affordances.
