"""Organization contact type metadata."""
from __future__ import annotations

from .base import TypeDefinitionMixin


class OrganizationType(TypeDefinitionMixin):
    """Metadata accessors for organization directory entries."""

    TYPE_KEY = "organization"


TYPE_KEY = OrganizationType.type_key()
SCHEMA_REF = OrganizationType.schema_ref()
CAPABILITIES = OrganizationType.capabilities()

__all__ = ["OrganizationType", "TYPE_KEY", "SCHEMA_REF", "CAPABILITIES"]

