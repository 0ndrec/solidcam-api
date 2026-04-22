from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from solidcam_api import SolidCAMClient


@pytest.fixture
def connected_client() -> SolidCAMClient:
    """Return a SolidCAMClient wired to a MagicMock COM object.

    The mock starts with LastError = 0 and LastErrorDescription = "" so that
    every _raise_on_error / _require_result call is a no-op unless the test
    itself overrides those attributes.
    """
    com = MagicMock(name="fake_com")
    com.LastError = 0
    com.LastErrorDescription = ""
    return SolidCAMClient(com_object=com)


@pytest.fixture
def fake_com(connected_client: SolidCAMClient) -> MagicMock:
    """Return the MagicMock COM object held by *connected_client*.

    Because both fixtures share the same pytest function scope, requesting
    both ``connected_client`` and ``fake_com`` in the same test always yields
    the client and its internal mock — never two separate instances.
    """
    return connected_client._com  # type: ignore[return-value]
