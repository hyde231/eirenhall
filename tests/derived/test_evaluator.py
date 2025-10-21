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
    assert set(evaluator.list_types()) == {
        "document",
        "task",
        "wiki_entry",
        "project",
        "correspondence",
        "conversation_thread",
        "person",
        "organization",
    }


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


def test_project_metrics():
    evaluator = DerivedEvaluator(schema_root=SCHEMA_ROOT)
    item = load_item("project")
    result = evaluator.evaluate_item(item)

    assert result.values["related_item_count"] == 1
    assert result.values["tag_count"] == 2
    assert result.values["has_notes"] is True
    assert result.values["has_summary"] is True
    assert result.values["has_progress"] is True

    assert result.provenance["related_item_count"] == ("path:fields.related_items",)
    assert result.provenance["has_progress"] == ("path:fields.summary.progress",)


def test_correspondence_metrics():
    evaluator = DerivedEvaluator(schema_root=SCHEMA_ROOT)
    item = load_item("correspondence")
    result = evaluator.evaluate_item(item)

    assert result.values["participant_count"] == 2
    assert result.values["tag_count"] == 2
    assert result.values["has_subject"] is True
    assert result.values["has_retention_policy"] is True
    assert result.values["has_attachments"] is True

    assert result.provenance["participant_count"] == ("path:fields.participants",)
    assert result.provenance["has_retention_policy"] == (
        "path:metadata.cap.correspondence.archive.retention",
    )


def test_conversation_thread_metrics():
    evaluator = DerivedEvaluator(schema_root=SCHEMA_ROOT)
    item = load_item("conversation_thread")
    result = evaluator.evaluate_item(item)

    assert result.values["message_count"] == 2
    assert result.values["external_message_count"] == 1
    assert result.values["has_summary"] is False
    assert result.values["has_last_synced"] is True

    assert result.provenance["message_count"] == ("path:fields.timeline.messages",)
    assert result.provenance["external_message_count"] == ("path:fields.timeline.messages",)


def test_person_metrics():
    evaluator = DerivedEvaluator(schema_root=SCHEMA_ROOT)
    item = load_item("person")
    result = evaluator.evaluate_item(item)

    assert result.values["contact_method_count"] == 2
    assert result.values["affiliation_count"] == 1
    assert result.values["linked_item_count"] == 1
    assert result.values["has_review_cadence"] is True
    assert result.values["has_last_contact"] is True

    assert result.provenance["contact_method_count"] == ("path:fields.contact_methods",)
    assert result.provenance["has_last_contact"] == (
        "path:metadata.cap.directory.profile.last_contact_at",
    )


def test_organization_metrics():
    evaluator = DerivedEvaluator(schema_root=SCHEMA_ROOT)
    item = load_item("organization")
    result = evaluator.evaluate_item(item)

    assert result.values["contact_method_count"] == 1
    assert result.values["site_count"] == 1
    assert result.values["linked_item_count"] == 2
    assert result.values["has_review_cadence"] is True
    assert result.values["has_last_contact"] is True

    assert result.provenance["site_count"] == ("path:fields.profile.sites",)
    assert result.provenance["linked_item_count"] == ("path:fields.related_items",)
