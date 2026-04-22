"""Internal COM wrapper for the SolidCAM Automation API.

This module is the *only* place in the package that imports ``win32com``.
All other modules depend on this one through :func:`create_com_object` and
:func:`ensure_windows`, keeping the rest of the codebase clean and easily
testable via mocking.

Responsibilities
----------------
* Guard against importing on non-Windows platforms with an early, descriptive
  :class:`OSError`.
* Raise a clear :class:`~solidcam_api.exceptions.SolidCAMConnectionError`
  when ``pywin32`` is not installed or the COM DLL is not registered.
* Provide :func:`create_com_object` as the single factory used by
  :class:`~solidcam_api.client.SolidCAMClient`.
"""

from __future__ import annotations

import sys

# ---------------------------------------------------------------------------
# Platform guard — SolidCAM is a Windows-only application.
# ---------------------------------------------------------------------------


def ensure_windows() -> None:
    """Raise :class:`OSError` when the current platform is not Windows.

    Call this inside any function that would otherwise fail with a confusing
    ``ImportError`` or ``AttributeError`` on Linux/macOS.

    Raises:
        OSError: Always raised on non-Windows platforms.
    """
    if sys.platform != "win32":
        raise OSError(
            "solidcam-api requires Windows.  "
            "The SolidCAM Automation API is implemented as a Windows COM "
            "component (scautom.dll) and cannot run on this platform."
        )


# ---------------------------------------------------------------------------
# Public constants
# ---------------------------------------------------------------------------

#: COM ProgID for the SolidCAM Automation object.
SOLIDCAM_PROG_ID: str = "SolidCAM.Automation"


# ---------------------------------------------------------------------------
# Factory
# ---------------------------------------------------------------------------


def create_com_object(prog_id: str = SOLIDCAM_PROG_ID) -> object:
    """Create and return a live SolidCAM Automation COM dispatch object.

    This function performs three checks before returning the object:

    1. **Platform** — raises :class:`OSError` on non-Windows systems.
    2. **pywin32 availability** — raises :class:`ImportError` with an
       install hint if ``win32com`` cannot be imported.
    3. **COM instantiation** — raises
       :class:`~solidcam_api.exceptions.SolidCAMConnectionError` if
       ``win32com.client.Dispatch`` fails (e.g. DLL not registered).

    Args:
        prog_id: The COM ProgID to instantiate.  Defaults to
            ``"SolidCAM.Automation"``.  Override only in tests or when
            targeting a custom registration.

    Returns:
        A live ``win32com.client.CDispatch`` object bound to the running (or
        newly started) SolidCAM Automation server.

    Raises:
        OSError: When the current platform is not Windows.
        ImportError: When ``pywin32`` is not installed.
        ~solidcam_api.exceptions.SolidCAMConnectionError: When the COM object
            cannot be created (DLL not registered, SolidCAM not installed, or
            a COM initialisation error).
    """
    ensure_windows()

    try:
        import win32com.client  # type: ignore[import]
    except ImportError as exc:
        raise ImportError(
            "pywin32 is required by solidcam-api but is not installed.  "
            "Install it with:\n\n"
            "    pip install pywin32\n\n"
            "Then re-run the script."
        ) from exc

    try:
        return win32com.client.Dispatch(prog_id)
    except Exception as exc:
        # Import here to avoid a circular dependency at module load time.
        from solidcam_api.exceptions import SolidCAMConnectionError

        raise SolidCAMConnectionError(
            f"Failed to create COM object '{prog_id}'.  "
            "Possible causes:\n"
            "  • SolidCAM is not installed on this machine.\n"
            "  • scautom.dll has not been registered (run: "
            'regsvr32 "<SolidCAM dir>\\scautom.dll").\n'
            "  • The COM server is blocked by security or UAC policy.\n"
            f"Original error: {exc}"
        ) from exc
