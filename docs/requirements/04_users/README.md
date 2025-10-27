# User & Use Cases

## Primary Persona
Privacy-first power user/developer running a home lab as a solo operator. Typical access happens on the home LAN from a desktop workstation with a GPU for AI tasks, complemented by a bulk-storage server that can be woken as needed. A Raspberry Pi orchestration node coordinates remote activity, with optional Wake-on-LAN to bring the desktop online for urgent AI jobs. When local-only work is required, the desktop can assume orchestration duties.

## Priority Use Cases
Ad hoc requests take precedence, covering code tasks/PRs, repo maintenance, file operations, knowledge recall, remote quick tasks (queueing captures, link retrieval, archival prep while off-LAN), and GPU jobs. Early milestones emphasize GTD flows over content scraping, while automation and recurring jobs arrive later. Additional must-haves: **link capture**, **archival + enrichment**, extensible plugins, unified query, bulk operations, **versioned captures per URL**, and offline exports.

## Sample Stories
- Paste URL → offline archived Item (with timestamped local copy; warmed in hot cache when recent/favorited).
- Saved search for “updates this week” (first-class saved search entity available across desktop/mobile).
- Export Household-safe Markdown bundle.
- Desktop-first collection curation session while automation defers heavy storage/GPU workloads to scheduled windows.

## Extended Use Case Scenarios
- **Break-glass emergency rehearsal:** Run a quarterly drill that walks through quorum approval, escrowed key retrieval, and a selective restore to keep emergency Personal-realm access audit-ready and technically viable.
- **Offline travel knowledge pack:** Before going off-grid, generate a tiered-cache bundle of recent tasks, reference material, and critical documents for mobile devices, verifying offline manifests and sync-back cues on return.
- **Weekly GTD + insight review:** Stage a Friday synthesis session via unified query, saved searches, and optional local AI summaries to merge pending tasks, new captures, and retrospective notes into an actionable dashboard.
- **Local coding assistant extension sprint:** Pair with the on-device coding persona to prototype a new automation or plugin end to end, including schema proposals, sandboxed tests, and human-reviewed pull requests.
- **Schema evolution dry run:** Stand up a staging dataset, apply a versioned schema change via the capability registry, run assistant-proposed migrations, and capture rollback artifacts to validate the extensibility workflow.
- **Heritage media ingest weekend:** Orchestrate the import of a multi-terabyte photo/video collection while confirming large-binary manifests, checksum validation, and background enrichment queues without overwhelming primary storage nodes.
- **Household onboarding with session presets:** Simulate adding a new family member, configuring roles, setting default session levels for shared devices, and reviewing audit trails to keep lifecycle flows manageable for a solo operator.
- **Remote capture triage queue:** While traveling, queue a batch of URLs through the secure intake path, then reconcile archived copies, realm tags, and enrichment metadata from a single review board upon returning home.
- **Guest access with automatic expiry:** Provide a guided flow for granting short-term guest access to selected artifacts, including optional expiration and audit confirmation, using session-level gating to guarantee appropriate exposure.
- **Human-in-the-loop AI enrichment queue:** Schedule local models to draft summaries or tags for newly captured items, presenting them in a review queue so the owner can accept, edit, or reject suggestions before publishing.
- **Coding assistant-guided maintenance sprint:** Spin up a structured session where the local coding assistant proposes refactors or test improvements on the platform itself, bundling diffs and rationale for manual approval at the end.
- **Household data stewardship checklist:** Offer a periodic workflow that walks the owner through verifying backups, exports, and retention settings to reinforce durability, privacy, and personal sovereignty responsibilities.
- **Household planning board (session-gated):** Surface a curated dashboard of shared tasks, documents, and automations for Household members while automatically filtering Personal and Intimate material via session-level gating.
- **Power-aware batch orchestration window:** Define a scheduled “maintenance night” that wakes storage servers, batches large captures, refreshes vector indexes, and returns nodes to low-power states to keep WoL and deferment policies observable.

## Milestone Emphasis
- **M1:** deliver generic document management, GTD task handling, and wiki-like knowledge storage as the baseline user value.

## Operational Notes
- Hot cache surfaces recent/favorite/priority documents while remote; mass-storage servers can be woken over LAN when deep archives are needed, with the orchestrator prompting before bringing the server online for remote sessions.
- Remote access typically happens from a smartphone, with one active session expected and at most two running in parallel.
