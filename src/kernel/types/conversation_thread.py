"""Conversation thread type metadata."""
from __future__ import annotations

from .base import TypeDefinitionMixin


class ConversationThreadType(TypeDefinitionMixin):
    """Metadata accessors for conversation thread items."""

    TYPE_KEY = "conversation_thread"


TYPE_KEY = ConversationThreadType.type_key()
SCHEMA_REF = ConversationThreadType.schema_ref()
CAPABILITIES = ConversationThreadType.capabilities()

__all__ = ["ConversationThreadType", "TYPE_KEY", "SCHEMA_REF", "CAPABILITIES"]

