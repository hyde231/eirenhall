# Scope

## In Scope
Local-only models; file/repo operations; code execution in isolated runtimes; Git operations (Gitea/LAN); long-term memory with summarization/vector search; privacy **realms**; orchestrated agent containers; power-aware WoL/auto-sleep; secure remote intake (VPN/SSH/bot); capture/archival of web/media with **versioned time-stamped captures**; extensible plugin SDK; unified query & collections; GTD workflows.

## Out of Scope (Current Phase)
Cloud LLMs/embeddings; multi-tenant SaaS; mobile beyond VPN + CLI/web.

## Assumptions
Nodes reachable via LAN; WoL supported; sufficient local storage; legal local models/quantizations.

## Constraints
End-to-end encryption; open formats (Markdown/CSV/JSON/YAML; optional WARC/MAFF/PDF); verifiable backups; offline usability.

---

## 3.1 Privacy Realms & Access Control (Genericized)

**Realms (configurable, examples):** `Shared`, `Household`, `Personal`, `Intimate`.

### Semantics
- Each **Artifact/Item** has exactly one **realm**. Sessions have an **active realm cap**; retrieval includes only items with realm ≤ cap.
- **Selective sharing:** time-boxed read-only sessions for `Shared`; never includes `Intimate`.
- **Break-glass (Personal only):** quorum + escrowed key; immutable audit; drills. `Intimate` excluded.
- Credentials, cookies, headless routes, and storage prefixes are scoped per realm.
