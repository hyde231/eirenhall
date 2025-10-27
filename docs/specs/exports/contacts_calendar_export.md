# Contacts and Calendar Export Specification (vCard/ICS)

## Goals
- Provide standards-compliant exports for contacts and events to interoperate with common tools.
- Preserve core fields and provenance to support practical round-trips.

## Contact Export (vCard 4.0)
- Format: vCard 4.0 (RFC 6350), UTF-8.
- File extension: .vcf (single or multiple vCards per file).
- Mapping (person/organization items → vCard):
  - UID ← item `id`
  - FN ← display name (person: full name; org: organization name)
  - N ← structured name (family; given; additional; prefix; suffix) when available
  - ORG ← organization name (for organizations; for persons when `fields.profile.organization` exists)
  - TITLE ← job title (optional)
  - EMAIL ← `fields.contact_methods[].email`
  - TEL ← `fields.contact_methods[].phone`
  - ADR ← `fields.postal_address` components
  - URL ← `fields.links[].url`
  - PHOTO ← `image_reference` (as embedded data URI or referenced URL)
  - NOTE ← `fields.notes` (plain text fallback)
  - CATEGORIES ← tags
  - REV ← `updated_at`

Acceptance criteria:
- Exported .vcf validates with vCard linters; imports into Thunderbird/Apple Contacts without warnings for the mapped fields.
- Multi-entry export from a saved search produces a .vcf containing multiple vCards.
- Round-trip test: re-import preserves FN, EMAIL, TEL, ORG, ADR, URL, NOTE.

## Event Export (iCalendar)
- Format: iCalendar 2.0 (RFC 5545), UTF-8.
- File extension: .ics.
- Mapping (Schedulable items → VEVENT):
  - UID ← item `id`
  - DTSTART ← start datetime (with timezone; use `TZID` or UTC `Z`)
  - DTEND or DURATION ← end datetime or duration
  - SUMMARY ← title
  - DESCRIPTION ← `fields.notes` (plain text)
  - LOCATION ← location field when present
  - URL ← canonical URL
  - CATEGORIES ← tags
  - ORGANIZER ← owner (mailto when available)
  - ATTENDEE ← participants (mailto when available)
  - LAST-MODIFIED ← `updated_at`

Timezone handling:
- Prefer floating times with explicit `TZID` blocks for local calendars; fallback to UTC `Z` when timezone is unknown.
- Include a VTIMEZONE component when using `TZID` that is not a well-known system zone.

Acceptance criteria:
- Exported .ics validates with icalendar validators; imports into Apple Calendar/Outlook/Thunderbird without warnings for mapped fields.
- Batch export from a saved search produces a calendar with multiple VEVENTs.
- Round-trip test: DTSTART/DTEND, SUMMARY, DESCRIPTION, LOCATION, and URL remain consistent.

## UI and CLI
- Per-item detail view: “Export vCard” (for contacts) and “Export ICS” (for schedulable items).
- Batch: from saved searches/collections.
- CLI examples:
  - `eirenhall export contacts --query "type=person AND tag=family" --out family.vcf`
  - `eirenhall export calendar --query "type=event AND date>=2025-01-01" --out events.ics`

## Provenance
- Include generator and timestamp in exported files where supported (e.g., PRODID for ICS; NOTE or X-PRODID for vCard).

