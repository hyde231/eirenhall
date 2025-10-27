# ADR-002: Schema versioning & migrations

- Status: Accepted
- Date: 2025-10-21
- Deciders: Eirenhall core maintainers
- Related work: docs/specs/capability_contracts.md, docs/specs/metadata_governance.md, schema/item_base.json, scripts/validate_schema.py

## Context

Kki’s registry evolves continuously through schema, capability, and derived
definition changes. We already publish semantic versioning guidance in the specs
but lack an enforced workflow tying documentation, code, and tests together.
Without consistent change control we risk introducing breaking schema updates
that invalidate fixtures, regress automation, or corrupt captures. We also need
reliable tooling to detect schema drift during pull requests.

## Decision

We adopt the following versioning and migration workflow:

1. **Semantic versioning:** Every schema or capability document declares a
   `version` using MAJOR.MINOR.PATCH. Breaking changes require a major bump,
   additive backwards-compatible changes require a minor bump, documentation or
   constraint clarifications use patch.
2. **Change proposals:** Breaking changes or new schema families must ship with
   either an ADR or a change summary in `docs/specs/CHANGELOG.md` (to be added)
   and include migration guidance in the relevant spec.
3. **Migration manifests:** Structural changes that impact stored items must
   provide playbooks under `docs/specs/migrations/` and optional automation
   scripts in `scripts/migrations/`.
4. **CI enforcement:** A GitHub Actions workflow runs `scripts/validate_schema.py`
   and the pytest suite. The workflow fails when fixtures violate schemas or
   when manifests lack the expected version bump (script TBD).
5. **Traceability:** Requirements referencing schema behaviour must include a
   traceability entry mapping to spec sections and test IDs (see spec scaffold).

## Consequences

Positive:

- Automated validation prevents silent schema regressions.
- Contributors follow a predictable process for deprecations and migrations.
- Release notes draw directly from ADRs and migration manifests.

Trade-offs:

- CI gate increases pull request feedback time, especially when optional
  dependencies (jsonschema, PyYAML) need installation.
- Writing migration guidance adds overhead for seemingly small changes.

Follow-up work:

- Extend `scripts/validate_schema.py` to enforce version bumps when schemas
  change (tracked as an enhancement).
- Create `docs/specs/CHANGELOG.md` to centralise schema evolution notes.
