from __future__ import annotations

from unittest.mock import MagicMock

from solidcam_api import SolidCAMClient
from solidcam_api.models import Machine


def test_machine_count_returns_int(connected_client: SolidCAMClient, fake_com: MagicMock) -> None:
    fake_com.MachineCount = 5
    assert connected_client.machine_count == 5


def test_machine_count_returns_zero_when_empty(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.MachineCount = 0
    assert connected_client.machine_count == 0


def test_current_machine_name_returns_string(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.CurrentMachineName = "Haas VF-2"
    assert connected_client.current_machine_name == "Haas VF-2"


def test_current_machine_returns_int(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.CurrentMachine = 2
    assert connected_client.current_machine == 2


def test_current_machine_setter_sets_com_value(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    connected_client.current_machine = 3
    assert fake_com.CurrentMachine == 3


def test_get_machine_name_returns_string(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.GetMachineName.return_value = "Haas VF-2"
    result = connected_client.get_machine_name(0)
    assert result == "Haas VF-2"


def test_get_machine_name_calls_com(connected_client: SolidCAMClient, fake_com: MagicMock) -> None:
    connected_client.get_machine_name(2)
    fake_com.GetMachineName.assert_called_once_with(2)


def test_list_machines_returns_empty_list(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.MachineCount = 0
    assert connected_client.list_machines() == []


def test_list_machines_returns_machine_list(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.MachineCount = 2
    fake_com.GetMachineName.side_effect = ["Haas VF-2", "DMG MORI"]
    result = connected_client.list_machines()
    assert len(result) == 2
    assert all(isinstance(m, Machine) for m in result)
    assert result[0].index == 0
    assert result[0].name == "Haas VF-2"
    assert result[1].index == 1
    assert result[1].name == "DMG MORI"
