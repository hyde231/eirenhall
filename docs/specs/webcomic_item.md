# Webcomic Item Specification (Draft)

Defines the schema elements introduced for the `webcomic` item type and references the supporting field composites.

## Item Envelope
- `item_type = "webcomic"` (see `schema/types/webcomic.yaml`).
- Reuses `schema/item_base.json` for the envelope, with the following notable fields:
  - `fields.title`: `std.title` (base)
  - `fields.base_url`: `std.url`
  - `fields.availability`: `webcomic_availability.json`
  - `fields.status`: `webcomic_status.json`
  - `fields.synopsis`: `std.rich_text`
  - `fields.artists[]`: `webcomic_artist.json`
  - `fields.cover_image`: `std.image_reference`
  - `fields.starting_date`: `std.calendar_date`
  - `fields.end_date?`: `std.calendar_date`
  - `fields.last_update`: `std.timestamp`
  - `fields.page_urls[]`: `std.url` 
  - `fields.images[]`: `std.image_reference`
  - `fields.thumbnails[]`: `std.image_reference`
  - `fields.language`: `std.locale`
  - `fields.tags`: `std.tag_list`
  - `fields.comment`: `std.rich_text`
  - `fields.rating`: `std.percentage` (0-1 scale; front-end renders as 0-100%)
  - `fields.scraping`: `webcomic_scraping_config.json` (under capability guard `webcomic.scraper`)

## Supporting Fields
- `schema/fields/webcomic_artist.json` — contributor metadata with role enums and optional profile URI.
- `schema/fields/webcomic_availability.json` — enum controlling availability widgets (`online`, `offline`, `unknown`).
- `schema/fields/webcomic_status.json` — lifecycle (`active`, `completed`, `hiatus`, `abandoned`, `unknown`).
- `schema/fields/webcomic_scraping_config.json` — technical configuration for automated monitoring.

## Capabilities
- `webcomic.library` (library/browse features, dashboards).
- `webcomic.scraper` (automation, diagnostics). Both registered under `schema/capabilities/webcomic.*.yaml` and attached to the type manifest.

## Derived & Automation (Future Work)
- Derived metrics (chapter counts, update cadence) to be captured in `schema/derived/webcomic.yaml`.
- Automation hooks: scraper events populate `metadata.cap.webcomic.scraper`.
- Fixtures: add sample payload (`tests/fixtures/items/webcomic_sample.json`) and derived evaluator coverage when metrics land.

## Open Questions
- Should artist roles reuse a shared enum across other media types? **Answer:** No, keep roles scoped to the webcomic domain for now; other media types can declare their own catalogs later.
- Do pages leverage dedicated item types or remain object references? **Answer:** Treat pages as external web pages referenced by URL (object references with `uri` pointing to the page).
- What retention policy applies to downloaded images/thumbnails? **Answer:** Match the hosting webcomic item—default infinite retention unless realm policy overrides it.
