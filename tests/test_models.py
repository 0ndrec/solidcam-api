from __future__ import annotations

import dataclasses

import pytest

from solidcam_api.enums import OperationType, ToolType
from solidcam_api.models import (
    CoordSys,
    GeomEntry,
    HomeEntry,
    Machine,
    Operation,
    ProcessTemplateEntry,
    TemplateEntry,
    Tool,
)

# ---------------------------------------------------------------------------
# Machine — field access
# ---------------------------------------------------------------------------


def test_machine_index_field() -> None:
    m = Machine(0, "MyMachine")
    assert m.index == 0


def test_machine_name_field() -> None:
    m = Machine(0, "MyMachine")
    assert m.name == "MyMachine"


def test_machine_index_nonzero() -> None:
    m = Machine(3, "Lathe")
    assert m.index == 3


# ---------------------------------------------------------------------------
# Machine — equality
# ---------------------------------------------------------------------------


def test_machine_equality_same_values() -> None:
    assert Machine(0, "X") == Machine(0, "X")


def test_machine_inequality_different_name() -> None:
    assert Machine(0, "X") != Machine(0, "Y")


def test_machine_inequality_different_index() -> None:
    assert Machine(0, "X") != Machine(1, "X")


def test_machine_inequality_both_different() -> None:
    assert Machine(0, "X") != Machine(1, "Y")


# ---------------------------------------------------------------------------
# Machine — immutability
# ---------------------------------------------------------------------------


def test_machine_is_immutable_name() -> None:
    m = Machine(0, "X")
    with pytest.raises(dataclasses.FrozenInstanceError):
        m.name = "Y"  # type: ignore[misc]


def test_machine_is_immutable_index() -> None:
    m = Machine(0, "X")
    with pytest.raises(dataclasses.FrozenInstanceError):
        m.index = 99  # type: ignore[misc]


# ---------------------------------------------------------------------------
# Machine — hashability
# ---------------------------------------------------------------------------


def test_machine_is_hashable() -> None:
    m = Machine(0, "X")
    assert isinstance(hash(m), int)


def test_machine_can_be_put_in_set() -> None:
    s = {Machine(0, "X"), Machine(1, "Y")}
    assert len(s) == 2


def test_machine_equal_instances_deduplicate_in_set() -> None:
    s = {Machine(0, "X"), Machine(0, "X")}
    assert len(s) == 1


# ---------------------------------------------------------------------------
# Operation — field access
# ---------------------------------------------------------------------------


def test_operation_index_field() -> None:
    op = Operation(0, "Roughing", 0)
    assert op.index == 0


def test_operation_name_field() -> None:
    op = Operation(0, "Roughing", 0)
    assert op.name == "Roughing"


def test_operation_type_code_field() -> None:
    op = Operation(0, "Roughing", 0)
    assert op.type_code == 0


# ---------------------------------------------------------------------------
# Operation — .type property
# ---------------------------------------------------------------------------


def test_operation_type_known_code_returns_enum() -> None:
    op = Operation(0, "Roughing", 0)
    assert op.type == OperationType.NC_POCKET


def test_operation_type_nc_drill_returns_enum() -> None:
    op = Operation(1, "Drill", 13)
    assert op.type is OperationType.NC_DRILL


def test_operation_type_unknown_code_returns_raw_int() -> None:
    op = Operation(0, "X", 9999)
    assert op.type == 9999


def test_operation_type_unknown_code_is_plain_int() -> None:
    op = Operation(0, "X", 9999)
    result = op.type
    assert isinstance(result, int)
    assert not isinstance(result, OperationType)


def test_operation_type_nc_back_spindle_returns_enum() -> None:
    op = Operation(0, "BackSpindle", 124)
    assert op.type is OperationType.NC_BACK_SPINDLE_OPERATION


# ---------------------------------------------------------------------------
# Operation — immutability
# ---------------------------------------------------------------------------


def test_operation_is_immutable() -> None:
    op = Operation(0, "Roughing", 0)
    with pytest.raises(dataclasses.FrozenInstanceError):
        op.name = "Finishing"  # type: ignore[misc]


# ---------------------------------------------------------------------------
# Operation — hashability
# ---------------------------------------------------------------------------


def test_operation_is_hashable() -> None:
    op = Operation(0, "Op", 0)
    assert isinstance(hash(op), int)


def test_operation_can_be_put_in_set() -> None:
    s = {Operation(0, "Op1", 0), Operation(1, "Op2", 1)}
    assert len(s) == 2


def test_operation_equal_instances_deduplicate_in_set() -> None:
    s = {Operation(0, "Op1", 0), Operation(0, "Op1", 0)}
    assert len(s) == 1


# ---------------------------------------------------------------------------
# Tool — field access
# ---------------------------------------------------------------------------


def test_tool_index_field() -> None:
    t = Tool(0, "Endmill", 1)
    assert t.index == 0


def test_tool_name_field() -> None:
    t = Tool(0, "Endmill", 1)
    assert t.name == "Endmill"


def test_tool_type_code_field() -> None:
    t = Tool(0, "Endmill", 1)
    assert t.type_code == 1


# ---------------------------------------------------------------------------
# Tool — .type property
# ---------------------------------------------------------------------------


def test_tool_type_milling_returns_enum() -> None:
    t = Tool(0, "Endmill", 1)
    assert t.type == ToolType.MILLING


def test_tool_type_turning_returns_enum() -> None:
    t = Tool(0, "Insert", 2)
    assert t.type is ToolType.TURNING


def test_tool_type_wire_cut_returns_enum() -> None:
    t = Tool(0, "Wire", 3)
    assert t.type is ToolType.WIRE_CUT


def test_tool_type_none_returns_enum() -> None:
    t = Tool(0, "Unknown", 0)
    assert t.type is ToolType.NONE


def test_tool_type_unknown_code_returns_raw_int() -> None:
    t = Tool(0, "FutureTool", 99)
    assert t.type == 99
    assert isinstance(t.type, int)
    assert not isinstance(t.type, ToolType)


# ---------------------------------------------------------------------------
# Tool — immutability
# ---------------------------------------------------------------------------


def test_tool_is_immutable() -> None:
    t = Tool(0, "Endmill", 1)
    with pytest.raises(dataclasses.FrozenInstanceError):
        t.name = "Ballmill"  # type: ignore[misc]


# ---------------------------------------------------------------------------
# Tool — hashability
# ---------------------------------------------------------------------------


def test_tool_is_hashable() -> None:
    t = Tool(0, "Endmill", 1)
    assert isinstance(hash(t), int)


def test_tool_can_be_put_in_set() -> None:
    s = {Tool(0, "Endmill", 1), Tool(1, "Ballmill", 1)}
    assert len(s) == 2


# ---------------------------------------------------------------------------
# CoordSys — basic field access
# ---------------------------------------------------------------------------


def test_coord_sys_index_field() -> None:
    cs = CoordSys(index=0, name="MCS1")
    assert cs.index == 0


def test_coord_sys_name_field() -> None:
    cs = CoordSys(index=0, name="MCS1")
    assert cs.name == "MCS1"


def test_coord_sys_equality() -> None:
    assert CoordSys(0, "MCS1") == CoordSys(0, "MCS1")


def test_coord_sys_inequality() -> None:
    assert CoordSys(0, "MCS1") != CoordSys(1, "MCS2")


def test_coord_sys_is_immutable() -> None:
    cs = CoordSys(0, "MCS1")
    with pytest.raises(dataclasses.FrozenInstanceError):
        cs.name = "MCS2"  # type: ignore[misc]


def test_coord_sys_is_hashable() -> None:
    cs = CoordSys(0, "MCS1")
    assert isinstance(hash(cs), int)


def test_coord_sys_can_be_put_in_set() -> None:
    s = {CoordSys(0, "MCS1"), CoordSys(1, "MCS2")}
    assert len(s) == 2


# ---------------------------------------------------------------------------
# HomeEntry — basic field access
# ---------------------------------------------------------------------------


def test_home_entry_index_field() -> None:
    h = HomeEntry(index=1, name="Home1")
    assert h.index == 1


def test_home_entry_name_field() -> None:
    h = HomeEntry(index=1, name="Home1")
    assert h.name == "Home1"


def test_home_entry_equality() -> None:
    assert HomeEntry(0, "Home1") == HomeEntry(0, "Home1")


def test_home_entry_inequality() -> None:
    assert HomeEntry(0, "Home1") != HomeEntry(1, "Home2")


def test_home_entry_is_immutable() -> None:
    h = HomeEntry(0, "Home1")
    with pytest.raises(dataclasses.FrozenInstanceError):
        h.name = "Home2"  # type: ignore[misc]


def test_home_entry_is_hashable() -> None:
    h = HomeEntry(0, "Home1")
    assert isinstance(hash(h), int)


def test_home_entry_can_be_put_in_set() -> None:
    s = {HomeEntry(0, "Home1"), HomeEntry(1, "Home2")}
    assert len(s) == 2


# ---------------------------------------------------------------------------
# GeomEntry — basic field access
# ---------------------------------------------------------------------------


def test_geom_entry_index_field() -> None:
    g = GeomEntry(index=2, name="Stock1")
    assert g.index == 2


def test_geom_entry_name_field() -> None:
    g = GeomEntry(index=2, name="Stock1")
    assert g.name == "Stock1"


def test_geom_entry_equality() -> None:
    assert GeomEntry(0, "Stock1") == GeomEntry(0, "Stock1")


def test_geom_entry_inequality() -> None:
    assert GeomEntry(0, "Stock1") != GeomEntry(1, "Target1")


def test_geom_entry_is_immutable() -> None:
    g = GeomEntry(0, "Stock1")
    with pytest.raises(dataclasses.FrozenInstanceError):
        g.name = "Target1"  # type: ignore[misc]


def test_geom_entry_is_hashable() -> None:
    g = GeomEntry(0, "Stock1")
    assert isinstance(hash(g), int)


def test_geom_entry_can_be_put_in_set() -> None:
    s = {GeomEntry(0, "Stock1"), GeomEntry(1, "Target1")}
    assert len(s) == 2


# ---------------------------------------------------------------------------
# TemplateEntry — basic field access
# ---------------------------------------------------------------------------


def test_template_entry_index_field() -> None:
    t = TemplateEntry(index=0, name="Roughing Template")
    assert t.index == 0


def test_template_entry_name_field() -> None:
    t = TemplateEntry(index=0, name="Roughing Template")
    assert t.name == "Roughing Template"


def test_template_entry_equality() -> None:
    assert TemplateEntry(0, "T1") == TemplateEntry(0, "T1")


def test_template_entry_inequality() -> None:
    assert TemplateEntry(0, "T1") != TemplateEntry(1, "T2")


def test_template_entry_is_immutable() -> None:
    t = TemplateEntry(0, "T1")
    with pytest.raises(dataclasses.FrozenInstanceError):
        t.name = "T2"  # type: ignore[misc]


def test_template_entry_is_hashable() -> None:
    t = TemplateEntry(0, "T1")
    assert isinstance(hash(t), int)


def test_template_entry_can_be_put_in_set() -> None:
    s = {TemplateEntry(0, "T1"), TemplateEntry(1, "T2")}
    assert len(s) == 2


# ---------------------------------------------------------------------------
# ProcessTemplateEntry — basic field access
# ---------------------------------------------------------------------------


def test_process_template_entry_index_field() -> None:
    p = ProcessTemplateEntry(index=1, name="Full Process")
    assert p.index == 1


def test_process_template_entry_name_field() -> None:
    p = ProcessTemplateEntry(index=1, name="Full Process")
    assert p.name == "Full Process"


def test_process_template_entry_equality() -> None:
    assert ProcessTemplateEntry(0, "P1") == ProcessTemplateEntry(0, "P1")


def test_process_template_entry_inequality() -> None:
    assert ProcessTemplateEntry(0, "P1") != ProcessTemplateEntry(1, "P2")


def test_process_template_entry_is_immutable() -> None:
    p = ProcessTemplateEntry(0, "P1")
    with pytest.raises(dataclasses.FrozenInstanceError):
        p.name = "P2"  # type: ignore[misc]


def test_process_template_entry_is_hashable() -> None:
    p = ProcessTemplateEntry(0, "P1")
    assert isinstance(hash(p), int)


def test_process_template_entry_can_be_put_in_set() -> None:
    s = {ProcessTemplateEntry(0, "P1"), ProcessTemplateEntry(1, "P2")}
    assert len(s) == 2


# ---------------------------------------------------------------------------
# All model types are hashable — combined set membership test
# ---------------------------------------------------------------------------


def test_all_model_types_are_hashable_and_usable_in_set() -> None:
    models: list[object] = [
        Machine(0, "M"),
        Operation(0, "Op", 0),
        Tool(0, "T", 1),
        CoordSys(0, "CS"),
        HomeEntry(0, "H"),
        GeomEntry(0, "G"),
        TemplateEntry(0, "TE"),
        ProcessTemplateEntry(0, "PTE"),
    ]
    result = set(models)
    # All eight instances are distinct objects — the set must have all of them.
    assert len(result) == len(models)
