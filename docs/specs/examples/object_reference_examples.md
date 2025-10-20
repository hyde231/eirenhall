# Object Reference Examples

Illustrative payloads that comply with `schema/fields/object_reference.json` and
the standard field library entry for `std.object_ref`.

## Minimal item reference
```json
{
  "object_type": "task",
  "object_id": "task_456789"
}
```

## Reference with URI and relationship
```json
{
  "object_type": "incident",
  "object_id": "inc_20251020",
  "uri": "kki://item/inc_20251020",
  "display_name": "INC-20251020 Major Outage",
  "relationship": "depends-on",
  "version": 3
}
```

## Reference with contextual notes
```json
{
  "object_type": "dataset",
  "object_id": "data_catalog_prod",
  "uri": "https://data.example.com/catalogs/prod",
  "display_name": "Production Catalog",
  "relationship": "source-of-truth",
  "notes": {
    "type": "delta",
    "ops": [
      {
        "insert": "Linked for lineage tracing\n"
      }
    ]
  }
}
```
