# Chapter 1 – Goals & Vision

## 1.0 Mission Context
A self-hosted personal knowledge and life-management system must capture heterogeneous content, preserve it for decades, and help its owner act on it without ever surrendering control. The platform spans documents, media, personal data, tasks, and automations while running entirely on trusted hardware that the owner operates at home.

## 1.1 Elevator Pitch
_A realm-aware, privacy-first personal hub that unifies knowledge, tasks, and automations, keeps everything portable, and grows into a local AI assistant without depending on the cloud._

## 1.2 Vision Narrative
- **Holistic life substrate:** Notes, files, archives, tasks, household records, and ad-hoc automations live in one place with consistent structure and provenance.
- **Realm-aware sharing:** Individuals retain absolute control but can selectively expose read or write access to family members or trusted contacts across personal, family, and guest realms.
- **Longevity & portability:** Data rests in long-lived, open formats with straightforward export so that no tool lock-in threatens future access.
- **AI-augmented evolution:** Core functionality operates without AI. Local models—when available—assist with organization, summarization, workflow design, and eventually richer automations, always under explicit human approval.
- **Local coding companion:** On-device AI delivers developer support for personal projects and the platform itself—suggesting code, refactors, and tests while honoring guardrails and demanding human review before changes land.
- **Personal sovereignty:** The owner defines boundaries, reviews automations, and assumes responsibility for social, ethical, and legal considerations; the system never overrides those decisions.
- **Anywhere via the web:** A browser-based interface makes the system reachable from any device on the local network (and beyond when safely exposed), without requiring native apps.

## 1.3 Core Goals
1. **Self-hosted trust boundary:** Operate exclusively on owner-controlled infrastructure, prioritizing offline-first behavior and avoiding unsolicited cloud dependencies.
2. **Unified content management:** Normalize ingestion, search, and retrieval across documents, media, knowledge artifacts, and personal records while preserving original context.
3. **Task and automation hub:** Provide robust personal and household task tracking plus workflow automation that can orchestrate local services and devices.
4. **Realm hierarchy & sharing:** Support nested visibility scopes (personal, family, selective guests) with fine-grained read/write controls and easy auditing of shared items.
5. **Durability & export:** Guarantee straightforward backup, restore, and export to open standards so migrations remain practical even at tens of terabytes.
6. **Privacy & data ownership:** Encrypt at rest and in transit, maintain explicit consent for any sharing, and ensure the owner can inspect or revoke access at any time.
7. **Progressive AI enablement:** Enable local AI helpers to propose classifications, summarize content, suggest automations, and evolve their remit over time, all optional and reviewable before execution.
8. **On-device coding assistant:** Equip a local model to provide code generation, refactoring, testing, and self-improvement proposals for the system and adjacent projects, with enforced review gates and audit trails.
9. **Extensible schema & workflows:** Allow the owner to evolve data types, integrations, and automations over time with transparent diffs and rollback paths.
10. **Operational simplicity:** Favor predictable maintenance, straightforward monitoring, and the ability to scale up to tens of terabytes without complex orchestration.

## 1.4 Guiding Principles
- **User agency first:** The human remains the final arbiter for every automated action or AI proposal.
- **Security by design:** Default-deny access, compartmentalized realms, and strong authentication protect household data.
- **Offline resilience:** Core operations must continue when external connectivity is unavailable.
- **Clarity over metrics:** Qualitative outcomes (control, longevity, usability) matter more than numeric KPIs in this phase.

## 1.5 Non-Goals (Current Phase)
- Supporting broad multi-tenant deployments beyond a single household.
- Depending on third-party cloud services for critical functionality.
- Defining time-bound milestones or adoption targets.
- Pursuing societal impact narratives beyond the owner’s personal use cases.

## 1.6 AI Personas and Guardrails

| Persona | Purpose | Scope | Capabilities | Constraints |
| --- | --- | --- | --- | --- |
| Librarian | Archival, retrieval, curation | Archives, indexes, metadata (R/O except tagging & collections) | Search, summarize, cross-reference | Strict realm caps; provenance for changes |
| System Advisor | Evolve workflows, schema, infra | Schemas, configs, manifests, metrics | Introspection, simulation, proposals | Sandbox; proposals only; human approval to apply |
| Assistant | GTD/tasks/projects, reflective notes | Personal/Household realms | Conversation, planning, scheduling | Undo/redo; non-destructive edits |
| Coding Assistant | Local dev support | Repos, docs, tests | Code gen, refactor, tests, PRs | No direct writes to prod data; PRs + tests required |

## 1.7 Out-of-Scope Considerations
The owner retains responsibility for legal, ethical, and social compliance. The system will not second-guess these decisions; its role is to faithfully execute within the boundaries the owner defines.
