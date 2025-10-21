# Capture & Storage Blueprint (M1)

Establishes the storage conventions and manifest-first handling required by
Milestone M1. The blueprint ensures every captured artifact and derived item can
be traced, restored, and migrated without bespoke tooling.

## Objectives
- Define deterministic storage paths for all realms and item types.
- Describe capture manifests so ingestion, validation, and exports share a
  single source of truth.
- Specify checksum, version, and provenance expectations for stored blobs.
- Outline backup, restore, and verification routines that keep the archive
  trustworthy.

## Directory Layout

```
/data/<realm>/<item_type>/<year>/<item_id>/
    captures/
        <capture_id>/
            manifest.json
            assets/
    attachments/
        <attachment_id>/
            manifest.json
            payload.<ext>
    derived/
        metrics.json
```

- `realm` uses the canonical identifier defined by the realm registry.
- `item_type` aligns with `schema/types/<type>.yaml` (e.g. `document`,
  `correspondence`, `conversation_thread`, `project`).
- `capture_id` defaults to the ISO 8601 timestamp of ingestion; alternate ids
  (e.g. vendor-provided reference) are allowed when recorded in the manifest.

## Capture Manifest
Each capture directory contains `manifest.json` with:

| Field | Description |
| --- | --- |
| `capture_id` | Identifier matching the directory name. |
| `source` | Original URI, file path, or automation identifier. |
| `ingested_at` | UTC timestamp when the capture was stored. |
| `toolchain` | Versions and settings of tools used (download agent, OCR, parser). |
| `hashes` | SHA-256 (required) plus optional additional hashes for the primary payload. |
| `attachments` | Array describing related binaries (filenames, media types, hashes). |
| `notes` | Optional free-form remarks or operator annotations. |
| `links` | References back to the owning item (`kki://item/...`) and related captures. |

Manifests are canonical; downstream services read them instead of inferring
metadata from filenames.

## Tiering & Caching
- **Primary store:** ZFS/Btrfs pool mounted at `/data`. All canonical blobs live
  here with checksums verified during writes.
- **Tier-1 cache:** NVMe SSD mounted at `/cache/primary`. Holds the most recent
  90 days of captures plus in-progress ingestion batches. Items promote to the
  primary store after verification.
- **Tier-2 cache (optional):** External USB/SATA volume mounted at
  `/cache/secondary` for bulky media or seldom touched archives. Manifests note
  `storage_tier` so retrieval workflows know where to look.

Cache eviction policies:
- Promote new captures to primary only after checksum verification.
- Keep derived assets and manifests in cache until exports that reference them
  succeed.
- Evict cache entries least recently accessed, but never remove items flagged
  `retain_indefinitely` in metadata.

## Integrity & Verification
- Every capture write recomputes SHA-256 and records it in the manifest; the
  ingestion pipeline refuses to mark the capture complete if verification fails.
- Weekly job `scripts/verify_storage.py` walks `/data`, re-hashes stored blobs,
  and compares results to manifest entries. Discrepancies trigger alerts and are
  recorded under `metadata.sys.integrity`.
- `var/registry/schemas.json` and `var/registry/capabilities.json` (populated by
  the loaders) are included in integrity checks to guard against schema drift.

## Backup & Restore
- Nightly encrypted snapshots stored under `/backups/<date>/` with retention
  policy: keep 30 daily, 12 monthly, 5 yearly.
- Use `restic` (default) pointing at an SFTP or local mirror target on the LAN.
- Each backup run logs:
  - manifest count (`captures`, `attachments`),
  - total bytes synced,
  - checksum validation summary (mismatches, repaired items),
  - restore drill reminder (once per quarter).
- Restore procedure:
  1. Select snapshot and run `restic restore` into an empty staging volume.
  2. Execute `scripts/verify_storage.py --root <staging>` to confirm hashes.
  3. Swap mounts or rsync back into `/data` during maintenance window.

## Export Alignment
- Exports embed manifest snippets so round-trip imports retain capture metadata.
- Markdown/JSON export packages include `MANIFEST.md` summarising capture ids,
  hashes, and attachment counts per item.
- Capability-driven exports (e.g. `conversations.timeline`) read the capture
  manifest to pick transcript segments instead of traversing blobs manually.

## Next Steps
- Automate manifest creation in the ingestion CLI (pending scripting work).
- Add health metrics (capture throughput, verification lag) to the default
  dashboard once the telemetry stack is in place.
- Extend the blueprint with encryption-at-rest guidance when hardware-backed
  keys are provisioned.

