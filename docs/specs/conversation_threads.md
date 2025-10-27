# Conversation Thread Specification

Describes the `conversation_thread` item type and associated schemas that store
assistant/operator transcripts, referenced correspondence, and GTD linkages.

## Objectives
- Capture dialog between the operator, local assistants, and external parties in
  a structured, searchable format.
- Link messages to correspondence items, projects, and tasks so long-running
  processes remain traceable.
- Support mixed-language transcripts (German primary, English/Polish secondary)
  while preserving the original message ordering and speaker attribution.
- Enable exports that reconstruct timeline context, including message metadata,
  references, and attachments.

## Item Envelope
Conversation threads reuse `item_base.json` with `item_type = "conversation_thread"`.
Key fields:

| Field                     | Schema                                        | Notes |
| ------------------------- | --------------------------------------------- | ----- |
| `fields.timeline`         | `schema/fields/conversation_timeline.json`    | Ordered message timeline (`messages[]`, optional summary, sync timestamp). |
| `fields.participants`     | `schema/fields/correspondence_party.json[]`   | Distinct participants involved across the timeline. |
| `fields.related_items`    | `object_reference.json[]`                     | Pinned references (projects, tasks, correspondence). |
| `fields.notes`            | `rich_text.json`                              | Scratchpad for unresolved questions, migration breadcrumbs, or operator commentary (links normalize via standard backlinking). |
| `metadata.cap.conversations.timeline` | Capability metadata (filters, widgets, summarized stats). | Managed by capability contract. |

Each message in the timeline references `schema/fields/conversation_message.json`
and includes speaker role (`owner`, `assistant`, `external`), optional contact
details, timestamps, body (rich text or plain), attachments, and linked items.

## Capability Behavior
The `conversations.timeline` capability unlocks:
- Timeline rendering with jump-to-message anchors.
- Transcript search facets (speaker, tag, referenced item).
- Excerpt pinning for dashboards and project views.
- Automation hooks that append messages when correspondence or tasks change.

Removing the capability retains raw timeline data but hides specialized UI.

## Language Handling
- OCR/text extraction pipelines annotate each message with `language`
  hints (from `conversation_message.tags` or metadata) prioritizing German,
  with fallback support for English and Polish.
- Mixed-language threads keep per-message language tags for future translation
  workflows.

## Long-Running Exchanges
- Threads can aggregate multiple correspondence items. Messages reference the
  underlying `correspondence` item via `references[]` to maintain provenance.
- GTD tasks created from conversation outcomes link back to specific messages via
  `references` metadata, enabling "jump to source" actions in dashboards.
- Status cues (open, waiting, resolved) derive from GTD task state and are stored
  under `metadata.sys.conversation`.

## Exports
- `content.md` renders the timeline with timestamp headings and speaker labels,
  embedding `<<Eirenhall:conversation_message:...>>` tokens for structured data.
- `objects.json` stores each message (`std.conversation.message`), participants,
  and attachments to guarantee round-trip fidelity.
- Attachments referenced in messages are exported via `assets/`.

## Next Steps
- Define automation hooks for correspondence ingestion to propose thread linkage.
- Implement timeline UI components (message grouping, filters, excerpt pinning).
- Add derived analytics (message count by participant, response latencies) under
  `metadata.sys.conversation`.
