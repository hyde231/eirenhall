# Capability: conversations.voice

Provides voice capture, local transcription, and optional local TTS for conversational interactions driving conversation threads and GTD outcomes.

## Purpose
- Enable hands-free or quick capture via push-to-talk.
- Keep all speech processing local and session-gated.
- Standardize how UI and runners invoke ASR/TTS and surface review flows.

## Affordances
- `voice.capture` — start/stop recording; attach audio to a conversation thread; run local ASR.
- `voice.review` — show transcript, extraction results, and proposed items; confirm/apply edits.
- `voice.synthesize` — (optional) local TTS for confirmations or summaries.

## Events
- `voice.capture.started` | `voice.capture.stopped` (with device and timestamps)
- `voice.transcribed` (transcript, language, confidence)
- `voice.items.proposed` (event/task drafts, links)
- `voice.items.published` (finalized item ids)

## Configuration
`configuration_schema: null` — initial version relies on installation-wide ASR/TTS configuration and per-area enablement. Future versions may add per-device profiles and sampling rates.

## Security
- ASR/TTS must be local; any attempt at network calls is blocked.
- Transcripts and derived items respect session `max_level`.

## Usage
1. UI triggers `voice.capture` in the active area.
2. Local ASR produces transcript and metadata; runner emits `voice.transcribed`.
3. Extraction module proposes items; `voice.review` flow confirms.
4. Published items are linked to the conversation thread and indexed per vector_memory.md rules.
