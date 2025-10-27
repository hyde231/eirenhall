# Scope

## In Scope
Local-only models on consumer-grade hardware; file/repo operations; code execution in isolated runtimes; Git operations (Gitea/LAN); long-term memory with summarization/vector search; organizational **realms** (areas/projects); orchestrated agent containers; power-aware WoL/auto-sleep; secure remote intake (VPN/SSH/bot); capture/archival of web/media with **versioned time-stamped captures**; extensible plugin SDK; unified query & collections; GTD workflows.

## Out of Scope (Current Phase)
Cloud LLMs/embeddings; specialized accelerator dependency; multi-tenant SaaS; mobile beyond VPN + CLI/web.

## Assumptions
Nodes reachable via LAN; WoL supported; sufficient local storage; legal local models/quantizations.

## Constraints
End-to-end encryption; open formats (Markdown/CSV/JSON/YAML; optional WARC/MAFF/PDF); verifiable backups; offline usability.

---

## 3.1 Sensitivity Levels & Sessions

The platform enforces access at the session level. Realms are organizational only.

### Levels
- Ordered scale: `public < family < partner < personal < private < intimate`.
- Each item has a `level` (one of the above).

### Sessions
- Each interactive session declares a `max_level`.
- All reads, search results, and conversations MUST filter to
  `item.level <= session.max_level`.

### Defaults and Reclassification
- New items default to the current session’s `max_level` (overrideable).
- Upgrading sensitivity (more restrictive) is allowed.
- Downgrading sensitivity requires explicit confirmation and an audit entry.

### Realms (Organizational)
- Realms are GTD-style areas/projects for organization and storage paths.
- Realms DO NOT define access; there is no “realm cap.”
- Queries may facet by realm for navigation; security derives solely from item
  `level` and the session filter.

### Operational Notes
- Credentials and storage prefixes can be configured per realm for convenience
  and routing, without implying different access levels.
- Sharing and guest flows can be layered later (e.g., link-based or copy-based)
  without changing the session-level enforcement model.

