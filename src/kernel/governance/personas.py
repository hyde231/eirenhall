"""Persona manifest loader and validation helpers."""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Iterator, List, Mapping, MutableMapping, Tuple

try:  # Optional dependency. JSON-compatible manifests keep this non-blocking.
    import yaml  # type: ignore
except Exception:  # pragma: no cover - optional dependency
    yaml = None  # type: ignore


@dataclass(frozen=True)
class WritePermission:
    """Declarative write permission for a persona."""

    action: str
    requires_approval: bool
    dry_run_only: bool


@dataclass(frozen=True)
class EscalationRule:
    """Condition that requires human intervention."""

    condition: str
    requires_human: bool


@dataclass(frozen=True)
class PersonaManifest:
    """Structured representation of a persona manifest."""

    id: str
    name: str
    summary: str
    intended_outcomes: Tuple[str, ...]
    inputs: Tuple[str, ...]
    outputs: Tuple[str, ...]
    data_access: Mapping[str, Tuple[str, ...]]
    write_permissions: Tuple[WritePermission, ...]
    escalation: Tuple[EscalationRule, ...]
    safety_rails: Tuple[str, ...]
    dry_run_default: bool

    @classmethod
    def from_mapping(cls, payload: Mapping[str, object], *, source: Path) -> "PersonaManifest":
        """Validate raw manifest payload and convert into a dataclass."""

        def _require_str(key: str) -> str:
            value = payload.get(key)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{source}: '{key}' must be a non-empty string")
            return value.strip()

        def _require_str_list(key: str) -> Tuple[str, ...]:
            value = payload.get(key, [])
            if not isinstance(value, list) or any(not isinstance(item, str) or not item for item in value):
                raise ValueError(f"{source}: '{key}' must be a list of non-empty strings")
            return tuple(item.strip() for item in value)

        def _require_bool(key: str, default: bool | None = None) -> bool:
            if key not in payload:
                if default is None:
                    raise ValueError(f"{source}: '{key}' must be provided")
                return default
            value = payload.get(key)
            if not isinstance(value, bool):
                raise ValueError(f"{source}: '{key}' must be a boolean")
            return value

        manifest_id = _require_str("id")
        name = _require_str("name")
        summary = _require_str("summary")
        intended_outcomes = _require_str_list("intended_outcomes")
        inputs = _require_str_list("inputs")
        outputs = _require_str_list("outputs")

        data_access_raw = payload.get("data_access")
        if not isinstance(data_access_raw, Mapping):
            raise ValueError(f"{source}: 'data_access' must be a mapping")
        data_access: MutableMapping[str, Tuple[str, ...]] = {}
        for key in ("realms", "sensitivity_bands", "item_types", "capability_scopes"):
            entries_raw = data_access_raw.get(key, [])
            if not isinstance(entries_raw, list) or any(not isinstance(entry, str) or not entry for entry in entries_raw):
                raise ValueError(f"{source}: 'data_access.{key}' must be a list of non-empty strings")
            data_access[key] = tuple(entry.strip() for entry in entries_raw)

        write_permissions_raw = payload.get("write_permissions", [])
        if not isinstance(write_permissions_raw, list):
            raise ValueError(f"{source}: 'write_permissions' must be a list")
        write_permissions: List[WritePermission] = []
        for entry in write_permissions_raw:
            if not isinstance(entry, Mapping):
                raise ValueError(f"{source}: write permission entries must be mappings")
            action = entry.get("action")
            requires_approval = entry.get("requires_approval")
            dry_run_only = entry.get("dry_run_only", False)
            if not isinstance(action, str) or not action:
                raise ValueError(f"{source}: write permission 'action' must be a non-empty string")
            if not isinstance(requires_approval, bool):
                raise ValueError(f"{source}: write permission '{action}' must declare 'requires_approval'")
            if not isinstance(dry_run_only, bool):
                raise ValueError(f"{source}: write permission '{action}' must declare 'dry_run_only' as boolean")
            write_permissions.append(
                WritePermission(
                    action=action.strip(),
                    requires_approval=requires_approval,
                    dry_run_only=dry_run_only,
                )
            )

        escalation_raw = payload.get("escalation", [])
        if not isinstance(escalation_raw, list):
            raise ValueError(f"{source}: 'escalation' must be a list")
        escalation: List[EscalationRule] = []
        for entry in escalation_raw:
            if not isinstance(entry, Mapping):
                raise ValueError(f"{source}: escalation entries must be mappings")
            condition = entry.get("condition")
            requires_human = entry.get("requires_human")
            if not isinstance(condition, str) or not condition:
                raise ValueError(f"{source}: escalation 'condition' must be a non-empty string")
            if not isinstance(requires_human, bool):
                raise ValueError(f"{source}: escalation '{condition}' must declare 'requires_human'")
            escalation.append(EscalationRule(condition=condition.strip(), requires_human=requires_human))

        safety_rails = _require_str_list("safety_rails")
        dry_run_default = _require_bool("dry_run_default", default=True)

        return cls(
            id=manifest_id,
            name=name,
            summary=summary,
            intended_outcomes=intended_outcomes,
            inputs=inputs,
            outputs=outputs,
            data_access=data_access,
            write_permissions=tuple(write_permissions),
            escalation=tuple(escalation),
            safety_rails=safety_rails,
            dry_run_default=dry_run_default,
        )


def _load_raw_manifest(path: Path) -> Mapping[str, object]:
    text = path.read_text(encoding="utf-8")
    if yaml is not None:
        data = yaml.safe_load(text)
    else:
        data = json.loads(text)
    if not isinstance(data, Mapping):
        raise ValueError(f"{path}: manifest must parse to a mapping")
    return data


def load_persona(path: Path) -> PersonaManifest:
    """Load a single persona manifest."""

    payload = _load_raw_manifest(path)
    return PersonaManifest.from_mapping(payload, source=path)


def iter_personas(root: Path | str) -> Iterator[PersonaManifest]:
    """Yield persona manifests sorted by filename."""

    root_path = Path(root)
    if not root_path.exists():
        raise FileNotFoundError(f"Persona root '{root}' does not exist")
    for path in sorted(root_path.glob("*.yaml")):
        yield load_persona(path)


def list_personas(root: Path | str) -> Tuple[PersonaManifest, ...]:
    """Return persona manifests as a tuple for convenience."""

    return tuple(iter_personas(root))


def load_personas(root: Path | str | None = None) -> Tuple[PersonaManifest, ...]:
    """Load manifests from the provided root or default 'personas/' directory."""

    if root is None:
        root = Path.cwd() / "personas"
    return list_personas(root)
