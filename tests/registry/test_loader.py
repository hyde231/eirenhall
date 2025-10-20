from __future__ import annotations

import json
from pathlib import Path

import pytest

from kernel.registry import SchemaLoader, TypeRegistry


@pytest.fixture()
def schema_dir(tmp_path: Path) -> Path:
    directory = tmp_path / "schema"
    directory.mkdir()
    (directory / "example.json").write_text(
        json.dumps({"title": "Example", "type": "object"}),
        encoding="utf-8",
    )
    (directory / "nested").mkdir()
    (directory / "nested" / "other.json").write_text(
        json.dumps({"title": "Nested", "type": "object"}),
        encoding="utf-8",
    )
    return directory


@pytest.fixture()
def manifest_dir(tmp_path: Path) -> Path:
    directory = tmp_path / "var" / "registry"
    directory.mkdir(parents=True)
    return directory


def test_loader_registers_and_persists(schema_dir: Path, manifest_dir: Path) -> None:
    registry = TypeRegistry()
    loader = SchemaLoader(schema_dir, registry, manifest_dir)

    report = loader.load()

    assert sorted(report.loaded) == ["example.json", "nested/other.json"]
    assert report.unchanged == []
    assert report.removed == []

    assert registry.get("example.json") == {"title": "Example", "type": "object"}
    assert registry.get("nested/other.json") == {"title": "Nested", "type": "object"}

    manifest_path = manifest_dir / "schemas.json"
    assert manifest_path.exists()
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert set(manifest["schemas"].keys()) == {"example.json", "nested/other.json"}


def test_loader_tracks_changes(schema_dir: Path, manifest_dir: Path) -> None:
    registry = TypeRegistry()
    loader = SchemaLoader(schema_dir, registry, manifest_dir)
    loader.load()

    report = loader.load()
    assert sorted(report.unchanged) == ["example.json", "nested/other.json"]
    assert report.loaded == []

    # Modify a schema and remove another
    (schema_dir / "example.json").write_text(
        json.dumps({"title": "Example", "type": "object", "additionalProperties": False}),
        encoding="utf-8",
    )
    (schema_dir / "nested" / "other.json").unlink()

    report = loader.load()
    assert report.loaded == ["example.json"]
    assert report.removed == ["nested/other.json"]

    # Loading into a new registry should still populate values even if manifest matches.
    new_registry = TypeRegistry()
    new_loader = SchemaLoader(schema_dir, new_registry, manifest_dir)
    report = new_loader.load()
    assert report.loaded == ["example.json"]
    assert new_registry.get("example.json") == {
        "title": "Example",
        "type": "object",
        "additionalProperties": False,
    }
