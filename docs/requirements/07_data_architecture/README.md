# Data & Information Architecture

## Extensibility-First Content Model
Items = base fields + capabilities.

### Base Fields
`id, type, realm, sensitivity, title, description, created_at, updated_at, tags[], source_url?, canonical_url?, captures[], attachments[], links[], checksum, size, metadata{}`

### Capabilities (Mix-ins)
Viewable, Listable, Queryable, Storable, Importable/Exportable, Versioned, Scrapeable, Downloadable, Readable, Playable, Workflown, Schedulable, Annotatable.

### Type Registry
`{type_key, version, capabilities[], schema.json, facets[], actions[], migrations[]}`.

### Captures
`capture_id, captured_at, paths, hashes, size, tool_versions` (multiple per Item).

### Storage Layout (Illustrative)
`/data/archive/<realm>/<type>/<YYYY>/<MM>/<id>/<captured_at-ISO8601>/` with `meta.json`, normalized content (`.md/.html/.cbz/.pdf`), assets, optional `snapshot.pdf`/`page.warc`.

> POC-oriented example: hardware roles may consolidate into VMs/containers as long as required capabilities (e.g., GPU passthrough) are preserved.

### Indexing & Search
Full-text over normalized text + fields (including **captured_at**); optional vector index; plugin facets (e.g., series/episode/author/duration/language).

### Retention & Deletion
Deferred. Treat storage as fixed for now and plan cleanup workflows after functional feasibility is proven.

## 7.1 Storage & Data Sinks (Decisions & Options)
- **Metadata/docs/code → Git** (great for text, diffs, ADRs). Avoid huge binaries in repos.
- **Large binaries → raw FS/object store** with open **manifests** (JSON/YAML), checksums, optional CAS/dedup.
- **git-annex/Git LFS (optional)** if repo-centric workflows benefit; keep plain-file exportability.
- **Tiered caching** across Mini PC/Desktop/Server with realm/recency/favorites/saved searches policies.

### Open Questions (Working Positions)
- **SQ‑1:** Prioritize cache by recency and favorites (with realm awareness as already modeled).
- **SQ‑2:** “Manifest-first” = sidecar metadata files that travel with content; preferred default.
- **SQ‑3:** Favor plain filesystem storage for compatibility; consider S3-compatible layers only with clear benefits on homelab hardware.
