from __future__ import annotations


class SolidCAMError(Exception):
    """Base exception for all SolidCAM API errors."""


class SolidCAMConnectionError(SolidCAMError):
    """COM object creation failed or the SolidCAM DLL is not registered."""


class SolidCAMNotRunningError(SolidCAMError):
    """SolidCAM process is not currently running."""


class SolidCAMNotOpenError(SolidCAMError):
    """No CAM part is currently open in SolidCAM."""


class SolidCAMAPIError(SolidCAMError):
    """An API call to the SolidCAM COM interface returned a failure code."""

    method: str
    code: int
    description: str

    def __init__(self, method: str, code: int, description: str) -> None:
        self.method = method
        self.code = code
        self.description = description
        super().__init__(f"{method} failed: {description} (code {code})")
