from __future__ import annotations

import json
from pathlib import Path

import pytest

from kernel.derived import DerivedEvaluator

FIXTURES = Path(__file__).resolve().parent.parent / "fixtures" / "items"
SCHEMA_ROOT = Path(__file__).resolve().parents[2] / "schema" / "derived"


def load_item(name: str) -> dict:
    path = FIXTURES / f"{name}.json"
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def test_definitions_are_loaded():
    evaluator = DerivedEvaluator(schema_root=SCHEMA_ROOT)
    assert set(evaluator.list_types()) == {"document", "task", "wiki_entry"}


def test_task_metrics_and_provenance():
    evaluator = DerivedEvaluator(schema_root=SCHEMA_ROOT)
    item = load_item("task")
    result = evaluator.evaluate_item(item)

    assert result.values["checklist_total"] == 2
    assert result.values["checklist_completed"] == 1
    assert result.values["completion_ratio"] == 0.5

    assert result.provenance["checklist_total"] == ("path:fields.checklist",)
    assert result.provenance["checklist_completed"] == ("path:fields.checklist",)
    assert result.provenance["completion_ratio"] == (
        "metric:checklist_completed",
        "metric:checklist_total",
    )


def test_document_metrics_handle_delta_body():
    evaluator = DerivedEvaluator(schema_root=SCHEMA_ROOT)
    item = load_item("document")
    result = evaluator.evaluate_item(item)

    assert result.values["word_count"] == 6
    assert result.values["reading_time_minutes"] == 0.03
    assert result.values["has_summary"] is False


def test_wiki_entry_metrics_detect_links():
    evaluator = DerivedEvaluator(schema_root=SCHEMA_ROOT)
    item = load_item("wiki_entry")
    result = evaluator.evaluate_item(item)

    assert result.values["link_count"] == 2
    assert result.values["reference_links"] == 2
    assert result.values["has_body"] is True


def test_unknown_item_type():
    evaluator = DerivedEvaluator(schema_root=SCHEMA_ROOT)
    with pytest.raises(KeyError):
        evaluator.evaluate_item({"item_type": "nonexistent"})
