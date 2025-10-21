"""Evaluate derived metrics for kernel items."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Sequence, Tuple

try:  # Optional dependency used when available.
    import yaml  # type: ignore
except Exception:  # pragma: no cover - optional dependency fallback
    yaml = None  # type: ignore

from kernel.observability import emit_event, trace_span
from kernel.types import get_manifest

__all__ = [
    "DerivedEvaluator",
    "DerivedMetricDefinition",
    "DerivedTypeDefinition",
    "EvaluationResult",
]


@dataclass(frozen=True)
class DerivedMetricDefinition:
    """Definition for a single derived metric."""

    key: str
    description: str
    operation: str
    config: Mapping[str, Any]
    depends_on: Tuple[str, ...]

    @classmethod
    def from_mapping(cls, payload: Mapping[str, Any], *, source: str) -> "DerivedMetricDefinition":
        key = _require_str(payload, "key", source)
        description = _require_str(payload, "description", source)
        operation = _require_str(payload, "operation", source)
        config_raw = payload.get("config", {})
        if not isinstance(config_raw, Mapping):
            raise ValueError(f"Metric '{key}' in {source} must define a mapping under 'config'")
        depends_raw = payload.get("depends_on", [])
        depends: List[str] = []
        if depends_raw:
            if not isinstance(depends_raw, Sequence) or isinstance(depends_raw, (str, bytes)):
                raise ValueError(f"'depends_on' for metric '{key}' in {source} must be a sequence")
            for dep in depends_raw:
                if not isinstance(dep, str) or not dep:
                    raise ValueError(
                        f"Dependencies for metric '{key}' in {source} must be non-empty strings"
                    )
                depends.append(dep)
        return cls(
            key=key,
            description=description,
            operation=operation,
            config=dict(config_raw),
            depends_on=tuple(depends),
        )


@dataclass(frozen=True)
class DerivedTypeDefinition:
    """Collection of derived metrics for an item type."""

    type_key: str
    metrics: Tuple[DerivedMetricDefinition, ...]

    @classmethod
    def from_mapping(cls, payload: Mapping[str, Any], *, source: str) -> "DerivedTypeDefinition":
        type_key = _require_str(payload, "type", source)
        metrics_raw = payload.get("metrics")
        if not isinstance(metrics_raw, Sequence) or isinstance(metrics_raw, (str, bytes)):
            raise ValueError(f"'{source}' must contain a list of metric definitions under 'metrics'")
        metrics: List[DerivedMetricDefinition] = []
        seen: Dict[str, None] = {}
        for index, entry in enumerate(metrics_raw):
            if not isinstance(entry, Mapping):
                raise ValueError(f"Metric entry #{index + 1} in {source} must be a mapping")
            metric = DerivedMetricDefinition.from_mapping(entry, source=source)
            if metric.key in seen:
                raise ValueError(f"Duplicate metric key '{metric.key}' in {source}")
            seen[metric.key] = None
            metrics.append(metric)
        return cls(type_key=type_key, metrics=tuple(metrics))


@dataclass(frozen=True)
class EvaluationResult:
    """Result of a derived metric evaluation run."""

    type_key: str
    values: Mapping[str, Any]
    provenance: Mapping[str, Tuple[str, ...]]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.type_key,
            "values": dict(self.values),
            "provenance": {key: list(value) for key, value in self.provenance.items()},
        }


class DerivedEvaluator:
    """Evaluate derived metrics declared under ``schema/derived``."""

    def __init__(self, schema_root: str | Path | None = None) -> None:
        self.schema_root = Path(schema_root or _default_schema_root())
        self._definitions: Dict[str, DerivedTypeDefinition] = {}
        self.load_definitions()

    # ------------------------------------------------------------------
    # public API
    # ------------------------------------------------------------------
    def load_definitions(self) -> None:
        """Load derived definitions from disk."""

        self._definitions.clear()
        if not self.schema_root.exists():
            return
        for path in sorted(self.schema_root.glob("*.yaml")):
            document = _load_yaml(path)
            if not isinstance(document, Mapping):
                raise ValueError(f"Derived definition '{path}' must contain a mapping")
            definition = DerivedTypeDefinition.from_mapping(document, source=str(path))
            # Ensure referenced type exists and is bootstrapped
            get_manifest(definition.type_key)
            if definition.type_key in self._definitions:
                raise ValueError(f"Duplicate derived definition for type '{definition.type_key}'")
            self._definitions[definition.type_key] = definition

    def list_types(self) -> Tuple[str, ...]:
        return tuple(sorted(self._definitions))

    def definition_for(self, type_key: str) -> DerivedTypeDefinition:
        try:
            return self._definitions[type_key]
        except KeyError as exc:  # pragma: no cover - defensive
            raise KeyError(f"No derived definition registered for '{type_key}'") from exc

    def evaluate_item(self, item: Mapping[str, Any]) -> EvaluationResult:
        type_key = _require_item_type(item)
        definition = self.definition_for(type_key)
        computed: Dict[str, Any] = {}
        provenance: Dict[str, Tuple[str, ...]] = {}
        item_id = item.get("id") if isinstance(item, Mapping) else None
        with trace_span("derived.evaluate_item", type_key=type_key, item_id=item_id) as span_id:
            for metric in definition.metrics:
                value, sources = self._compute_metric(metric, item, computed)
                computed[metric.key] = value
                provenance[metric.key] = tuple(sources)
                emit_event(
                    "derived.metric",
                    span_id=span_id,
                    type_key=type_key,
                    item_id=item_id,
                    metric=metric.key,
                    value=value,
                    sources=list(sources),
                )
        emit_event(
            "derived.evaluation_complete",
            type_key=type_key,
            item_id=item_id,
            metrics=sorted(computed),
        )
        return EvaluationResult(type_key=type_key, values=computed, provenance=provenance)

    def evaluate_many(
        self, items: Iterable[Mapping[str, Any]]
    ) -> List[Tuple[Mapping[str, Any], EvaluationResult]]:
        """Evaluate multiple items returning value pairs."""

        results: List[Tuple[Mapping[str, Any], EvaluationResult]] = []
        for item in items:
            results.append((item, self.evaluate_item(item)))
        return results

    # ------------------------------------------------------------------
    # helpers
    # ------------------------------------------------------------------
    def _compute_metric(
        self,
        metric: DerivedMetricDefinition,
        item: Mapping[str, Any],
        computed: Mapping[str, Any],
    ) -> Tuple[Any, Tuple[str, ...]]:
        for dependency in metric.depends_on:
            if dependency not in computed:
                raise ValueError(
                    f"Metric '{metric.key}' depends on '{dependency}' but it has not been computed"
                )
        operation = metric.operation.lower()
        handler = getattr(self, f"_op_{operation}", None)
        if handler is None:
            raise ValueError(f"Unsupported operation '{metric.operation}' in metric '{metric.key}'")
        value, provenance = handler(metric, item, computed)
        return value, tuple(provenance)

    def _op_length(
        self,
        metric: DerivedMetricDefinition,
        item: Mapping[str, Any],
        computed: Mapping[str, Any],
    ) -> Tuple[int, Tuple[str, ...]]:
        path = _require_path(metric)
        value = _resolve_path(item, path, default=[])
        if isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
            result = len(value)
        elif isinstance(value, Mapping):
            result = len(value)
        else:
            result = 0
        return result, (f"path:{path}",)

    def _op_count_where(
        self,
        metric: DerivedMetricDefinition,
        item: Mapping[str, Any],
        computed: Mapping[str, Any],
    ) -> Tuple[int, Tuple[str, ...]]:
        path = _require_path(metric)
        field = _require_config_key(metric, "field")
        needle = metric.config.get("equals", True)
        values = _resolve_path(item, path, default=[])
        count = 0
        if isinstance(values, Sequence) and not isinstance(values, (str, bytes)):
            for entry in values:
                if not isinstance(entry, Mapping):
                    continue
                current: Any = entry
                for part in field.split("."):
                    if isinstance(current, Mapping) and part in current:
                        current = current[part]
                    else:
                        current = object()
                        break
                if current == needle:
                    count += 1
        return count, (f"path:{path}",)

    def _op_ratio(
        self,
        metric: DerivedMetricDefinition,
        item: Mapping[str, Any],
        computed: Mapping[str, Any],
    ) -> Tuple[float, Tuple[str, ...]]:
        numerator_key = _require_config_key(metric, "numerator")
        denominator_key = _require_config_key(metric, "denominator")
        numerator = computed.get(numerator_key, 0)
        denominator = computed.get(denominator_key, 0)
        default = metric.config.get("default", 0.0)
        precision = metric.config.get("precision")
        if not denominator:
            value = default
        else:
            value = numerator / denominator
            if isinstance(precision, int):
                value = round(value, precision)
        return value, (f"metric:{numerator_key}", f"metric:{denominator_key}")

    def _op_word_count(
        self,
        metric: DerivedMetricDefinition,
        item: Mapping[str, Any],
        computed: Mapping[str, Any],
    ) -> Tuple[int, Tuple[str, ...]]:
        path = _require_path(metric)
        value = _resolve_path(item, path)
        text = _extract_text(value)
        count = _count_words(text)
        return count, (f"path:{path}",)

    def _op_rate(
        self,
        metric: DerivedMetricDefinition,
        item: Mapping[str, Any],
        computed: Mapping[str, Any],
    ) -> Tuple[float, Tuple[str, ...]]:
        metric_key = _require_config_key(metric, "metric")
        rate = metric.config.get("per", 1)
        if not isinstance(rate, (int, float)) or rate == 0:
            raise ValueError(f"Metric '{metric.key}' in operation 'rate' must specify a non-zero 'per'")
        base = computed.get(metric_key, 0)
        value = base / rate
        precision = metric.config.get("precision")
        if isinstance(precision, int):
            value = round(value, precision)
        return value, (f"metric:{metric_key}",)

    def _op_exists(
        self,
        metric: DerivedMetricDefinition,
        item: Mapping[str, Any],
        computed: Mapping[str, Any],
    ) -> Tuple[bool, Tuple[str, ...]]:
        path = _require_path(metric)
        value = _resolve_path(item, path)
        exists = bool(value)
        return exists, (f"path:{path}",)


# ----------------------------------------------------------------------
# utility helpers
# ----------------------------------------------------------------------

def _require_str(payload: Mapping[str, Any], key: str, source: str) -> str:
    value = payload.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"'{key}' must be a non-empty string in {source}")
    return value.strip()


def _require_item_type(item: Mapping[str, Any]) -> str:
    type_key = item.get("item_type")
    if not isinstance(type_key, str) or not type_key:
        raise ValueError("Item is missing a valid 'item_type' field")
    return type_key


def _default_schema_root() -> Path:
    return Path(__file__).resolve().parents[3] / "schema" / "derived"


def _load_yaml(path: Path) -> Any:
    content = path.read_text(encoding="utf-8")
    if not content.strip():
        return {}
    if yaml is not None:
        loaded = yaml.safe_load(content)
    else:  # Fallback to JSON subset
        import json

        loaded = json.loads(content)
    return loaded


def _resolve_path(data: Any, path: str, default: Any = None) -> Any:
    parts = path.split(".") if path else []
    current: Any = data
    index = 0
    while index < len(parts):
        if not isinstance(current, Mapping):
            return default
        part = parts[index]
        if part in current:
            current = current[part]
            index += 1
            continue
        matched = False
        for end in range(len(parts), index, -1):
            candidate = ".".join(parts[index:end])
            if candidate in current:
                current = current[candidate]
                index = end
                matched = True
                break
        if not matched:
            return default
    return current


def _extract_text(value: Any) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, Mapping):
        ops = value.get("ops")
        if isinstance(ops, Sequence):
            fragments: List[str] = []
            for entry in ops:
                if isinstance(entry, Mapping):
                    chunk = entry.get("insert")
                    if isinstance(chunk, str):
                        fragments.append(chunk)
            return "".join(fragments)
    return ""


def _count_words(text: str) -> int:
    if not text:
        return 0
    words = [token for token in text.replace("\n", " ").split(" ") if token.strip()]
    return len(words)


def _require_path(metric: DerivedMetricDefinition) -> str:
    path = metric.config.get("path")
    if not isinstance(path, str) or not path:
        raise ValueError(f"Metric '{metric.key}' must provide a 'path' in configuration")
    return path


def _require_config_key(metric: DerivedMetricDefinition, key: str) -> str:
    value = metric.config.get(key)
    if not isinstance(value, str) or not value:
        raise ValueError(f"Metric '{metric.key}' must provide '{key}' in configuration")
    return value
