# Interfaces & Integrations

## Local Systems
Gitea, NFS/Samba, WireGuard, Prometheus/Grafana.

## Capture & Archive Pipeline
Readability extractors → Markdown; OCR; yt-dlp; headless (Playwright) → PDF/HTML; optional WARC/MAFF; RSS/Atom.

## Plugin SDK
- **Manifest:** `type_key, display_name, version, capabilities[], schema, facets[], actions[]`
- **Hooks:** `identify(url|path)`, `ingest(input)`, `fetch(item)`, `enrich(item,capture)`, `render(item,mode)`, `actions()`, `schedule(item)`, `migrate(item,from,to)`

## APIs
Content (CRUD Items/Captures, query, bulk, export/import); Registry (types/schemas/validation); Actions (invoke with realm checks & audit).

## Network Policy
Default-deny egress; realm-scoped proxies/identities; explicit consent per outbound call.
