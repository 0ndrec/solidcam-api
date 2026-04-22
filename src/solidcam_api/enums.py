from __future__ import annotations

from enum import IntEnum


class PartType(IntEnum):
    """Type of the currently open CAM part (or status indicator)."""

    SOLIDCAM_NOT_RUNNING = -2
    NO_OPEN_DOCUMENTS = -1
    NOT_CAM_PART = 0
    MILLING = 1
    TURNING = 2
    TURN_MILL = 3
    WIRE_CUT = 4


class NewPartType(IntEnum):
    """Part type used when creating a new CAM part."""

    MILLING = 0
    TURNING = 1
    WIRE_CUT = 2
    MILL_TURN = 3
    MILL_TURN_FULL = 4


class HomeOriginPosition(IntEnum):
    """Position of the home origin for milling parts."""

    TOP_CORNER = 0
    TOP_CENTER = 1
    CAD_ORIGIN = 2


class StockDefineBy(IntEnum):
    """How the stock geometry is defined."""

    SOLID = 0
    SURFACE = 1
    ALL = 2


class TargetDefineBy(IntEnum):
    """How the target geometry is defined."""

    SOLID = 0
    SURFACE = 1
    ALL = 2


class ToolType(IntEnum):
    """Category of a tool entry."""

    NONE = 0
    MILLING = 1
    TURNING = 2
    WIRE_CUT = 3


class OperationType(IntEnum):
    """NC operation type codes as returned by the SolidCAM COM API."""

    NC_JOB_NONE = -1
    NC_POCKET = 0
    NC_PROFILE = 1
    NC_CHAMFER = 2
    NC_DRILL_OLD = 3
    NC_SLOT = 4
    NC_RS = 5
    NC_TS = 6
    NC_SP = 7
    NC_VRS = 8
    NC_LFS = 9
    NC_CNS = 10
    NC_MSC = 11
    NC_THREAD = 12
    NC_DRILL = 13
    NC_DRILL_3D = 14
    NC_MSC_ENGRAV = 15
    NC_JOB_MW_5X = 16
    NC_JOB_MW_ELECTRODE_5X = 17
    NC_JOB_MW_ENGRAVING_5X = 18
    NC_JOB_MW_PORT_5X = 19
    NC_JOB_MW_SWARF_5X = 20
    NC_JOB_MW_TURBINE_5X = 21
    NC_JOB_MW_CONVERTED_5X = 22
    NC_JOB_MW_3X = 23
    NC_JOB_MW_4X = 24
    NC_JOB_HSM_CONST_STEP = 25
    NC_JOB_HSM_WATERLINE = 26
    NC_JOB_HSM_AREA_CLEARANCE = 27
    NC_JOB_HSM_RASTER_CLEARANCE = 28
    NC_JOB_HSM_HORIZ_AREA = 29
    NC_JOB_HSM_RASTER = 30
    NC_JOB_HSM_RADIAL = 31
    NC_JOB_HSM_SPIRAL = 32
    NC_JOB_HSM_MORPHED = 33
    NC_JOB_HSM_BOUNDARY = 34
    NC_JOB_HSM_PENCIL = 35
    NC_JOB_HSM_PAR_PENCIL = 36
    NC_JOB_HSM_REST_MACH = 37
    NC_JOB_HSM_REST_ROUGHING = 38
    NC_JOB_HSM_CORNER_OFFSET = 39
    NC_POCKET_3D = 40
    NC_PROFILE_3D = 41
    NC_TSLOT = 42
    NC_JOB_HSM_COMBINE_CONST_Z_HORIZONTAL = 43
    NC_JOB_HSM_COMBINE_CONST_Z_LINEAR = 44
    NC_JOB_HSM_COMBINE_CONST_Z_CONST_STEP = 45
    NC_JOB_MW_SWARF_4X = 46
    NC_JOB_MW_CONVERTED_3X = 47
    NC_JOB_MW_CONVERTED_4X = 48
    NC_JOB_MW_IMPELER_ROUGH_5X = 49
    NC_JOB_MW_IMPELLER_FLOOR_TC_5X = 50
    NC_JOB_MW_IMPELLER_FLOOR_NO_TC_5X = 51
    NC_JOB_MW_IMPELLER_BLADE_5X = 52
    NC_JOB_MW_DRILL_5X = 53
    NC_JOB_MW_CAVITY_WITH_GOUGE_5X = 54
    NC_FACE_MILLING = 55
    NC_JOB_HSM_HELICAL = 56
    NC_JOB_HSM_OFFSET_CUTTING = 57
    NC_JOB_HSM_MIXED_CONST_Z_CONST_STEP = 58
    NC_DRILL_HR = 59
    NC_SPIRAL_POCKET = 60
    NC_SPIRAL_MSC = 61
    NC_JOB_MW_DRILL_4X = 62
    NC_TURN_TURN = 63
    NC_TURN_DRILL = 64
    NC_TURN_THREAD = 65
    NC_TURN_GROOVE = 66
    NC_TURN_GROOVE_CUT = 67
    NC_JOB_MW_DEBURRING = 68
    NC_JOB_HSS_CONSTANT_Z = 69
    NC_JOB_HSS_LINEAR = 70
    NC_JOB_HSS_PERP_TOCURVE = 71
    NC_JOB_HSS_MORPH_BETWEEN_CURVES = 72
    NC_JOB_HSS_PARALLEL_TO_CURVE = 73
    NC_JOB_HSS_MORPH_BETWEEN_SURF = 74
    NC_JOB_HSS_PROJECTION = 75
    NC_JOB_HSS_PARALLEL_TO_SURF = 76
    NC_JOB_HSS_HATCH = 77
    NC_JOB_MW_CONSTANT_Z_4X = 78
    NC_JOB_MW_LINEAR_4X = 79
    NC_JOB_MW_PERP_TOCURVE_4X = 80
    NC_JOB_MW_MORPH_BETWEEN_CURVES_4X = 81
    NC_JOB_MW_PARALLEL_TO_CURVE_4X = 82
    NC_JOB_MW_MORPH_BETWEEN_SURF_4X = 83
    NC_JOB_MW_PROJECTION_4X = 84
    NC_JOB_MW_PARALLEL_TO_SURF_4X = 85
    NC_JOB_MW_HATCH_4X = 86
    NC_JOB_MW_CONSTANT_Z_5X = 87
    NC_JOB_MW_LINEAR_5X = 88
    NC_JOB_MW_PERP_TOCURVE_5X = 89
    NC_JOB_MW_MORPH_BETWEEN_CURVES_5X = 90
    NC_JOB_MW_PARALLEL_TO_CURVE_5X = 91
    NC_JOB_MW_MORPH_BETWEEN_SURF_5X = 92
    NC_JOB_MW_PROJECTION_5X = 93
    NC_JOB_MW_PARALLEL_TO_SURF_5X = 94
    NC_JOB_MW_HATCH_5X = 95
    NC_JOB_MW_NAVIROBO_DEBURRING = 96
    NC_JOB_MW_PARALLEL_CUTS_4X = 97
    NC_JOB_MW_PARALLEL_CUTS_5X = 98
    NC_JOB_HSM_COMBINE_CONST_Z_CORNER_OFFSET = 99
    NC_TOOL_BOX = 100
    NC_BACK_SPINDLE_OPERATION = 124
    NC_FIXTURE = 125
    NC_G_SPLIT = 126
    NC_EXTERN_FILE = 127


class WireCutOperationType(IntEnum):
    """Operation type codes specific to Wire Cut parts."""

    WC_PROFILE = 1
    WC_4X = 2
    WC_ANGLE = 3
    WC_POS_JOB = 4


def try_parse_operation_type(code: int) -> OperationType | int:
    """Return the ``OperationType`` member for *code*, or *code* itself if unknown.

    This is intentionally permissive so that future SolidCAM versions that
    introduce new operation type codes do not raise exceptions in calling code.

    Args:
        code: Raw integer operation-type code returned by the COM API.

    Returns:
        The matching :class:`OperationType` member when the code is recognised,
        otherwise the original ``int`` value unchanged.
    """
    try:
        return OperationType(code)
    except ValueError:
        return code
