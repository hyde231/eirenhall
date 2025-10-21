"""Project type metadata."""
from __future__ import annotations

from .base import TypeDefinitionMixin


class ProjectType(TypeDefinitionMixin):
    """Metadata accessors for project items."""

    TYPE_KEY = "project"


TYPE_KEY = ProjectType.type_key()
SCHEMA_REF = ProjectType.schema_ref()
CAPABILITIES = ProjectType.capabilities()

__all__ = ["ProjectType", "TYPE_KEY", "SCHEMA_REF", "CAPABILITIES"]

