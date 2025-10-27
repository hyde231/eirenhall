# Correspondence Management Specification

Defines how the platform ingests, normalizes, stores, and surfaces personal correspondence, including scanned physical mail, email exports, digital letters, and ad-hoc attachments. Complements functional requirement FR-045, the item schema envelope, and the linking/backlink specification.

## Objectives
- Provide a single workflow for capturing inbound and outbound correspondence regardless of origin (paper, email, portal downloads, messenger exports).
- Preserve original artifacts (PDF, image, MSG/EML, text) while extracting structured metadata for search, dashboards, and automations.
- Support item-level sensitivity with session-level gating, retention controls, and cross-linking to projects, tasks, wiki entries, and financial/health records.
- Enable repeatable exports that recreate both normalized metadata and the original file hierarchy for audits or legal purposes.

## Scope
- **In scope:** Paper mail scans, handwritten notes, postal receipts, invoices, statements, contracts, letters, emails (exported EML/MSG/MBOX), messenger conversations exported as files, correspondence attachments (images, spreadsheets), return receipts, and outbound communication drafts.
- **Out of scope (initially):** Live IMAP/SMTP sync, automatic OCR correction feedback loops, legally binding digital signatures (tracked as attachments), and third-party SaaS mailroom integrations.

## Intake Sources & Triggers
| Source | Trigger | Notes |
| --- | --- | --- |
| Watched filesystem folders | New file arrival | Supports multi-root (e.g., `/Scans/Inbox`, `/EmailExports/2025`) with per-folder default realm and classification hints. |
| Manual upload UI | User drag/drop or file picker | Allows batching with per-batch metadata presets (realm, sender, topic, project). |
| Email export import | EML/MSG/MBOX dropped into watched folder or CLI command (`Eirenhall import-correspondence`) | Parser extracts headers, body, attachments, inline images, message-id/thread-id, recipients. |
| Mobile/remote capture | Secure intake endpoint accepts zipped bundles or single files with metadata form | Piggybacks on remote intake from FR-008; queued for review when offline. |
| Automation jobs | Scheduled fetch of portal downloads (e.g., insurance statements) via plugin | Requires per-area credentials; records provenance in metadata. |

## Item Type & Capability
- `item_type = "correspondence"` with manifest `schema/types/correspondence.yaml`.
- Activates the `correspondence.archive` capability (`schema/capabilities/correspondence.archive.yaml`) to expose ingestion dashboards, retention controls, and archive/export actions.
- Core field: `fields.entry` referencing `schema/fields/correspondence_entry.json` (includes parties, channel, timestamps, language, references, retention policy).
- Additional fields: `fields.parties` (`correspondence_party.json[]`), `fields.attachments` (`binary_reference.json[]`), `fields.notes` (`rich_text.json`) for operator scratchpads or migration breadcrumbs (embedded URIs participate in the standard backlink pipeline).

## Normalized Metadata Model
Correspondence items reuse the base item schema and declare the following domain fields (schema definitions now live under `schema/fields/std.correspondence.*`):
- `direction`: enum `inbound` / `outbound`.
- `sender` / `recipient`: list of `std.correspondence.party` entries describing people or organizations involved.
- `channel`: enum of `postal_mail`, `email`, `portal`, `messenger`, `fax`, `other`.
- `received_at` / `sent_at`: timestamps (optional when unknown).
- `subject` / `summary`: text derived from letterhead, email subject, or operator input.
- `reference_ids`: array of external identifiers (invoice number, tracking code, message-id).
- `topics`: ordered tags reflecting domain taxonomy (finance, health, household, legal, personal).
- `source_files`: attachment manifest referencing preserved originals, scans, or extracted attachments.
- `ocr_text`: optional machine-generated transcript for scanned documents.
- `related_items`: array of `std.object_reference` linking to projects, tasks, wiki entries, or financial records.
- `retention_policy`: structured metadata indicating retention schedule, legal hold, or review dates, with support for explicit indefinite retention (`retain_indefinitely = true`) when archival policies require permanent storage.

Attachments retain original filenames, checksums, media type, page count, and optional OCR confidence metrics.

## Processing Pipeline
1. **Ingestion:** Detect new artifact (filesystem, upload, automation). Create a draft correspondence item with provisional metadata (source path, capture timestamp, default realm).
2. **Extraction:** Run OCR (for images/PDF), parse email headers, detect page count, and generate text previews. Capture provenance (`metadata.sys.provenance`) with tool versions and confidence scores.
   - OCR/language handling prioritizes German dictionaries and hyphenation, with fallbacks for English and Polish. Language hints are stored alongside OCR output to support future spell-check or transliteration.
3. **Classification:** Apply rule-based or AI-assisted tagging for topics, sender/recipient normalization, and project linkage suggestions. Present operator review queue to confirm or adjust.
4. **Normalization:** Move or copy original files into managed storage (`/data/<realm>/correspondence/<year>/...`), recording checksum and storage manifest entry. Update item attachments to reference managed location.
5. **Publication:** Mark draft as finalized, enabling search, dashboards, and exports. Trigger downstream automations (e.g., task creation for required follow-up, financial reconciliation).

PII redaction is not enforced during ingestion because the system operates inside a personal trust boundary. Operators retain manual control if selective redaction is ever required for sharing.

## Queries & Dashboards
- Saved searches by sender, recipient, channel, topic, direction, or retention status.
- Dashboard widgets: daily/weekly inbound summary, open follow-ups, expiring retention holds, per-project correspondence timeline.
- Cross-project view: `project` detail surfaces correspondence linked to the project with filters by direction or status.
- Conversation transcript links: highlight when correspondence references or originates from assistant conversations.

## Retention & Compliance
- Default retention per area/realm (organizational) (e.g., household mail retained indefinitely, financial documents per tax regulations). `retain_indefinitely` defaults to `true` when no policy is supplied, ensuring archival items persist unless explicitly time-bound.
- Legal hold flag prevents deletion and adds audit requirement for removal.
- Export profiles: full archive (original files + metadata CSV/JSON), redacted share (selected fields + rendered PDFs).

## Integration Points
- **Projects:** Auto-link to the active project when correspondence arrives in project-specific intake folders or when metadata contains project identifiers.
- **Tasks/GTD:** Optional rule to spawn tasks for follow-up, with backlink to correspondence item.
- **Financial records:** Suggest linking invoices/statements to relevant `financial_transaction` or `account_statement` items based on parsed amounts or reference IDs.
- **Health records (future):** Placeholder hook to connect with upcoming health schemas via shared reference IDs or patient identifiers.

## Open Questions
1. **PII masking:** Not required for the personal deployment; exports preserve original content without automated redaction.
2. **Language support:** Prioritize German OCR/spell dictionaries with secondary support for English and Polish. Additional languages can be configured later.
3. **Encrypted exports:** Not needed for the current scope because ingestion runs within a trusted environment and encrypted mail is not expected.
4. **Messenger exports:** Retain group conversations intact. Individual messages are tagged with sender metadata, but no automatic splitting occurs.

## Long-Lived Exchanges & GTD Integration
- A `conversation_thread` represents the enduring narrative that spans multiple correspondence items, tasks, and decisions (e.g., medical invoice → insurer response → tax follow-up). Each thread references the underlying correspondence items and links to any GTD tasks or projects used to track work.
- Correspondence ingestion can automatically suggest new or existing conversation threads based on shared reference IDs, participants, or topics. Operators confirm the linkage in the review queue.
- GTD flows capture actionable steps triggered by correspondence (e.g., schedule payment, prepare tax report). Tasks maintain backlinks to both the conversation thread and the individual correspondence artifact for traceability.
- Dashboards and saved searches surface conversation-level status (open, awaiting response, resolved) derived from GTD task completion and correspondence timestamps, ensuring long-running processes remain visible without duplicating artifacts.

## Next Steps
- Wire ingestion pipeline to populate `std.correspondence.entry`, including party normalization and language hints.
- Implement review UI for validating extracted metadata, thread linkage, and retention policy suggestions.
- Seed classification taxonomy (topics, senders, retention categories) and associated lookup tables.
- Extend export tooling to embed `std.correspondence.entry` and `std.conversation.message` tokens for round-trip fidelity.
