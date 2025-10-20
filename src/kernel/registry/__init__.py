"""Registry utilities for kernel schema definitions."""
from __future__ import annotations

from collections import OrderedDict
from typing import Iterable, Iterator, Tuple, TypeVar

T = TypeVar("T")


class TypeRegistry:
    """In-memory registry for schema objects."""

    def __init__(self) -> None:
        self._entries: "OrderedDict[str, T]" = OrderedDict()

    def __contains__(self, name: str) -> bool:
        return name in self._entries

    def register(self, name: str, value: T, *, overwrite: bool = False) -> None:
        """Register a value under ``name``."""

        if not overwrite and name in self._entries:
            raise ValueError(f"'{name}' is already registered")
        self._entries[name] = value

    def get(self, name: str) -> T:
        """Return the registered value for ``name``."""

        try:
            return self._entries[name]
        except KeyError as exc:  # pragma: no cover - defensive branch
            raise KeyError(f"'{name}' is not registered") from exc

    def deregister(self, name: str) -> T:
        """Remove ``name`` from the registry and return its value."""

        try:
            return self._entries.pop(name)
        except KeyError as exc:
            raise KeyError(f"'{name}' is not registered") from exc

    def list(self) -> Iterable[Tuple[str, T]]:
        """Iterate over registered entries in insertion order."""

        return tuple(self._entries.items())

    def clear(self) -> None:
        """Remove all registered entries."""

        self._entries.clear()

    def __iter__(self) -> Iterator[Tuple[str, T]]:
        return iter(self._entries.items())


from .loader import SchemaLoadReport, SchemaLoader

__all__ = ["TypeRegistry", "SchemaLoader", "SchemaLoadReport"]
