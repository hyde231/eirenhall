#!/usr/bin/env python3
"""Run a proof-of-concept workflow that exercises the derived evaluator."""
from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Iterable, List, Mapping, MutableMapping, Sequence, Tuple

try:  # Optional dependency
    import jsonschema  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    jsonschema = None  # type: ignore

REPO_ROOT = Path(__file__).resolve().parent.parent
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from kernel.derived import DerivedEvaluator, EvaluationResult
from kernel.registry import SchemaLoader, TypeRegistry
from kernel.types import bootstrap_types, get_manifest, list_registered_types
SCHEMA_ROOT = REPO_ROOT / "schema"
DEFAULT_ITEMS_DIR = REPO_ROOT / "tests" / "fixtures" / "items"


def load_items(directory: Path) -> List[Tuple[Path, MutableMapping[str, object]]]:
    items: List[Tuple[Path, MutableMapping[str, object]]] = []
    for path in sorted(directory.glob("*.json")):
        with path.open("r", encoding="utf-8") as handle:
            items.append((path, json.load(handle)))
    return items


def validate_items(items: Sequence[Tuple[Path, Mapping[str, object]]]) -> Tuple[bool, List[str]]:
    schema_path = SCHEMA_ROOT / "item_base.json"
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    if jsonschema is not None:
        base_uri = schema_path.resolve().parent.as_uri() + "/"
        resolver = jsonschema.RefResolver(base_uri=base_uri, referrer=schema)
        validator = jsonschema.Draft7Validator(schema, resolver=resolver)
        messages: List[str] = []
        for path, payload in items:
            errors = sorted(validator.iter_errors(payload), key=lambda err: list(err.path))
            if errors:
                messages.append(f"{path.name}: {errors[0].message}")
        return (not messages, messages)

    # Fallback validation performs a lightweight structural check.
    required_fields = {
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
    messages = []
    known_types = set(list_registered_types())
    for path, payload in items:
        missing = sorted(required_fields - set(payload))
        if missing:
            messages.append(f"{path.name}: missing fields {', '.join(missing)}")
            continue
        item_type = payload.get("item_type")
        if item_type not in known_types:
            messages.append(f"{path.name}: unknown item_type '{item_type}'")
    return (not messages, messages)


def summarise_results(
    results: Sequence[Tuple[Mapping[str, object], EvaluationResult]]
) -> str:
    lines: List[str] = []
    totals: MutableMapping[str, int] = defaultdict(int)
    lines.append("Summary Report")
    lines.append("=" * 60)
    lines.append("")
    for _, result in results:
        type_key = result.type_key
        totals[type_key] += 1
    if not totals:
        lines.append("No items were processed.")
        return "\n".join(lines)
    for type_key in sorted(totals):
        manifest = get_manifest(type_key)
        lines.append(f"Type: {type_key} (schema: {manifest.schema_ref}) -> {totals[type_key]} item(s)")
    lines.append("")
    for item, evaluation in results:
        lines.append(f"Item {item.get('id')} [{item.get('item_type')}]")
        for key, value in evaluation.values.items():
            lines.append(f"  - {key}: {value}")
        lines.append("")
    return "\n".join(lines)


def ensure_registry(schema_root: Path) -> None:
    registry = TypeRegistry()
    loader = SchemaLoader(schema_root=schema_root / "types", registry=registry)
    loader.load()
    bootstrap_types(force=True)


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run the derived evaluator proof-of-concept")
    parser.add_argument(
        "--items-dir",
        type=Path,
        default=DEFAULT_ITEMS_DIR,
        help="Directory containing sample item payloads",
    )
    parser.add_argument(
        "--derived-root",
        type=Path,
        default=SCHEMA_ROOT / "derived",
        help="Directory containing derived metric definitions",
    )
    args = parser.parse_args(list(argv) if argv is not None else None)

    ensure_registry(SCHEMA_ROOT)
    items = load_items(args.items_dir)
    ok, messages = validate_items(items)
    if not ok:
        for message in messages:
            print(f"Validation error: {message}", file=sys.stderr)
        return 1

    evaluator = DerivedEvaluator(schema_root=args.derived_root)
    results = evaluator.evaluate_many([payload for _, payload in items])
    print(summarise_results(results))
    return 0


if __name__ == "__main__":  # pragma: no cover - CLI entrypoint
    raise SystemExit(main())
