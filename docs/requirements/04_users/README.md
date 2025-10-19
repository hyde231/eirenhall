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

## Milestone Emphasis
- **M1:** deliver generic document management, GTD task handling, and wiki-like knowledge storage as the baseline user value.

## Operational Notes
- Hot cache surfaces recent/favorite/priority documents while remote; mass-storage servers can be woken over LAN when deep archives are needed, with the orchestrator prompting before bringing the server online for remote sessions.
- Remote access typically happens from a smartphone, with one active session expected and at most two running in parallel.
