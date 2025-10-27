# Source-Specific Ingestion Plugins

Defines how per-source ingestion (website/service-specific) plugins are packaged,
enabled, and executed alongside domain/type bundles (e.g., OnlineStories).

## Rationale
- Not every operator wants every site importer; enable site-by-site installs.
- Keep item types, validators, and shared workflows in a reusable base bundle.
- Encapsulate credentials/cookies/sessions and site quirks in separate plugins.

## Architecture
- Base type bundle (e.g., `onlinestories.bundle`) provides:
  - Item types (`online_story`), schemas, validators.
  - Shared capability contracts (e.g., `stories.workspace`).
  - Normalizers and exporters.
- Source plugin (e.g., `websitea.onlinestories.ingestion`) provides:
  - Fetchers (requests/playwright/cloudscraper) for a single site.
  - Cookie/session and credential handling.
  - Site-specific normalization rules mapping to base schemas.
  - Schedulers/rate limits and provenance logging.

## Manifest Shape (example)
```yaml
id: websitea.onlinestories.ingestion
version: 0.1.0
kind: source_ingestion
summary: "WebsiteA importer for OnlineStories"
requires:
  - id: onlinestories.bundle
    version: ">=0.3.0 <1.0.0"
compatibility:
  min_core: 1.3.0
provides:
  features:
    - ingestion_for: ["online_story"]
declares:
  ingestion:
    - module: websitea.ingest.v1
      entrypoints: ["fetch", "normalize", "schedule"]
permissions:
  network:
    allowed_hosts: ["www.websitea.example", "api.websitea.example"]
    user_agent: "EirenhallBot/1.0"
    rate_limit:
      requests_per_min: 30
      burst: 10
  secrets:
    needs:
      - key: websitea.credentials
        description: "Username/password or API token"
        scope: area
      - key: websitea.cookies
        description: "Cookie jar for logged-in sessions"
        scope: area
``` 

## Execution Model
- The ingestion runner loads enabled source plugins for the area, exposes UI/CLI
  entry points, and schedules jobs respecting per-plugin rate limits.
- Fetchers must emit provenance (HTTP status, headers subset, timing, redirect
  chain) into `metadata.sys.provenance` of the created/updated items.
- Normalizers map fetched data to `online_story` fields using the base schemas.
- Schedulers can register cron-like triggers that the operator may enable/disable.

## Security & Secrets
- Secrets are issued via the Eirenhall secrets API; plugins request specific keys
  in the manifest. Secrets are scoped to areas by default.
- Cookie jars are stored encrypted at rest with rotation hooks.
- Playwright/Cloudflare bypass techniques must be opt-in and documented; network
  allowlists restrict destinations.

## UI/CLI
- UI surface lists available source plugins with enable/disable toggles per area.
- Each source plugin can expose forms for credentials/cookies and a “test login”.
- CLI examples:
  - `eirenhall ingest onlinestories --source websitea --since 2025-01-01`
  - `eirenhall ingest onlinestories --source websitea --login`

## Acceptance Criteria
- Loader enforces `requires` and version constraints; missing base bundle blocks enablement with a clear error.
- Network egress limited to declared hosts; requests logged in provenance.
- Secrets are not written to logs or exports; cookie jars encrypted.
- Batch ingest from WebsiteA produces valid `online_story` items with required fields and links to originals.
