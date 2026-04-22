from __future__ import annotations

from solidcam_api.enums import (
    HomeOriginPosition,
    NewPartType,
    OperationType,
    PartType,
    StockDefineBy,
    TargetDefineBy,
    ToolType,
    WireCutOperationType,
    try_parse_operation_type,
)

# ---------------------------------------------------------------------------
# PartType
# ---------------------------------------------------------------------------


def test_part_type_milling_value() -> None:
    assert PartType.MILLING == 1


def test_part_type_turning_value() -> None:
    assert PartType.TURNING == 2


def test_part_type_turn_mill_value() -> None:
    assert PartType.TURN_MILL == 3


def test_part_type_wire_cut_value() -> None:
    assert PartType.WIRE_CUT == 4


def test_part_type_not_cam_part_value() -> None:
    assert PartType.NOT_CAM_PART == 0


def test_part_type_no_open_documents_value() -> None:
    assert PartType.NO_OPEN_DOCUMENTS == -1


def test_part_type_solidcam_not_running_value() -> None:
    assert PartType.SOLIDCAM_NOT_RUNNING == -2


def test_part_type_is_int_comparable() -> None:
    assert PartType.MILLING == 1
    assert int(PartType.MILLING) == 1


# ---------------------------------------------------------------------------
# NewPartType
# ---------------------------------------------------------------------------


def test_new_part_type_milling_value() -> None:
    assert NewPartType.MILLING == 0


def test_new_part_type_turning_value() -> None:
    assert NewPartType.TURNING == 1


def test_new_part_type_wire_cut_value() -> None:
    assert NewPartType.WIRE_CUT == 2


def test_new_part_type_mill_turn_value() -> None:
    assert NewPartType.MILL_TURN == 3


def test_new_part_type_mill_turn_full_value() -> None:
    assert NewPartType.MILL_TURN_FULL == 4


# ---------------------------------------------------------------------------
# HomeOriginPosition
# ---------------------------------------------------------------------------


def test_home_origin_position_top_corner_value() -> None:
    assert HomeOriginPosition.TOP_CORNER == 0


def test_home_origin_position_top_center_value() -> None:
    assert HomeOriginPosition.TOP_CENTER == 1


def test_home_origin_position_cad_origin_value() -> None:
    assert HomeOriginPosition.CAD_ORIGIN == 2


# ---------------------------------------------------------------------------
# StockDefineBy
# ---------------------------------------------------------------------------


def test_stock_define_by_solid_value() -> None:
    assert StockDefineBy.SOLID == 0


def test_stock_define_by_surface_value() -> None:
    assert StockDefineBy.SURFACE == 1


def test_stock_define_by_all_value() -> None:
    assert StockDefineBy.ALL == 2


# ---------------------------------------------------------------------------
# TargetDefineBy
# ---------------------------------------------------------------------------


def test_target_define_by_solid_value() -> None:
    assert TargetDefineBy.SOLID == 0


def test_target_define_by_surface_value() -> None:
    assert TargetDefineBy.SURFACE == 1


def test_target_define_by_all_value() -> None:
    assert TargetDefineBy.ALL == 2


# ---------------------------------------------------------------------------
# ToolType
# ---------------------------------------------------------------------------


def test_tool_type_none_value() -> None:
    assert ToolType.NONE == 0


def test_tool_type_milling_value() -> None:
    assert ToolType.MILLING == 1


def test_tool_type_turning_value() -> None:
    assert ToolType.TURNING == 2


def test_tool_type_wire_cut_value() -> None:
    assert ToolType.WIRE_CUT == 3


def test_tool_type_is_int_comparable() -> None:
    assert int(ToolType.WIRE_CUT) == 3


# ---------------------------------------------------------------------------
# OperationType — spot-check key values
# ---------------------------------------------------------------------------


def test_operation_type_nc_job_none_value() -> None:
    assert OperationType.NC_JOB_NONE == -1


def test_operation_type_nc_pocket_value() -> None:
    assert OperationType.NC_POCKET == 0


def test_operation_type_nc_profile_value() -> None:
    assert OperationType.NC_PROFILE == 1


def test_operation_type_nc_drill_value() -> None:
    assert OperationType.NC_DRILL == 13


def test_operation_type_nc_back_spindle_operation_value() -> None:
    assert OperationType.NC_BACK_SPINDLE_OPERATION == 124


def test_operation_type_nc_fixture_value() -> None:
    assert OperationType.NC_FIXTURE == 125


def test_operation_type_nc_extern_file_value() -> None:
    assert OperationType.NC_EXTERN_FILE == 127


def test_operation_type_is_int_comparable() -> None:
    assert int(OperationType.NC_POCKET) == 0


# ---------------------------------------------------------------------------
# WireCutOperationType
# ---------------------------------------------------------------------------


def test_wire_cut_operation_type_wc_profile_value() -> None:
    assert WireCutOperationType.WC_PROFILE == 1


def test_wire_cut_operation_type_wc_4x_value() -> None:
    assert WireCutOperationType.WC_4X == 2


def test_wire_cut_operation_type_wc_angle_value() -> None:
    assert WireCutOperationType.WC_ANGLE == 3


def test_wire_cut_operation_type_wc_pos_job_value() -> None:
    assert WireCutOperationType.WC_POS_JOB == 4


# ---------------------------------------------------------------------------
# try_parse_operation_type
# ---------------------------------------------------------------------------


def test_try_parse_operation_type_known_code_returns_enum() -> None:
    result = try_parse_operation_type(0)
    assert result is OperationType.NC_POCKET


def test_try_parse_operation_type_known_code_13_returns_enum() -> None:
    result = try_parse_operation_type(13)
    assert result is OperationType.NC_DRILL


def test_try_parse_operation_type_known_code_124_returns_enum() -> None:
    result = try_parse_operation_type(124)
    assert result is OperationType.NC_BACK_SPINDLE_OPERATION


def test_try_parse_operation_type_unknown_code_returns_raw_int() -> None:
    result = try_parse_operation_type(9999)
    assert result == 9999


def test_try_parse_operation_type_unknown_code_is_int_instance() -> None:
    result = try_parse_operation_type(9999)
    assert isinstance(result, int)
    assert not isinstance(result, OperationType)


def test_try_parse_operation_type_negative_unknown_returns_raw_int() -> None:
    # -1 is NC_JOB_NONE, but e.g. -99 is unknown
    result = try_parse_operation_type(-99)
    assert result == -99


def test_try_parse_operation_type_negative_one_returns_enum() -> None:
    result = try_parse_operation_type(-1)
    assert result is OperationType.NC_JOB_NONE


def test_try_parse_operation_type_zero_is_nc_pocket() -> None:
    # Double-check the zero case is the canonical NC_POCKET member.
    result = try_parse_operation_type(0)
    assert result == OperationType.NC_POCKET
