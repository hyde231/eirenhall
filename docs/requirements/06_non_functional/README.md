# Non-Functional Requirements

## Reliability
Orchestrator uptime ≥99.5%; durable queues.

## Performance
Capture enqueue <300ms; p95 query <800ms; page snapshot <30s; videos at download wall-clock.

## Security & Privacy
E2E encryption; realm-scoped tokens; immutable audits; default-deny egress.

## Operability
Metrics for capture rate, success/failure, retries, storage growth, **captures per URL (version count)**, dedupe hit rate, query latency, realm scope violations (must be 0).

## Formats & Compatibility
Archives in open formats (Markdown + assets; optional PDF/WARC/MAFF); yt-dlp sidecars; import/export CSV/JSON; **preserve capture timestamps**.

## Maintainability
Plugin SDK with semver hooks; end-to-end tests for core plugins; sandboxed execution.
