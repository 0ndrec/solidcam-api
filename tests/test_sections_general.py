from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from solidcam_api import SolidCAMClient
from solidcam_api.exceptions import SolidCAMAPIError

# ---------------------------------------------------------------------------
# last_error property
# ---------------------------------------------------------------------------


def test_last_error_returns_int_of_com_last_error(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.LastError = 7
    assert connected_client.last_error == 7


def test_last_error_returns_zero_when_no_error(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.LastError = 0
    assert connected_client.last_error == 0


def test_last_error_is_int_type(connected_client: SolidCAMClient, fake_com: MagicMock) -> None:
    fake_com.LastError = 3
    assert isinstance(connected_client.last_error, int)


def test_last_error_reflects_updated_com_value(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.LastError = 0
    assert connected_client.last_error == 0
    fake_com.LastError = 42
    assert connected_client.last_error == 42


# ---------------------------------------------------------------------------
# last_error_description property
# ---------------------------------------------------------------------------


def test_last_error_description_returns_str_of_com_value(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.LastErrorDescription = "part not found"
    assert connected_client.last_error_description == "part not found"


def test_last_error_description_returns_empty_string_by_default(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.LastErrorDescription = ""
    assert connected_client.last_error_description == ""


def test_last_error_description_is_str_type(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.LastErrorDescription = "some error"
    assert isinstance(connected_client.last_error_description, str)


def test_last_error_description_reflects_updated_com_value(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.LastErrorDescription = "first"
    assert connected_client.last_error_description == "first"
    fake_com.LastErrorDescription = "second"
    assert connected_client.last_error_description == "second"


# ---------------------------------------------------------------------------
# log_file property — getter
# ---------------------------------------------------------------------------


def test_log_file_getter_reads_com_log_file(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.LogFile = "/var/log/solidcam.log"
    assert connected_client.log_file == "/var/log/solidcam.log"


def test_log_file_getter_returns_string(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.LogFile = "C:\\solidcam\\automation.log"
    assert isinstance(connected_client.log_file, str)


def test_log_file_getter_returns_empty_string_when_unset(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.LogFile = ""
    assert connected_client.log_file == ""


# ---------------------------------------------------------------------------
# log_file property — setter
# ---------------------------------------------------------------------------


def test_log_file_setter_assigns_to_com_log_file(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    connected_client.log_file = "C:\\logs\\sc.log"
    assert fake_com.LogFile == "C:\\logs\\sc.log"


def test_log_file_setter_overwrites_previous_value(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    connected_client.log_file = "old.log"
    connected_client.log_file = "new.log"
    assert fake_com.LogFile == "new.log"


def test_log_file_round_trip(connected_client: SolidCAMClient, fake_com: MagicMock) -> None:
    connected_client.log_file = "round_trip.log"
    # The setter writes to fake_com.LogFile; the getter reads it back.
    assert connected_client.log_file == "round_trip.log"


# ---------------------------------------------------------------------------
# pid property — getter (now returns int, read-only)
# ---------------------------------------------------------------------------


def test_pid_getter_returns_int(connected_client: SolidCAMClient, fake_com: MagicMock) -> None:
    fake_com.pid = 1234
    assert isinstance(connected_client.pid, int)


def test_pid_getter_returns_correct_value(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.pid = 5678
    assert connected_client.pid == 5678


def test_pid_getter_reflects_float_value(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.pid = 1234.5
    # Float is truncated to int
    assert connected_client.pid == 1234


def test_pid_getter_returns_zero_when_unset(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.pid = 0
    assert connected_client.pid == 0


# ---------------------------------------------------------------------------
# is_solidcam_running()
# ---------------------------------------------------------------------------


def test_is_solidcam_running_returns_true_when_com_returns_true(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.IsSolidCamRunning.return_value = True
    assert connected_client.is_solidcam_running() is True


def test_is_solidcam_running_returns_false_when_com_returns_false(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.IsSolidCamRunning.return_value = False
    assert connected_client.is_solidcam_running() is False


def test_is_solidcam_running_calls_com_method(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.IsSolidCamRunning.return_value = True
    connected_client.is_solidcam_running()
    fake_com.IsSolidCamRunning.assert_called_once_with()


def test_is_solidcam_running_returns_bool_type(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.IsSolidCamRunning.return_value = 1  # truthy int, not bool
    result = connected_client.is_solidcam_running()
    assert isinstance(result, bool)


# ---------------------------------------------------------------------------
# start_application()
# ---------------------------------------------------------------------------


def test_start_application_calls_com_with_path_and_default_wait(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.StartApplication.return_value = 1
    connected_client.start_application("C:\\SolidWorks\\SLDWORKS.exe")
    fake_com.StartApplication.assert_called_once_with("C:\\SolidWorks\\SLDWORKS.exe", 0)


def test_start_application_calls_com_with_custom_wait(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.StartApplication.return_value = 1
    connected_client.start_application("C:\\app.exe", wait_for_plugin=5000)
    fake_com.StartApplication.assert_called_once_with("C:\\app.exe", 5000)


def test_start_application_raises_api_error_on_falsy_return(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.StartApplication.return_value = 0
    with pytest.raises(SolidCAMAPIError):
        connected_client.start_application("C:\\app.exe")


def test_start_application_raises_api_error_on_none_return(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.StartApplication.return_value = None
    with pytest.raises(SolidCAMAPIError):
        connected_client.start_application("C:\\app.exe")


def test_start_application_does_not_raise_on_truthy_return(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.StartApplication.return_value = 1
    # Should complete without raising.
    connected_client.start_application("C:\\app.exe")


def test_start_application_error_includes_method_name(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.StartApplication.return_value = 0
    with pytest.raises(SolidCAMAPIError) as exc_info:
        connected_client.start_application("C:\\app.exe")
    assert exc_info.value.method == "StartApplication"


# ---------------------------------------------------------------------------
# start_solidcam()
# ---------------------------------------------------------------------------


def test_start_solidcam_calls_com_method(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.StartSolidCAM.return_value = 1
    connected_client.start_solidcam()
    fake_com.StartSolidCAM.assert_called_once_with()


def test_start_solidcam_raises_api_error_on_falsy_return(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.StartSolidCAM.return_value = 0
    with pytest.raises(SolidCAMAPIError):
        connected_client.start_solidcam()


def test_start_solidcam_does_not_raise_on_truthy_return(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.StartSolidCAM.return_value = 1
    connected_client.start_solidcam()


def test_start_solidcam_error_includes_method_name(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.StartSolidCAM.return_value = 0
    with pytest.raises(SolidCAMAPIError) as exc_info:
        connected_client.start_solidcam()
    assert exc_info.value.method == "StartSolidCAM"
