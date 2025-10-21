from __future__ import annotations

import pytest

from kernel.capabilities import bootstrap_capabilities, get_capability, list_capabilities


def test_bootstrap_registers_capabilities() -> None:
    bootstrap_capabilities(force=True)
    keys = list_capabilities()
    assert "read" in keys
    assert "conversations.timeline" in keys
    assert "directory.profile" in keys

    definition = get_capability("conversations.timeline")
    assert definition.version == "1.0.0"
    assert "timeline" in definition.affordances
    assert definition.dependencies == ("read",)

    directory = get_capability("directory.profile")
    assert directory.metadata_namespace == "cap.directory.profile"
    assert "analytics" in directory.affordances


def test_unknown_capability_lookup() -> None:
    bootstrap_capabilities(force=True)
    with pytest.raises(KeyError):
        get_capability("nonexistent.capability")
