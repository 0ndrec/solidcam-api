from __future__ import annotations

import pytest

from solidcam_api.exceptions import (
    SolidCAMAPIError,
    SolidCAMConnectionError,
    SolidCAMError,
    SolidCAMNotOpenError,
    SolidCAMNotRunningError,
)

# ---------------------------------------------------------------------------
# SolidCAMError — base class
# ---------------------------------------------------------------------------


def test_solidcam_error_is_subclass_of_exception() -> None:
    assert issubclass(SolidCAMError, Exception)


def test_solidcam_error_can_be_raised_and_caught() -> None:
    with pytest.raises(SolidCAMError):
        raise SolidCAMError("base error")


# ---------------------------------------------------------------------------
# SolidCAMAPIError — message format
# ---------------------------------------------------------------------------


def test_solidcam_api_error_message_format() -> None:
    err = SolidCAMAPIError("Open", 42, "connection refused")
    assert str(err) == "Open failed: connection refused (code 42)"


def test_solidcam_api_error_message_contains_method() -> None:
    err = SolidCAMAPIError("Calculate", 1, "something went wrong")
    assert "Calculate failed" in str(err)


def test_solidcam_api_error_message_contains_code() -> None:
    err = SolidCAMAPIError("Open", 42, "connection refused")
    assert "(code 42)" in str(err)


def test_solidcam_api_error_message_contains_description() -> None:
    err = SolidCAMAPIError("Open", 42, "connection refused")
    assert "connection refused" in str(err)


# ---------------------------------------------------------------------------
# SolidCAMAPIError — stored attributes
# ---------------------------------------------------------------------------


def test_solidcam_api_error_stores_method() -> None:
    err = SolidCAMAPIError("Open", 42, "connection refused")
    assert err.method == "Open"


def test_solidcam_api_error_stores_code() -> None:
    err = SolidCAMAPIError("Open", 42, "connection refused")
    assert err.code == 42


def test_solidcam_api_error_stores_description() -> None:
    err = SolidCAMAPIError("Open", 42, "connection refused")
    assert err.description == "connection refused"


# ---------------------------------------------------------------------------
# SolidCAMAPIError — empty description
# ---------------------------------------------------------------------------


def test_solidcam_api_error_empty_description_stores_empty_string() -> None:
    err = SolidCAMAPIError("Open", 42, "")
    assert err.description == ""


def test_solidcam_api_error_empty_description_still_contains_code() -> None:
    err = SolidCAMAPIError("Open", 42, "")
    assert "(code 42)" in str(err)


def test_solidcam_api_error_empty_description_still_contains_method() -> None:
    err = SolidCAMAPIError("Open", 42, "")
    assert "Open failed" in str(err)


# ---------------------------------------------------------------------------
# SolidCAMAPIError — is a SolidCAMError
# ---------------------------------------------------------------------------


def test_solidcam_api_error_is_subclass_of_solidcam_error() -> None:
    assert issubclass(SolidCAMAPIError, SolidCAMError)


def test_solidcam_api_error_can_be_caught_as_solidcam_error() -> None:
    with pytest.raises(SolidCAMError):
        raise SolidCAMAPIError("Close", 5, "failed")


# ---------------------------------------------------------------------------
# SolidCAMConnectionError
# ---------------------------------------------------------------------------


def test_solidcam_connection_error_is_subclass_of_solidcam_error() -> None:
    assert issubclass(SolidCAMConnectionError, SolidCAMError)


def test_solidcam_connection_error_can_be_raised_and_caught() -> None:
    with pytest.raises(SolidCAMConnectionError):
        raise SolidCAMConnectionError("DLL not registered")


def test_solidcam_connection_error_caught_as_solidcam_error() -> None:
    with pytest.raises(SolidCAMError):
        raise SolidCAMConnectionError("DLL not registered")


# ---------------------------------------------------------------------------
# SolidCAMNotRunningError
# ---------------------------------------------------------------------------


def test_solidcam_not_running_error_is_subclass_of_solidcam_error() -> None:
    assert issubclass(SolidCAMNotRunningError, SolidCAMError)


def test_solidcam_not_running_error_can_be_raised_and_caught() -> None:
    with pytest.raises(SolidCAMNotRunningError):
        raise SolidCAMNotRunningError("SolidCAM is not running")


def test_solidcam_not_running_error_caught_as_solidcam_error() -> None:
    with pytest.raises(SolidCAMError):
        raise SolidCAMNotRunningError("SolidCAM is not running")


# ---------------------------------------------------------------------------
# SolidCAMNotOpenError
# ---------------------------------------------------------------------------


def test_solidcam_not_open_error_is_subclass_of_solidcam_error() -> None:
    assert issubclass(SolidCAMNotOpenError, SolidCAMError)


def test_solidcam_not_open_error_can_be_raised_and_caught() -> None:
    with pytest.raises(SolidCAMNotOpenError):
        raise SolidCAMNotOpenError("No CAM part is open")


def test_solidcam_not_open_error_caught_as_solidcam_error() -> None:
    with pytest.raises(SolidCAMError):
        raise SolidCAMNotOpenError("No CAM part is open")
