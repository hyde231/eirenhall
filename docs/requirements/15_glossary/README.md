# Glossary (Selected)

- **Item:** Typed, realm-scoped content entity.
- **Capture:** Time-stamped snapshot/version of an Item.
- **Realm:** Privacy boundary (configurable names) such as `Shared`, `Household`, `Personal`, `Intimate`; governs storage prefixes, credentials, and sharing policies.
- **Sensitivity:** Visibility control (configurable levels) determining UI/API presentation within a realm.
- **Tag:** First-class classification entity (ID, aliases, hierarchy, lineage).
- **Manifest:** Open JSON/YAML index of Items & file references (sidecar files that travel with content).
- **Capability:** Modular behavior mix-in (e.g., Queryable, Annotatable) attached to Item types.
- **Collection:** Saved search (dynamic) or snapshot export (static) that groups Items for navigation or distribution.
- **Persona (AI):** Bounded automated role with scoped tools and realm caps executed within sandboxed runtimes.
- **Persona (Human):** Household operator, steward, or collaborator interacting with the system via UI/CLI, inheriting realm caps defined in governance.
- **Persona Sandbox:** Execution environment (container/VM) constraining an AI persona’s resources, credentials, and network access.
