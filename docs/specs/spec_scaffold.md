# Spec scaffold & traceability

This scaffold links requirements, specifications, and tests so contributors can
trace behaviour from stakeholder needs to executable checks. Each spec in
`docs/specs/` should reference this table and include a short traceability block
mirroring the format below.

## How to use

1. When adding or updating a requirement, register it in the table with the
   associated spec section and automated test.
2. Specs should include a “Traceability” subsection referencing requirement IDs
   and concrete test modules.
3. Tests must cite the requirement ID in a docstring or comment so readers can
   navigate back to the originating need.

## Current mapping

| Spec section | Purpose | Requirements | Tests |
| --- | --- | --- | --- |
| docs/specs/capture_storage_blueprint.md | Storage tiers, manifests, retention | FR-014, FR-015, FR-027, ADR-000, ADR-003 | scripts/run_poc.py (manifest validation), tests/derived/test_evaluator.py::test_document_metrics_handle_delta_body |
| docs/specs/metadata_governance.md | Metadata namespaces & lifecycle | FR-001, FR-003, FR-038 | tests/fixtures/items/*.json (metadata shape), tests/types/test_core_types.py |
| docs/specs/item_schema.md | Item envelope contract | FR-002, FR-003, NFR-PERF | scripts/validate_schema.py, tests/fixtures/items/*.json |
| docs/specs/capability_contracts.md | Capability registration/versioning | FR-005, FR-023 | tests/capabilities/test_capabilities.py |
| docs/specs/generic_item_surface.md | UI surface & diff model | FR-018, FR-019, FR-020, UX tenets | Manual UI acceptance (pending automation) |
| docs/specs/project_workspace.md | Project summarisation & rollups | FR-042 | tests/derived/test_evaluator.py::test_project_metrics |
| docs/specs/correspondence_management.md | Correspondence ingestion & retention | FR-045 | tests/fixtures/items/correspondence.json, tests/derived/test_correspondence_metrics (TBD) |
| docs/specs/field_library.md | Reusable field definitions | FR-005, FR-038 | scripts/validate_schema.py (field refs) |

Add new rows for future specs and update the mapping when requirements or tests
shift. If a requirement lacks automated coverage, call it out explicitly so it
can be prioritised.
