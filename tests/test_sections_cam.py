from __future__ import annotations

from unittest.mock import MagicMock, call

import pytest

from solidcam_api import SolidCAMClient
from solidcam_api.exceptions import SolidCAMAPIError

# ---------------------------------------------------------------------------
# open()
# ---------------------------------------------------------------------------


def test_open_calls_com_open_with_part_path_and_default_model_path(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.Open.return_value = 1
    connected_client.open("part.sldprt")
    fake_com.Open.assert_called_once_with("part.sldprt", "")


def test_open_calls_com_open_with_explicit_model_path(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.Open.return_value = 1
    connected_client.open("part.sldprt", "model.sldprt")
    fake_com.Open.assert_called_once_with("part.sldprt", "model.sldprt")


def test_open_empty_model_path_is_forwarded_to_com(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.Open.return_value = 1
    connected_client.open("part.sldprt", "")
    fake_com.Open.assert_called_once_with("part.sldprt", "")


def test_open_raises_api_error_when_com_returns_zero(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.Open.return_value = 0
    with pytest.raises(SolidCAMAPIError):
        connected_client.open("part.sldprt")


def test_open_raises_api_error_when_com_returns_none(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.Open.return_value = None
    with pytest.raises(SolidCAMAPIError):
        connected_client.open("part.sldprt")


def test_open_raises_api_error_when_com_returns_false(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.Open.return_value = False
    with pytest.raises(SolidCAMAPIError):
        connected_client.open("part.sldprt")


def test_open_error_includes_method_name(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.Open.return_value = 0
    with pytest.raises(SolidCAMAPIError) as exc_info:
        connected_client.open("part.sldprt")
    assert exc_info.value.method == "Open"


def test_open_does_not_raise_when_com_returns_truthy(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.Open.return_value = 1
    connected_client.open("part.sldprt")  # must not raise


def test_open_error_code_comes_from_last_error(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.Open.return_value = 0
    fake_com.LastError = 99
    fake_com.LastErrorDescription = "file not found"
    with pytest.raises(SolidCAMAPIError) as exc_info:
        connected_client.open("part.sldprt")
    assert exc_info.value.code == 99
    assert exc_info.value.description == "file not found"


# ---------------------------------------------------------------------------
# synchronize()
# ---------------------------------------------------------------------------


def test_synchronize_calls_com_synchronize(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    connected_client.synchronize()
    fake_com.Synchronize.assert_called_once_with()


def test_synchronize_checks_last_error_after_call(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    # With LastError = 0 (conftest default), no exception should be raised.
    connected_client.synchronize()
    fake_com.Synchronize.assert_called_once()


def test_synchronize_raises_api_error_when_last_error_nonzero(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.LastError = 5
    fake_com.LastErrorDescription = "sync failed"
    with pytest.raises(SolidCAMAPIError) as exc_info:
        connected_client.synchronize()
    assert exc_info.value.method == "Synchronize"
    assert exc_info.value.code == 5


def test_synchronize_does_not_raise_when_last_error_zero(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.LastError = 0
    connected_client.synchronize()  # must not raise


# ---------------------------------------------------------------------------
# calculate()
# ---------------------------------------------------------------------------


def test_calculate_calls_com_calculate_with_false_by_default(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    connected_client.calculate()
    fake_com.Calculate.assert_called_once_with(False)


def test_calculate_calls_com_calculate_with_true_when_flag_set(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    connected_client.calculate(only_not_calculated=True)
    fake_com.Calculate.assert_called_once_with(True)


def test_calculate_does_not_raise_when_last_error_zero(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.LastError = 0
    connected_client.calculate()  # must not raise


def test_calculate_raises_api_error_when_last_error_nonzero(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.LastError = 3
    with pytest.raises(SolidCAMAPIError) as exc_info:
        connected_client.calculate()
    assert exc_info.value.method == "Calculate"


def test_calculate_only_not_calculated_false_also_calls_with_false(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    connected_client.calculate(only_not_calculated=False)
    fake_com.Calculate.assert_called_once_with(False)


# ---------------------------------------------------------------------------
# generate_gcode()
# ---------------------------------------------------------------------------


def test_generate_gcode_calls_com_generate_g_code(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    connected_client.generate_gcode()
    fake_com.GenerateGCode.assert_called_once_with()


def test_generate_gcode_does_not_raise_when_last_error_zero(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.LastError = 0
    connected_client.generate_gcode()  # must not raise


def test_generate_gcode_raises_api_error_when_last_error_nonzero(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.LastError = 7
    with pytest.raises(SolidCAMAPIError) as exc_info:
        connected_client.generate_gcode()
    assert exc_info.value.method == "GenerateGCode"


# ---------------------------------------------------------------------------
# save()
# ---------------------------------------------------------------------------


def test_save_calls_com_save_with_folder(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.Save.return_value = r"C:\out\part.cmp"
    connected_client.save(r"C:\out")
    fake_com.Save.assert_called_once_with(r"C:\out")


def test_save_returns_string_result_from_com(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.Save.return_value = r"C:\out\part.cmp"
    result = connected_client.save(r"C:\out")
    assert result == r"C:\out\part.cmp"


def test_save_returns_str_type(connected_client: SolidCAMClient, fake_com: MagicMock) -> None:
    fake_com.Save.return_value = r"C:\out\part.cmp"
    result = connected_client.save(r"C:\out")
    assert isinstance(result, str)


def test_save_raises_api_error_when_com_returns_falsy(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.Save.return_value = 0
    with pytest.raises(SolidCAMAPIError):
        connected_client.save(r"C:\out")


def test_save_raises_api_error_when_com_returns_none(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.Save.return_value = None
    with pytest.raises(SolidCAMAPIError):
        connected_client.save(r"C:\out")


def test_save_error_includes_method_name(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.Save.return_value = 0
    with pytest.raises(SolidCAMAPIError) as exc_info:
        connected_client.save(r"C:\out")
    assert exc_info.value.method == "Save"


def test_save_does_not_raise_when_com_returns_truthy_path(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.Save.return_value = r"C:\result\part.cmp"
    connected_client.save(r"C:\result")  # must not raise


# ---------------------------------------------------------------------------
# close()
# ---------------------------------------------------------------------------


def test_close_calls_com_close(connected_client: SolidCAMClient, fake_com: MagicMock) -> None:
    connected_client.close()
    fake_com.Close.assert_called_once_with()


def test_close_does_not_raise_when_last_error_zero(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.LastError = 0
    connected_client.close()  # must not raise


def test_close_raises_api_error_when_last_error_nonzero(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.LastError = 2
    with pytest.raises(SolidCAMAPIError) as exc_info:
        connected_client.close()
    assert exc_info.value.method == "Close"
    assert exc_info.value.code == 2


def test_close_raises_api_error_with_description(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.LastError = 2
    fake_com.LastErrorDescription = "cannot close"
    with pytest.raises(SolidCAMAPIError) as exc_info:
        connected_client.close()
    assert exc_info.value.description == "cannot close"


# ---------------------------------------------------------------------------
# exit()
# ---------------------------------------------------------------------------


def test_exit_calls_com_exit(connected_client: SolidCAMClient, fake_com: MagicMock) -> None:
    connected_client.exit()
    fake_com.Exit.assert_called_once_with()


def test_exit_does_not_raise_when_last_error_zero(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.LastError = 0
    connected_client.exit()  # must not raise


def test_exit_raises_api_error_when_last_error_nonzero(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.LastError = 8
    with pytest.raises(SolidCAMAPIError) as exc_info:
        connected_client.exit()
    assert exc_info.value.method == "Exit"
    assert exc_info.value.code == 8


def test_exit_error_includes_description(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.LastError = 8
    fake_com.LastErrorDescription = "exit blocked"
    with pytest.raises(SolidCAMAPIError) as exc_info:
        connected_client.exit()
    assert exc_info.value.description == "exit blocked"
