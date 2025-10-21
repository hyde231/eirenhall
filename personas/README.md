# Persona manifests

Persona manifests codify governance rules for automation agents that operate
within Kki. Each manifest is a YAML document (JSON-compatible for ease of
parsing) that records the persona’s intent, data access, and required human
checkpoints.

## File layout

```
personas/
  librarian.yaml
  system_advisor.yaml
  assistant.yaml
  coding_assistant.yaml
```

## Schema

| Field | Description |
| --- | --- |
| `id` | Stable identifier (`persona.<slug>`). |
| `name` | Human-friendly label. |
| `summary` | Short description of the persona’s role. |
| `intended_outcomes` | List of expected outputs or goals. |
| `inputs` | Data sources the persona consumes. |
| `outputs` | Artifacts the persona produces. |
| `data_access` | Realms, sensitivity bands, item types, and capability scopes the persona can read. |
| `write_permissions` | Actions the persona may perform, indicating whether human approval or dry-run mode is required. |
| `escalation` | Conditions that force human involvement. |
| `safety_rails` | Non-negotiable prohibitions. |
| `dry_run_default` | Whether automation must stay in dry-run unless escalated. |

See ADR-001 for the governance policy behind these manifests and
`tests/governance/test_persona_manifests.py` for validation logic.
