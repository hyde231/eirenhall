# Acceptance Criteria

Acceptance criteria are captured as lightweight Gherkin scenarios so they can be automated or demonstrated quickly, even when
working solo with AI assistance. Each referenced ID maps to the backlog table.

- **Format:** Given <context> When <action> Then <outcome> (including negative cases where relevant).
- **Evidence:** Link a unit/integration test, CLI script, or metrics capture proving the outcome during the milestone demo.

## Functional Requirements

### AC‑FR‑001 · Local-only execution
- **Scenario:** Given a workstation without outbound firewall exceptions When the orchestrator starts Then all capture, query, and
  enrichment services run locally and every external request is denied with a logged reason.
- **Scenario:** Given an integration test with mocked internet access When it attempts to fetch external resources Then the call is
  blocked and the request/response pair is persisted to the audit log.

### AC‑FR‑002 · Open data formats
- **Scenario:** Given an archived capture When exported Then the payload contains Markdown/JSON metadata with relative asset paths
  and reimports without loss using the import CLI.
- **Scenario:** Given a saved search export When inspected with standard tools (jq, unzip) Then the files open without proprietary
  software and round-trip back into the library with byte-for-byte checksum parity.

### AC‑FR‑003 · Realm tagging & scoping
- **Scenario:** Given two realms with disjoint content When a query is executed in Realm A Then zero Realm B items appear and the
  audit log records the realm context.
- **Scenario (negative):** Given a bulk move request that crosses realms When processed Then the operation is rejected and the UI
  surfaces the violation message defined in the governance chapter.

### AC‑FR‑006 · Power-aware scheduling
- **Scenario:** Given the device is idle and on AC power When the capture queue has work Then jobs dispatch immediately and a metric
  records power state at dispatch time.
- **Scenario:** Given battery drops below the configured threshold When background captures run Then they are paused and a retry is
  scheduled after power recovers or the user manually resumes.

### AC‑FR‑014 · Link capture & normalization
- **Scenario:** Given a URL submission When the capture completes Then the archive includes normalized metadata (title, canonical
  URL, timestamp) and a snapshot stored in the offline cache.
- **Scenario (negative):** Given a URL that times out When captured Then the failure is surfaced with retry guidance and logged with
  HTTP status/timeout data.

### AC‑FR‑015 · Offline archiving (versioned)
- **Scenario:** Given an existing capture When a new version is created Then both versions remain browsable offline, each with
  checksums and provenance metadata.
- **Scenario:** Given offline mode enabled When the user opens a captured item Then assets load from the local manifest without
  network access.

### AC‑FR‑016 · Plugin processors
- **Scenario:** Given a plugin implementing identify/fetch/enrich/render When run in the sandbox Then lifecycle hooks execute in
  order and failures bubble up with structured errors.
- **Scenario:** Given a plugin update with a breaking change When executed against the semver contract Then it is rejected and the
  orchestrator reports the incompatibility.

### AC‑FR‑018 · Unified query
- **Scenario:** Given captures across realms and formats When executing a combined search Then results merge chronologically with
  p95 latency under 800ms on the reference dataset.
- **Scenario:** Given a saved search definition When scheduled Then the results persist and trigger notifications according to
  governance rules.

### AC‑FR‑019 · Bulk operations
- **Scenario:** Given a selection of captures When applying a bulk tag Then every item reflects the tag, an audit entry is stored,
  and conflicting realm assignments are flagged.
- **Scenario:** Given an export of more than 500 items When executed Then progress feedback is shown and retries occur automatically
  on transient failures.

### AC‑FR‑020 · Dynamic & static collections
- **Scenario:** Given a smart collection definition When relevant captures change Then the collection refreshes within five minutes
  and emits a metrics event.
- **Scenario:** Given a static collection When exported Then the manifest reproduces the exact membership via import with checksum
  parity.

### AC‑FR‑026 · Large-binary handling
- **Scenario:** Given a binary over the streaming threshold When captured Then the system generates a manifest, stores chunk
  checksums, and allows resume after interruption.
- **Scenario:** Given a restore from cold storage When executed Then the manifest reconstructs the binary without checksum drift.

### AC‑FR‑027 · Tiered caching
- **Scenario:** Given the device enters offline mode When browsing captured items Then media is served from the offline tier with a
  cache hit rate ≥80% on the reference corpus.
- **Scenario:** Given the cache warmer runs overnight When metrics are inspected Then they show prefetch counts, miss reasons, and
  eviction totals.

## Non-Functional Requirements

### AC‑NFR‑SEC · E2E encryption & egress block
- **Scenario:** Given a new realm key rotation When performed Then all in-flight services continue operating and data remains
  encrypted at rest with the new key recorded in the key log.
- **Scenario:** Given an unauthorized outbound request When attempted Then the firewall denies the connection, raises an alert, and
  the audit log captures the payload hash.

### AC‑NFR‑PERF · Capture/search performance
- **Scenario:** Given the reference workload When capture jobs enqueue Then median latency is under 200ms and p95 under 300ms with
  metrics exported to the observability dashboard.
- **Scenario:** Given the same workload When queries execute Then p95 latency stays below 800ms and the regression test fails if the
  threshold is exceeded.
