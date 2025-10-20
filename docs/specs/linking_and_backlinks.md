# Linking & Backlink Specification

Defines the canonical linking model for the Knowledge Kernel Initiative,
covering internal URIs, inline reference syntaxes, storage, and backlink
propagation. Complements the field library (`link.json`), metadata governance,
and the relations requirements in FR-030.

## Goals
- Provide a deterministic identifier scheme for items, captures, attachments,
  and other linkable resources.
- Support multiple authoring syntaxes (Markdown links, wiki links) that resolve
  to the same canonical targets.
- Persist outbound links and derived backlinks in predictable metadata
  structures for search, dashboards, and automation.
- Align with relation modeling so links can participate in graph queries and
  saved collections.

## Canonical Identifiers & URIs
All internal references resolve to a `kki://` URI. Downstream services may map
these URIs to HTTP routes or CLI commands, but the canonical form remains
stable.

| Resource | URI pattern | Example |
| --- | --- | --- |
| Item | `kki://item/<item_id>` | `kki://item/task_456789` |
| Item field anchor | `kki://item/<item_id>#field/<field_key>` | `kki://item/task_456789#field/checklist` |
| Capture | `kki://item/<item_id>/capture/<capture_id>` | `kki://item/doc_123456/capture/20240114T140000Z` |
| Attachment | `kki://item/<item_id>/attachment/<attachment_id>` | `kki://item/doc_123456/attachment/att_cover_pdf` |
| Realm | `kki://realm/<realm_id>` | `kki://realm/eng-data` |

Rules:
- `<item_id>` matches the item identifier stored in `id` and must remain
  globally unique.
- Field anchors use the schema field key (snake case) and optional sub-paths
  (`#field/checklist/0` for list elements).
- Capture identifiers default to ISO 8601 timestamps; alternative IDs are
  permitted if declared in the storage blueprint.
- Attachment identifiers mirror the attachment manifest entries.
- Query parameters may be appended (`?view=detail`) but must not alter target
  resolution.

### Deep Linking Guidance
- Prefer stable anchors tied to schema keys or capture identifiers
  (`#field/summary`, `/capture/<timestamp>`). Avoid positional anchors that
  depend on list ordering (`#field/checklist/2`) unless the list entries carry
  immutable IDs.
- When a schema change renames or removes an anchored field, migrations must
  update affected URIs and relation items. Reconciliation jobs should flag
  orphaned anchors as warnings.
- Editors should offer friendly labels for anchors (for example, display field
  titles) while keeping the stored URI canonical.
- When referencing derived data, anchor to the logical metric
  (`#field/derived/progress_summary`) rather than transient presentation
  elements.

## Inline Reference Syntax
Authoring tools must normalize inline references to canonical URIs during save
or ingestion. Two syntaxes are supported out of the box.

### Markdown Links

```
[Label](kki://item/task_456789)
[Checklist](kki://item/task_456789#field/checklist)
[External](https://example.com/spec)
```

Markdown remains the preferred format for export compatibility.

### Wiki Links

```
[[task_456789]]
[[item:task_456789#field/summary]]
[[realm:eng-data]]
[[capture:doc_123456/20240114T140000Z]]
[[https://example.com/spec]]
```

Resolution order:
1. If the link starts with `item:`, `realm:`, `capture:`, resolve directly.
2. Bare identifiers (no prefix) attempt item lookup within the current realm
   context.
3. Strings containing `://` are treated as absolute URIs (internal or external).

Authoring surfaces must display canonical URIs in tooltips or inspector panes
to aid debugging.

## Storage Model

### Outbound Links
Explicit, curated links appear in `fields.links` using the `link.json` field
schema. Each entry includes at minimum `title`, `url`, and `kind` (`reference`,
`attachment`, `external`).

All detected links (including wiki references) are captured under
`metadata.sys.links.outbound` with the following shape:

```
metadata.sys.links = {
  "outbound": [
    {
      "uri": "kki://item/task_456789#field/checklist",
      "kind": "item",
      "context": "fields.body",
      "label": "Checklist",
      "detected_at": "2025-10-20T15:45:00Z"
    }
  ]
}
```

`context` stores the JSON pointer (dot notation) where the link was found. The
`kind` enum mirrors the URI table (`item`, `capture`, `attachment`, `realm`,
`external`).

### Backlinks (Inbound)
Backlinks are derived values surfaced under `metadata.sys.links.inbound`:

```
{
  "uri": "kki://item/wiki_987654",
  "kind": "item",
  "source": "task_456789",
  "context": "fields.body",
  "detected_at": "2025-10-20T15:45:01Z"
}
```

`source` is the originating item identifier for backlink metadata. Backlinks
are read-only; editing occurs on the outbound source. Link relation items
capture richer object references via `std.object_ref`.

### Relation Items
To align with FR-030, each link creates or updates a `link_relation` item with:

```
{
  "id": "link_rel_<hash>",
  "source": {
    "object_type": "task",
    "object_id": "task_456789",
    "uri": "kki://item/task_456789"
  },
  "target": {
    "object_type": "wiki",
    "object_id": "wiki_987654",
    "uri": "kki://item/wiki_987654"
  },
  "kind": "item",
  "context": "fields.body",
  "label": "See runbook",
  "first_seen_at": "...",
  "last_seen_at": "..."
}
```

Relation items enable graph queries, caching, and automation without forcing
core item payloads to carry every link. See
[link_relation.json](../schema/relations/link_relation.json) for the JSON
Schema.

## Inclusion & Transclusion
In addition to plain links, content authors can embed data from other items.
All inclusion directives compile down to canonical URIs so provenance and
backlinks remain accurate.

### Dynamic inclusion
```
{{include:item:wiki_987654}}
{{include:item:task_456789#field/summary}}
```

- Resolves the referenced item or field at render time.
- Displays the latest content subject to realm permissions.
- Recorded under `metadata.sys.includes.dynamic` with the same object shape as
  outbound links (`uri`, `context`, `detected_at`).

### Value inclusion
```
{{value:item:task_456789#field/due_at}}
```

- Pulls the current scalar value (string, number, timestamp) into the host
  document.
- Updates automatically when the source changes.
- Stored under `metadata.sys.includes.values` along with the destination field
  pointer.

### Static copy
```
{{copy:item:doc_123456#field/summary}}
```

- Inserts a snapshot of the referenced value at save time.
- The host item keeps the copied value; no further synchronization occurs.
- Inclusion metadata records the source URI and `copied_at` timestamp so audits
  can trace provenance.

### Inclusion rules
- Inclusion directives share the same URI validation rules as links.
- Capability-specific inclusion features should namespace their metadata under
  `metadata.cap.<capability_key>.includes` while reusing the documented object
  shapes.
- Exporters must preserve inclusion directives and metadata so re-imports can
  reconstruct dynamic references.
- Backlink generation treats inclusions as links; embedded items appear in the
  target's inbound list with `kind = "include"` when additional disambiguation
  is needed.

## Extraction & Reconciliation
1. **Ingress:** When an item is created or updated, the ingestion pipeline
   scans relevant fields (`fields.*`, capability configs, metadata) for `kki://`
   URIs or wiki syntax. Links are normalized and stored in outbound metadata.
2. **Backlink Update:** For each outbound link, the system updates the target's
   inbound metadata. Missing targets are recorded as validation warnings.
3. **Relation Sync:** Link relation items are upserted and stale entries removed
   when links disappear.
4. **Derived Jobs:** Periodic reconciliation jobs ensure backlink lists remain
   consistent, especially when restorations or migrations bypass the normal
   write path.

## Resolution & Rendering
- Clients resolve `kki://` URIs via registry lookups or API helpers; unresolved
  URIs render with warning banners.
- Backlinks display in item sidebars, showing source title, context excerpt,
  and last detected timestamp.
- Dashboards can surface quick links or backlink widgets by querying relation
  items or the `metadata.sys.links` structure.

## Extension Guidelines
- New link kinds must be registered with the namespace registry and documented
  here; prefer extending the URI pattern table instead of ad-hoc prefixes.
- Capability-specific link metadata should live under
  `metadata.cap.<capability_key>.links` but reuse the same object shape.
- When introducing new authoring syntaxes, ensure they compile down to canonical
  URIs before persistence.
- Export tooling must preserve both outbound and inbound metadata, allowing
  re-import to rebuild backlinks.

This specification ensures all linking behavior is predictable, searchable, and
compatible with the broader schema and metadata tooling.


See [link_relation.json](../schema/relations/link_relation.json) for the JSON Schema and [examples](examples/link_relation_examples.md) for sample payloads.



