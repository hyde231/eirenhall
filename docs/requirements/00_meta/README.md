# Document Meta

This chapter captures the meta-information for the System X requirements set. It preserves the source context from the v0.5 consolidated draft while documenting how the material is now organized in the `docs/requirements` tree.

## Mini Table of Contents

1. Vision & Goals (`../01_vision/`)
2. Stakeholders (`../02_stakeholders/`)
3. Scope (`../03_scope/`)
4. User & Use Cases (`../04_users/`)
5. Functional Requirements (`../05_functional/`)
6. Non-Functional Requirements (`../06_non_functional/`)
7. Data & Information Architecture (`../07_data_architecture/`)
8. Interfaces & Integrations (`../08_integrations/`)
9. UX Principles & Views (`../09_ux/`)
10. Governance & Safety Rails (`../10_governance/`)
11. Risks & Mitigations (`../11_risks/`)
12. Roadmap & Releases (`../12_roadmap/`)
13. Requirement Backlog (`../13_backlog/`)
14. Acceptance Criteria Patterns (`../14_acceptance/`)
15. Glossary (`../15_glossary/`)
16. References (`../16_references/`)

## Change Log (v0.5)

- Merged vNext addendum into primary structure: Documents & Records now §7.5 (detailed); Collectable Content as §7.6.1; Tagging extended in §7.4.1; Health workspace §7.7.1; GTD workflows §7.8.1.
- Adopted session-level access gating; realms are organizational (GTD) only.
- Added mini Table of Contents for navigability.
- Clarified sensitivity levels: `public < family < partner < personal < private < intimate`.
- Cross-referenced FR sections to detailed narratives.

## Reconciliation Notes

- **Generic realm naming** (no personal names baked into models/paths/UI).
- **Assistant personas** (Librarian, System Advisor, Assistant, Coding Assistant) with clear scopes.
- **Versioned captures per URL** with **time-stamped local copies** and visible history.
- **Data sinks separation**: Git for metadata/docs/code; raw FS/object store for large binaries; optional git-annex/LFS; manifests tie all together.
- **Tiered caching** for Mini PC/Desktop/Server with policy knobs and metrics.
- **Series/completeness detection** for archival subtypes → tasks.
- **Redaction/export profiles** ensuring level-safe sharing; masters remain immutable.
- **Watched sources & ingestion scheduling** producing due/overdue tasks.
- **Provenance** across captures, tagging, automation, personas, and exports.

## Source Consolidation

Consolidated from: System X working draft; Combined Requirements (vNext); archival/GTD addenda; internal notes.
