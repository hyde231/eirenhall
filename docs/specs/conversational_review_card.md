# Conversational Review Card Specification

Defines the review-and-confirm surface shown after voice/text capture and NLU extraction. The card enables quick validation, light edits, and safe publishing of proposed items while maintaining privacy and provenance.

## Goals
- Make capture → confirm → publish fast and reliable.
- Show exactly what was heard, what was inferred, and what will be created.
- Keep sensitive data session-gated; default new items to the session level.
- Preserve provenance and allow undo.

## UI Structure
- Header
  - Session level chip (e.g., Family), area/realm, capture timestamp, language, ASR model, confidence.
  - Actions: Publish All, Publish Selected, Save as Drafts, Cancel.
- Transcript
  - Editable transcript with confidence heatmap (low-confidence spans subtly highlighted).
  - Quick fixes: punctuation, time normalization (e.g., "eben" → concrete timestamp), language toggle.
- Entities & Disambiguation
  - Chips for detected people/organizations/topics with confidence.
  - Resolve control: search existing contacts/projects, create new, or remove.
- Proposed Items
  - One card per item (Event, Task/Idea, etc.) with inline fields:
    - Type icon, confidence badge.
    - Title, when/duration, participants, topics/tags, realm (organizational), level (defaults to session), notes.
    - Links preview (conversation_thread, related items).
    - Toggles: Draft vs Publish; "Save distilled fact to memory" (off by default).
- Memory (optional)
  - Suggested durable memory facts (1–2 short sentences) with explicit enable toggles.
- Footer
  - Audit preview: items/links/memory to be written; provenance note.

## Keyboard & Shortcuts
- Enter = Publish Selected
- Ctrl/Cmd+Enter = Publish All
- Esc = Cancel
- Tab/Shift+Tab cycle unresolved fields
- Alt+1/2/… jump to item cards

## Proposal Payload (wire format)
```json
{
  "proposal_id": "prop_20250303_183012",
  "session": {"area": "personal", "max_level": "personal"},
  "capture": {
    "ts": "2025-03-03T18:30:12Z",
    "device": "desktop-mic",
    "language": "de",
    "asr_model": "whisper-small-int8",
    "confidence": 0.87
  },
  "transcript": {
    "text": "Ich hatte eben ein Telefonat mit Stefan Halmagyi...",
    "spans": [{"start":0, "end": 12, "confidence": 0.62}]
  },
  "entities": [
    {"kind": "person", "text": "Stefan Halmagyi-Fischer", "candidate_ids": ["person_abc"], "chosen_id": null, "confidence": 0.78},
    {"kind": "topic", "text": "Optionen auf Rohstoffe", "confidence": 0.82}
  ],
  "items": [
    {
      "temp_id": "evt1",
      "type": "event",
      "confidence": 0.84,
      "fields": {
        "title": "Telefonat mit Stefan Halmagyi-Fischer",
        "start_at": "2025-03-03T18:25:00Z",
        "participants": [{"ref": "person_abc", "display": "Stefan Halmagyi-Fischer"}],
        "topics": ["Finanzen", "Optionen auf Rohstoffe"],
        "realm_id": "personal",
        "level": "personal"
      },
      "links": {"thread_id": "thread_123"}
    },
    {
      "temp_id": "task1",
      "type": "task",
      "confidence": 0.76,
      "fields": {
        "title": "Thema Optionen auf Rohstoffe recherchieren",
        "realm_id": "personal",
        "level": "personal"
      },
      "links": {"related_item_ids": ["evt1"]}
    }
  ],
  "memory_suggestions": [
    {"text": "Kontakt interessiert sich für Rohstoff-Optionen", "source_refs": ["evt1"], "enabled": false}
  ]
}
```

## Publish Response
```json
{
  "proposal_id": "prop_20250303_183012",
  "published_items": [{"temp_id": "evt1", "item_id": "event_9f2e"}, {"temp_id": "task1", "item_id": "task_aa10"}],
  "drafts": [],
  "memory_created": ["mem_123"],
  "audit_id": "aud_77b1"
}
```

## Rules & Guarantees
- Default item level = session `max_level`; downgrades require explicit confirmation and create an audit entry.
- No network egress during ASR/NLU/TTS.
- Vector memory uses allowlists/redaction and respects session-level filters.
- Provenance recorded: transcript checksum, model ids, confidences, user edits, final field values, created links.

## Error Handling
- Partial failure: publish what succeeded; show per-item error chips; allow retry.
- Offline: queue publishes; show "awaiting sync" labels.
- Undo: limited window; revert created items/links/memory; log audit.

## Accessibility
- Full keyboard navigation, visible focus states, screen reader labels, high-contrast cues for low confidence/required edits.

## Acceptance Criteria
- Example utterance yields correct entities and accurate drafts; user can resolve the person entity and publish both items.
- Published items default to session level; links from conversation_thread are created.
- Provenance is captured; no external network calls occur.
- Undo reverses created items and links within the allowed window.

## Extensibility Hooks
- Plugins can append additional item cards (e.g., bookmark, contact update) before publish.
- Validators may add warnings (non-blocking) to item cards.
