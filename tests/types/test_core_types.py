from __future__ import annotations

from pathlib import Path

import pytest

from kernel.types import (
    AccountStatementType,
    ConversationThreadType,
    CorrespondenceType,
    DocumentType,
    FinancialAccountType,
    FinancialTransactionType,
    OrganizationType,
    PersonType,
    ProjectType,
    TaskType,
    WikiEntryType,
    bootstrap_types,
    list_registered_types,
)
from kernel.types.base import TypeManifest


def test_bootstrap_registers_core_types() -> None:
    bootstrap_types(force=True)
    assert list_registered_types() == (
        "account_statement",
        "conversation_thread",
        "correspondence",
        "dashboard",
        "document",
        "financial_account",
        "financial_transaction",
        "organization",
        "person",
        "project",
        "task",
        "wiki_entry",
    )


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
        (WikiEntryType, "comment", True),
        (WikiEntryType, "archive", False),
        (FinancialAccountType, "manage", True),
        (FinancialTransactionType, "comment", True),
        (FinancialTransactionType, "manage", False),
        (AccountStatementType, "manage", False),
        (ProjectType, "projects.workspace", True),
        (ProjectType, "conversations.timeline", False),
        (CorrespondenceType, "correspondence.archive", True),
        (CorrespondenceType, "projects.workspace", False),
        (ConversationThreadType, "conversations.timeline", True),
        (PersonType, "directory.profile", True),
        (OrganizationType, "directory.profile", True),
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
    assert WikiEntryType.type_key() == "wiki_entry"
    assert FinancialAccountType.schema_ref() == "item_base.json"
    assert FinancialAccountType.capabilities() == ("read", "write", "comment", "manage")
    assert FinancialTransactionType.capabilities() == ("read", "write", "comment")
    assert AccountStatementType.type_key() == "account_statement"
    assert ProjectType.capabilities() == ("read", "write", "comment", "manage", "projects.workspace")
    assert CorrespondenceType.capabilities() == (
        "read",
        "write",
        "comment",
        "manage",
        "correspondence.archive",
    )
    assert ConversationThreadType.capabilities() == (
        "read",
        "write",
        "comment",
        "manage",
        "conversations.timeline",
    )
    assert PersonType.capabilities() == (
        "read",
        "write",
        "comment",
        "manage",
        "directory.profile",
    )
    assert OrganizationType.capabilities() == (
        "read",
        "write",
        "comment",
        "manage",
        "directory.profile",
    )


def test_bootstrap_rejects_unknown_capability(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    capability_dir = tmp_path / "capabilities"
    capability_dir.mkdir()

    type_dir = tmp_path / "types"
    type_dir.mkdir()
    (type_dir / "example.yaml").write_text(
        "type: example\nschema: item_base.json\ncapabilities:\n  - nonexistent.capability\n",
        encoding="utf-8",
    )

    cache_dir = tmp_path / "cache"
    monkeypatch.setenv("KERNEL_CAPABILITY_SCHEMA_DIR", str(capability_dir))
    monkeypatch.setenv("KERNEL_REGISTRY_CACHE_DIR", str(cache_dir))

    import kernel.types.base as types_base

    monkeypatch.setattr(types_base, "_schema_root", lambda: type_dir)

    with pytest.raises(ValueError, match="unknown capability"):
        bootstrap_types(force=True)


def test_bootstrap_rejects_missing_capability_dependencies(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    capability_dir = tmp_path / "capabilities"
    capability_dir.mkdir()
    (capability_dir / "example.timeline.yaml").write_text(
        (
            "key: example.timeline\n"
            "version: 1.0.0\n"
            "summary: Example timeline capability\n"
            "configuration_schema: null\n"
            "affordances:\n"
            "  - timeline\n"
            "dependencies:\n"
            "  - read\n"
            "metadata_namespace: cap.example.timeline\n"
            "events: []\n"
        ),
        encoding="utf-8",
    )

    type_dir = tmp_path / "types"
    type_dir.mkdir()
    (type_dir / "example.yaml").write_text(
        "type: example\nschema: item_base.json\ncapabilities:\n  - example.timeline\n",
        encoding="utf-8",
    )

    cache_dir = tmp_path / "cache"
    monkeypatch.setenv("KERNEL_CAPABILITY_SCHEMA_DIR", str(capability_dir))
    monkeypatch.setenv("KERNEL_REGISTRY_CACHE_DIR", str(cache_dir))

    import kernel.types.base as types_base

    monkeypatch.setattr(types_base, "_schema_root", lambda: type_dir)

    with pytest.raises(ValueError, match="missing capability dependencies"):
        bootstrap_types(force=True)
