from pathlib import Path

import pytest

from kernel.governance import PersonaManifest, load_personas


PERSONA_ROOT = Path("personas")


@pytest.fixture(scope="module")
def manifests() -> tuple[PersonaManifest, ...]:
    return load_personas(PERSONA_ROOT)


def test_persona_files_exist(manifests: tuple[PersonaManifest, ...]) -> None:
    names = {manifest.id for manifest in manifests}
    assert names == {
        "persona.librarian",
        "persona.system_advisor",
        "persona.assistant",
        "persona.coding_assistant",
    }


def test_write_permissions_flagged(manifests: tuple[PersonaManifest, ...]) -> None:
    for manifest in manifests:
        for permission in manifest.write_permissions:
            assert permission.action
            if permission.requires_approval:
                # Dry run is preferred, but explicit opt-out is allowed.
                assert isinstance(permission.dry_run_only, bool)


def test_safety_rails_present(manifests: tuple[PersonaManifest, ...]) -> None:
    for manifest in manifests:
        assert manifest.safety_rails, f"{manifest.id} must declare safety rails"
        assert manifest.dry_run_default, f"{manifest.id} must default to dry-run mode"


def test_data_access_scopes_are_non_empty(manifests: tuple[PersonaManifest, ...]) -> None:
    for manifest in manifests:
        for scope_name, scope_values in manifest.data_access.items():
            assert scope_values, f"{manifest.id}: data_access.{scope_name} cannot be empty"
