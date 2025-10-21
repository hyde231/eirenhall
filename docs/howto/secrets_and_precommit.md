# Secrets & pre-commit hygiene

This guide documents how secrets flow through the local deployment and how to
use the new pre-commit checks to prevent accidental leaks.

## Secrets flow

- Environment variables live in `.env` files stored outside the repository and
  injected via shell scripts or the process supervisor. Never commit `.env`
  files; add entries to `.gitignore` when introducing new ones.
- Long-lived secrets (API keys, vault tokens) are stored in the password manager
  and mounted at runtime using `age`-encrypted files or the home server’s
  secrets store (see ADR-000 for storage placement).
- Automation containers receive capability-scoped tokens. Tokens are issued via
  the governance layer and grant the minimum privileges required for the target
  persona/action.
- Backups encrypt manifests and attachments using Restic repository keys stored
  offline. Rotation procedures document how to update keys without downtime.

## Pre-commit checks

The repository ships with `.pre-commit-config.yaml` and a detect-secrets
baseline. Enable hooks once per clone:

```bash
pip install -r requirements-dev.txt
pre-commit install
```

Run checks manually before opening a pull request:

```bash
pre-commit run --all-files
```

The detect-secrets hook fails when new secrets are detected. If a false positive
occurs, update `.secrets.baseline` using:

```bash
detect-secrets scan --baseline .secrets.baseline
```

Review the diff carefully to confirm no real secrets are being suppressed.
