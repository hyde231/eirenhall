"""Task type metadata."""
from __future__ import annotations

from .base import TypeDefinitionMixin


class TaskType(TypeDefinitionMixin):
    """Metadata accessors for task items."""

    TYPE_KEY = "task"


TYPE_KEY = TaskType.type_key()
SCHEMA_REF = TaskType.schema_ref()
CAPABILITIES = TaskType.capabilities()

__all__ = ["TaskType", "TYPE_KEY", "SCHEMA_REF", "CAPABILITIES"]
