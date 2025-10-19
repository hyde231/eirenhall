# Governance & Safety Rails

- Personas operate under **realm/sensitivity** with default-deny egress.
- **Sandboxed proposals:** Advisor/Coder output ADRs/PRs with tests; no direct live mutations.
- **Promotion gates:** human approval, semver bump, migration+rollback plan.
- **Audit:** immutable provenance for schema/tag/realm changes, exports, rules.
