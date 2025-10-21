# Minimum Viable Product (MVP)

This document pins the first production-quality slice of Kki so scope growth is
intentional. The MVP emphasises a traceable ingestion → enrichment → retrieval
loop backed by storage and governance foundations.

## MVP scope

- **Vertical slice:** Document capture → OCR/normalise → JSON manifest →
  searchable index → reader view.
- **Content types:** `document`, `task`, and `project` items with derived metrics
  and cross-linking.
- **Capabilities:** `projects.workspace`, `tasks.board`, and timeline rendering
  for captured conversations (read-only in MVP).
- **Automation:** Persona-guided enrichment runs in dry-run mode with human
  approval for updates.

## Entry criteria

- Repositories, storage tiers, and personas initialised per ADR-000/ADR-001.
- Schema registry and fixtures validate cleanly via `scripts/validate_schema.py`.
- Core personas manifests landed under `personas/`.

## Exit criteria

- Capture pipeline ingests a sample bundle, produces manifest + attachments, and
  indexes metadata for search in under 30 seconds.
- Offline bundle renders in reader view using cached assets (per FR-015).
- Governance review confirms personas stay within declared permissions.
- CI pipeline (see `.github/workflows/ci.yml`) passes on tagged release.

## Won’t do for MVP

- Full-text vector embeddings or semantic search.
- Live email/IMAP ingestion streams.
- Automatic schema migrations for legacy datasets (manual scripts only).
- Autonomous persona writes without human checkpoint.
- Multi-tenant UI polish beyond core operator experience.

## Traceability

| Requirement | Spec coverage | Test coverage |
| --- | --- | --- |
| FR-014 (Link capture & normalization) | docs/specs/capture_storage_blueprint.md | tests/fixtures/items/document_insurance_policy_pdf.json; acceptance scenario AC‑FR‑014 |
| FR-015 (Offline archiving) | docs/adr/ADR-003-conflict-resolution-and-offline-policy.md; docs/specs/capture_storage_blueprint.md | tests/derived/test_evaluator.py::test_document_metrics_handle_delta_body |
| FR-018 (Unified query) | docs/specs/project_workspace.md; docs/specs/generic_item_surface.md | tests/derived/test_evaluator.py::test_project_metrics |
| FR-027 (Tiered caching) | docs/adr/ADR-003-conflict-resolution-and-offline-policy.md | Manual cache drill (tracked for automation) |
| AC-NFR-SEC (E2E encryption & egress block) | docs/requirements/06_non_functional/README.md | Security drill scripts (TBD) |

Update the table whenever requirements, specs, or tests change. New requirements
should not be merged without mapping to at least one spec and test row.
