"""Capability registry utilities."""
from __future__ import annotations

import os
import re
import threading
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, Iterator, Mapping, Sequence, Tuple

from kernel.registry import SchemaLoader, TypeRegistry

__all__ = [
    "CapabilityDefinition",
    "bootstrap_capabilities",
    "get_capability",
    "iter_capabilities",
    "list_capabilities",
]

_KEY_PATTERN = re.compile(r"^[a-z]+(?:\.[a-z0-9_]+)+$")
_SEMVER_PATTERN = re.compile(r"^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?$")


@dataclass(frozen=True)
class CapabilityDefinition:
    """Validated metadata describing a capability contract."""

    key: str
    version: str
    summary: str
    configuration_schema: str | None
    affordances: Tuple[str, ...]
    dependencies: Tuple[str, ...]
    metadata_namespace: str | None
    events: Tuple[str, ...]

    @classmethod
    def from_mapping(cls, payload: Mapping[str, object], *, source: str) -> "CapabilityDefinition":
        """Create a definition from ``payload`` raising ``ValueError`` on errors."""

        def _require_str(name: str, *, allow_empty: bool = False) -> str:
            value = payload.get(name)
            if not isinstance(value, str):
                raise ValueError(f"'{name}' must be a string in {source}")
            if not value.strip() and not allow_empty:
                raise ValueError(f"'{name}' must be a non-empty string in {source}")
            return value.strip()

        key = _require_str("key")
        if not _KEY_PATTERN.fullmatch(key):
            raise ValueError(f"Capability key '{key}' in {source} must match '{_KEY_PATTERN.pattern}'")

        version = _require_str("version")
        if not _SEMVER_PATTERN.fullmatch(version):
            raise ValueError(f"Capability '{key}' in {source} must declare a semantic version")

        summary = _require_str("summary")

        configuration_schema_raw = payload.get("configuration_schema")
        configuration_schema: str | None
        if configuration_schema_raw in {None, ""}:
            configuration_schema = None
        elif isinstance(configuration_schema_raw, str):
            configuration_schema = configuration_schema_raw.strip() or None
        else:
            raise ValueError(f"'configuration_schema' for capability '{key}' in {source} must be a string or null")

        affordances_raw = payload.get("affordances", [])
        affordances = _normalize_string_list(
            affordances_raw,
            field="affordances",
            source=source,
            allow_empty=True,
        )

        dependencies_raw = payload.get("dependencies", [])
        dependencies = _normalize_string_list(
            dependencies_raw,
            field="dependencies",
            source=source,
            allow_empty=True,
        )

        metadata_namespace_raw = payload.get("metadata_namespace")
        metadata_namespace: str | None
        if metadata_namespace_raw in {None, ""}:
            metadata_namespace = None
        elif isinstance(metadata_namespace_raw, str):
            metadata_namespace = metadata_namespace_raw.strip() or None
        else:
            raise ValueError(
                f"'metadata_namespace' for capability '{key}' in {source} must be a string or null"
            )

        events_raw = payload.get("events", [])
        events = _normalize_string_list(
            events_raw,
            field="events",
            source=source,
            allow_empty=True,
        )

        return cls(
            key=key,
            version=version,
            summary=summary,
            configuration_schema=configuration_schema,
            affordances=affordances,
            dependencies=dependencies,
            metadata_namespace=metadata_namespace,
            events=events,
        )


_registry = TypeRegistry()
_capabilities_by_key: Dict[str, CapabilityDefinition] = {}
_bootstrap_lock = threading.Lock()
_bootstrapped = False


def bootstrap_capabilities(*, force: bool = False) -> None:
    """Load capability definitions from disk."""

    global _bootstrapped

    if _bootstrapped and not force:
        return

    with _bootstrap_lock:
        if _bootstrapped and not force:
            return

        _capabilities_by_key.clear()

        loader = SchemaLoader(
            schema_root=_schema_root(),
            registry=_registry,
            manifest_dir=_manifest_dir(),
            manifest_name="capabilities.json",
        )
        loader.load()

        for source, payload in _registry:
            if not isinstance(payload, Mapping):
                raise ValueError(f"Capability document '{source}' must contain a mapping")
            definition = CapabilityDefinition.from_mapping(payload, source=source)
            if definition.key in _capabilities_by_key:
                raise ValueError(f"Duplicate capability key '{definition.key}' detected")
            _capabilities_by_key[definition.key] = definition

        for definition in _builtin_capabilities():
            _capabilities_by_key.setdefault(definition.key, definition)

        _bootstrapped = True


def get_capability(key: str) -> CapabilityDefinition:
    """Return the capability definition for ``key``."""

    bootstrap_capabilities()
    try:
        return _capabilities_by_key[key]
    except KeyError as exc:
        raise KeyError(f"Capability '{key}' is not registered") from exc


def iter_capabilities() -> Iterator[CapabilityDefinition]:
    """Iterate over registered capability definitions."""

    bootstrap_capabilities()
    return iter(_capabilities_by_key.values())


def list_capabilities() -> Tuple[str, ...]:
    """Return registered capability keys in insertion order."""

    bootstrap_capabilities()
    return tuple(_capabilities_by_key.keys())


def _normalize_string_list(
    value: object,
    *,
    field: str,
    source: str,
    allow_empty: bool,
) -> Tuple[str, ...]:
    if value is None:
        return ()
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        raise ValueError(f"'{field}' must be a list of strings in {source}")
    items: Dict[str, None] = {}
    for entry in value:
        if not isinstance(entry, str):
            raise ValueError(f"Entries in '{field}' must be strings in {source}")
        token = entry.strip()
        if not token and not allow_empty:
            raise ValueError(f"Entries in '{field}' must be non-empty strings in {source}")
        if token:
            items.setdefault(token, None)
    return tuple(items.keys())


def _schema_root() -> Path:
    override = os.environ.get("KERNEL_CAPABILITY_SCHEMA_DIR")
    if override:
        return Path(override)
    return Path(__file__).resolve().parents[3] / "schema" / "capabilities"


def _manifest_dir() -> Path:
    override = os.environ.get("KERNEL_REGISTRY_CACHE_DIR")
    if override:
        return Path(override)
    return Path(os.environ.get("TMPDIR", "/tmp")) / "kernel-registry"


def _builtin_capabilities() -> Iterable[CapabilityDefinition]:
    """Return core capability definitions that do not have schema files."""

    base_capabilities = {
        "read": "Allows viewing of item content.",
        "write": "Allows editing of item content.",
        "comment": "Allows commenting on item content.",
        "manage": "Allows administrative actions on items.",
        "configure": "Allows configuration of dashboards or layouts tied to the item.",
    }
    return (
        CapabilityDefinition(
            key=key,
            version="1.0.0",
            summary=summary,
            configuration_schema=None,
            affordances=(),
            dependencies=(),
            metadata_namespace=None,
            events=(),
        )
        for key, summary in base_capabilities.items()
    )
