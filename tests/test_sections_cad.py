from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from solidcam_api import SolidCAMClient
from solidcam_api.exceptions import SolidCAMAPIError


def test_is_active_doc_cam_part_returns_true(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.IsActiveDocCamPart = True
    assert connected_client.is_active_doc_cam_part is True


def test_is_active_doc_cam_part_returns_false(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.IsActiveDocCamPart = False
    assert connected_client.is_active_doc_cam_part is False


def test_open_host_file_calls_com(connected_client: SolidCAMClient, fake_com: MagicMock) -> None:
    fake_com.LastError = 0
    connected_client.open_host_file(r"C:\model.sldprt")
    fake_com.OpenHostFile.assert_called_once()


def test_open_host_file_raises_on_error(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.LastError = 1
    fake_com.LastErrorDescription = "cannot open"
    with pytest.raises(SolidCAMAPIError):
        connected_client.open_host_file(r"C:\model.sldprt")


def test_render_preview_calls_com(connected_client: SolidCAMClient, fake_com: MagicMock) -> None:
    fake_com.LastError = 0
    connected_client.render_preview(r"C:\preview.png")
    fake_com.RenderPreview.assert_called_once()


def test_render_preview_raises_on_error(
    connected_client: SolidCAMClient, fake_com: MagicMock
) -> None:
    fake_com.LastError = 1
    with pytest.raises(SolidCAMAPIError):
        connected_client.render_preview(r"C:\preview.png")
