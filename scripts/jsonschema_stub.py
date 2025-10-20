"""Fallback JSON Schema validator implementing a subset of Draft 7."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterator, List, Sequence
from urllib.parse import urlparse


@dataclass
class ValidationError(Exception):
    """Minimal validation error carrying a message and instance path."""

    message: str
    path: List[Any]

    def __str__(self) -> str:  # pragma: no cover - debug helper
        return self.message


class RefResolver:
    """Resolve `$ref` documents relative to the current schema file."""

    def __init__(self, base_uri: str, referrer: Dict[str, Any]):
        parsed = urlparse(base_uri)
        base = Path(parsed.path or ".")
        if base.is_file():
            base = base.parent
        self.base_path = base
        self.referrer = referrer

    def resolve(self, ref: str, *, base_path: Path | None = None) -> tuple[str, Dict[str, Any]]:
        if ref.startswith("#"):
            raise ValueError("Fragment-only references are not supported in stub validator")
        if ref.startswith("http://") or ref.startswith("https://"):
            raise ValueError("Network references are not supported in stub validator")
        base = base_path or self.base_path
        ref_path = (base / ref).resolve()
        with ref_path.open("r", encoding="utf-8") as handle:
            schema = json.load(handle)
        schema["__base_path__"] = ref_path.parent
        return ref, schema


class Draft7Validator:
    """Tiny subset of the Draft 7 validator surface required for fixtures."""

    def __init__(self, schema: Dict[str, Any], resolver: RefResolver | None = None):
        self.schema = schema
        self.resolver = resolver

    def iter_errors(self, instance: Any) -> Iterator[ValidationError]:
        yield from self._validate(instance, self.schema, [], self._schema_base(self.schema))

    # Internal helpers -------------------------------------------------
    def _schema_base(self, schema: Dict[str, Any]) -> Path | None:
        base = schema.get("__base_path__")
        if isinstance(base, Path):
            return base
        return None

    def _validate(self, instance: Any, schema: Dict[str, Any], path: List[Any], schema_base: Path | None) -> Iterator[ValidationError]:
        if "$ref" in schema:
            if self.resolver is None:
                raise ValueError("$ref encountered but no resolver was provided")
            base_for_ref = schema_base or self.resolver.base_path
            _, resolved = self.resolver.resolve(schema["$ref"], base_path=base_for_ref)
            yield from self._validate(instance, resolved, path, resolved.get("__base_path__"))
            return

        schema_type = schema.get("type")
        if schema_type is not None and not self._check_type(instance, schema_type):
            yield ValidationError(self._type_message(instance, schema_type), list(path))
            return

        enum = schema.get("enum")
        if enum is not None and instance not in enum:
            yield ValidationError(f"{instance!r} is not one of {enum}", list(path))
            return

        const = schema.get("const")
        if const is not None and instance != const:
            yield ValidationError(f"{instance!r} was expected to be {const!r}", list(path))
            return

        if isinstance(instance, str):
            yield from self._validate_string(instance, schema, path)
        elif isinstance(instance, list):
            yield from self._validate_array(instance, schema, path, schema_base)
        elif isinstance(instance, dict):
            yield from self._validate_object(instance, schema, path, schema_base)

        one_of = schema.get("oneOf")
        if one_of is not None:
            matches = 0
            for option in one_of:
                option_base = schema_base
                if isinstance(option, dict):
                    option_base = self._schema_base(option) or schema_base
                if not list(self._validate(instance, option, path, option_base)):
                    matches += 1
            if matches != 1:
                yield ValidationError("oneOf constraints not satisfied", list(path))

    @staticmethod
    def _check_type(instance: Any, schema_type: Any) -> bool:
        if isinstance(schema_type, list):
            return any(Draft7Validator._check_type(instance, t) for t in schema_type)
        if schema_type == "string":
            return isinstance(instance, str)
        if schema_type == "number":
            return isinstance(instance, (int, float)) and not isinstance(instance, bool)
        if schema_type == "integer":
            return isinstance(instance, int) and not isinstance(instance, bool)
        if schema_type == "boolean":
            return isinstance(instance, bool)
        if schema_type == "object":
            return isinstance(instance, dict)
        if schema_type == "array":
            return isinstance(instance, list)
        if schema_type == "null":
            return instance is None
        return True

    @staticmethod
    def _type_message(instance: Any, schema_type: Any) -> str:
        if isinstance(schema_type, list):
            return f"Expected instance to be one of {schema_type}, got {type(instance).__name__}"
        return f"Expected type {schema_type}, got {type(instance).__name__}"

    def _validate_string(self, instance: str, schema: Dict[str, Any], path: List[Any]) -> Iterator[ValidationError]:
        min_length = schema.get("minLength")
        if min_length is not None and len(instance) < min_length:
            yield ValidationError(f"String is shorter than minimum length {min_length}", list(path))
        max_length = schema.get("maxLength")
        if max_length is not None and len(instance) > max_length:
            yield ValidationError(f"String is longer than maximum length {max_length}", list(path))
        pattern = schema.get("pattern")
        if pattern is not None and re.fullmatch(pattern, instance) is None:
            yield ValidationError(f"String does not match pattern {pattern}", list(path))

    def _validate_array(self, instance: Sequence[Any], schema: Dict[str, Any], path: List[Any], schema_base: Path | None) -> Iterator[ValidationError]:
        min_items = schema.get("minItems")
        if min_items is not None and len(instance) < min_items:
            yield ValidationError(f"Array has fewer than {min_items} items", list(path))
        max_items = schema.get("maxItems")
        if max_items is not None and len(instance) > max_items:
            yield ValidationError(f"Array has more than {max_items} items", list(path))
        if schema.get("uniqueItems"):
            markers = set()
            for idx, item in enumerate(instance):
                marker = json.dumps(item, sort_keys=True)
                if marker in markers:
                    yield ValidationError("Array items are not unique", list(path) + [idx])
                    break
                markers.add(marker)
        items = schema.get("items")
        if isinstance(items, dict):
            item_base = self._schema_base(items) or schema_base
            for idx, item in enumerate(instance):
                yield from self._validate(item, items, list(path) + [idx], item_base)

    def _validate_object(self, instance: Dict[str, Any], schema: Dict[str, Any], path: List[Any], schema_base: Path | None) -> Iterator[ValidationError]:
        required = schema.get("required", [])
        for key in required:
            if key not in instance:
                yield ValidationError(f"'{key}' is a required property", list(path))
        properties = schema.get("properties", {})
        for key, subschema in properties.items():
            if key in instance:
                sub_base = self._schema_base(subschema) or schema_base
                yield from self._validate(instance[key], subschema, list(path) + [key], sub_base)
        property_names = schema.get("propertyNames")
        if property_names:
            pattern = property_names.get("pattern")
            if pattern:
                for key in instance.keys():
                    if re.fullmatch(pattern, key) is None:
                        yield ValidationError(f"Property name '{key}' does not match pattern {pattern}", list(path) + [key])
        allowed = set(properties.keys())
        additional = schema.get("additionalProperties", True)
        for key, value in instance.items():
            if key in allowed:
                continue
            if isinstance(additional, bool):
                if not additional:
                    yield ValidationError(f"Additional properties are not allowed ('{key}')", list(path) + [key])
                continue
            if isinstance(additional, dict):
                if "oneOf" in additional:
                    matched = False
                    for option in additional["oneOf"]:
                        option_base = self._schema_base(option) or schema_base
                        if not list(self._validate(value, option, list(path) + [key], option_base)):
                            matched = True
                            break
                    if not matched:
                        yield ValidationError("Value does not match any allowed schema", list(path) + [key])
                else:
                    option_base = self._schema_base(additional) or schema_base
                    yield from self._validate(value, additional, list(path) + [key], option_base)


__all__ = ["Draft7Validator", "RefResolver", "ValidationError"]
