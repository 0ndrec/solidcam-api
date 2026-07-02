from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock

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
    connected_client.open("part.prz")
    fake_com.Open.assert_called_once_with("part.prz", "")


def test_open_calls_com_open_with_explicit_model_path(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.Open.return_value = 1
    connected_client.open("part.prz", "model.sldprt")
    fake_com.Open.assert_called_once_with("part.prz", "model.sldprt")


def test_open_empty_model_path_is_forwarded_to_com(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.Open.return_value = 1
    connected_client.open("part.prz", "")
    fake_com.Open.assert_called_once_with("part.prz", "")


def test_open_raises_api_error_when_com_returns_zero(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.Open.return_value = 0
    with pytest.raises(SolidCAMAPIError):
        connected_client.open("part.prz")


def test_open_raises_api_error_when_com_returns_none(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.Open.return_value = None
    with pytest.raises(SolidCAMAPIError):
        connected_client.open("part.prz")


def test_open_raises_api_error_when_com_returns_false(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.Open.return_value = False
    with pytest.raises(SolidCAMAPIError):
        connected_client.open("part.prz")


def test_open_error_includes_method_name(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.Open.return_value = 0
    with pytest.raises(SolidCAMAPIError) as exc_info:
        connected_client.open("part.prz")
    assert exc_info.value.method == "Open"


def test_open_does_not_raise_when_com_returns_truthy(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.Open.return_value = 1
    connected_client.open("part.prz")  # must not raise


def test_open_error_code_comes_from_last_error(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.Open.return_value = 0
    fake_com.LastError = 99
    fake_com.LastErrorDescription = "file not found"
    with pytest.raises(SolidCAMAPIError) as exc_info:
        connected_client.open("part.prz")
    assert exc_info.value.code == 99
    assert exc_info.value.description == "file not found"


# ---------------------------------------------------------------------------
# check_synchronization()
# ---------------------------------------------------------------------------


def test_check_synchronization_calls_com(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    connected_client.check_synchronization()
    fake_com.CheckSynchronization.assert_called_once_with()


def test_check_synchronization_raises_on_error(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.LastError = 1
    fake_com.LastErrorDescription = "not synced"
    with pytest.raises(SolidCAMAPIError) as exc_info:
        connected_client.check_synchronization()
    assert exc_info.value.method == "CheckSynchronization"


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
# calculate_operations()
# ---------------------------------------------------------------------------


def test_calculate_operations_calls_com(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    connected_client.calculate_operations(["op1", "op2"])
    fake_com.CalculateOperations.assert_called_once_with(["op1", "op2"], False)


def test_calculate_operations_with_flag(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    connected_client.calculate_operations(["op1"], only_not_calculated=True)
    fake_com.CalculateOperations.assert_called_once_with(["op1"], True)


# ---------------------------------------------------------------------------
# calculate_single_operation()
# ---------------------------------------------------------------------------


def test_calculate_single_operation_calls_com(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    connected_client.calculate_single_operation(5)
    fake_com.CalculateSingleOperation.assert_called_once_with(5)


def test_calculate_single_operation_raises_on_error(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.LastError = 1
    with pytest.raises(SolidCAMAPIError):
        connected_client.calculate_single_operation(5)


# ---------------------------------------------------------------------------
# change_post_processor_directory()
# ---------------------------------------------------------------------------


def test_change_post_processor_directory_calls_com(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    connected_client.change_post_processor_directory(r"C:\posts")
    fake_com.ChangePostProcessorDirectory.assert_called_once()


def test_change_post_processor_directory_raises_on_error(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.LastError = 1
    with pytest.raises(SolidCAMAPIError):
        connected_client.change_post_processor_directory(r"C:\posts")


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
    fake_com.Save.return_value = r"C:\out\part.prz"
    connected_client.save(r"C:\out")
    fake_com.Save.assert_called_once_with(r"C:\out")


def test_save_returns_path_result_from_com(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.Save.return_value = r"C:\out\part.prz"
    result = connected_client.save(r"C:\out")
    assert result == Path(r"C:\out\part.prz")


def test_save_returns_path_type(connected_client: SolidCAMClient, fake_com: MagicMock) -> None:
    fake_com.Save.return_value = r"C:\out\part.prz"
    result = connected_client.save(r"C:\out")
    assert isinstance(result, Path)


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
    fake_com.Save.return_value = r"C:\result\part.prz"
    connected_client.save(r"C:\result")  # must not raise


# ---------------------------------------------------------------------------
# save_as()
# ---------------------------------------------------------------------------


def test_save_as_calls_com(connected_client: SolidCAMClient, fake_com: MagicMock) -> None:
    fake_com.SaveAs.return_value = 1
    connected_client.save_as(r"C:\out\part.prz")
    fake_com.SaveAs.assert_called_once()


def test_save_as_raises_on_error(connected_client: SolidCAMClient, fake_com: MagicMock) -> None:
    fake_com.SaveAs.return_value = 0
    with pytest.raises(SolidCAMAPIError):
        connected_client.save_as(r"C:\out\part.prz")


# ---------------------------------------------------------------------------
# save_to_folder()
# ---------------------------------------------------------------------------


def test_save_to_folder_calls_com(connected_client: SolidCAMClient, fake_com: MagicMock) -> None:
    fake_com.SaveToFolder.return_value = r"C:\out\part.prz"
    result = connected_client.save_to_folder(r"C:\out")
    assert isinstance(result, Path)


def test_save_to_folder_raises_on_error(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.SaveToFolder.return_value = 0
    with pytest.raises(SolidCAMAPIError):
        connected_client.save_to_folder(r"C:\out")


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


# ---------------------------------------------------------------------------
# open_part() context manager
# ---------------------------------------------------------------------------


def test_open_part_opens_and_closes_on_success(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.Open.return_value = 1
    fake_com.LastError = 0
    with connected_client.open_part("part.prz"):
        pass
    fake_com.Open.assert_called_once()
    fake_com.Close.assert_called_once()


def test_open_part_closes_on_exception(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.Open.return_value = 1
    fake_com.LastError = 0
    with pytest.raises(ValueError):
        with connected_client.open_part("part.prz"):
            raise ValueError("test error")
    fake_com.Close.assert_called_once()


def test_open_part_with_model_path(connected_client: SolidCAMClient, fake_com: MagicMock) -> None:
    fake_com.Open.return_value = 1
    fake_com.LastError = 0
    with connected_client.open_part("part.prz", "model.sldprt"):
        pass
    fake_com.Open.assert_called_once_with("part.prz", "model.sldprt")
