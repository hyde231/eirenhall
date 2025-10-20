"""Financial domain type metadata."""
from __future__ import annotations

from .base import TypeDefinitionMixin


class FinancialTransactionType(TypeDefinitionMixin):
    """Metadata accessors for financial transaction items."""

    TYPE_KEY = "financial_transaction"


class AccountStatementType(TypeDefinitionMixin):
    """Metadata accessors for account statement items."""

    TYPE_KEY = "account_statement"


class FinancialAccountType(TypeDefinitionMixin):
    """Metadata accessors for financial account items."""

    TYPE_KEY = "financial_account"


FINANCIAL_TRANSACTION_TYPE_KEY = FinancialTransactionType.type_key()
ACCOUNT_STATEMENT_TYPE_KEY = AccountStatementType.type_key()
FINANCIAL_ACCOUNT_TYPE_KEY = FinancialAccountType.type_key()

FINANCIAL_TRANSACTION_SCHEMA_REF = FinancialTransactionType.schema_ref()
ACCOUNT_STATEMENT_SCHEMA_REF = AccountStatementType.schema_ref()
FINANCIAL_ACCOUNT_SCHEMA_REF = FinancialAccountType.schema_ref()

FINANCIAL_TRANSACTION_CAPABILITIES = FinancialTransactionType.capabilities()
ACCOUNT_STATEMENT_CAPABILITIES = AccountStatementType.capabilities()
FINANCIAL_ACCOUNT_CAPABILITIES = FinancialAccountType.capabilities()

__all__ = [
    "FinancialTransactionType",
    "AccountStatementType",
    "FinancialAccountType",
    "FINANCIAL_TRANSACTION_TYPE_KEY",
    "ACCOUNT_STATEMENT_TYPE_KEY",
    "FINANCIAL_ACCOUNT_TYPE_KEY",
    "FINANCIAL_TRANSACTION_SCHEMA_REF",
    "ACCOUNT_STATEMENT_SCHEMA_REF",
    "FINANCIAL_ACCOUNT_SCHEMA_REF",
    "FINANCIAL_TRANSACTION_CAPABILITIES",
    "ACCOUNT_STATEMENT_CAPABILITIES",
    "FINANCIAL_ACCOUNT_CAPABILITIES",
]
