# M1 Capability Execution Plan

This note captures the concrete engineering work that will be performed next to
close the gaps identified for Milestone M1. It focuses on operationalising the
capability registry and extending executable coverage for the newly documented
item types.

## Objectives
- Enforce capability contracts during bootstrap so type manifests cannot declare
  unknown or invalid capabilities.
- Provide runtime helpers and tests for `project`, `correspondence`, and
  `conversation_thread` types to keep code and specifications in sync.

## Work Breakdown
1. **Capability Registry Loader**
   - Introduce a loader that reads files from `schema/capabilities`.
   - Validate capability keys, dependency chains, and configuration schema
     references.
   - Expose query helpers (`get_capability`, `list_capabilities`) for bootstrap
     checks.
   - Wire the loader into `kernel.types.bootstrap_types` so type manifests are
     validated against the capability catalog.
2. **Type Helpers & Fixtures**
   - Add Python metadata wrappers for `project`, `correspondence`, and
     `conversation_thread` types similar to the existing document/task helpers.
   - Seed fixture items exercising their schema signatures (capabilities, key
     fields) for use in tests.
3. **Test Coverage**
   - Extend capability bootstrap tests to assert dependency validation and error
     handling.
   - Add type tests confirming capability accessors for the new item types.
   - Expand derived-evaluator coverage once metrics are introduced (tracked as a
     follow-up).

## Validation
- Unit test suite passes (`pytest`).
- Type bootstrap fails fast when manifests reference unknown capabilities.
- Fixtures load without schema violations when processed by the registry
  loader.

