import re
import string

import pytest

hypothesis = pytest.importorskip("hypothesis")
given = hypothesis.given
strategies = hypothesis.strategies


METADATA_PATTERN = re.compile(r"^(?:(?:sys|tmp)\.[a-z0-9_.-]+|cap\.[a-z0-9_]+(?:\.[a-z0-9_]+)+|ext\.[a-z0-9_-]+\.[a-z0-9_.-]+)$")


def _valid_sys_keys():
    token = strategies.text(alphabet=string.ascii_lowercase + string.digits + "_.-", min_size=1)
    return strategies.builds(lambda suffix: f"sys.{suffix}", token)


def _valid_cap_keys():
    segment = strategies.text(alphabet=string.ascii_lowercase + string.digits + "_", min_size=1)
    tail = strategies.lists(segment, min_size=1)
    return strategies.builds(lambda head, rest: "cap." + head + "." + ".".join(rest), segment, tail)


def _valid_ext_keys():
    vendor = strategies.text(alphabet=string.ascii_lowercase + string.digits + "-_", min_size=1)
    suffix = strategies.text(alphabet=string.ascii_lowercase + string.digits + "_.-", min_size=1)
    return strategies.builds(lambda vendor_slug, key: f"ext.{vendor_slug}.{key}", vendor, suffix)


@given(strategies.one_of(_valid_sys_keys(), _valid_cap_keys(), _valid_ext_keys()))
def test_metadata_pattern_accepts_valid_keys(key: str) -> None:
    assert METADATA_PATTERN.fullmatch(key)


@given(strategies.text(min_size=1).filter(lambda candidate: not METADATA_PATTERN.fullmatch(candidate)))
def test_metadata_pattern_rejects_invalid_keys(candidate: str) -> None:
    assert not METADATA_PATTERN.fullmatch(candidate)
