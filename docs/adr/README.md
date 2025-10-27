# Architecture Decision Records

The ADR catalog captures long-lived architectural choices for Eirenhall. Each record
links back to the primary specifications and requirements that motivated the
decision so contributors can trace rationale and constraints quickly.

| ADR | Title | Status | When | Notes |
| --- | --- | --- | --- | --- |
| [ADR-000](ADR-000-data-sinks-and-replication.md) | Data sinks & replication strategy | Accepted | 2025-10-21 | Defines authoritative stores, replication tiers, and retention policy. |
| [ADR-001](ADR-001-agent-capability-model.md) | Agent capability model & governance | Accepted | 2025-10-21 | Codifies persona authorities and human approval checkpoints. |
| [ADR-002](ADR-002-schema-versioning-and-migrations.md) | Schema versioning & migrations | Accepted | 2025-10-21 | Establishes compatibility rules, migration workflow, and CI guards. |
| [ADR-003](ADR-003-conflict-resolution-and-offline-policy.md) | Conflict resolution & offline policy | Accepted | 2025-10-21 | Documents sync model, conflict semantics, and cache freshness. |

## Authoring guidelines

- Create new ADRs in numerical order using the `ADR-XYZ-title.md` naming
  pattern.
- Set the *Status* field to `Accepted`, `Superseded`, or `Proposed` depending on
  readiness. Drafts should live in feature branches until they exit review.
- Reference related specs, requirements, and test suites in the *Related work*
  section of each ADR to keep traceability intact.
