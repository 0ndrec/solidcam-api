from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from solidcam_api import SolidCAMClient
from solidcam_api.enums import HomeOriginPosition, NewPartType, PartType
from solidcam_api.exceptions import SolidCAMAPIError


def test_part_path_returns_string(connected_client: SolidCAMClient, fake_com: MagicMock) -> None:
    fake_com.Path = r"C:\parts\part.prz"
    assert connected_client.part_path == r"C:\parts\part.prz"


def test_part_type_returns_enum_for_known_value(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.Type = int(PartType.MILLING)
    assert connected_client.part_type is PartType.MILLING


def test_part_type_returns_int_for_unknown_value(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.Type = 9999
    assert connected_client.part_type == 9999


def test_reference_model_returns_string(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.ReferenceModel = r"C:\models\part.sldprt"
    assert connected_client.reference_model == r"C:\models\part.sldprt"


def test_change_reference_model_calls_com(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.ChangeReferenceModel.return_value = 1
    connected_client.change_reference_model(r"C:\models\part.sldprt")
    fake_com.ChangeReferenceModel.assert_called_once()


def test_change_reference_model_raises_on_error(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.ChangeReferenceModel.return_value = 0
    with pytest.raises(SolidCAMAPIError):
        connected_client.change_reference_model(r"C:\models\part.sldprt")


def test_create_new_part_calls_com(connected_client: SolidCAMClient, fake_com: MagicMock) -> None:
    fake_com.LastError = 0
    connected_client.create_new_part(
        name="TestPart",
        path=r"C:\parts",
        part_type=NewPartType.MILLING,
        machine_index=0,
        home_origin_position=HomeOriginPosition.CAD_ORIGIN,
        inch=False,
    )
    fake_com.CreateNewPart.assert_called_once()


def test_create_new_part_raises_on_error(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.LastError = 1
    with pytest.raises(SolidCAMAPIError):
        connected_client.create_new_part(
            name="TestPart",
            path=r"C:\parts",
            part_type=NewPartType.MILLING,
            machine_index=0,
            home_origin_position=HomeOriginPosition.CAD_ORIGIN,
            inch=False,
        )
