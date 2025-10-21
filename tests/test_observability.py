import logging

from kernel.observability import emit_event, trace_span


def test_emit_event_records_json(caplog):
    caplog.set_level(logging.INFO, logger="kernel")
    record = emit_event("test.event", foo="bar", answer=42)
    assert record["event"] == "test.event"
    assert record["foo"] == "bar"
    assert record["answer"] == 42
    logged = "\n".join(message for _, _, message in caplog.record_tuples if "test.event" in message)
    assert '"foo": "bar"' in logged


def test_trace_span_emits_start_and_end(caplog):
    caplog.set_level(logging.INFO, logger="kernel")
    with trace_span("unit-test", label="demo") as span_id:
        assert span_id
    messages = [message for _, _, message in caplog.record_tuples]
    assert any('"event": "trace.start"' in message for message in messages)
    assert any('"event": "trace.end"' in message for message in messages)
