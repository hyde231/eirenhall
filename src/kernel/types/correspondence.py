"""Correspondence type metadata."""
from __future__ import annotations

from .base import TypeDefinitionMixin


class CorrespondenceType(TypeDefinitionMixin):
    """Metadata accessors for correspondence items."""

    TYPE_KEY = "correspondence"


TYPE_KEY = CorrespondenceType.type_key()
SCHEMA_REF = CorrespondenceType.schema_ref()
CAPABILITIES = CorrespondenceType.capabilities()

__all__ = ["CorrespondenceType", "TYPE_KEY", "SCHEMA_REF", "CAPABILITIES"]

