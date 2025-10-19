# Risks & Mitigations

| ID | Risk | Impact | Likelihood | Mitigation |
| --- | --- | --- | --- | --- |
| R‑01 | Model/code assist quality insufficient | High | Med | Escalate model size; tests; human review gates; keep models swappable/interchangeable |
| R‑02 | Power mgmt flakiness (WoL/sleep) | Med | Med | Health checks; conservative timers; manual override |
| R‑03 | Data leakage via misconfig | High | Med | Realm-scoped stores; default-deny egress; leakage tests in CI |
| R‑04 | Key/backup failure | High | Low | Offline encrypted backups; restore drills; escrow policy (not for Intimate) |
| R‑05 | Vector/index bloat | Med | Med | Distillation/compaction; tiered storage; cache |
