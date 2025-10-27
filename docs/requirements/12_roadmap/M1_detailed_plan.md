# Milestone M1 Detailed Plan

## Overview
Milestone M1 ("Discovery") establishes the foundational capabilities required for the knowledge kernel initiative. The sprint spans Weeks 1-2 and focuses on defining the canonical data model, validating session-level handling (item levels and session max-level filtering), and preparing ingestion and storage pathways that later milestones will extend.

> **Scope note:** Infrastructure enablement (e.g., Wake-on-LAN, power-aware orchestration, hardware readiness) is explicitly deferred to later milestones so M1 can concentrate on data modeling and storage primitives.

## Objectives
- Deliver a unified Item model that supports documents, GTD-style tasks, and wiki entries from the outset.
- Stand up the type registry and capability mix-in framework so new item types can be added safely.
- Produce baseline schemas, validation rules, and derived value conventions that downstream services can reuse.
- Document storage, capture, and indexing practices to ensure artifacts remain portable and queryable.

## Key Deliverables
1. **Item Base Schema**
   - Shared identifiers, timestamps, tagging, capture metadata, attachment manifests, and extensible metadata map.
   - Session-level enforcement rules: item-level classifications and session max-level filtering applied consistently across attachments and annotations.
2. **Capability Contracts**
   - Definition of mix-in interfaces (Viewable, Workflown, Schedulable, Annotatable) and the UI/workflow affordances each unlocks.
   - Validation that capability declarations register automatically with list/detail/timeline boards.
3. **Type Registry Implementation**
   - Registry structure with type key, version, capability list, JSON schema reference, facet/action catalog, migration hooks, and relation descriptors.
   - Plugin registration lifecycle (load, validate, migrate) documented and exercised with core item types.
4. **Standard Field Library**
   - Primitive types (text, numeric, boolean, temporal, measurement, currency, percentage, enum, tags, formatted text, JSON/CSV, media reference, secret, geolocation, rating) with validation semantics.
   - Composite types (lists, ordered references with role/annotation hints, graph relations, inline notes) and associated schema metadata.
5. **Derived Value Framework**
   - Formula definition format, evaluator lifecycle, provenance recording, and normalized output storage under reserved metadata namespaces.
   - Sample derived metrics for each core item type (e.g., task completion ratio, document checksum summaries).
6. **Capture & Storage Blueprint**
   - Directory conventions (realm/type/year), manifest structure, snapshot metadata (hashes, tool versions), and tiered caching approach.
   - Indexing outline covering normalized fields, tag facets, and optional vector embeddings.
7. **Ingestion & Conversion Recipes**
   - Guided mapping flow aligning detected fields with target schemas, including soft/hard constraint handling.
   - Repository for reusable conversion recipes seeded with at least one document, task backlog, and wiki import example.

## Execution Timeline
- **Week 1**
  - Finalize Item base schema and publish initial JSON schemas in the registry.
  - Implement capability contracts and register document/task/wiki prototypes.
  - Draft storage blueprint and circulate for security review.
- **Week 2**
  - Build derived value evaluators and integrate provenance capture.
  - Complete ingestion mapping UI specification and conversion recipe storage format.
  - Validate registry lifecycle with plugin add/remove tests and document migration process.

## Dependencies & Coordination
- Align with security to confirm encryption/backup approach; per-realm key management is not required under the session model.
- Coordinate with operations for storage provisioning that meets manifest-first handling requirements.
- Schedule Wake-on-LAN and broader infrastructure readiness reviews for the next milestone (M2) once the PoC storage flows are validated.

## Acceptance Criteria
- All core schemas and capability definitions reviewed and merged into the shared registry repository.
- Demonstrable sample items (document, task, wiki entry) pass validation, render in baseline views, and expose derived metrics.
- Storage blueprint and ingestion playbooks published in the knowledge base with sign-offs from security and operations leads.
- Backlog entries linked to M1 updated with status notes referencing the completed artifacts.
