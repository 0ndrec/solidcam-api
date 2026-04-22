from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from solidcam_api import SolidCAMClient
from solidcam_api.enums import ToolType
from solidcam_api.exceptions import SolidCAMAPIError
from solidcam_api.models import Tool

# ---------------------------------------------------------------------------
# tool_count property
# ---------------------------------------------------------------------------


def test_tool_count_reads_com_tool_count(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.ToolCount = 5
    assert connected_client.tool_count == 5


def test_tool_count_returns_zero_when_empty(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.ToolCount = 0
    assert connected_client.tool_count == 0


def test_tool_count_is_int_type(connected_client: SolidCAMClient, fake_com: MagicMock) -> None:
    fake_com.ToolCount = 3
    assert isinstance(connected_client.tool_count, int)


def test_tool_count_reflects_updated_com_value(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.ToolCount = 2
    assert connected_client.tool_count == 2
    fake_com.ToolCount = 7
    assert connected_client.tool_count == 7


# ---------------------------------------------------------------------------
# tool_sheet_count property
# ---------------------------------------------------------------------------


def test_tool_sheet_count_reads_com_tool_sheet_count(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.ToolSheetCount = 3
    assert connected_client.tool_sheet_count == 3


def test_tool_sheet_count_returns_zero_when_no_sheets(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.ToolSheetCount = 0
    assert connected_client.tool_sheet_count == 0


def test_tool_sheet_count_is_int_type(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.ToolSheetCount = 2
    assert isinstance(connected_client.tool_sheet_count, int)


def test_tool_sheet_count_reflects_updated_com_value(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.ToolSheetCount = 1
    assert connected_client.tool_sheet_count == 1
    fake_com.ToolSheetCount = 4
    assert connected_client.tool_sheet_count == 4


# ---------------------------------------------------------------------------
# get_tool_name()
# ---------------------------------------------------------------------------


def test_get_tool_name_calls_com_with_index(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.GetToolName.return_value = "Endmill_10mm"
    connected_client.get_tool_name(0)
    fake_com.GetToolName.assert_called_once_with(0)


def test_get_tool_name_returns_string_from_com(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.GetToolName.return_value = "Endmill_10mm"
    result = connected_client.get_tool_name(0)
    assert result == "Endmill_10mm"


def test_get_tool_name_returns_str_type(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.GetToolName.return_value = "Drill_5mm"
    result = connected_client.get_tool_name(0)
    assert isinstance(result, str)


def test_get_tool_name_forwards_nonzero_index(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.GetToolName.return_value = "Ballmill_8mm"
    connected_client.get_tool_name(4)
    fake_com.GetToolName.assert_called_once_with(4)


# ---------------------------------------------------------------------------
# get_tool_type()
# ---------------------------------------------------------------------------


def test_get_tool_type_calls_com_with_index(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.GetToolType.return_value = 1
    connected_client.get_tool_type(0)
    fake_com.GetToolType.assert_called_once_with(0)


def test_get_tool_type_returns_int_from_com(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.GetToolType.return_value = 1
    result = connected_client.get_tool_type(0)
    assert result == 1


def test_get_tool_type_returns_int_type(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.GetToolType.return_value = 2
    result = connected_client.get_tool_type(0)
    assert isinstance(result, int)


def test_get_tool_type_forwards_nonzero_index(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.GetToolType.return_value = 3
    connected_client.get_tool_type(5)
    fake_com.GetToolType.assert_called_once_with(5)


def test_get_tool_type_returns_zero_for_tool_type_none(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.GetToolType.return_value = 0
    assert connected_client.get_tool_type(0) == int(ToolType.NONE)


def test_get_tool_type_returns_milling_code(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.GetToolType.return_value = int(ToolType.MILLING)
    assert connected_client.get_tool_type(0) == 1


# ---------------------------------------------------------------------------
# get_tool_tag()
# ---------------------------------------------------------------------------


def test_get_tool_tag_calls_com_with_number_position_and_defaults(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.GetToolTag.return_value = 42
    connected_client.get_tool_tag(1, 0)
    fake_com.GetToolTag.assert_called_once_with(1, 0, 0, 0)


def test_get_tool_tag_returns_int_tag(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.GetToolTag.return_value = 42
    result = connected_client.get_tool_tag(1, 0)
    assert result == 42


def test_get_tool_tag_returns_int_type(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.GetToolTag.return_value = 99
    result = connected_client.get_tool_tag(1, 0)
    assert isinstance(result, int)


def test_get_tool_tag_calls_com_with_explicit_station_and_turret(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.GetToolTag.return_value = 7
    connected_client.get_tool_tag(2, 1, station=3, turret=1)
    fake_com.GetToolTag.assert_called_once_with(2, 1, 3, 1)


def test_get_tool_tag_does_not_raise_when_last_error_zero(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.GetToolTag.return_value = 5
    fake_com.LastError = 0
    result = connected_client.get_tool_tag(1, 0)
    assert result == 5


def test_get_tool_tag_raises_api_error_when_last_error_nonzero(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.GetToolTag.return_value = 0
    fake_com.LastError = 4
    fake_com.LastErrorDescription = "tool not found"
    with pytest.raises(SolidCAMAPIError) as exc_info:
        connected_client.get_tool_tag(99, 0)
    assert exc_info.value.method == "GetToolTag"
    assert exc_info.value.code == 4


def test_get_tool_tag_error_includes_description(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.GetToolTag.return_value = 0
    fake_com.LastError = 4
    fake_com.LastErrorDescription = "tool not found"
    with pytest.raises(SolidCAMAPIError) as exc_info:
        connected_client.get_tool_tag(99, 0)
    assert exc_info.value.description == "tool not found"


def test_get_tool_tag_forwards_number_correctly(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.GetToolTag.return_value = 10
    connected_client.get_tool_tag(7, 0)
    args, _ = fake_com.GetToolTag.call_args
    assert args[0] == 7


def test_get_tool_tag_forwards_position_correctly(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.GetToolTag.return_value = 10
    connected_client.get_tool_tag(1, 3)
    args, _ = fake_com.GetToolTag.call_args
    assert args[1] == 3


# ---------------------------------------------------------------------------
# get_tool() — composite helper
# ---------------------------------------------------------------------------


def test_get_tool_returns_tool_instance(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.GetToolName.return_value = "Endmill"
    fake_com.GetToolType.return_value = 1
    result = connected_client.get_tool(0)
    assert isinstance(result, Tool)


def test_get_tool_index_matches_requested_index(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.GetToolName.return_value = "Endmill"
    fake_com.GetToolType.return_value = 1
    t = connected_client.get_tool(2)
    assert t.index == 2


def test_get_tool_name_field_matches_com_value(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.GetToolName.return_value = "Ballmill_6mm"
    fake_com.GetToolType.return_value = 1
    t = connected_client.get_tool(0)
    assert t.name == "Ballmill_6mm"


def test_get_tool_type_code_field_matches_com_value(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.GetToolName.return_value = "Insert"
    fake_com.GetToolType.return_value = 2
    t = connected_client.get_tool(0)
    assert t.type_code == 2


def test_get_tool_type_property_resolves_milling(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.GetToolName.return_value = "Endmill"
    fake_com.GetToolType.return_value = int(ToolType.MILLING)
    t = connected_client.get_tool(0)
    assert t.type is ToolType.MILLING


def test_get_tool_type_property_resolves_wire_cut(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.GetToolName.return_value = "Wire"
    fake_com.GetToolType.return_value = int(ToolType.WIRE_CUT)
    t = connected_client.get_tool(0)
    assert t.type is ToolType.WIRE_CUT


# ---------------------------------------------------------------------------
# list_tools() — convenience wrapper
# ---------------------------------------------------------------------------


def test_list_tools_returns_list(connected_client: SolidCAMClient, fake_com: MagicMock) -> None:
    fake_com.ToolCount = 0
    result = connected_client.list_tools()
    assert isinstance(result, list)


def test_list_tools_returns_empty_list_when_count_is_zero(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.ToolCount = 0
    assert connected_client.list_tools() == []


def test_list_tools_length_matches_tool_count(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.ToolCount = 3
    fake_com.GetToolName.return_value = "T"
    fake_com.GetToolType.return_value = 1
    result = connected_client.list_tools()
    assert len(result) == 3


def test_list_tools_all_items_are_tool_instances(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.ToolCount = 2
    fake_com.GetToolName.return_value = "T"
    fake_com.GetToolType.return_value = 1
    result = connected_client.list_tools()
    assert all(isinstance(t, Tool) for t in result)


def test_list_tools_indices_are_sequential(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.ToolCount = 3
    fake_com.GetToolName.return_value = "T"
    fake_com.GetToolType.return_value = 1
    result = connected_client.list_tools()
    assert [t.index for t in result] == [0, 1, 2]


# ---------------------------------------------------------------------------
# set_operation_tool()
# ---------------------------------------------------------------------------


def test_set_operation_tool_calls_com_with_name_and_tag(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    connected_client.set_operation_tool("Op1", 42)
    fake_com.SetOperationTool.assert_called_once_with("Op1", 42)


def test_set_operation_tool_forwards_operation_name(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    connected_client.set_operation_tool("FinishProfile", 7)
    args, _ = fake_com.SetOperationTool.call_args
    assert args[0] == "FinishProfile"


def test_set_operation_tool_forwards_tool_tag(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    connected_client.set_operation_tool("Op1", 99)
    args, _ = fake_com.SetOperationTool.call_args
    assert args[1] == 99


def test_set_operation_tool_does_not_raise_when_last_error_zero(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.LastError = 0
    connected_client.set_operation_tool("Op1", 42)  # must not raise


def test_set_operation_tool_raises_api_error_when_last_error_nonzero(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.LastError = 9
    fake_com.LastErrorDescription = "tool tag invalid"
    with pytest.raises(SolidCAMAPIError) as exc_info:
        connected_client.set_operation_tool("Op1", -1)
    assert exc_info.value.method == "SetOperationTool"
    assert exc_info.value.code == 9


def test_set_operation_tool_error_includes_description(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.LastError = 9
    fake_com.LastErrorDescription = "tool tag invalid"
    with pytest.raises(SolidCAMAPIError) as exc_info:
        connected_client.set_operation_tool("Op1", -1)
    assert exc_info.value.description == "tool tag invalid"


# ---------------------------------------------------------------------------
# get_operation_tool_tag()
# ---------------------------------------------------------------------------


def test_get_operation_tool_tag_calls_com_with_operation_name(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.GetOperationToolTag.return_value = 55
    connected_client.get_operation_tool_tag("Op1")
    fake_com.GetOperationToolTag.assert_called_once_with("Op1")


def test_get_operation_tool_tag_returns_int_tag(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.GetOperationToolTag.return_value = 55
    result = connected_client.get_operation_tool_tag("Op1")
    assert result == 55


def test_get_operation_tool_tag_returns_int_type(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.GetOperationToolTag.return_value = 12
    result = connected_client.get_operation_tool_tag("Op1")
    assert isinstance(result, int)


def test_get_operation_tool_tag_forwards_operation_name(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.GetOperationToolTag.return_value = 1
    connected_client.get_operation_tool_tag("MyFinishOp")
    fake_com.GetOperationToolTag.assert_called_once_with("MyFinishOp")


def test_get_operation_tool_tag_does_not_raise_when_last_error_zero(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.GetOperationToolTag.return_value = 3
    fake_com.LastError = 0
    result = connected_client.get_operation_tool_tag("Op1")
    assert result == 3


def test_get_operation_tool_tag_raises_api_error_when_last_error_nonzero(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.GetOperationToolTag.return_value = 0
    fake_com.LastError = 13
    fake_com.LastErrorDescription = "operation not found"
    with pytest.raises(SolidCAMAPIError) as exc_info:
        connected_client.get_operation_tool_tag("NoSuchOp")
    assert exc_info.value.method == "GetOperationToolTag"
    assert exc_info.value.code == 13


def test_get_operation_tool_tag_error_includes_description(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.GetOperationToolTag.return_value = 0
    fake_com.LastError = 13
    fake_com.LastErrorDescription = "operation not found"
    with pytest.raises(SolidCAMAPIError) as exc_info:
        connected_client.get_operation_tool_tag("NoSuchOp")
    assert exc_info.value.description == "operation not found"


# ---------------------------------------------------------------------------
# get_tool_sheet_name()
# ---------------------------------------------------------------------------


def test_get_tool_sheet_name_calls_com_with_index(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.GetToolSheetName.return_value = "Sheet_Full_HTML"
    connected_client.get_tool_sheet_name(0)
    fake_com.GetToolSheetName.assert_called_once_with(0)


def test_get_tool_sheet_name_returns_string_from_com(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.GetToolSheetName.return_value = "Sheet_Full_HTML"
    result = connected_client.get_tool_sheet_name(0)
    assert result == "Sheet_Full_HTML"


def test_get_tool_sheet_name_returns_str_type(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.GetToolSheetName.return_value = "Sheet_Full_RTF"
    result = connected_client.get_tool_sheet_name(0)
    assert isinstance(result, str)


def test_get_tool_sheet_name_forwards_nonzero_index(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.GetToolSheetName.return_value = "Sheet_Full_RTF"
    connected_client.get_tool_sheet_name(1)
    fake_com.GetToolSheetName.assert_called_once_with(1)


# ---------------------------------------------------------------------------
# list_tool_sheet_names()
# ---------------------------------------------------------------------------


def test_list_tool_sheet_names_returns_list(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.ToolSheetCount = 0
    result = connected_client.list_tool_sheet_names()
    assert isinstance(result, list)


def test_list_tool_sheet_names_returns_empty_list_when_count_is_zero(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.ToolSheetCount = 0
    assert connected_client.list_tool_sheet_names() == []


def test_list_tool_sheet_names_length_matches_tool_sheet_count(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.ToolSheetCount = 2
    fake_com.GetToolSheetName.return_value = "Sheet_Full_HTML"
    result = connected_client.list_tool_sheet_names()
    assert len(result) == 2


def test_list_tool_sheet_names_all_items_are_strings(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.ToolSheetCount = 3
    fake_com.GetToolSheetName.return_value = "Sheet_Full_HTML"
    result = connected_client.list_tool_sheet_names()
    assert all(isinstance(name, str) for name in result)


def test_list_tool_sheet_names_single_item(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.ToolSheetCount = 1
    fake_com.GetToolSheetName.return_value = "Sheet_Full_HTML"
    result = connected_client.list_tool_sheet_names()
    assert len(result) == 1
    assert result[0] == "Sheet_Full_HTML"


def test_list_tool_sheet_names_calls_get_sheet_name_for_each_index(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.ToolSheetCount = 2
    fake_com.GetToolSheetName.return_value = "Sheet_Full_HTML"
    connected_client.list_tool_sheet_names()
    assert fake_com.GetToolSheetName.call_count == 2


# ---------------------------------------------------------------------------
# generate_tool_sheet()
# ---------------------------------------------------------------------------


def test_generate_tool_sheet_calls_com_with_template_name(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    connected_client.generate_tool_sheet("Sheet_Full_HTML")
    fake_com.GenerateToolSheet.assert_called_once_with("Sheet_Full_HTML")


def test_generate_tool_sheet_forwards_template_name(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    connected_client.generate_tool_sheet("Sheet_Full_RTF")
    args, _ = fake_com.GenerateToolSheet.call_args
    assert args[0] == "Sheet_Full_RTF"


def test_generate_tool_sheet_does_not_raise_when_last_error_zero(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.LastError = 0
    connected_client.generate_tool_sheet("Sheet_Full_HTML")  # must not raise


def test_generate_tool_sheet_raises_api_error_when_last_error_nonzero(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.LastError = 15
    fake_com.LastErrorDescription = "template not found"
    with pytest.raises(SolidCAMAPIError) as exc_info:
        connected_client.generate_tool_sheet("Nonexistent_Template")
    assert exc_info.value.method == "GenerateToolSheet"
    assert exc_info.value.code == 15


def test_generate_tool_sheet_error_includes_description(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.LastError = 15
    fake_com.LastErrorDescription = "template not found"
    with pytest.raises(SolidCAMAPIError) as exc_info:
        connected_client.generate_tool_sheet("Nonexistent_Template")
    assert exc_info.value.description == "template not found"


def test_generate_tool_sheet_error_method_name_is_generate_tool_sheet(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.LastError = 1
    with pytest.raises(SolidCAMAPIError) as exc_info:
        connected_client.generate_tool_sheet("Bad_Template")
    assert "GenerateToolSheet" in exc_info.value.method
