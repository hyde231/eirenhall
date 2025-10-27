# Conversational Capture & Voice I/O Specification

Defines the end-to-end pipeline for conversational interaction with Eirene (the local assistant within Eirenhall): voice input, local transcription, understanding, item creation, and optional voice output. All processing is local and governed by session-level gating.

## Goals
- Capture quick voice memos and free-form utterances and turn them into structured data (events, tasks/ideas, links, and notes) with minimal friction.
- Keep speech-to-text (ASR) and text-to-speech (TTS) fully local; no cloud egress.
- Respect session-level gating so sensitive content never surfaces across levels.
- Provide confirmations and undo for generated items.

## Inputs
- Audio: PCM/WAV/FLAC/Opus; recorded via push-to-talk or uploaded file.
- Text: typed input or pasted content.
- Metadata: capture timestamp (defaults to now), device, area, and session `max_level`.

## Pipeline
1. Transcription (ASR)
   - Local ASR (e.g., Whisper-small/int8, Vosk, faster-whisper) with German primary; fallback English/Polish.
   - Emit transcript + language + confidence + timing.
2. Normalization
   - Normalize timestamps (“eben” → capture_ts), number/date phrases, and light punctuation.
3. Extraction (NLU)
   - Entities: people/organizations/projects (resolve against contacts/projects by fuzzy match).
   - Intents: event mention (Telefonat), task/idea, follow-up, topic tags.
   - Topics: finance, options/commodities (taxonomy driven).
   - Owner resolution: first-person pronouns map to operator.
4. Item generation (drafts)
   - Event (conversation/phone call) item with participant link (e.g., Person: Stefan Halmagyi-Fischer), datetime = transcript_ts, topics.
   - Task/Idea item: “Research Optionen auf Rohstoffe” linked to the event and topics.
   - Conversation thread: append message with transcript and extraction summary; link created items.
5. Review & confirm
   - Present a compact diff: transcript, detected entities, proposed items.
   - User approves/edits; only then publish items (drafts → active).
6. Memory (optional)
   - Ephemeral: last N turns cached with TTL.
   - Durable: only when explicitly “save to memory”; store distilled facts with source links (see vector_memory.md (see also conversational_review_card.md)).
7. Voice output (optional)
   - Local TTS (e.g., Coqui TTS/XTTS, Piper) to confirm actions or read summaries.

## Privacy & Security
- Local only: ASR/TTS and NLU run on local nodes; no cloud API calls.
- Session gating: all retrieval and suggestions filter by `item.level <= session.max_level`.
- Field allowlist and redaction before embedding into vector memory.
- Provenance: transcript, model ids, confidences, and extraction results recorded under `metadata.sys.provenance`.

## UX States
- Push-to-talk widget with explicit recording indicator and cancel.
- Review card showing transcript, detected person/topic, and proposed items with per-field edits.
- Undo for recent publishes; link to generated items and conversation thread.

## Example (German)
Input (audio):
“Ich hatte eben ein Telefonat mit Stefan Halmagyi. War ganz interessant, weil er sich auch sehr mit dem Finanzmarkt beschäftigt. Er ist begeistert von Optionen auf Rohstoffe, vielleicht sollte ich da auch mal reinschauen.”

Derived:
- Owner = operator (Ich)
- When = capture_ts (eben)
- Event = Telefonat (with Person: Stefan Halmagyi‑Fischer)
- Topics = Finanzen; Optionen auf Rohstoffe
- Task/Idea = “Thema Optionen auf Rohstoffe recherchieren”

Generated items (drafts):
- Event: conversation/phone call on capture_ts; participant link to contact; topics.
- Task: linked to event; due = unset; level = session `max_level`.
- Conversation thread: new message (speaker=owner) with transcript + links.

## Engines & Placement
- ASR: Whisper small/int8 or Vosk on desktop/minipc; batch jobs can use GPU.
- TTS: Piper or Coqui XTTS locally on desktop/minipc.
- Extraction: local NLU (rules + small LLM if available locally) with deterministic fallbacks.
- Vector memory: content/memory indices per vector_memory.md (see also conversational_review_card.md); rebuildable; session gated.

## Acceptance Criteria
- Voice transcription succeeds offline and yields German transcripts with timing and confidence.
- Proposed items are accurate for the example and editable before publish.
- Conversation threads are updated with the transcript and links.
- No external network calls during ASR/TTS/NLU; provenance recorded.
- Session `max_level` applied to created items by default.
