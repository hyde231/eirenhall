# Non-Functional Requirements (Committed Baseline)

These targets are now the minimum service levels for the solo homelab deployment. Measurements are captured via the telemetry
stack defined in the operability section and reviewed at each milestone demo.

## Reliability
- **Target:** Orchestrator uptime ≥99.5% per 30-day rolling window.
- **Validation:** Synthetic ping + job dispatch canaries running hourly with alerting to the local notifier.
- **Resilience:** Capture and enrichment queues must persist through power cycles using disk-backed storage.

## Performance
- **Capture:** Median enqueue latency <200ms; p95 <300ms on the reference workload.
- **Query:** p95 unified query latency <800ms for the mixed-format dataset defined in AC-FR-018.
- **Snapshot:** Full page snapshot complete within 30s; streaming media mirrors source duration ±10%.
- **Instrumentation:** Export metrics via Prometheus endpoints scraped locally and preserved with the run artifacts.

## Security & Privacy
- **Encryption:** Encryption at rest for sensitive stores (vector memory, secrets); keys rotated with re-encryption proof logged.
- **Access:** Session-level gating enforced on every query; failed checks emit structured audit records.
- **Egress:** Default-deny firewall policy with per-service allow lists verified weekly.

## Operability
- **Observability:** Dashboards covering capture rate, success/failure ratios, retries, storage growth, captures per URL,
  dedupe hit rate, query latency, and session-gating violations (target = 0) stored in Grafana snapshots.
- **Runbooks:** Each high-priority requirement has a one-page runbook with restart, rollback, and verification steps.
- **Alerting:** Pager rules for queue backlog >50 jobs (15 min) and storage saturation >80% of reserved space.

## Formats & Compatibility
- **Archives:** Markdown + asset bundle is authoritative; optional PDF/WARC/MAFF generated asynchronously and validated via checksum.
- **Sidecars:** yt-dlp sidecars stored adjacent to video captures with schema-validated JSON.
- **Interchange:** Import/export contracts for CSV and JSON include schema versioning and capture timestamps preserved end-to-end.

## Maintainability
- **SDK:** Plugin SDK published with semver hooks; incompatible plugins rejected during installation.
- **Testing:** Core plugins covered by end-to-end regression tests running nightly on the lab machine.
- **Sandboxing:** Plugin execution isolated via container or process sandbox with resource quotas enforced.

## Traceability

| Requirement | Spec references | Automated coverage |
| --- | --- | --- |
| Reliability targets | docs/specs/capture_storage_blueprint.md; docs/requirements/12_roadmap/README.md | Monitoring canary scripts (planned) |
| Performance targets | docs/specs/spec_scaffold.md; docs/specs/generic_item_surface.md | tests/derived/test_project_metrics (latency proxies), performance benchmark harness (planned) |
| Security & privacy | docs/requirements/10_governance/README.md; docs/adr/ADR-001-agent-capability-model.md; docs/specs/vector_memory.md | Security drill scripts (TBD) |
| Vector memory | docs/specs/vector_memory.md | Indexer tests (planned); privacy/redaction unit tests (planned) |
| Observability | docs/specs/spec_scaffold.md; docs/specs/capture_storage_blueprint.md | Observability stub instrumentation (pending) |
| Formats & compatibility | docs/specs/item_schema.md; docs/specs/field_library.md | scripts/validate_schema.py; export/import regression tests (planned) |
| Maintainability | docs/specs/capability_contracts.md; docs/specs/field_library.md | tests/capabilities/test_capabilities.py |

Link additional specs or tests as they come online to maintain coverage visibility.
