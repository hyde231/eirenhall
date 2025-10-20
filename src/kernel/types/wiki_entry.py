"""Wiki entry type metadata."""
from __future__ import annotations

from .base import TypeDefinitionMixin


class WikiEntryType(TypeDefinitionMixin):
    """Metadata accessors for wiki entry items."""

    TYPE_KEY = "wiki_entry"


# Backwards compatibility alias (deprecated).
WikiType = WikiEntryType


TYPE_KEY = WikiEntryType.type_key()
SCHEMA_REF = WikiEntryType.schema_ref()
CAPABILITIES = WikiEntryType.capabilities()

__all__ = [
    "WikiEntryType",
    "WikiType",
    "TYPE_KEY",
    "SCHEMA_REF",
    "CAPABILITIES",
]
