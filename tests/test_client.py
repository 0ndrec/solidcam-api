from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from solidcam_api import SolidCAMClient

# ---------------------------------------------------------------------------
# Construction — is_connected state
# ---------------------------------------------------------------------------


def test_client_is_connected_when_com_object_injected() -> None:
    mock_com = MagicMock()
    client = SolidCAMClient(com_object=mock_com)
    assert client.is_connected is True


def test_client_is_disconnected_without_com_object() -> None:
    client = SolidCAMClient()
    assert client.is_connected is False


def test_client_com_attribute_set_when_injected() -> None:
    mock_com = MagicMock()
    client = SolidCAMClient(com_object=mock_com)
    assert client._com is mock_com


def test_client_com_attribute_none_before_connect() -> None:
    client = SolidCAMClient()
    assert client._com is None


def test_client_stores_custom_prog_id() -> None:
    client = SolidCAMClient(prog_id="Custom.ProgId")
    assert client.prog_id == "Custom.ProgId"


def test_client_default_prog_id() -> None:
    client = SolidCAMClient()
    assert client.prog_id == "SolidCAM.Automation"


# ---------------------------------------------------------------------------
# connect()
# ---------------------------------------------------------------------------


def test_connect_sets_com_object() -> None:
    with patch("solidcam_api._com.create_com_object") as mock_create:
        mock_create.return_value = MagicMock()
        client = SolidCAMClient()
        client.connect()
        assert client._com is mock_create.return_value


def test_connect_makes_client_connected() -> None:
    with patch("solidcam_api._com.create_com_object") as mock_create:
        mock_create.return_value = MagicMock()
        client = SolidCAMClient()
        client.connect()
        assert client.is_connected is True


def test_connect_passes_prog_id_to_factory() -> None:
    with patch("solidcam_api._com.create_com_object") as mock_create:
        mock_create.return_value = MagicMock()
        client = SolidCAMClient(prog_id="My.ProgId")
        client.connect()
        mock_create.assert_called_once_with("My.ProgId")


def test_connect_twice_is_noop_does_not_overwrite_com() -> None:
    with patch("solidcam_api._com.create_com_object") as mock_create:
        mock_create.return_value = MagicMock()
        client = SolidCAMClient()
        client.connect()
        first_com = client._com
        client.connect()
        assert client._com is first_com


def test_connect_twice_calls_factory_only_once() -> None:
    with patch("solidcam_api._com.create_com_object") as mock_create:
        mock_create.return_value = MagicMock()
        client = SolidCAMClient()
        client.connect()
        client.connect()
        mock_create.assert_called_once()


def test_connect_noop_when_com_already_injected() -> None:
    mock_com = MagicMock()
    client = SolidCAMClient(com_object=mock_com)
    with patch("solidcam_api._com.create_com_object") as mock_create:
        client.connect()
        mock_create.assert_not_called()
    assert client._com is mock_com


# ---------------------------------------------------------------------------
# disconnect()
# ---------------------------------------------------------------------------


def test_disconnect_clears_com_attribute(connected_client: SolidCAMClient) -> None:
    connected_client.disconnect()
    assert connected_client._com is None


def test_disconnect_makes_client_disconnected(connected_client: SolidCAMClient) -> None:
    connected_client.disconnect()
    assert connected_client.is_connected is False


def test_disconnect_when_already_disconnected_is_safe() -> None:
    client = SolidCAMClient()
    # Must not raise any exception.
    client.disconnect()


def test_disconnect_twice_is_safe(connected_client: SolidCAMClient) -> None:
    connected_client.disconnect()
    connected_client.disconnect()  # second call must not raise
    assert connected_client.is_connected is False


# ---------------------------------------------------------------------------
# __repr__
# ---------------------------------------------------------------------------


def test_repr_contains_connected_when_connected(connected_client: SolidCAMClient) -> None:
    assert "connected" in repr(connected_client)


def test_repr_contains_disconnected_when_not_connected() -> None:
    client = SolidCAMClient()
    assert "disconnected" in repr(client)


def test_repr_contains_prog_id(connected_client: SolidCAMClient) -> None:
    assert "SolidCAM.Automation" in repr(connected_client)


def test_repr_changes_after_disconnect(connected_client: SolidCAMClient) -> None:
    assert "connected" in repr(connected_client)
    connected_client.disconnect()
    assert "disconnected" in repr(connected_client)


def test_repr_is_string(connected_client: SolidCAMClient) -> None:
    assert isinstance(repr(connected_client), str)


# ---------------------------------------------------------------------------
# Context manager — __enter__ / __exit__
# ---------------------------------------------------------------------------


def test_context_manager_enter_calls_connect() -> None:
    with patch("solidcam_api._com.create_com_object") as mock_create:
        mock_create.return_value = MagicMock()
        client = SolidCAMClient()
        assert not client.is_connected
        with client:
            assert client.is_connected


def test_context_manager_enter_returns_client() -> None:
    with patch("solidcam_api._com.create_com_object") as mock_create:
        mock_create.return_value = MagicMock()
        client = SolidCAMClient()
        with client as ctx:
            assert ctx is client


def test_context_manager_exit_calls_disconnect() -> None:
    with patch("solidcam_api._com.create_com_object") as mock_create:
        mock_create.return_value = MagicMock()
        client = SolidCAMClient()
        with client:
            pass
        assert not client.is_connected


def test_context_manager_disconnects_on_exception() -> None:
    with patch("solidcam_api._com.create_com_object") as mock_create:
        mock_create.return_value = MagicMock()
        client = SolidCAMClient()
        with pytest.raises(RuntimeError):
            with client:
                raise RuntimeError("boom")
        assert not client.is_connected


def test_context_manager_does_not_suppress_exception() -> None:
    with patch("solidcam_api._com.create_com_object") as mock_create:
        mock_create.return_value = MagicMock()
        client = SolidCAMClient()
        with pytest.raises(ValueError, match="test value error"):
            with client:
                raise ValueError("test value error")


def test_context_manager_with_injected_com_enters_connected() -> None:
    mock_com = MagicMock()
    client = SolidCAMClient(com_object=mock_com)
    with client as ctx:
        assert ctx.is_connected
    assert not ctx.is_connected
