# Directory Profiles Specification

Defines the data model, capabilities, and behavioural expectations for the
lightweight CRM/address book extension described in the vision chapter. Builds
on existing correspondence, project, and conversation specs so contacts become a
first-class part of the knowledge kernel graph.

## Objectives
- Maintain canonical profiles for individuals (`person`) and organisations
  (`organization`) with consistent contact methods, identifiers, and lifecycle
  metadata.
- Link contacts to correspondence, projects, tasks, financial records, and
  conversation threads so every interaction carries full context.
- Provide directory-aware capabilities (search, relationship analytics, quick
  actions) without compromising session-level access guarantees.
- Enable automation pipelines (reminders, onboarding checklists, compliance
  reviews) by exposing structured role and cadence data.

## Item Types
Contacts reuse the shared item envelope (`schema/item_base.json`) with dedicated
schemas:

| Item Type | Manifest | Summary |
| --- | --- | --- |
| `person` | `schema/types/person.yaml` | Individual contact with identity, communication channels, affiliations, and cadence metadata. |
| `organization` | `schema/types/organization.yaml` | Business, institution, or collective entity with legal identifiers, sites, contact methods, and relationship roles. |

Both types activate the `directory.profile` capability to unlock directory views,
search facets, and quick actions.

### Core Fields
- `fields.profile` refers to `schema/fields/person_profile.json` or
  `schema/fields/organization_profile.json`.
- `fields.contact_methods` uses `schema/fields/contact_method.json[]` capturing
  emails, phones, portals, messengers.
- `fields.links` leverages the existing `link.json[]` for external resources.
- `fields.related_items` uses `object_reference.json[]` for pinned tasks,
  correspondence, or projects.
- Optional `fields.notes` and `fields.tags` mirror other item types for ad-hoc
  annotations and segmentation.

### Capability Behaviour
`directory.profile` (`schema/capabilities/directory.profile.yaml`) offers:
- **Directory view:** Timeline of interactions (correspondence, tasks) with filter
  chips for realms and stages.
- **Relationship analytics:** Derived metrics for last interaction, open follow-ups,
  number of linked projects.
- **Quick actions:** Jump to new correspondence, schedule check-ins, or open
  templated exports.

Removing the capability preserves the raw schema while hiding directory-specific
affordances.

## Derived Metrics
- `person`: last-contact timestamp, open follow-up count, linked-project count,
  relationship stage presence.
- `organization`: number of active people, linked correspondence count, open
  invoices/contracts (future), last review.
Definitions live in `schema/derived/person.yaml` and `schema/derived/organization.yaml`.

## Interactions with Existing Domains
- **Correspondence:** `fields.participants` should reference contact profiles via
  `object_reference` entries; ingestion pipelines attempt to resolve or propose
  matches using identifiers and normalized names.
- **Conversation Threads:** Message references link back to contacts so timelines
  show which participants joined each exchange.
- **Projects & Tasks:** Contacts can be owners, stakeholders, or reviewers, with
  saved searches surfacing overdue follow-ups or missing documentation.
- **Financial Records:** Organisations tie to accounts/statements; derived metrics
  may show outstanding balances or recurring charges.

## Governance & Sensitivity
- Contacts organize by area/realm (organizational). Sensitivity follows the
  item-level classification model; all surfaces respect the session `max_level`.
- Sensitive fields (medical contacts, legal counsel) default to `private` or
  `intimate` classifications with audit requirements for capability activations.
- Exports respect redaction profiles; metadata namespaces under
  `cap.directory.profile.*` log automated suggestions and review results.

## Next Steps
- Implement ingestion helpers to reconcile imported address books (vCard, CSV)
  into contact items with provenance manifests.
?- Build automated review schedules (quarterly for key providers) using derived
  metrics and GTD hooks.
- Integrate directory widgets into project dashboards and correspondence review
  queues.
