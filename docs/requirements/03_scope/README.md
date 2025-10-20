# Scope

## In Scope
Local-only models on consumer-grade hardware; file/repo operations; code execution in isolated runtimes; Git operations (Gitea/LAN); long-term memory with summarization/vector search; privacy **realms**; orchestrated agent containers; power-aware WoL/auto-sleep; secure remote intake (VPN/SSH/bot); capture/archival of web/media with **versioned time-stamped captures**; extensible plugin SDK; unified query & collections; GTD workflows.

## Out of Scope (Current Phase)
Cloud LLMs/embeddings; specialized accelerator dependency; multi-tenant SaaS; mobile beyond VPN + CLI/web.

## Assumptions
Nodes reachable via LAN; WoL supported; sufficient local storage; legal local models/quantizations.

## Constraints
End-to-end encryption; open formats (Markdown/CSV/JSON/YAML; optional WARC/MAFF/PDF); verifiable backups; offline usability.

---

## 3.1 Privacy Realms & Access Control (Genericized)

### Access Levels
- **Intimate, Personal, Household, Shared, Guest (examples):** Named access levels define sensitivity tiers, audit expectations, and required approval flows. They are long-lived governance concepts rather than individual workspaces.
- Each access level declares default policies (storage tiers, credential pools, authentication factors) that realm instances inherit unless explicitly overridden.

### Realms
- A **realm** is an instantiation of an access level (e.g., "Project Phoenix" at the Personal level, "Family Cookbook" at the Household level). The platform must support creating, cloning, splitting, merging, and archiving realms without changing the underlying access-level catalog.
- Realm definitions record lineage (origin realm/access level) so provenance survives operations like copy/clone/merge.
- Sessions adopt an **active realm cap** derived from the operator’s access level allowances; retrieval includes only items in realms whose access level is ≤ cap.
- **Selective sharing:** time-boxed read-only sessions for `Shared`-level realms; never includes `Intimate`; managed via sharable content/action types so policy variants can be versioned per realm instance.
- **Break-glass (Personal-level realms only):** quorum + escrowed key; immutable audit; drills; expressed as a managed content/action type so policies stay flexible. `Intimate`-level realms are excluded.
- Credentials, cookies, headless routes, and storage prefixes are scoped per realm instance, with inheritance from the parent access level for defaults.
