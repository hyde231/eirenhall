"""Schema loader that keeps a manifest of checksums on disk."""
from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, List, Mapping

try:  # Optional dependency, used only when available.
    import yaml  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    yaml = None  # type: ignore

from kernel.observability import emit_event, trace_span

from . import TypeRegistry

SUPPORTED_EXTENSIONS = {".json", ".yaml", ".yml"}


@dataclass
class SchemaLoadReport:
    """Summary of a loader run."""

    loaded: List[str] = field(default_factory=list)
    unchanged: List[str] = field(default_factory=list)
    removed: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, List[str]]:
        return {
            "loaded": list(self.loaded),
            "unchanged": list(self.unchanged),
            "removed": list(self.removed),
        }


class SchemaLoader:
    """Load schema files into a :class:`TypeRegistry` with persistence."""

    def __init__(
        self,
        schema_root: Path | str,
        registry: TypeRegistry,
        manifest_dir: Path | str = "var/registry",
        manifest_name: str | None = None,
    ) -> None:
        self.schema_root = Path(schema_root)
        self.registry = registry
        self.manifest_dir = Path(manifest_dir)
        self.manifest_dir.mkdir(parents=True, exist_ok=True)
        suffix = "json" if manifest_name is None else Path(manifest_name).suffix.lstrip(".") or "json"
        if manifest_name is None:
            manifest_name = f"schemas.{suffix}"
        self.manifest_path = self.manifest_dir / manifest_name

    def load(self) -> SchemaLoadReport:
        with trace_span(
            "registry.load_schemas",
            schema_root=str(self.schema_root),
            manifest_path=str(self.manifest_path),
        ) as span_id:
            manifest = self._read_manifest()
            report = SchemaLoadReport()
            discovered = {}

            for path in self._discover_schema_files():
                key = path.relative_to(self.schema_root).as_posix()
                checksum = self._checksum(path)
                previous_checksum = manifest.get("schemas", {}).get(key, {}).get("checksum")
                should_skip = previous_checksum == checksum and key in self.registry

                if should_skip:
                    report.unchanged.append(key)
                    discovered[key] = {"checksum": checksum}
                    emit_event(
                        "registry.schema.skipped",
                        span_id=span_id,
                        key=key,
                        checksum=checksum,
                    )
                    continue

                data = self._load_schema(path)
                self.registry.register(key, data, overwrite=True)
                report.loaded.append(key)
                discovered[key] = {"checksum": checksum}
                emit_event(
                    "registry.schema.loaded",
                    span_id=span_id,
                    key=key,
                    checksum=checksum,
                )

            for key in sorted(set(manifest.get("schemas", {})) - set(discovered)):
                if key in self.registry:
                    self.registry.deregister(key)
                report.removed.append(key)
                emit_event(
                    "registry.schema.removed",
                    span_id=span_id,
                    key=key,
                )

            self._write_manifest(discovered)
            emit_event(
                "registry.schema.manifest_written",
                span_id=span_id,
                manifest=str(self.manifest_path),
                count=len(discovered),
            )
            emit_event(
                "registry.schema.load_complete",
                span_id=span_id,
                loaded=len(report.loaded),
                skipped=len(report.unchanged),
                removed=len(report.removed),
            )
        return report

    def _discover_schema_files(self) -> Iterable[Path]:
        if not self.schema_root.exists():
            return []
        files: List[Path] = []
        for path in sorted(self.schema_root.rglob("*")):
            if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS:
                files.append(path)
        return files

    def _load_schema(self, path: Path) -> Mapping[str, object]:
        suffix = path.suffix.lower()
        with path.open("r", encoding="utf-8") as handle:
            content = handle.read()
        if suffix == ".json":
            return json.loads(content)
        if suffix in {".yaml", ".yml"}:
            if yaml is None:
                return self._load_simple_yaml(content)
            data = yaml.safe_load(content)
            return data or {}
        raise ValueError(f"Unsupported schema format: {path.suffix}")

    @staticmethod
    def _load_simple_yaml(content: str) -> Mapping[str, object]:
        """Parse a restricted YAML subset without external dependencies."""

        result: Dict[str, object] = {}
        current_list: list[str] | None = None
        for raw_line in content.splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("-"):
                if current_list is None:
                    raise RuntimeError("Invalid YAML structure: list item without key")
                item = line[1:].strip()
                current_list.append(item)
                continue
            if ":" not in line:
                raise RuntimeError("Invalid YAML line: missing ':' delimiter")
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()
            if value:
                result[key] = value
                current_list = None
            else:
                current_list = []
                result[key] = current_list
        return result

    def _checksum(self, path: Path) -> str:
        digest = hashlib.sha256()
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(4096), b""):
                digest.update(chunk)
        return digest.hexdigest()

    def _read_manifest(self) -> Dict[str, Dict[str, Dict[str, str]]]:
        if not self.manifest_path.exists():
            return {}
        suffix = self.manifest_path.suffix.lower()
        with self.manifest_path.open("r", encoding="utf-8") as handle:
            content = handle.read().strip()
            if not content:
                return {}
            if suffix in {".yaml", ".yml"}:
                if yaml is None:
                    raise RuntimeError("PyYAML is required to read YAML manifests")
                loaded = yaml.safe_load(content) or {}
            else:
                loaded = json.loads(content)
        if not isinstance(loaded, dict):
            raise ValueError("Manifest content must be a mapping")
        if "schemas" not in loaded:
            loaded["schemas"] = {}
        return loaded

    def _write_manifest(self, schemas: Mapping[str, Mapping[str, str]]) -> None:
        payload = {
            "version": 1,
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "schemas": {key: {"checksum": value["checksum"]} for key, value in schemas.items()},
        }
        suffix = self.manifest_path.suffix.lower()
        with self.manifest_path.open("w", encoding="utf-8") as handle:
            if suffix in {".yaml", ".yml"}:
                if yaml is None:
                    raise RuntimeError("PyYAML is required to write YAML manifests")
                yaml.safe_dump(payload, handle)
            else:
                json.dump(payload, handle, indent=2, sort_keys=True)
                handle.write("\n")


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Load schemas into the registry")
    parser.add_argument("--schema-root", default="schema", help="Directory containing schema documents")
    parser.add_argument(
        "--manifest-dir",
        default="var/registry",
        help="Directory where the manifest will be stored",
    )
    parser.add_argument(
        "--manifest-name",
        default=None,
        help="Optional manifest filename (defaults to schemas.json)",
    )
    parser.add_argument(
        "--registry-dump",
        default=None,
        help="Optional path to write the loaded registry contents as JSON",
    )
    args = parser.parse_args(list(argv) if argv is not None else None)

    registry = TypeRegistry()
    loader = SchemaLoader(
        schema_root=Path(args.schema_root),
        registry=registry,
        manifest_dir=Path(args.manifest_dir),
        manifest_name=args.manifest_name,
    )
    report = loader.load()

    summary = report.to_dict()
    print(json.dumps(summary, indent=2, sort_keys=True))

    if args.registry_dump:
        dump_path = Path(args.registry_dump)
        dump_path.parent.mkdir(parents=True, exist_ok=True)
        registry_payload = {name: value for name, value in registry.list()}
        dump_path.write_text(json.dumps(registry_payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    return 0


if __name__ == "__main__":  # pragma: no cover - CLI entrypoint
    raise SystemExit(main())
