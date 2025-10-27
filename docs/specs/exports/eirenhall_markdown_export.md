# Eirenhall Markdown Export Specification

## Goals
- Preserve full fidelity of Knowledge Kernel items while producing human-readable artifacts.
- Ensure exported bundles remain tool-agnostic, accessible with standard Markdown viewers, and re-importable without data loss.
- Provide a consistent structure for exporting single items (e.g., wiki entries) and collections, supporting attachments and derived metadata.

## Package Layout
Exports are packaged as a directory or archive with the following structure:

```
<export_root>/
  manifest.json                     # Top-level bundle manifest (see below)
  items/
    <item_id>/
      content.md                   # Human-readable Markdown body with inline object tokens
      objects.json                 # Sidecar JSON listing structured objects referenced in content.md
      assets/                      # Binary assets linked from the item (images, files)
        <object_id>.<ext>
```

### manifest.json
Describes the export bundle, schema versions, and metadata.

```json
{
  "version": "1.0",
  "generated_at": "2025-10-20T20:55:00Z",
  "exporter": "eirenhall.exporter/0.3.0",
  "items": [
    {
      "id": "wiki_987654",
      "type": "wiki_entry",
      "path": "items/wiki_987654/"
    }
  ]
}
```

## Markdown Content (`content.md`)
- Plain Markdown representing the item body, including narratives, checklists, code blocks, etc.
- Structured field values appear inline as **tokens** using a reserved grammar:

```
<<Eirenhall:type:id::rendered_text>>
```
- `type`: canonical field type key (e.g., `money_amount`, `quote`, `code_snippet`).
- `id`: unique identifier within the item (UUID or slug). Reusing the same `id` for multiple appearances references a single JSON object.
- `rendered_text`: human-readable representation. Markdown rules apply (escaped as needed).

### Token Guidelines
- Tokens may appear inline or as standalone lines (e.g., block-level content).
- Escaping `<<` or `>>` within `rendered_text` is performed using HTML entities (`&lt;&lt;`, `&gt;&gt;`).
- Unknown tokens should be displayed verbatim by Markdown viewers; importers treat unknown `type` values as opaque objects.
- For code snippets, wrap the token inside a fenced code block to preserve formatting.

## Sidecar JSON (`objects.json`)
Maps each token `id` to the full structured object representation.

```json
{
  "amount_001": {
    "type": "std.money_amount",
    "schema": "https://eirenhall.com/schema/fields/money_amount.json",
    "value": {
      "value": 150.1,
      "currency": "EUR"
    }
  },
  "quote_002": {
    "type": "std.quote",
    "schema": "https://eirenhall.com/schema/fields/quote.json",
    "value": {
      "text": "Any sufficiently advanced technology...",
      "attribution": "Arthur C. Clarke"
    }
  }
}
```

- Each entry includes `type` and `schema` references to support validation during import.
- `value` holds the JSON payload as defined by the field schema.
- Importers rehydrate the structured fields by replacing tokens with the JSON data.

## Attachments & Media
- Binary artifacts (images, files) referenced in the Markdown should use relative paths (e.g., `![diagram](assets/image_001.png)`).
- Corresponding `file_reference` or `image_reference` objects in `objects.json` include metadata (hash, size, media type).
- An `assets/manifest.json` file may list checksums to verify integrity.

## Collections & Multi-item Exports
- When exporting multiple items, the top-level `manifest.json` enumerates all item directories.
- Optional `collections/` directory contains saved search definitions, with manifests referencing included item IDs.

## Import Process Overview
1. Read `manifest.json` to discover bundle contents.
2. For each item:
   - Parse `content.md`, capture tokens, and build rendered Markdown for display.
   - Load `objects.json`, validate each entry against the schema referenced in `type`/`schema`.
   - Reattach binary assets as `binary_reference` objects, ensuring checksums match.
3. Reconstruct the item payload (e.g., `fields.body`, structured fields) from tokens, falling back to raw Markdown if a token type is unknown.
4. Preserve provenance metadata such as `generated_at`, exporter version, and sensitivity settings.

## Extensibility & Versioning
- The root manifest `version` and `objects.json` entries should increment when format changes occur.
- Importers encountering a newer version must degrade gracefully: warn, skip unknown tokens, but retain raw Markdown text.
- Additional metadata (e.g., item-level attributes, derived metrics) can be added to `objects.json` under reserved keys like `_meta`.

## Open Questions & TODOs
- Embed an automatic references section summarizing object IDs/types (scientific-paper style) for quick parsing.
- Allow embedding `objects.json` as front matter when payload = ~10?kB; omit separate catalog in that case.
- Use a simple checksum per asset for tamper detection; no additional manifest required initially.
- Package bulk exports as ZIP archives; streaming support can target ZIP-compatible tooling.
- Provide reference exporter/importer tooling and unit tests demonstrating round-trip fidelity.
