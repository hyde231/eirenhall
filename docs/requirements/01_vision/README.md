# Vision & Goals

## Problem Statement
Build a privacy-respecting, local-first platform that captures and normalizes information, runs code and automations on LAN-only hardware, and smartly orchestrates compute to minimize power usage.

## Product Vision
_A self-hosted, realm-aware personal knowledge & automation substrate that privately understands, writes, and runs code, preserves online/offline content, and wakes the right machine to get work done._

## Goals & Outcomes (SMART)
- **G1 Locality:** ≥95% of use cases run fully local (no cloud egress) by GA.
- **G2 Code throughput:** Typical code task (≤150 LOC + tests) completes in ≤5 minutes p95 when a GPU node is available.
- **G3 Power:** Orchestrator wakes nodes on demand and auto-sleeps idle; 24/7 baseline power ≤ 15W on average.
- **G4 Memory:** Persistent, queryable long-term memory; <1s p95 retrieval for top‑k context.

## Non-Goals (Current Phase)
No cloud LLMs/SaaS telemetry; no multi-tenant IAM beyond a single household.

## Success Metrics & Guardrails
Task completion rate; p95 time-to-result; baseline power; **privacy incidents = 0**; default-deny egress; encrypted at rest & in transit; idle auto-sleep on heavy nodes.

## 1.1 Vision Clarification Table

| # | Theme | Decided Direction | Implications |
| --- | --- | --- | --- |
| 1 | Primary Identity | **Platform-first** substrate for data/automation/AI | Open formats & modular automation outlive individual models/UIs |
| 2 | AI’s Role | **Meta-layer advisor** | AI proposes/assists; deterministic automation executes |
| 3 | System Evolution | **Advisory evolution** | Human approval gates; sandbox proposals; no unsupervised self-modifying behavior |
| 4 | Data Cohesion | **Unified substrate, modular interfaces** | Common data core; per-type plugins |
| 5 | User Scope / Realms | **Single-user privacy hierarchy** | Visibility/encryption scopes; simple sharing later |
| 6 | Extensibility Target | **AI-assisted, human-approved** | Schema evolution is auditable |
| 7 | Knowledge vs Action | **Action-driven foundation** | Deterministic core under flexible reasoning layer |
| 8 | Longevity | **Strict openness** | Human-readable, portable formats |

## 1.2 Living Schema & AI-Assisted Integration
Principles: (1) ingest first, model later; (2) AI proposes structures/relations; (3) schemas/workflows are **data** (JSON/YAML) with versions and diffs; (4) reflective loop with dry-runs; (5) iterative, human-approved evolution.

## 1.3 AI Personas (Contexts & Boundaries)
Roles are logical contexts with scoped permissions/tools. All personas are **local-only** and **realm-aware**.

| Persona | Purpose | Scope | Capabilities | Constraints |
| --- | --- | --- | --- | --- |
| Librarian | Archival, retrieval, curation | Archives, indexes, metadata (R/O except tagging & collections) | Search, summarize, cross-reference | Strict realm caps; provenance for changes |
| System Advisor | Evolve workflows, schema, infra | Schemas, configs, manifests, metrics | Introspection, simulation, proposals | Sandbox; proposals only; human approval to apply |
| Assistant | GTD/tasks/projects, reflective notes | Personal/Household realms | Conversation, planning, scheduling | Undo/redo; non-destructive edits |
| Coding Assistant | Local dev support | Repos, docs, tests | Code gen, refactor, tests, PRs | No direct writes to prod data; PRs + tests required |
