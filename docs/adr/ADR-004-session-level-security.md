# ADR-004: Session-Level Access Gating and Organizational Realms

## Status
Accepted

## Context
Earlier drafts used realms as both organizational containers and security
boundaries, with optional realm-imposed sensitivity floors and item-level
inheritance. The practical need driving security is simpler: when collaborating
or presenting (e.g., with family present), the operator must be able to set a
session scope so that more sensitive content never surfaces. Using realms for
security increased conceptual and implementation complexity (inheritance,
per-realm policies/keys) without clear benefits for a single-household
deployment.

## Decision
Adopt a linear sensitivity model and enforce access at the session level.
- Items declare a single sensitivity (level).
- Sessions declare a maximum level (`max_level`).
- All reads/search/conversations MUST filter on `item.level <= session.max_level`.
- Realms are GTD-style organizational contexts (areas/projects) only.

Recommended levels: `public < family < partner < personal < private < intimate`.

## Consequences
- Item schema docs updated to remove realm-driven sensitivity inheritance.
- Realm fields remain for organization and storage paths; any `sensitivity_floor`
  is deprecated and MUST NOT be used.
- The legacy `sensitivity.inherited` flag is deprecated; treat as `false` by
  default until the JSON Schemas are revised.
- Functional requirements updated: FR-003 becomes session-level gating; FR-040
  becomes level presets and quick switching.
- Roadmap updated to validate the session model rather than per-realm keys.
- Metadata governance now references item-level sensitivity with session-level
  filtering; “realm crossings” are no longer a security concept.

## Alternatives Considered
- Realm-based security with inheritance: rejected for added complexity and UX
  overhead relative to the primary use case.
- Group-based ACLs: deferred; can be layered later if needed (e.g., friends,
  neighbors) without altering the session-level baseline.

## Follow-ups
- Update JSON Schemas to remove `realm.sensitivity_floor` and the `inherited`
  property from the sensitivity descriptor; align enums with the recommended
  level set.
- Implement session-level switch UI and ensure all surfaces respect it.

### Migration Notes (old → new levels)
- `public` → `public`
- `internal` → `personal`
- `confidential` → `private`
- `secret` → `intimate`
