#!/usr/bin/env python3
"""Validate fixture payloads against the item base schema."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Iterable

try:
    from jsonschema import Draft7Validator, RefResolver  # type: ignore
except ModuleNotFoundError:  # pragma: no cover - fallback for offline environments
    from jsonschema_stub import Draft7Validator, RefResolver


def load_schema(schema_path: Path) -> dict:
    with schema_path.open("r", encoding="utf-8") as fp:
        schema = json.load(fp)
    schema["__base_path__"] = schema_path.parent
    return schema


def iter_fixtures(fixtures_dir: Path) -> Iterable[Path]:
    for path in sorted(fixtures_dir.glob("*.json")):
        if path.is_file():
            yield path


def validate(fixtures: Iterable[Path], schema: dict, resolver: RefResolver) -> int:
    validator = Draft7Validator(schema, resolver=resolver)
    failures = 0
    for fixture in fixtures:
        with fixture.open("r", encoding="utf-8") as fp:
            payload = json.load(fp)
        errors = sorted(validator.iter_errors(payload), key=lambda e: e.path)
        if errors:
            failures += 1
            print(f"✖ {fixture.relative_to(Path.cwd())}")
            for error in errors:
                location = ".".join(str(part) for part in error.path)
                print(f"    → {location or '<root>'}: {error.message}")
        else:
            print(f"✔ {fixture.relative_to(Path.cwd())}")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--fixtures",
        type=Path,
        default=Path("tests/fixtures/items"),
        help="Directory containing fixture payloads to validate.",
    )
    parser.add_argument(
        "--schema",
        type=Path,
        default=Path("schema/item_base.json"),
        help="Schema file to validate against.",
    )
    args = parser.parse_args()

    schema_path = args.schema.resolve()
    schema = load_schema(schema_path)
    base_uri = schema_path.parent.resolve().as_uri() + "/"
    resolver = RefResolver(base_uri=base_uri, referrer=schema)

    fixtures_dir = args.fixtures.resolve()
    failures = validate(iter_fixtures(fixtures_dir), schema, resolver)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
