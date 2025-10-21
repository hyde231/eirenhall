# Capability: conversations.timeline

Provides timeline rendering, transcript search, and excerpt linking for `conversation_thread` items.

## Purpose
- Standardize how conversation threads expose ordered messages to clients.
- Advertise timeline/search affordances that UI components can rely on.
- Define metadata namespace for timeline summaries, filters, or analytics.

## Affordances
- `detail` – renders chronological message view with speaker attribution, attachments, and references.
- `timeline` – exposes sequential timeline widgets (e.g., in dashboards or sidebars).
- `search` – supports filtering messages by speaker, tags, or referenced items.

## Metadata Namespace
`cap.conversations.timeline.*` – reserved entries may include:
- `cap.conversations.timeline.filters` – persisted filter presets.
- `cap.conversations.timeline.excerpts` – pinned snippets for dashboards or GTD follow-ups.
- `cap.conversations.timeline.metrics` – cached analytics (message counts, response latency).

## Events
- `conversation.message.appended` – emitted when a new message is added.
- `conversation.status.changed` – tracks state shifts (open, waiting, resolved).

## Configuration
`configuration_schema: null` – no configuration payload is required initially. Future iterations may formalize filter presets or timeline styling.

## Usage
1. `conversation_thread` manifest includes `conversations.timeline`.
2. Timeline field (`fields.timeline`) stores messages conforming to `std.conversation.timeline`.
3. UI components listen to capability events to refresh views when messages or status change.
4. Exports embed message tokens (`std.conversation.message`) ensuring round-trip fidelity.

## Future Considerations
- Introduce configuration options for default filters or summary widgets.
- Add analytics hooks to compute derived metrics on schedule.
- Provide automation to auto-link new messages with related correspondence.
