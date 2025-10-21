import json
from pathlib import Path
from typing import Iterable, Mapping

import pytest

from scripts.jsonschema_stub import Draft7Validator, RefResolver


SCHEMA_PATH = Path("schema/item_base.json")
VALID_FIXTURES = Path("tests/fixtures/items")
INVALID_FIXTURES = Path("tests/fixtures/items_invalid")


@pytest.fixture(scope="module")
def validator() -> Draft7Validator:
    schema = _load_json(SCHEMA_PATH)
    schema["__base_path__"] = SCHEMA_PATH.parent
    base_uri = SCHEMA_PATH.parent.resolve().as_uri() + "/"
    resolver = RefResolver(base_uri=base_uri, referrer=schema)
    return Draft7Validator(schema, resolver=resolver)


def _load_json(path: Path) -> Mapping[str, object]:
    with path.open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def _iter_fixture_paths(root: Path) -> Iterable[Path]:
    return sorted(p for p in root.glob("*.json") if p.is_file())


def test_valid_fixtures_have_required_envelope() -> None:
    required_keys = {
        "id",
        "item_type",
        "title",
        "realm",
        "sensitivity",
        "capabilities",
        "fields",
        "metadata",
        "derived",
    }
    missing = {}
    for path in _iter_fixture_paths(VALID_FIXTURES):
        payload = _load_json(path)
        absent = sorted(key for key in required_keys if key not in payload)
        if absent:
            missing[path.name] = absent
    assert not missing, f"Valid fixtures are missing envelope keys: {missing}"


def test_invalid_fixtures_fail_validation(validator: Draft7Validator) -> None:
    failing = {}
    for path in _iter_fixture_paths(INVALID_FIXTURES):
        payload = _load_json(path)
        found = list(validator.iter_errors(payload))
        if not found:
            failing[path.name] = "expected schema violations but found none"
    assert not failing, f"Invalid fixtures unexpectedly passed validation: {failing}"
