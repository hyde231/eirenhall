"""Wiki type metadata."""
from __future__ import annotations

from .base import TypeDefinitionMixin


class WikiType(TypeDefinitionMixin):
    """Metadata accessors for wiki entries."""

    TYPE_KEY = "wiki"


TYPE_KEY = WikiType.type_key()
SCHEMA_REF = WikiType.schema_ref()
CAPABILITIES = WikiType.capabilities()

__all__ = ["WikiType", "TYPE_KEY", "SCHEMA_REF", "CAPABILITIES"]
