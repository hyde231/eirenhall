# Registry lifecycle

This document describes how schema definitions are ingested into the kernel and
kept in sync with the filesystem using the registry tooling introduced in this
change set.

## Components

### `TypeRegistry`

* Located at `src/kernel/registry/__init__.py`.
* Maintains an ordered in-memory mapping from a schema identifier to its parsed
  representation.
* Exposes four primary operations:
  * `register(name, value, *, overwrite=False)` – adds a new entry and optionally
    overwrites existing definitions.
  * `get(name)` – fetches the stored value and raises `KeyError` when the schema
    is not registered.
  * `list()` – returns a tuple of `(name, value)` pairs in insertion order.
  * `deregister(name)` – removes an entry from the registry and returns the
    stored value.
* Additional helpers include `clear()` and the ability to iterate over the
  registry directly.

### `SchemaLoader`

* Implemented in `src/kernel/registry/loader.py`.
* Discovers JSON and YAML schema documents within a provided root directory.
* Calculates a SHA-256 checksum for every schema to track changes over time.
* Registers parsed schemas into a supplied `TypeRegistry` instance, only
  re-reading files when the checksum differs or the registry does not yet hold
  the entry.
* Removes registry entries for schemas that disappeared from the filesystem.
* Persists checksum metadata to `var/registry/schemas.json` (or another
  user-specified manifest path). The manifest includes the generation timestamp
  and is updated after each load.

## Loader lifecycle

1. **Discovery** – the loader walks the schema root (recursively) and collects
   files with supported extensions (`.json`, `.yaml`, `.yml`).
2. **Checksum evaluation** – for each schema, the loader computes a SHA-256 hash
   and compares it to the persisted manifest entry.
3. **Registry synchronisation** – schemas with new or missing checksums are
   parsed and registered; unchanged schemas already present in the registry are
   skipped. When a schema is removed from disk, it is also deregistered.
4. **Manifest persistence** – once the filesystem and registry are reconciled,
   the loader writes an updated manifest containing the latest checksums and a
   UTC timestamp.

The loader returns a `SchemaLoadReport` that summarises which schemas were
loaded, skipped (unchanged), or removed. This can be used to drive logging or
additional automation.

## CLI usage

To synchronise schemas from the command line run:

```bash
python -m kernel.registry.loader --schema-root schema --manifest-dir var/registry
```

This command loads schemas from the repository’s `schema/` directory into a
fresh registry instance and emits a short report. The manifest directory is
created automatically if it does not already exist.

Additional options are available:

* `--manifest-name` – override the default `schemas.json` manifest filename.
* `--registry-dump` – when provided, serialises the resulting registry to the
  specified JSON file for inspection or debugging.

## Notes

* YAML schema support is optional and requires PyYAML to be installed. If it is
  not available, YAML schemas will trigger a runtime error prompting the user to
  install the dependency.
* The loader keeps manifest files compact – only the schema identifier and its
  checksum are persisted alongside metadata about when the manifest was
  generated. This keeps the persistence lightweight while still allowing change
  detection across restarts.
