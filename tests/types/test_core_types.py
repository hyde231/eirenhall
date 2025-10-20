from __future__ import annotations

import pytest

from kernel.types import (
    DocumentType,
    TaskType,
    WikiType,
    bootstrap_types,
    list_registered_types,
)
from kernel.types.base import TypeManifest


def test_bootstrap_registers_core_types() -> None:
    bootstrap_types(force=True)
    assert list_registered_types() == ("document", "task", "wiki")


def test_manifest_validation_success() -> None:
    manifest = TypeManifest.from_mapping(
        {"type": "example", "schema": "example.json", "capabilities": ["read", "write", "read"]},
        source="example.yaml",
    )
    assert manifest.type_key == "example"
    assert manifest.schema_ref == "example.json"
    assert manifest.capabilities == ("read", "write")


@pytest.mark.parametrize(
    "payload",
    [
        {},
        {"type": "", "schema": "example.json"},
        {"type": "example", "schema": ""},
        {"type": "example", "schema": "example.json", "capabilities": "not-a-list"},
        {"type": "example", "schema": "example.json", "capabilities": ["", "read"]},
    ],
)
def test_manifest_validation_errors(payload: dict[str, object]) -> None:
    with pytest.raises(ValueError):
        TypeManifest.from_mapping(payload, source="invalid.yaml")


@pytest.mark.parametrize(
    "type_cls, capability, expected",
    [
        (DocumentType, "read", True),
        (DocumentType, "manage", False),
        (TaskType, "manage", True),
        (WikiType, "comment", True),
        (WikiType, "archive", False),
    ],
)
def test_capability_queries(type_cls, capability: str, expected: bool) -> None:
    bootstrap_types(force=True)
    assert type_cls.supports(capability) is expected
    if expected:
        type_cls.require_capability(capability)
    else:
        with pytest.raises(ValueError):
            type_cls.require_capability(capability)


def test_metadata_accessors() -> None:
    bootstrap_types(force=True)
    assert DocumentType.schema_ref() == "item_base.json"
    assert TaskType.capabilities() == ("read", "write", "comment", "manage")
    assert WikiType.type_key() == "wiki"
