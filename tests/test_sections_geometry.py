from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from solidcam_api import SolidCAMClient
from solidcam_api.exceptions import SolidCAMAPIError
from solidcam_api.models import CoordSys, GeomEntry, HomeEntry

# ---------------------------------------------------------------------------
# cad_coord_sys_count property
# ---------------------------------------------------------------------------


def test_cad_coord_sys_count_reads_com_property(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.CADCoordSysCount = 4
    assert connected_client.cad_coord_sys_count == 4


def test_cad_coord_sys_count_returns_zero_when_none_defined(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.CADCoordSysCount = 0
    assert connected_client.cad_coord_sys_count == 0


def test_cad_coord_sys_count_is_int_type(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.CADCoordSysCount = 2
    assert isinstance(connected_client.cad_coord_sys_count, int)


def test_cad_coord_sys_count_reflects_updated_value(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.CADCoordSysCount = 1
    assert connected_client.cad_coord_sys_count == 1
    fake_com.CADCoordSysCount = 5
    assert connected_client.cad_coord_sys_count == 5


# ---------------------------------------------------------------------------
# get_cad_coord_sys_name()
# ---------------------------------------------------------------------------


def test_get_cad_coord_sys_name_calls_com_with_index(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.GetCADCoordSysName.return_value = "MCS1"
    connected_client.get_cad_coord_sys_name(0)
    fake_com.GetCADCoordSysName.assert_called_once_with(0)


def test_get_cad_coord_sys_name_returns_string_from_com(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.GetCADCoordSysName.return_value = "MCS1"
    result = connected_client.get_cad_coord_sys_name(0)
    assert result == "MCS1"


def test_get_cad_coord_sys_name_returns_str_type(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.GetCADCoordSysName.return_value = "TopPlane"
    result = connected_client.get_cad_coord_sys_name(0)
    assert isinstance(result, str)


def test_get_cad_coord_sys_name_forwards_nonzero_index(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.GetCADCoordSysName.return_value = "MCS2"
    connected_client.get_cad_coord_sys_name(3)
    fake_com.GetCADCoordSysName.assert_called_once_with(3)


# ---------------------------------------------------------------------------
# get_cad_coord_sys() — single-entry accessor
# ---------------------------------------------------------------------------


def test_get_cad_coord_sys_returns_coord_sys_instance(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.GetCADCoordSysName.return_value = "MCS1"
    result = connected_client.get_cad_coord_sys(0)
    assert isinstance(result, CoordSys)


def test_get_cad_coord_sys_index_matches_requested_index(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.GetCADCoordSysName.return_value = "MCS1"
    cs = connected_client.get_cad_coord_sys(2)
    assert cs.index == 2


def test_get_cad_coord_sys_name_field_matches_com_value(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.GetCADCoordSysName.return_value = "FrontPlane"
    cs = connected_client.get_cad_coord_sys(0)
    assert cs.name == "FrontPlane"


# ---------------------------------------------------------------------------
# list_cad_coord_sys()
# ---------------------------------------------------------------------------


def test_list_cad_coord_sys_returns_list(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.CADCoordSysCount = 0
    result = connected_client.list_cad_coord_sys()
    assert isinstance(result, list)


def test_list_cad_coord_sys_returns_empty_list_when_count_is_zero(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.CADCoordSysCount = 0
    assert connected_client.list_cad_coord_sys() == []


def test_list_cad_coord_sys_length_matches_count(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.CADCoordSysCount = 3
    fake_com.GetCADCoordSysName.return_value = "MCS"
    result = connected_client.list_cad_coord_sys()
    assert len(result) == 3


def test_list_cad_coord_sys_all_items_are_coord_sys_instances(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.CADCoordSysCount = 2
    fake_com.GetCADCoordSysName.return_value = "MCS"
    result = connected_client.list_cad_coord_sys()
    assert all(isinstance(cs, CoordSys) for cs in result)


def test_list_cad_coord_sys_indices_are_sequential(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.CADCoordSysCount = 3
    fake_com.GetCADCoordSysName.return_value = "MCS"
    result = connected_client.list_cad_coord_sys()
    assert [cs.index for cs in result] == [0, 1, 2]


def test_list_cad_coord_sys_single_item_name(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.CADCoordSysCount = 1
    fake_com.GetCADCoordSysName.return_value = "OnlyMCS"
    result = connected_client.list_cad_coord_sys()
    assert len(result) == 1
    assert result[0].name == "OnlyMCS"


def test_list_cad_coord_sys_calls_get_name_for_each_index(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.CADCoordSysCount = 2
    fake_com.GetCADCoordSysName.return_value = "MCS"
    connected_client.list_cad_coord_sys()
    assert fake_com.GetCADCoordSysName.call_count == 2


# ---------------------------------------------------------------------------
# home_count property
# ---------------------------------------------------------------------------


def test_home_count_reads_com_property(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.HomeCount = 2
    assert connected_client.home_count == 2


def test_home_count_returns_zero_when_no_homes(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.HomeCount = 0
    assert connected_client.home_count == 0


def test_home_count_is_int_type(connected_client: SolidCAMClient, fake_com: MagicMock) -> None:
    fake_com.HomeCount = 1
    assert isinstance(connected_client.home_count, int)


def test_home_count_reflects_updated_com_value(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.HomeCount = 1
    assert connected_client.home_count == 1
    fake_com.HomeCount = 4
    assert connected_client.home_count == 4


# ---------------------------------------------------------------------------
# get_home_name()
# ---------------------------------------------------------------------------


def test_get_home_name_calls_com_with_index(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.GetHomeName.return_value = "Home1"
    connected_client.get_home_name(0)
    fake_com.GetHomeName.assert_called_once_with(0)


def test_get_home_name_returns_string_from_com(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.GetHomeName.return_value = "Home1"
    result = connected_client.get_home_name(0)
    assert result == "Home1"


def test_get_home_name_returns_str_type(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.GetHomeName.return_value = "WorkOffset1"
    result = connected_client.get_home_name(0)
    assert isinstance(result, str)


def test_get_home_name_forwards_nonzero_index(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.GetHomeName.return_value = "Home3"
    connected_client.get_home_name(2)
    fake_com.GetHomeName.assert_called_once_with(2)


# ---------------------------------------------------------------------------
# get_home() — single-entry accessor
# ---------------------------------------------------------------------------


def test_get_home_returns_home_entry_instance(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.GetHomeName.return_value = "Home1"
    result = connected_client.get_home(0)
    assert isinstance(result, HomeEntry)


def test_get_home_index_matches_requested_index(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.GetHomeName.return_value = "Home1"
    h = connected_client.get_home(1)
    assert h.index == 1


def test_get_home_name_field_matches_com_value(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.GetHomeName.return_value = "G54"
    h = connected_client.get_home(0)
    assert h.name == "G54"


# ---------------------------------------------------------------------------
# list_home_positions()
# ---------------------------------------------------------------------------


def test_list_home_positions_returns_list(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.HomeCount = 0
    result = connected_client.list_home_positions()
    assert isinstance(result, list)


def test_list_home_positions_returns_empty_list_when_count_is_zero(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.HomeCount = 0
    assert connected_client.list_home_positions() == []


def test_list_home_positions_length_matches_home_count(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.HomeCount = 3
    fake_com.GetHomeName.return_value = "Home"
    result = connected_client.list_home_positions()
    assert len(result) == 3


def test_list_home_positions_all_items_are_home_entry_instances(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.HomeCount = 2
    fake_com.GetHomeName.return_value = "Home"
    result = connected_client.list_home_positions()
    assert all(isinstance(h, HomeEntry) for h in result)


def test_list_home_positions_indices_are_sequential(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.HomeCount = 3
    fake_com.GetHomeName.return_value = "Home"
    result = connected_client.list_home_positions()
    assert [h.index for h in result] == [0, 1, 2]


# ---------------------------------------------------------------------------
# create_home()
# ---------------------------------------------------------------------------


def test_create_home_calls_com_create_home_with_int_position(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    connected_client.create_home(0)
    fake_com.CreateHome.assert_called_once_with(0)


def test_create_home_converts_position_to_int(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    from solidcam_api.enums import HomeOriginPosition

    connected_client.create_home(HomeOriginPosition.CAD_ORIGIN)
    # HomeOriginPosition.CAD_ORIGIN == 2; the section calls int() on it.
    fake_com.CreateHome.assert_called_once_with(2)


def test_create_home_top_center_position(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    from solidcam_api.enums import HomeOriginPosition

    connected_client.create_home(HomeOriginPosition.TOP_CENTER)
    fake_com.CreateHome.assert_called_once_with(1)


def test_create_home_does_not_raise_when_last_error_zero(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.LastError = 0
    connected_client.create_home(0)  # must not raise


def test_create_home_raises_api_error_when_last_error_nonzero(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.LastError = 20
    fake_com.LastErrorDescription = "cannot create home"
    with pytest.raises(SolidCAMAPIError) as exc_info:
        connected_client.create_home(0)
    assert exc_info.value.method == "CreateHome"
    assert exc_info.value.code == 20


def test_create_home_error_includes_description(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.LastError = 20
    fake_com.LastErrorDescription = "cannot create home"
    with pytest.raises(SolidCAMAPIError) as exc_info:
        connected_client.create_home(0)
    assert exc_info.value.description == "cannot create home"


def test_create_home_raw_int_position_is_forwarded(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    connected_client.create_home(2)
    fake_com.CreateHome.assert_called_once_with(2)


# ---------------------------------------------------------------------------
# create_home_by_cad()
# ---------------------------------------------------------------------------


def test_create_home_by_cad_calls_com_with_cad_home_name(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.CreateHomeByCAD.return_value = 1
    connected_client.create_home_by_cad("MCS1")
    fake_com.CreateHomeByCAD.assert_called_once_with("MCS1")


def test_create_home_by_cad_forwards_name(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.CreateHomeByCAD.return_value = 1
    connected_client.create_home_by_cad("FrontFaceMCS")
    args, _ = fake_com.CreateHomeByCAD.call_args
    assert args[0] == "FrontFaceMCS"


def test_create_home_by_cad_does_not_raise_on_truthy_result(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.CreateHomeByCAD.return_value = 1
    connected_client.create_home_by_cad("MCS1")  # must not raise


def test_create_home_by_cad_raises_api_error_on_falsy_result(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.CreateHomeByCAD.return_value = 0
    with pytest.raises(SolidCAMAPIError):
        connected_client.create_home_by_cad("MCS1")


def test_create_home_by_cad_raises_api_error_on_none_result(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.CreateHomeByCAD.return_value = None
    with pytest.raises(SolidCAMAPIError):
        connected_client.create_home_by_cad("MCS1")


def test_create_home_by_cad_error_includes_method_name(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.CreateHomeByCAD.return_value = 0
    with pytest.raises(SolidCAMAPIError) as exc_info:
        connected_client.create_home_by_cad("BadMCS")
    assert exc_info.value.method == "CreateHomeByCAD"


def test_create_home_by_cad_error_includes_code_from_last_error(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.CreateHomeByCAD.return_value = 0
    fake_com.LastError = 30
    fake_com.LastErrorDescription = "cad home not found"
    with pytest.raises(SolidCAMAPIError) as exc_info:
        connected_client.create_home_by_cad("BadMCS")
    assert exc_info.value.code == 30
    assert exc_info.value.description == "cad home not found"


# ---------------------------------------------------------------------------
# geom_count property
# ---------------------------------------------------------------------------


def test_geom_count_reads_com_property(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.GeomCount = 6
    assert connected_client.geom_count == 6


def test_geom_count_returns_zero_when_no_geometries(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.GeomCount = 0
    assert connected_client.geom_count == 0


def test_geom_count_is_int_type(connected_client: SolidCAMClient, fake_com: MagicMock) -> None:
    fake_com.GeomCount = 4
    assert isinstance(connected_client.geom_count, int)


def test_geom_count_reflects_updated_value(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.GeomCount = 2
    assert connected_client.geom_count == 2
    fake_com.GeomCount = 8
    assert connected_client.geom_count == 8


# ---------------------------------------------------------------------------
# get_geom_name()
# ---------------------------------------------------------------------------


def test_get_geom_name_calls_com_with_index(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.GetGeomName.return_value = "Stock1"
    connected_client.get_geom_name(0)
    fake_com.GetGeomName.assert_called_once_with(0)


def test_get_geom_name_returns_string_from_com(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.GetGeomName.return_value = "Stock1"
    result = connected_client.get_geom_name(0)
    assert result == "Stock1"


def test_get_geom_name_returns_str_type(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.GetGeomName.return_value = "Target_Solid"
    result = connected_client.get_geom_name(0)
    assert isinstance(result, str)


def test_get_geom_name_forwards_nonzero_index(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.GetGeomName.return_value = "Curve1"
    connected_client.get_geom_name(5)
    fake_com.GetGeomName.assert_called_once_with(5)


# ---------------------------------------------------------------------------
# get_geom() — single-entry accessor
# ---------------------------------------------------------------------------


def test_get_geom_returns_geom_entry_instance(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.GetGeomName.return_value = "Stock1"
    result = connected_client.get_geom(0)
    assert isinstance(result, GeomEntry)


def test_get_geom_index_matches_requested_index(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.GetGeomName.return_value = "Stock1"
    g = connected_client.get_geom(3)
    assert g.index == 3


def test_get_geom_name_field_matches_com_value(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.GetGeomName.return_value = "BarStock"
    g = connected_client.get_geom(0)
    assert g.name == "BarStock"


# ---------------------------------------------------------------------------
# list_geometries()
# ---------------------------------------------------------------------------


def test_list_geometries_returns_list(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.GeomCount = 0
    result = connected_client.list_geometries()
    assert isinstance(result, list)


def test_list_geometries_returns_empty_list_when_count_is_zero(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.GeomCount = 0
    assert connected_client.list_geometries() == []


def test_list_geometries_length_matches_geom_count(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.GeomCount = 4
    fake_com.GetGeomName.return_value = "Geom"
    result = connected_client.list_geometries()
    assert len(result) == 4


def test_list_geometries_all_items_are_geom_entry_instances(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.GeomCount = 3
    fake_com.GetGeomName.return_value = "Geom"
    result = connected_client.list_geometries()
    assert all(isinstance(g, GeomEntry) for g in result)


def test_list_geometries_indices_are_sequential(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.GeomCount = 3
    fake_com.GetGeomName.return_value = "Geom"
    result = connected_client.list_geometries()
    assert [g.index for g in result] == [0, 1, 2]


def test_list_geometries_single_item_name(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.GeomCount = 1
    fake_com.GetGeomName.return_value = "OnlyStock"
    result = connected_client.list_geometries()
    assert len(result) == 1
    assert result[0].name == "OnlyStock"


# ---------------------------------------------------------------------------
# create_stock_box()
# ---------------------------------------------------------------------------


def test_create_stock_box_calls_com_create_stock_box(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.CreateStockBox.return_value = 1
    connected_client.create_stock_box("Stock", 2.0, 2.0, 2.0, 2.0, 2.0, 0.0)
    fake_com.CreateStockBox.assert_called_once()


def test_create_stock_box_passes_all_args_to_com(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.CreateStockBox.return_value = 1
    connected_client.create_stock_box("Stock", 2.0, 2.0, 2.0, 2.0, 2.0, 0.0)
    # Signature: name, x+, y+, z+, x-, y-, z-, absolute, define_by(int), add_3d_sketch,
    #            generate_stock_envelope, facet_tolerance
    # define_by default = StockDefineBy.ALL = 2
    fake_com.CreateStockBox.assert_called_once_with(
        "Stock",
        2.0,
        2.0,
        2.0,
        2.0,
        2.0,
        0.0,
        False,
        2,
        False,
        True,
        0.0,
    )


def test_create_stock_box_forwards_name(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.CreateStockBox.return_value = 1
    connected_client.create_stock_box("MyStock")
    args, _ = fake_com.CreateStockBox.call_args
    assert args[0] == "MyStock"


def test_create_stock_box_forwards_x_plus_offset(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.CreateStockBox.return_value = 1
    connected_client.create_stock_box("S", x_plus=5.0)
    args, _ = fake_com.CreateStockBox.call_args
    assert args[1] == 5.0


def test_create_stock_box_forwards_z_minus_offset(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.CreateStockBox.return_value = 1
    connected_client.create_stock_box("S", 2.0, 2.0, 2.0, 2.0, 2.0, 3.5)
    args, _ = fake_com.CreateStockBox.call_args
    assert args[6] == 3.5


def test_create_stock_box_default_define_by_is_all(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.CreateStockBox.return_value = 1
    connected_client.create_stock_box("S")
    args, _ = fake_com.CreateStockBox.call_args
    # define_by is the 9th argument (index 8) and should be int(StockDefineBy.ALL) = 2
    assert args[8] == 2


def test_create_stock_box_does_not_raise_when_com_returns_truthy(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.CreateStockBox.return_value = 1
    connected_client.create_stock_box("Stock")  # must not raise


def test_create_stock_box_raises_api_error_when_com_returns_zero(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.CreateStockBox.return_value = 0
    with pytest.raises(SolidCAMAPIError):
        connected_client.create_stock_box("Stock")


def test_create_stock_box_raises_api_error_when_com_returns_none(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.CreateStockBox.return_value = None
    with pytest.raises(SolidCAMAPIError):
        connected_client.create_stock_box("Stock")


def test_create_stock_box_error_includes_method_name(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.CreateStockBox.return_value = 0
    with pytest.raises(SolidCAMAPIError) as exc_info:
        connected_client.create_stock_box("Stock")
    assert exc_info.value.method == "CreateStockBox"


def test_create_stock_box_error_includes_code_from_last_error(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.CreateStockBox.return_value = 0
    fake_com.LastError = 25
    fake_com.LastErrorDescription = "stock creation failed"
    with pytest.raises(SolidCAMAPIError) as exc_info:
        connected_client.create_stock_box("Stock")
    assert exc_info.value.code == 25
    assert exc_info.value.description == "stock creation failed"


def test_create_stock_box_absolute_flag_is_forwarded(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.CreateStockBox.return_value = 1
    connected_client.create_stock_box("S", absolute=True)
    args, _ = fake_com.CreateStockBox.call_args
    # absolute is the 8th argument (index 7)
    assert args[7] is True


def test_create_stock_box_add_3d_sketch_flag_is_forwarded(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.CreateStockBox.return_value = 1
    connected_client.create_stock_box("S", add_3d_sketch=True)
    args, _ = fake_com.CreateStockBox.call_args
    # add_3d_sketch is the 10th argument (index 9)
    assert args[9] is True


# ---------------------------------------------------------------------------
# create_stock_cylinder()
# ---------------------------------------------------------------------------


def test_create_stock_cylinder_calls_com_create_stock_cylinder(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.CreateStockCylinder.return_value = 1
    connected_client.create_stock_cylinder("CylStock")
    fake_com.CreateStockCylinder.assert_called_once()


def test_create_stock_cylinder_forwards_name(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.CreateStockCylinder.return_value = 1
    connected_client.create_stock_cylinder("BarStock")
    args, _ = fake_com.CreateStockCylinder.call_args
    assert args[0] == "BarStock"


def test_create_stock_cylinder_does_not_raise_on_truthy_result(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.CreateStockCylinder.return_value = 1
    connected_client.create_stock_cylinder("CylStock")  # must not raise


def test_create_stock_cylinder_raises_api_error_on_falsy_result(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.CreateStockCylinder.return_value = 0
    with pytest.raises(SolidCAMAPIError):
        connected_client.create_stock_cylinder("CylStock")


def test_create_stock_cylinder_error_includes_method_name(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.CreateStockCylinder.return_value = 0
    with pytest.raises(SolidCAMAPIError) as exc_info:
        connected_client.create_stock_cylinder("CylStock")
    assert exc_info.value.method == "CreateStockCylinder"


def test_create_stock_cylinder_default_define_by_is_all(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.CreateStockCylinder.return_value = 1
    connected_client.create_stock_cylinder("C")
    args, _ = fake_com.CreateStockCylinder.call_args
    # Signature: name, right, left, internal_diameter, external_diameter,
    #            absolute, int(define_by), add_3d_sketch, generate_stock_envelope, facet_tolerance
    # define_by is index 6; default = StockDefineBy.ALL = 2
    assert args[6] == 2


# ---------------------------------------------------------------------------
# create_target()
# ---------------------------------------------------------------------------


def test_create_target_calls_com_create_target(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.CreateTarget.return_value = 1
    connected_client.create_target("Target")
    fake_com.CreateTarget.assert_called_once()


def test_create_target_passes_all_default_args_to_com(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.CreateTarget.return_value = 1
    connected_client.create_target("Target")
    # Signature: name, int(define_by), model_without_envelope, generate_envelope,
    #            generate_section, generate_mirror_envelope, facet_tolerance
    # define_by default = TargetDefineBy.ALL = 2
    fake_com.CreateTarget.assert_called_once_with(
        "Target",
        2,
        False,
        True,
        False,
        False,
        0.0,
    )


def test_create_target_forwards_name(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.CreateTarget.return_value = 1
    connected_client.create_target("MyTarget")
    args, _ = fake_com.CreateTarget.call_args
    assert args[0] == "MyTarget"


def test_create_target_default_define_by_is_all(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.CreateTarget.return_value = 1
    connected_client.create_target("T")
    args, _ = fake_com.CreateTarget.call_args
    # int(TargetDefineBy.ALL) == 2; it is the second argument (index 1)
    assert args[1] == 2


def test_create_target_does_not_raise_on_truthy_result(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.CreateTarget.return_value = 1
    connected_client.create_target("Target")  # must not raise


def test_create_target_raises_api_error_on_falsy_result(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.CreateTarget.return_value = 0
    with pytest.raises(SolidCAMAPIError):
        connected_client.create_target("Target")


def test_create_target_raises_api_error_on_none_result(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.CreateTarget.return_value = None
    with pytest.raises(SolidCAMAPIError):
        connected_client.create_target("Target")


def test_create_target_error_includes_method_name(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.CreateTarget.return_value = 0
    with pytest.raises(SolidCAMAPIError) as exc_info:
        connected_client.create_target("Target")
    assert exc_info.value.method == "CreateTarget"


def test_create_target_error_includes_code_from_last_error(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.CreateTarget.return_value = 0
    fake_com.LastError = 50
    fake_com.LastErrorDescription = "no solid body selected"
    with pytest.raises(SolidCAMAPIError) as exc_info:
        connected_client.create_target("Target")
    assert exc_info.value.code == 50
    assert exc_info.value.description == "no solid body selected"


def test_create_target_generate_envelope_flag_forwarded(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.CreateTarget.return_value = 1
    connected_client.create_target("T", generate_envelope=False)
    args, _ = fake_com.CreateTarget.call_args
    # generate_envelope is the 4th argument (index 3)
    assert args[3] is False


def test_create_target_generate_section_flag_forwarded(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.CreateTarget.return_value = 1
    connected_client.create_target("T", generate_section=True)
    args, _ = fake_com.CreateTarget.call_args
    # generate_section is the 5th argument (index 4)
    assert args[4] is True


def test_create_target_facet_tolerance_is_forwarded(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.CreateTarget.return_value = 1
    connected_client.create_target("T", facet_tolerance=0.01)
    args, _ = fake_com.CreateTarget.call_args
    # facet_tolerance is the 7th argument (index 6)
    assert args[6] == pytest.approx(0.01)
