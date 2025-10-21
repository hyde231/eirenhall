"""Webcomic type metadata."""
from __future__ import annotations

from .base import TypeDefinitionMixin


class WebcomicType(TypeDefinitionMixin):
    """Metadata accessors for webcomic items."""

    TYPE_KEY = "webcomic"


TYPE_KEY = WebcomicType.type_key()
SCHEMA_REF = WebcomicType.schema_ref()
CAPABILITIES = WebcomicType.capabilities()

__all__ = ["WebcomicType", "TYPE_KEY", "SCHEMA_REF", "CAPABILITIES"]
