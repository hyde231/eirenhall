"""Person contact type metadata."""
from __future__ import annotations

from .base import TypeDefinitionMixin


class PersonType(TypeDefinitionMixin):
    """Metadata accessors for person directory entries."""

    TYPE_KEY = "person"


TYPE_KEY = PersonType.type_key()
SCHEMA_REF = PersonType.schema_ref()
CAPABILITIES = PersonType.capabilities()

__all__ = ["PersonType", "TYPE_KEY", "SCHEMA_REF", "CAPABILITIES"]

