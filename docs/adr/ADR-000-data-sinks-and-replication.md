# ADR-000: Data sinks and replication strategy

- Status: Accepted
- Date: 2025-10-21
- Deciders: Eirenhall core maintainers
- Related work: docs/specs/capture_storage_blueprint.md, docs/requirements/00_meta/README.md, docs/requirements/07_data_architecture/README.md

## Context

Eirenhall operates on heterogeneous artifacts ranging from lightweight metadata to
multi-gigabyte media captures. Early discussions explored storing everything in
Git, but binary artifacts and capture bundles quickly outgrew that approach.
Without an explicit authoritative-store definition, contributors could diverge
on where truth lives, how replication is handled, and which indices or manifests
must be kept consistent. The project now spans multiple nodes (desktop, mini-PC
cache, NAS) with varying uptime guarantees, making clear replication and
retention policies essential for durability and offline access.

## Decision

We split storage responsibilities across three coordinated sinks:

1. **Metadata repository (authoritative):** Git repository containing schemas,
   manifests, derived definitions, personas, and automation recipes. Stored under
   `repo/` (this repository) with Git as the source of truth. Git LFS and
   git-annex remain optional and must not contain primary binaries.
2. **Object store (authoritative for binaries):** Filesystem-backed object store
   rooted at `/data` as described in `capture_storage_blueprint.md`. Capture
   manifests, attachments, and derived bundles reside here. Each object is
   addressed by deterministic paths and includes SHA-256 hashes in
   `manifest.json`.
3. **Indices & caches (derived, reconstructable):** Materialised search indices,
   vector embeddings, and cache warmers live under `/var/eirenhall`. These assets are
   regenerated from authoritative data and excluded from primary backups.

Replication and retention policies:

- Primary object store: ZFS/Btrfs pool with nightly `restic` snapshots to
  `/backups/<date>/`, keeping 30 daily, 12 monthly, and 5 yearly copies.
- Mini-PC cache: Hot cache at `/cache/primary` containing the last 90 days of
  captures plus pinned favorites. Eviction uses LRU with area-aware pinning.
- Cold tier (optional): External USB/SATA volume at `/cache/secondary` retaining
  large media flagged `retain_indefinitely`. Metadata manifests always remain in
  `/data`.
- Git repository: Pushed to self-hosted mirror nightly and whenever release tags
  are cut.

Indices (Whoosh/Lucene, SQLite, vector DB) reference captures by manifest
checksum. They rebuild automatically after restores using replay scripts stored
under `scripts/`.

## Consequences

Positive:

- Clear authority boundaries prevent schema drift between Git and blob storage.
- Manifest-first approach enables deterministic restore drills and integrity
  audits.
- Cache tiers can be rebuilt or resized without affecting canonical data.

Trade-offs:

- Operators must run both filesystem snapshots and Git pushes to satisfy the
  backup policy.
- Object storage restore requires verifying manifests before reattaching caches,
  adding complexity to disaster recovery.
- Keeping indices ephemeral demands reliable rebuild tooling; failure to run the
  replay scripts delays search availability after restores.

Follow-up work:

- Implement automated verification (`scripts/verify_storage.py`) in CI/cron as
  outlined in the capture blueprint.
- Document restic configuration in docs/howto once hardware assignments settle.
