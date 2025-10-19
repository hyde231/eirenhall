# Requirement Backlog (Living Table)

| Key | Type | Title | Priority | Acceptance Criteria | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- |
| FR‑001 | FR | Local‑only execution | Must | No external egress; tests verify | You | Draft |
| FR‑002 | FR | Open data formats | Must | Readable externally; round-trip tests | You | Draft |
| FR‑003 | FR | Realm tagging & scoping | Must | Zero cross‑realm retrievals in tests | You | Draft |
| FR‑006 | FR | Power-aware scheduling | Must | WoL + idle sleep verified | You | Draft |
| FR‑014 | FR | Link capture & normalization | Must | URL → archived item with metadata + timestamped copy | You | Draft |
| FR‑015 | FR | Offline archiving (versioned) | Must | Items render offline; checksums saved; captures listed | You | Draft |
| FR‑016 | FR | Plugin processors | Must | Identify/fetch/enrich/render hooks pass tests | You | Draft |
| FR‑018 | FR | Unified query | Must | p95 < 800ms; saved searches work | You | Draft |
| FR‑019 | FR | Bulk operations | Should | Mass‑tag/move/export with audit | You | Draft |
| FR‑020 | FR | Dynamic & static collections | Must | Views auto‑refresh; exports reproducible | You | Draft |
| FR‑026 | FR | Large-binary handling | Must | Manifests; integrity via checksums | You | Draft |
| FR‑027 | FR | Tiered caching | Must | Cache metrics; offline manifests enable browsing | You | Draft |
| NFR‑SEC | NFR | E2E encryption & egress block | Must | WG/mTLS + firewall verified | You | Draft |
| NFR‑PERF | NFR | Capture/search performance | Must | Enqueue <300ms; query p95 <800ms | You | Draft |
