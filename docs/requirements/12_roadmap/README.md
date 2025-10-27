# Roadmap & Releases (Backlog-Aligned)

Each milestone now ties directly to backlog entries so progress can be tracked incrementally.

- See [Milestone M1 Detailed Plan](./M1_detailed_plan.md) for a deeper breakdown of the discovery sprint deliverables.

Note: This roadmap reflects the simplified session model. Where older language
mentions “realm enforcement,” read it as “session-level enforcement.”

## Infrastructure Stream (Containers/VMs/WoL)

- M2 (Single-node baseline)
  - Stand up a single-node Docker Compose stack (can run on a desktop VM) for all core services.
  - Create Ansible roles and inventories for nodes (desktop GPU, NAS, Raspberry Pi orchestrator).
  - Seed lightweight observability (e.g., Netdata or Prometheus + node_exporter).

- M3 (Multi-node placement and power)
  - Introduce placement policy across nodes (desktop GPU, NAS, Pi orchestrator); verify routing and service discovery.
  - Implement Wake-on-LAN playbooks and tests; schedule maintenance windows for heavy jobs.
  - Document recovery procedures for orchestrator and storage services.

- M4 (Hardening and runbooks)
  - Harden power-aware scheduling (FR-006) and tiered caching (FR-027); validate metrics and thresholds.
  - Finalize backup/restore runbooks; exercise partial and full restore drills.
  - Polish dashboards for health and placement visibility.

- **M1 Discovery (Weeks 1‑2):**
  - Establish storage + repository, realm model validation → groundwork for FR‑003, NFR‑SEC.
  - Document baselines for formats and data contracts → FR‑002, FR‑015, Formats & Compatibility commitments.
  - Defer infrastructure enablement (WoL, orchestration, hardware prep) to M2+ so the PoC can focus on data and storage.
- **M2 Walking Skeleton (Weeks 3‑4):**
  - Deliver local-only capture loop with realm enforcement → FR‑001, FR‑014, FR‑018 (happy path).
  - Stand up telemetry + uptime checks → NFR‑PERF, Reliability targets.
- **M3 Alpha (Weeks 5‑7):**
  - Expand adapters and offline workflows → FR‑015, FR‑026, FR‑027.
  - Introduce plugin sandbox and automation hooks → FR‑016, FR‑019 (initial mass actions).
- **M4 Beta (Weeks 8–10):**
  - Harden power-aware scheduling and tiered caching → FR‑006, FR‑027.
  - Enrich export capabilities and saved searches → FR‑018 (full scope), FR‑020.
  - Deliver open-format export/import pipeline (bundle spec, CLI, rehydrate tests) → FR‑019, FR‑037.
- **M5 GA (Weeks 11‑12):**
  - Security/egress validation drills + key rotation → NFR‑SEC.
  - Operability polish: dashboards, runbooks, docs → Operability commitments, residual FR/NFR cleanup.

## Dependencies
- Wake-on-LAN readiness for FR‑006 and nightly maintenance windows is rescheduled to M2 alongside wider infrastructure tasks.
- VPN availability for remote administration without violating FR‑001.
 - Storage planning and encryption/backup approach ahead of M2 security tests (per-realm keys not required under session model).
