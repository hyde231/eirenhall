# Vector Memory & Retrieval Spec

Defines the purpose, scope, data model, hardware sizing, and multi-machine topology for Eirenhall’s vector memory. The vector database is a derived, rebuildable aide for recall and context; it is never the source of truth.

## Scope & Collections
- content_index: embeddings of allowed user content (titles, summaries, wiki/notes/body text, task descriptions, OCR-derived text from documents, selected correspondence text).
- memory_ephemeral_index: last N conversation turns per thread with TTL; built for short-term context.
- memory_durable_index: explicit “save to memory” insights (facts, commitments, decisions, pointers to items), not raw transcripts.
- entity_index: normalized entities and short fact sentences derived from items.
- dev_index (opt‑in, isolated): embeddings of Eirenhall’s own repo/docs/specs to assist local coding; never mixes with personal data.

## Security & Gating
- Session-level gating: All queries enforce `item.level <= session.max_level`.
- Allowlist fields to embed; never embed secrets or restricted fields.
- Redaction: heuristics remove emails, token-like strings, IBANs, etc., from embedded text.
- Encryption at rest; strictly local (no network egress).
- Inspectability: per-item “show embedded text” and regenerate/purge controls.

## Chunking & Metadata
- Chunk 512–1024 tokens with 10–20% overlap.
- Persist with metadata: `eirenhall://` source URI, item id/type, field, chunk offsets, checksum of source text, model id, created_at, sensitivity level.
- Hybrid retrieval: vector + facets (type, tags, date) + optional BM25.

## Lifecycle
- Triggers on create/update; re-embed when the model changes or source text changes (checksum mismatch).
- Ephemeral memory TTL (e.g., 7–30 days). Durable memories persist until removed.
- Treat as derived: exclude from primary backups by default; keep periodic snapshots for faster startup.

## Hardware Sizing
- Memory estimate: `count × dims × 4 bytes` (float32); HNSW + metadata ≈ 2–3× vector memory. Plan ≈1 GB RAM per 100k 768‑dim vectors plus headroom.
- Storage: NVMe SSD improves index build and query latency; size by vectors + HNSW graph + WAL/snapshots.
- Quantization (e.g., int8/PQ) can reduce RAM/disk 2–4× with modest recall trade-offs.

Tiers (guidance):
- Small (≤50k vectors @384–768 dims): 4 cores, 8–16 GB RAM, 20–50 GB NVMe.
- Medium (100k–500k @768 dims): 6–8 cores, 16–32 GB RAM, 100–200 GB NVMe.
- Large (1M+ @768–1024 dims): 12–16 cores, 64 GB+ RAM, 0.5–1 TB NVMe.

## Multi‑Machine Topology
- Centralized store (recommended):
  - Run the vector DB on the always‑on node (mini‑PC/NAS) with NVMe.
  - Run embedding workers on the GPU desktop; push vectors via LAN.
  - Nightly snapshots to bulk storage; rebuildable on demand.
- Ephemeral per‑node caches (optional):
  - Small embedded stores for “recent session” or dev_index; TTL enforced; no cross‑node sync.
- WoL‑aware flow: keep store up for low‑power recall; wake GPU node for batch (re)embeddings or model upgrades.

## Partitioning Strategy
- Single engine, multiple collections/partitions (content, entities, memories, dev). Avoid separate databases per persona; enforce session‑level gating at query time.
- Optional per‑node ephemeral caches for latency, not as authoritative stores.

## Engines & Deployment
- Central store: Qdrant (default) or Milvus for larger scale; Docker‑based.
- Local caches: LanceDB/Chroma for embedded use.
- Compose profile: vector DB + API; workers for embedding; snapshot job (see roadmap infra stream).

## Acceptance Criteria
- Queries respect session‑level gating; higher‑sensitivity content never surfaces at lower session levels.
- Allowlist and redaction enforced; secrets never embedded.
- Inspect, purge, and regenerate tools exist; re‑embedding triggers on source/model change.
- Central store operational with snapshot/restore; optional per‑node caches TTL‑expire and rebuild.
