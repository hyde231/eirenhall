"""Lightweight observability helpers for structured logging and tracing."""
from __future__ import annotations

import json
import logging
import time
import uuid
from contextlib import contextmanager
from typing import Any, Dict, Iterator

_LOGGER = logging.getLogger("kernel")


def emit_event(event: str, **payload: Any) -> Dict[str, Any]:
    """Emit a structured log event.

    Parameters
    ----------
    event:
        Event name, e.g. ``"derived.metric"``.
    payload:
        Arbitrary serialisable keyword arguments.

    Returns
    -------
    dict
        The record that was emitted. This makes it easy to re-use in tests or
        downstream processing.
    """

    record: Dict[str, Any] = {"event": event, **payload}
    try:
        message = json.dumps(record, sort_keys=True)
    except TypeError:
        # Fall back to repr for objects that are not JSON serialisable yet.
        serialisable = {key: repr(value) for key, value in record.items()}
        message = json.dumps(serialisable, sort_keys=True)
    _LOGGER.info(message)
    return record


@contextmanager
def trace_span(name: str, **attributes: Any) -> Iterator[str]:
    """Context manager emitting start/end events with duration metadata."""

    span_id = attributes.pop("span_id", str(uuid.uuid4()))
    start_time = time.monotonic()
    emit_event("trace.start", span=name, span_id=span_id, attributes=attributes)
    try:
        yield span_id
    finally:
        duration_ms = (time.monotonic() - start_time) * 1000.0
        emit_event(
            "trace.end",
            span=name,
            span_id=span_id,
            duration_ms=round(duration_ms, 3),
            attributes=attributes,
        )
