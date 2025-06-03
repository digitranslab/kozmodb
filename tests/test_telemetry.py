import os
from unittest.mock import patch

import pytest

KOZMODB_TELEMETRY = os.environ.get("KOZMODB_TELEMETRY", "True")

if isinstance(KOZMODB_TELEMETRY, str):
    KOZMODB_TELEMETRY = KOZMODB_TELEMETRY.lower() in ("true", "1", "yes")


def use_telemetry():
    if os.getenv("KOZMODB_TELEMETRY", "true").lower() == "true":
        return True
    return False


@pytest.fixture(autouse=True)
def reset_env():
    with patch.dict(os.environ, {}, clear=True):
        yield


def test_telemetry_enabled():
    with patch.dict(os.environ, {"KOZMODB_TELEMETRY": "true"}):
        assert use_telemetry() is True


def test_telemetry_disabled():
    with patch.dict(os.environ, {"KOZMODB_TELEMETRY": "false"}):
        assert use_telemetry() is False


def test_telemetry_default_enabled():
    assert use_telemetry() is True
