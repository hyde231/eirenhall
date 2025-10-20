# Financial Data Types Integration

## Overview
This document captures the financial-oriented field additions that extend the
standard field library. They are derived from an earlier home project and have
been translated into English while aligning with the kernel schema
conventions.

## Translated Domain Concepts
- **Transaction** -> `bank_transaction.json`
  - `datum` -> `booking_date`
  - `valuta` -> `value_date`
  - `vorgang` -> `entry_type`
  - `beteiligter` -> `counterparty_name`
  - `konto` -> `counterparty_account`
  - `bank` -> `counterparty_bank`
  - `text` -> `description`
  - `währung` + `betrag` -> `amount` (`money_amount`)
  - `saldo` -> `balance_after_transaction`
  - `tags`, `manual`, `source`, `comment` carried forward with richer typing.
- **TransactionList** -> `bank_transaction_list.json`
- **AccountStatement** -> `account_statement.json`
- **Account** -> `bank_account.json`

## Primitive Field Definitions (`schema/fields/`)
- `calendar_date.json` – ISO 8601 calendar date string.
- `currency_code.json` – ISO 4217 currency code.
- `iban.json` – Normalized IBAN string.
- `financial_institution_identifier.json` – BIC / national clearing identifier.
- `country_code.json` – ISO 3166-1 alpha-2 codes.
- `isbn.json` – Sanitized ISBN-10/13 code.

## Composite Field Definitions (`schema/fields/`)
- `money_amount.json` – Currency amount + code (+ optional metadata).
- `price.json` – Price wrapper with tax hints.
- `product_barcode.json` – Product barcode descriptor.
- `time_frequency.json` – Scheduling frequency descriptor.
- `color_reference.json` – CSS color names or hex triplets.
- `postal_address.json` – Structured postal addresses.
- `social_media_contact.json` – Social handle + metadata.
- `content_rating.json` – Media content classification.

## Financial Data Types (`schema/data_types/`)
- `bank_transaction.json`
- `bank_transaction_list.json`
- `account_statement.json`
- `bank_account.json`

## New Item Types (`schema/types/`)
- `financial_transaction`
- `account_statement`
- `financial_account`

Each uses the core `item_base.json` schema and exposes the manifest via
`kernel.types.finance`.

## Open Considerations
1. **Decimal precision** – `money_amount.value` is currently a JSON number.
   Depending on integration precision requirements we may switch to a string
   that conforms to `std.decimal` once the decimal primitive lands.
2. **Validation depth** – IBAN/BIC validation stops at shape checks. If we
   need checksum validation, add evaluator-backed derived checks.
3. **Barcode formats** – current enum covers common retail symbologies. Add
   niche industrial formats when required.
4. **Frequency conditionals** – JSON Schema conditionals (e.g., `if/then`)
   could enforce `days_of_week` when `pattern == "weekly"`. Presently we rely
   on higher-layer validation for simplicity.
5. **Content rating systems** – expand the enum when we map additional
   standards or regional boards.
