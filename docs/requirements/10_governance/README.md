# Governance & Safety Rails

- Personas operate under a session **max level** with default-deny egress.
- **Sandboxed proposals:** Advisor/Coder output ADRs/PRs with tests; no direct live mutations.
- **Promotion gates:** human approval, semver bump, migration+rollback plan.
- **Audit:** immutable provenance for schema/tag/level changes, exports, rules.
- **Delegated administration (optional):** Operators may organize content into areas/realms for GTD purposes. No realm lifecycle is required for security; session-level gating governs exposure.
- **Persona action matrix:** map capture/edit/export permissions per human and AI role; maintain as living governance artifact.

> Detailed audit log retention requirements are intentionally deferred until the system design stabilizes.
