from __future__ import annotations

import logging
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


def test_loader_registers_and_persists(schema_dir: Path, manifest_dir: Path, caplog) -> None:
    registry = TypeRegistry()
    loader = SchemaLoader(schema_dir, registry, manifest_dir)

    caplog.set_level(logging.INFO, logger="kernel")
    report = loader.load()
    records = [json.loads(record.message) for record in caplog.records if record.name == "kernel"]

    assert sorted(report.loaded) == ["example.json", "nested/other.json"]
    assert report.unchanged == []
    assert report.removed == []

    assert registry.get("example.json") == {"title": "Example", "type": "object"}
    assert registry.get("nested/other.json") == {"title": "Nested", "type": "object"}

    manifest_path = manifest_dir / "schemas.json"
    assert manifest_path.exists()
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert set(manifest["schemas"].keys()) == {"example.json", "nested/other.json"}

    loaded_events = [record for record in records if record.get("event") == "registry.schema.loaded"]
    assert any(event["key"] == "example.json" for event in loaded_events)
    assert any(event["event"] == "registry.schema.manifest_written" for event in records)


def test_loader_tracks_changes(schema_dir: Path, manifest_dir: Path, caplog) -> None:
    registry = TypeRegistry()
    loader = SchemaLoader(schema_dir, registry, manifest_dir)
    loader.load()

    caplog.set_level(logging.INFO, logger="kernel")
    caplog.clear()
    report = loader.load()
    assert sorted(report.unchanged) == ["example.json", "nested/other.json"]
    assert report.loaded == []

    # Modify a schema and remove another
    (schema_dir / "example.json").write_text(
        json.dumps({"title": "Example", "type": "object", "additionalProperties": False}),
        encoding="utf-8",
    )
    (schema_dir / "nested" / "other.json").unlink()

    caplog.clear()
    report = loader.load()
    assert report.loaded == ["example.json"]
    assert report.removed == ["nested/other.json"]
    removal_events = []
    for record in caplog.records:
        if record.name != "kernel":
            continue
        payload = json.loads(record.message)
        if payload.get("event") == "registry.schema.removed":
            removal_events.append(payload)
    assert any(event.get("key") == "nested/other.json" for event in removal_events)

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
