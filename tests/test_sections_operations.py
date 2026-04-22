from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from solidcam_api import SolidCAMClient
from solidcam_api.enums import OperationType
from solidcam_api.exceptions import SolidCAMAPIError
from solidcam_api.models import Operation

# ---------------------------------------------------------------------------
# operation_count property
# ---------------------------------------------------------------------------


def test_operation_count_returns_int_of_com_value(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.OperationCount = 5
    assert connected_client.operation_count == 5


def test_operation_count_returns_zero_when_no_operations(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.OperationCount = 0
    assert connected_client.operation_count == 0


def test_operation_count_is_int_type(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.OperationCount = 3
    assert isinstance(connected_client.operation_count, int)


def test_operation_count_reflects_updated_value(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.OperationCount = 2
    assert connected_client.operation_count == 2
    fake_com.OperationCount = 10
    assert connected_client.operation_count == 10


# ---------------------------------------------------------------------------
# number_of_jobs_with_exclamation_sign property
# ---------------------------------------------------------------------------


def test_number_of_jobs_with_exclamation_sign_reads_com_property(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.NumberOfJobsOpenedWithExclamationSign = 3
    assert connected_client.number_of_jobs_with_exclamation_sign == 3


def test_number_of_jobs_with_exclamation_sign_returns_zero(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.NumberOfJobsOpenedWithExclamationSign = 0
    assert connected_client.number_of_jobs_with_exclamation_sign == 0


def test_number_of_jobs_with_exclamation_sign_is_int_type(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.NumberOfJobsOpenedWithExclamationSign = 1
    assert isinstance(connected_client.number_of_jobs_with_exclamation_sign, int)


def test_number_of_jobs_with_exclamation_sign_large_value(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.NumberOfJobsOpenedWithExclamationSign = 42
    assert connected_client.number_of_jobs_with_exclamation_sign == 42


# ---------------------------------------------------------------------------
# get_operation_name()
# ---------------------------------------------------------------------------


def test_get_operation_name_calls_com_with_index(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.GetOperationName.return_value = "Roughing"
    connected_client.get_operation_name(0)
    fake_com.GetOperationName.assert_called_once_with(0)


def test_get_operation_name_returns_string_from_com(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.GetOperationName.return_value = "Roughing"
    result = connected_client.get_operation_name(0)
    assert result == "Roughing"


def test_get_operation_name_returns_str_type(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.GetOperationName.return_value = "FinishProfile"
    result = connected_client.get_operation_name(0)
    assert isinstance(result, str)


def test_get_operation_name_forwards_nonzero_index(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.GetOperationName.return_value = "Drilling"
    connected_client.get_operation_name(7)
    fake_com.GetOperationName.assert_called_once_with(7)


# ---------------------------------------------------------------------------
# get_operation_type()
# ---------------------------------------------------------------------------


def test_get_operation_type_calls_com_with_index(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.GetOperationType.return_value = 0
    connected_client.get_operation_type(0)
    fake_com.GetOperationType.assert_called_once_with(0)


def test_get_operation_type_returns_int_from_com(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.GetOperationType.return_value = 13
    result = connected_client.get_operation_type(0)
    assert result == 13


def test_get_operation_type_returns_int_type(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.GetOperationType.return_value = 0
    result = connected_client.get_operation_type(0)
    assert isinstance(result, int)


def test_get_operation_type_forwards_nonzero_index(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.GetOperationType.return_value = 1
    connected_client.get_operation_type(4)
    fake_com.GetOperationType.assert_called_once_with(4)


def test_get_operation_type_returns_zero_for_nc_pocket(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.GetOperationType.return_value = 0
    assert connected_client.get_operation_type(0) == int(OperationType.NC_POCKET)


# ---------------------------------------------------------------------------
# get_operation()
# ---------------------------------------------------------------------------


def test_get_operation_returns_operation_instance(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.GetOperationName.return_value = "Roughing"
    fake_com.GetOperationType.return_value = 0
    result = connected_client.get_operation(0)
    assert isinstance(result, Operation)


def test_get_operation_index_matches_requested_index(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.GetOperationName.return_value = "Roughing"
    fake_com.GetOperationType.return_value = 0
    op = connected_client.get_operation(0)
    assert op.index == 0


def test_get_operation_name_field_matches_com_value(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.GetOperationName.return_value = "Roughing"
    fake_com.GetOperationType.return_value = 0
    op = connected_client.get_operation(0)
    assert op.name == "Roughing"


def test_get_operation_type_code_field_matches_com_value(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.GetOperationName.return_value = "Roughing"
    fake_com.GetOperationType.return_value = 0
    op = connected_client.get_operation(0)
    assert op.type_code == 0


def test_get_operation_type_property_resolves_known_code(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.GetOperationName.return_value = "Drill"
    fake_com.GetOperationType.return_value = 13
    op = connected_client.get_operation(0)
    assert op.type is OperationType.NC_DRILL


def test_get_operation_type_property_returns_raw_int_for_unknown_code(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.GetOperationName.return_value = "FutureOp"
    fake_com.GetOperationType.return_value = 9999
    op = connected_client.get_operation(0)
    assert op.type == 9999


def test_get_operation_nonzero_index_is_stored(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.GetOperationName.return_value = "Profile"
    fake_com.GetOperationType.return_value = 1
    op = connected_client.get_operation(3)
    assert op.index == 3


def test_get_operation_calls_get_operation_name_with_index(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.GetOperationName.return_value = "Op"
    fake_com.GetOperationType.return_value = 0
    connected_client.get_operation(2)
    fake_com.GetOperationName.assert_called_once_with(2)


def test_get_operation_calls_get_operation_type_with_index(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.GetOperationName.return_value = "Op"
    fake_com.GetOperationType.return_value = 0
    connected_client.get_operation(2)
    fake_com.GetOperationType.assert_called_once_with(2)


# ---------------------------------------------------------------------------
# list_operations()
# ---------------------------------------------------------------------------


def test_list_operations_returns_list(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.OperationCount = 0
    result = connected_client.list_operations()
    assert isinstance(result, list)


def test_list_operations_length_matches_operation_count(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.OperationCount = 3
    fake_com.GetOperationName.return_value = "Op"
    fake_com.GetOperationType.return_value = 0
    result = connected_client.list_operations()
    assert len(result) == 3


def test_list_operations_returns_empty_list_when_count_is_zero(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.OperationCount = 0
    result = connected_client.list_operations()
    assert result == []


def test_list_operations_all_items_are_operation_instances(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.OperationCount = 4
    fake_com.GetOperationName.return_value = "Op"
    fake_com.GetOperationType.return_value = 0
    result = connected_client.list_operations()
    assert all(isinstance(op, Operation) for op in result)


def test_list_operations_indices_are_sequential(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.OperationCount = 3
    fake_com.GetOperationName.return_value = "Op"
    fake_com.GetOperationType.return_value = 0
    result = connected_client.list_operations()
    assert [op.index for op in result] == [0, 1, 2]


def test_list_operations_single_item(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.OperationCount = 1
    fake_com.GetOperationName.return_value = "SingleOp"
    fake_com.GetOperationType.return_value = 0
    result = connected_client.list_operations()
    assert len(result) == 1
    assert result[0].index == 0
    assert result[0].name == "SingleOp"


# ---------------------------------------------------------------------------
# suppress_operation()
# ---------------------------------------------------------------------------


def test_suppress_operation_calls_com_with_name_and_true(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    connected_client.suppress_operation("Op1", True)
    fake_com.SuppressOperation.assert_called_once_with("Op1", True)


def test_suppress_operation_calls_com_with_name_and_false(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    connected_client.suppress_operation("Op1", False)
    fake_com.SuppressOperation.assert_called_once_with("Op1", False)


def test_suppress_operation_does_not_raise_when_last_error_zero(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.LastError = 0
    connected_client.suppress_operation("Op1", True)  # must not raise


def test_suppress_operation_raises_api_error_when_last_error_nonzero(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.LastError = 11
    fake_com.LastErrorDescription = "operation not found"
    with pytest.raises(SolidCAMAPIError) as exc_info:
        connected_client.suppress_operation("NonExistent", True)
    assert exc_info.value.method == "SuppressOperation"
    assert exc_info.value.code == 11


def test_suppress_operation_error_includes_description(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.LastError = 11
    fake_com.LastErrorDescription = "operation not found"
    with pytest.raises(SolidCAMAPIError) as exc_info:
        connected_client.suppress_operation("NonExistent", True)
    assert exc_info.value.description == "operation not found"


def test_suppress_operation_forwards_operation_name(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    connected_client.suppress_operation("MySpecialOp", True)
    args, _ = fake_com.SuppressOperation.call_args
    assert args[0] == "MySpecialOp"


def test_suppress_operation_forwards_suppress_flag(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    connected_client.suppress_operation("Op1", False)
    args, _ = fake_com.SuppressOperation.call_args
    assert args[1] is False


# ---------------------------------------------------------------------------
# generate_gcode_for_operation()
# ---------------------------------------------------------------------------


def test_generate_gcode_for_operation_calls_com_with_name_and_file(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    connected_client.generate_gcode_for_operation("Op1", "out.nc")
    fake_com.GenerateGCodeForOperation.assert_called_once_with("Op1", "out.nc")


def test_generate_gcode_for_operation_does_not_raise_when_last_error_zero(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.LastError = 0
    connected_client.generate_gcode_for_operation("Op1", "out.nc")  # must not raise


def test_generate_gcode_for_operation_raises_api_error_when_last_error_nonzero(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.LastError = 6
    with pytest.raises(SolidCAMAPIError) as exc_info:
        connected_client.generate_gcode_for_operation("Op1", "out.nc")
    assert exc_info.value.method == "GenerateGCodeForOperation"
    assert exc_info.value.code == 6


def test_generate_gcode_for_operation_error_includes_description(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.LastError = 6
    fake_com.LastErrorDescription = "post-processing failed"
    with pytest.raises(SolidCAMAPIError) as exc_info:
        connected_client.generate_gcode_for_operation("Op1", "out.nc")
    assert exc_info.value.description == "post-processing failed"


def test_generate_gcode_for_operation_forwards_operation_name(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    connected_client.generate_gcode_for_operation("FinishContour", "C:\\output\\finish.nc")
    args, _ = fake_com.GenerateGCodeForOperation.call_args
    assert args[0] == "FinishContour"


def test_generate_gcode_for_operation_forwards_file_name(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    connected_client.generate_gcode_for_operation("Op1", "C:\\output\\op1.nc")
    args, _ = fake_com.GenerateGCodeForOperation.call_args
    assert args[1] == "C:\\output\\op1.nc"
