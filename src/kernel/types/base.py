"""Type registry integration helpers and mixins."""
from __future__ import annotations

import os
import threading
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterator, Mapping, Sequence, Tuple

from kernel.registry import SchemaLoader, TypeRegistry

__all__ = [
    "TypeManifest",
    "bootstrap_types",
    "get_manifest",
    "iter_manifests",
    "list_registered_types",
    "TypeDefinitionMixin",
]


@dataclass(frozen=True)
class TypeManifest:
    """Validated metadata describing a kernel type."""

    type_key: str
    schema_ref: str
    capabilities: Tuple[str, ...]

    @classmethod
    def from_mapping(cls, payload: Mapping[str, object], *, source: str) -> "TypeManifest":
        """Create a manifest from ``payload`` raising ``ValueError`` on errors."""

        def _require_str(name: str) -> str:
            value = payload.get(name)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"'{name}' must be a non-empty string in {source}")
            return value.strip()

        type_key = _require_str("type")
        schema_ref = _require_str("schema")

        capabilities_raw = payload.get("capabilities", [])
        if capabilities_raw is None:
            capabilities_raw = []
        if not isinstance(capabilities_raw, Sequence) or isinstance(capabilities_raw, (str, bytes)):
            raise ValueError(f"'capabilities' must be a sequence of strings in {source}")

        seen: Dict[str, None] = {}
        capabilities: list[str] = []
        for capability in capabilities_raw:
            if not isinstance(capability, str) or not capability.strip():
                raise ValueError(f"Capabilities must be non-empty strings in {source}")
            key = capability.strip()
            if key in seen:
                continue
            seen[key] = None
            capabilities.append(key)

        return cls(type_key=type_key, schema_ref=schema_ref, capabilities=tuple(capabilities))


_registry = TypeRegistry()
_manifests_by_type: Dict[str, TypeManifest] = {}
_bootstrap_lock = threading.Lock()
_bootstrapped = False


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def _schema_root() -> Path:
    return _repo_root() / "schema" / "types"


def _manifest_dir() -> Path:
    override = os.environ.get("KERNEL_REGISTRY_CACHE_DIR")
    if override:
        return Path(override)
    return Path(os.environ.get("TMPDIR", "/tmp")) / "kernel-registry"


def bootstrap_types(*, force: bool = False) -> None:
    """Load manifests from disk into memory if needed."""

    global _bootstrapped
    if _bootstrapped and not force:
        return

    with _bootstrap_lock:
        if _bootstrapped and not force:
            return

        _manifests_by_type.clear()
        loader = SchemaLoader(
            schema_root=_schema_root(),
            registry=_registry,
            manifest_dir=_manifest_dir(),
            manifest_name="types.json",
        )
        loader.load()

        for source, payload in _registry:
            if not isinstance(payload, Mapping):
                raise ValueError(f"Manifest '{source}' must contain a mapping")
            manifest = TypeManifest.from_mapping(payload, source=source)
            if manifest.type_key in _manifests_by_type:
                raise ValueError(f"Duplicate type key '{manifest.type_key}' detected")
            _manifests_by_type[manifest.type_key] = manifest

        _bootstrapped = True


def get_manifest(type_key: str) -> TypeManifest:
    """Return the manifest for ``type_key`` raising ``KeyError`` if missing."""

    bootstrap_types()
    try:
        return _manifests_by_type[type_key]
    except KeyError as exc:
        raise KeyError(f"Type '{type_key}' is not registered") from exc


def iter_manifests() -> Iterator[TypeManifest]:
    """Iterate over registered manifests."""

    bootstrap_types()
    return iter(_manifests_by_type.values())


def list_registered_types() -> Tuple[str, ...]:
    """Return a tuple of registered type keys in insertion order."""

    bootstrap_types()
    return tuple(_manifests_by_type.keys())


class TypeDefinitionMixin:
    """Mixin that exposes manifest-backed metadata helpers."""

    TYPE_KEY: str

    @classmethod
    def manifest(cls) -> TypeManifest:
        manifest = get_manifest(cls.TYPE_KEY)
        if manifest.type_key != cls.TYPE_KEY:
            raise ValueError(
                f"Manifest mismatch: expected '{cls.TYPE_KEY}' but received '{manifest.type_key}'"
            )
        return manifest

    @classmethod
    def type_key(cls) -> str:
        return cls.manifest().type_key

    @classmethod
    def schema_ref(cls) -> str:
        return cls.manifest().schema_ref

    @classmethod
    def capabilities(cls) -> Tuple[str, ...]:
        return cls.manifest().capabilities

    @classmethod
    def supports(cls, capability: str) -> bool:
        return capability in cls.capabilities()

    @classmethod
    def require_capability(cls, capability: str) -> None:
        if not cls.supports(capability):
            raise ValueError(f"Type '{cls.type_key()}' does not support '{capability}'")
