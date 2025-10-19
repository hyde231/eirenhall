# Roadmap & Releases (Backlog-Aligned)

Each milestone now ties directly to backlog entries so progress can be tracked incrementally.

- **M1 Discovery (Weeks 1‑2):**
  - Establish storage + repository, realm model validation → groundwork for FR‑003, NFR‑SEC.
  - Document baselines for formats and data contracts → FR‑002, FR‑015, Formats & Compatibility commitments.
- **M2 Walking Skeleton (Weeks 3‑4):**
  - Deliver local-only capture loop with realm enforcement → FR‑001, FR‑014, FR‑018 (happy path).
  - Stand up telemetry + uptime checks → NFR‑PERF, Reliability targets.
- **M3 Alpha (Weeks 5‑7):**
  - Expand adapters and offline workflows → FR‑015, FR‑026, FR‑027.
  - Introduce plugin sandbox and automation hooks → FR‑016, FR‑019 (initial mass actions).
- **M4 Beta (Weeks 8‑10):**
  - Harden power-aware scheduling and tiered caching → FR‑006, FR‑027.
  - Enrich export capabilities and saved searches → FR‑018 (full scope), FR‑020.
- **M5 GA (Weeks 11‑12):**
  - Security/egress validation drills + key rotation → NFR‑SEC.
  - Operability polish: dashboards, runbooks, docs → Operability commitments, residual FR/NFR cleanup.

## Dependencies
- Wake-on-LAN readiness for FR‑006 and nightly maintenance windows.
- VPN availability for remote administration without violating FR‑001.
- Storage planning + per-realm key management ahead of M2 security tests.
