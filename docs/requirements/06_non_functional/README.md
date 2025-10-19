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
- **Encryption:** Realm-specific keys rotated quarterly with automated re-encryption proof logged.
- **Access:** Realm-scoped tokens enforced on every API; failed checks emit structured audit records.
- **Egress:** Default-deny firewall policy with per-service allow lists verified weekly.

## Operability
- **Observability:** Dashboards covering capture rate, success/failure ratios, retries, storage growth, captures per URL,
  dedupe hit rate, query latency, and realm violations (target = 0) stored in Grafana snapshots.
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
