# Running the Derived Metrics Proof of Concept

The repository ships with a small proof-of-concept (PoC) command line tool
located at `scripts/run_poc.py`. The script demonstrates how to:

1. load the kernel type registry from `schema/types`,
2. read the sample items under `tests/fixtures/items`,
3. validate the payloads against `schema/item_base.json`, and
4. evaluate the derived metric definitions stored in `schema/derived`.

The output is a concise report enumerating the metrics computed for every
sample item.

## Prerequisites

The CLI requires Python 3.8 or newer. Optional dependencies are detected
at runtime:

- If `PyYAML` is installed the evaluator can parse the derived definitions as
  YAML. Otherwise the files are parsed using a JSON subset parser.
- If `jsonschema` is available the PoC validates the sample items against the
  full JSON Schema definition. Without it a lightweight structural validator
  checks for the required fields and type registration.

All commands shown below are expected to be executed from the repository root.

## Usage

```bash
python scripts/run_poc.py
```

By default the script loads the sample payloads that ship with the repository
and prints a report similar to:

```
Summary Report
============================================================
Type: document (schema: item_base.json) -> 1 item(s)
Type: task (schema: item_base.json) -> 1 item(s)
Type: wiki (schema: item_base.json) -> 1 item(s)

Item doc_123456 [document]
  - word_count: 6
  - reading_time_minutes: 0.03
  - has_summary: False

Item task_456789 [task]
  - checklist_total: 2
  - checklist_completed: 1
  - completion_ratio: 0.5

Item wiki_987654 [wiki]
  - link_count: 2
  - reference_links: 2
  - has_body: True
```

## Customising the inputs

Two optional flags let you point the script at alternative directories:

- `--items-dir PATH` – load JSON payloads from a different folder.
- `--derived-root PATH` – read derived metric definitions from another
  directory. This is useful when experimenting with new metrics alongside the
  bundled examples.

Both flags accept relative or absolute paths. The script continues to run the
validation step before invoking the evaluator to help catch schema regressions
early in a development workflow.
