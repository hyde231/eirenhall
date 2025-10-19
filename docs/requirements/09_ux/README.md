# UX Principles & Views

## UX Tenets
- **Generic views auto-derived from capabilities:** list/table (facets), detail, history (captures), reader mode (stories/threads), media panel (downloads/subtitles), workflow boards (tasks/projects), annotations.
- **Inputs:** paste box, watched folders, browser extension/bookmarklet, CLI (`kki capture <url> --realm R --tags a,b`).
- **Collections:** saved searches (dynamic) and snapshots (static exports with manifests).
- **Exports:** realm banners, redaction profiles, Markdown/CSV bundles + assets; masters untouched.

## 9.1 Saved Searches & Collections Specification

### Saved Search (Dynamic)
`id, name, owner, realm_cap, query_dsl, sort, limit?, schedule?`

- DSL: boolean over fields (`type, realm, tags, captured_at/published_at, plugin, duration, author, status`), operators (`=, !=, in, contains, regex?, range`).
- Example: `type=webcomic AND captured_at>=2025-10-01`.

### Static Collection (Snapshot)
`id, name, realm, item_ids[], manifest` (checksums, capture ids, paths). Export: Markdown/CSV + assets.
