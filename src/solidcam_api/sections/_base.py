"""Base mixin providing COM error-checking helpers."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    pass

logger = logging.getLogger("solidcam_api")


class _SectionBase:
    """Base mixin for all section classes.

    Requires that the concrete class sets ``self._com`` to the live win32com
    dispatch object before any section method is called.
    """

    _com: Any  # provided by SolidCAMClient via MRO

    def _raise_on_error(self, method: str) -> None:
        """Raise :exc:`~solidcam_api.exceptions.SolidCAMAPIError` if ``LastError != 0``.

        Args:
            method: Name of the calling API method, included in the exception
                message to aid debugging.

        Raises:
            SolidCAMAPIError: When ``self._com.LastError`` is non-zero.

        """
        from solidcam_api.exceptions import SolidCAMAPIError

        code = int(self._com.LastError or 0)
        if code != 0:
            desc = str(self._com.LastErrorDescription or "")
            logger.error("COM call %s failed: [%d] %s", method, code, desc)
            raise SolidCAMAPIError(method, code, desc)
        logger.debug("COM call %s OK", method)

    def _require_result(self, result: Any, method: str) -> None:  # noqa: ANN401
        """Raise :exc:`~solidcam_api.exceptions.SolidCAMAPIError` if *result* is falsy.

        Falsy values (``0``, ``False``, empty string, ``None``) are treated as
        a failure indicator returned by certain COM methods that do not set
        ``LastError`` but instead return a sentinel on failure.

        Args:
            result: The value returned by the COM method call.
            method: Name of the calling API method, included in the exception
                message to aid debugging.

        Raises:
            SolidCAMAPIError: When *result* is falsy.

        """
        from solidcam_api.exceptions import SolidCAMAPIError

        if not result:
            code = int(self._com.LastError or 0)
            desc = str(self._com.LastErrorDescription or "")
            raise SolidCAMAPIError(method, code, desc)
