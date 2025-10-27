# ADR-001: Agent capability model & governance

- Status: Accepted
- Date: 2025-10-21
- Deciders: Eirenhall core maintainers
- Related work: docs/requirements/01_vision/README.md, docs/requirements/10_governance/README.md, personas/*.yaml (new)

## Context

Eirenhall relies on a suite of automation personas (Librarian, System Advisor,
Assistant, Coding Assistant) to draft changes, enrich data, and manage system
health. The requirements articulate high-level duties, but until now there was
no machine-readable contract describing the authority, data access, and
escalation behaviour for each persona. Without codifying these rules, it is easy
for tooling to overreach (e.g., auto-applying destructive changes) or for tests
to drift from governance intent.

## Decision

We introduce persona manifests stored under `personas/*.yaml`. Each manifest
declares:

- `id` and `name`.
- `summary` and `intended_outcomes`.
- `data_access`: session levels (max allowed), organizational realms, item types,
  and capability scopes the persona can read or mutate.
- `write_permissions`: enumerated actions (e.g., `propose_schema_change`,
  `apply_metadata_tag`) plus whether human approval is required.
- `escalation`: human checkpoints and conditions that force dry-run mode.
- `safety_rails`: non-negotiable prohibitions (no credential exfiltration, no
  auto-deletion, no financial trades).

A helper module will load manifests and expose guardrails to agent runners.
Tooling must default to `dry_run=true` for destructive actions and require human
approval toggles specified in the manifest before committing changes.

Governance expectations:

- Every automation persona is backed by a manifest and a regression test that
  simulates typical operations against sample data.
- Pull requests modifying manifests must include updated governance tests and,
  when raising privilege, an ADR addendum or risk assessment.
- Human approval gates are enforced via the workflow engine; agents cannot
  bypass them.

## Consequences

Positive:

- Governance rules are auditable and versioned alongside code.
- Tests can assert that personas stay within scope by loading manifests.
- Dry-run defaults dramatically reduce the blast radius of automation bugs.

Trade-offs:

- Authoring manifests adds upfront work for new personas.
- Operational tooling must integrate manifest parsing before executing actions,
  slightly increasing startup time and complexity.

Follow-up work:

- Implement manifest parser and validation in `src/kernel/governance/personas.py`
  (tracked separately).
- Add tests in `tests/personas/test_persona_manifests.py` to verify boundaries
  using fixtures.
