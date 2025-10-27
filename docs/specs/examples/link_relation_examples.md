# Link Relation Examples

Illustrative payloads that comply with `schema/relations/link_relation.json` and
the [Linking & Backlink Specification](../linking_and_backlinks.md).

## Basic item-to-item link
```json
{
  "id": "link_rel_a1b2c3d4",
  "source": {
    "object_type": "task",
    "object_id": "task_456789",
    "uri": "eirenhall://item/task_456789"
  },
  "target": {
    "object_type": "wiki_entry",
    "object_id": "wiki_987654",
    "uri": "eirenhall://item/wiki_987654"
  },
  "kind": "item",
  "context": "fields.body",
  "label": "See incident runbook",
  "first_seen_at": "2025-10-20T15:42:10Z",
  "last_seen_at": "2025-10-20T15:42:10Z"
}
```

## Link targeting a specific field anchor
```json
{
  "id": "link_rel_e5f6g7h8",
  "source": {
    "object_type": "wiki_entry",
    "object_id": "wiki_987654",
    "uri": "eirenhall://item/wiki_987654"
  },
  "target": {
    "object_type": "task",
    "object_id": "task_456789",
    "uri": "eirenhall://item/task_456789#field/checklist",
    "relationship": "field-anchor"
  },
  "kind": "item",
  "context": "fields.links[0]",
  "label": "Track remediation checklist",
  "first_seen_at": "2025-10-21T09:05:00Z",
  "last_seen_at": "2025-10-22T10:11:45Z",
  "notes": "Auto-created from wiki body link"
}
```

## Capture-level link
```json
{
  "id": "link_rel_capture01",
  "source": {
    "object_type": "dashboard",
    "object_id": "dashboard_home",
    "uri": "eirenhall://item/dashboard_home"
  },
  "target": {
    "object_type": "capture",
    "object_id": "doc_123456__20240114T140000Z",
    "uri": "eirenhall://item/doc_123456/capture/20240114T140000Z",
    "relationship": "latest-capture"
  },
  "kind": "capture",
  "context": "fields.widgets[2]",
  "label": "Latest quarterly plan capture",
  "first_seen_at": "2025-10-22T08:00:00Z",
  "last_seen_at": "2025-10-23T08:00:00Z"
}
```

## Inclusion link
```json
{
  "id": "link_rel_include01",
  "source": {
    "object_type": "wiki_entry",
    "object_id": "wiki_runbook",
    "uri": "eirenhall://item/wiki_runbook"
  },
  "target": {
    "object_type": "task",
    "object_id": "task_456789",
    "uri": "eirenhall://item/task_456789#field/due_at",
    "relationship": "due-at"
  },
  "kind": "include",
  "context": "fields.body.sections[3]",
  "label": "Embed task due date",
  "first_seen_at": "2025-10-23T09:30:00Z",
  "last_seen_at": "2025-10-23T09:30:00Z"
}
```
