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

### Indexing & Search
Full-text over normalized text + fields (including **captured_at**); optional vector index; plugin facets (e.g., series/episode/author/duration/language).

### Retention & Deletion
Realm defaults; quarantine then purge; per-capture pruning; `Scrapeable` may pin.

## 7.1 Storage & Data Sinks (Decisions & Options)
- **Metadata/docs/code → Git** (great for text, diffs, ADRs). Avoid huge binaries in repos.
- **Large binaries → raw FS/object store** with open **manifests** (JSON/YAML), checksums, optional CAS/dedup.
- **git-annex/Git LFS (optional)** if repo-centric workflows benefit; keep plain-file exportability.
- **Tiered caching** across Mini PC/Desktop/Server with realm/recency/favorites/saved searches policies.

### Open Questions
- SQ‑1: Cache priority by realm vs. recency/favorites?
- SQ‑2: Any Git-centric mandate for photos/media or is manifest-first OK?
- SQ‑3: Comfort with optional local S3-compatible store if we preserve plain export?
