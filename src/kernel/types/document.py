"""Document type metadata."""
from __future__ import annotations

from .base import TypeDefinitionMixin


class DocumentType(TypeDefinitionMixin):
    """Metadata accessors for document items."""

    TYPE_KEY = "document"


TYPE_KEY = DocumentType.type_key()
SCHEMA_REF = DocumentType.schema_ref()
CAPABILITIES = DocumentType.capabilities()

__all__ = ["DocumentType", "TYPE_KEY", "SCHEMA_REF", "CAPABILITIES"]
