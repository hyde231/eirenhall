# Glossary (Selected)

- **Item:** Typed, realm-scoped content entity.
- **Capture:** Time-stamped snapshot/version of an Item.
- **Access Level:** Governance tier (e.g., `Intimate`, `Personal`, `Household`, `Shared`, `Guest`) that defines sensitivity, audit expectations, and default policies for any realms instantiated under it.
- **Realm:** Workspace instance bound to a single access level (e.g., "Travel Planning" at the Personal level) that inherits policy defaults while maintaining its own membership, storage prefixes, credentials, and lifecycle history.
- **Sensitivity:** Visibility control (configurable levels) determining UI/API presentation within a realm.
- **Tag:** First-class classification entity (ID, aliases, hierarchy, lineage).
- **Manifest:** Open JSON/YAML index of Items & file references (sidecar files that travel with content).
- **Capability:** Modular behavior mix-in (e.g., Queryable, Annotatable) attached to Item types.
- **Collection:** Saved search (dynamic) or snapshot export (static) that groups Items for navigation or distribution.
- **Persona (AI):** Bounded automated role with scoped tools and realm caps executed within sandboxed runtimes.
- **Persona (Human):** Household operator, steward, or collaborator interacting with the system via UI/CLI, inheriting realm caps defined in governance.
- **Persona Sandbox:** Execution environment (container/VM) constraining an AI persona’s resources, credentials, and network access.
