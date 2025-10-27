# Plugin Packaging & Discovery Specification

Defines how optional bundles (schemas, ingest flows, surfaces, editors) are
packaged, distributed, discovered, and enabled without modifying the core
distribution. Supports the vision requirement that personal additions ship as
plugins while the stock system remains neutral.

## Goals
- Make it easy to install/remove plugins without touching core files.
- Allow multiple plugin channels (official, personal, experimental) with clear
  provenance and compatibility metadata.
- Ensure plugins declare their footprint (schemas, capabilities, surfaces,
  actions) so the registry can validate and audit overrides.
- Support per-area/per-installation enablement so sensitive bundles stay
  scoped.

## Packaging Format
- Plugins are versioned archives (directory or zip) with manifest
  `plugin.yaml`:
  ```yaml
  id: stories.bundle
  version: 0.3.0
  summary: "Story capture and publishing tools"
  authors:
    - name: Jane Example
      email: jane@example.net
  license: MIT
  compatibility:
    min_core: 1.2.0
    max_core: 1.3.x
  declares:
    schemas:
      - schema/types/story.yaml
      - schema/fields/story_arc.json
    capabilities:
      - schema/capabilities/stories.workspace.yaml
    surfaces:
      - module: stories.ui
        provides:
          - type: story
            mode: detail
          - capability: stories.workspace
    ingestion:
      - module: stories.ingest.v1
    actions:
      - module: stories.actions.publish
  permissions:
    requires_manage: true
  ```
- Assets referenced in `declares.schemas` etc. live alongside the manifest and
  are loaded via the registry/capability/type loaders when the plugin is
  enabled.

## Discovery & Installation
- **Plugin Index:** Optional YAML/JSON index listing available plugins, their
  versions, checksums, and signing keys. Operators can point the CLI to multiple
  indices (official, personal).
- **CLI Commands:**
  - `Eirenhall plugin search <term>` – query indices and local cache.
  - `Eirenhall plugin install <id>@<version>` – download archive, verify checksum,
    unpack into `var/plugins/<id>/<version>`, and register with loaders.
  - `Eirenhall plugin enable <id>` / `disable` – toggle persisted enablement state.
  - `Eirenhall plugin inspect <id>` – show manifest, declared overrides, conflicts.
- **Conflicts:** When multiple plugins attempt to register the same schema or
  override, the surface registry resolves via priority; conflicting schema IDs
  are blocked unless explicitly overridden with `--force`.
- **Signing:** Optional GPG signature check per archive; core tools warn when
  installing unsigned bundles.

## Loading Lifecycle
1. On startup (or plugin enable), the system scans `var/plugins` for enabled
   bundles.
2. Each bundle’s `plugin.yaml` is parsed; declared schemas/capabilities/types
   are fed into existing loaders.
3. Surface/action overrides register via entry points defined in the manifest.
4. When disabling a plugin, the system deregisters overrides and drops loaded
   schemas/capabilities belonging to the plugin (after verifying no items use
   them unless `--force`).

## Isolation & Safety
- Plugins execute in dedicated namespaces; they cannot mutate core packages
  without explicit import.
- Resource limits (CPU, memory) can be applied to plugin background jobs via
  the orchestration layer.
- Sensitive areas can maintain per-area allowlists of enabled plugins.

## Testing & Validation
- Automated tests include `plugin smoke` runs that load the core system with no
  plugins, with official bundles, and with representative personal bundles.
- Manifest schema validates required keys/structures; CI rejects plugins with
  missing metadata.
- Upgrade paths: when core version bumps, compatibility checks flag plugins
  requiring revisions.

## Roadmap
- Phase 1: Implement manifest loader, CLI install/enable/disable, schema/cap
  integration.
- Phase 2: Add signed index support, per-area enablement, and conflict
  resolution UI.
- Phase 3: Provide SDK templates and sample plugins (stories, finance, health)
  demonstrating best practices.
