"""General section mixin — top-level SolidCAM application controls."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass

from solidcam_api.sections._base import _SectionBase


class GeneralSection(_SectionBase):
    """Mixin exposing the *General* section of the SolidCAM Automation COM API.

    Covers application lifecycle (start / detect running state), log-file
    configuration, and the PID of the hosted CAD process.

    This class is intended to be mixed into :class:`~solidcam_api.SolidCAMClient`
    alongside the other section mixins. It must not be instantiated directly.
    ``self._com`` is expected to be the live ``win32com`` dispatch object set by
    the concrete client class.
    """

    # ------------------------------------------------------------------
    # Read-only properties
    # ------------------------------------------------------------------

    @property
    def last_error(self) -> int:
        """Last error code reported by the COM API.

        Returns:
            Integer error code; ``0`` indicates no error.
        """
        return int(self._com.LastError or 0)

    @property
    def last_error_description(self) -> str:
        """Human-readable description of the last COM API error.

        Returns:
            Error description string, or an empty string when there is no error.
        """
        return str(self._com.LastErrorDescription or "")

    # ------------------------------------------------------------------
    # Read/write properties
    # ------------------------------------------------------------------

    @property
    def log_file(self) -> str:
        """Path to the SolidCAM automation log file.

        Setting this property redirects COM API log output to the given path.

        Returns:
            Absolute path to the current log file as a string.
        """
        return str(self._com.LogFile or "")

    @log_file.setter
    def log_file(self, value: str) -> None:
        """Set the path to the SolidCAM automation log file.

        Args:
            value: Absolute path to the desired log file location.
        """
        self._com.LogFile = value

    @property
    def pid(self) -> float:
        """Process ID of the hosted CAD application.

        The COM API exposes this as a floating-point value.

        Returns:
            PID of the running CAD host process.
        """
        return float(self._com.pid or 0)

    @pid.setter
    def pid(self, value: float) -> None:
        """Set the process ID of the hosted CAD application.

        Args:
            value: PID to assign.
        """
        self._com.pid = value

    # ------------------------------------------------------------------
    # Methods
    # ------------------------------------------------------------------

    def is_solidcam_running(self) -> bool:
        """Check whether SolidCAM is currently running.

        Polls the COM API to determine if the SolidCAM plugin or standalone
        application is active and responsive.

        Returns:
            ``True`` if SolidCAM is running, ``False`` otherwise.
        """
        return bool(self._com.IsSolidCamRunning())

    def start_application(self, path: str, wait_for_plugin: int = 0) -> None:
        """Start a host CAD application or the standalone SolidCAM executable.

        Passing an empty string for *path* with the SolidCAM plugin already
        loaded will start SolidCAM inside the running CAD host. *wait_for_plugin*
        should be left as ``0`` in all cases except when starting the standalone
        SolidCAM application, where the caller may want to wait for the plugin
        to finish initialising.

        Args:
            path: Absolute path to the CAD host or SolidCAM executable.
                Pass an empty string (``""``) to start SolidCAM via a plugin
                that is already loaded in the running CAD process.
            wait_for_plugin: Milliseconds to wait for the SolidCAM plugin to
                become ready after launch. Defaults to ``0`` (no wait).

        Raises:
            SolidCAMAPIError: When the COM call returns a falsy result,
                indicating that the application could not be started.
        """
        result = self._com.StartApplication(path, wait_for_plugin)
        self._require_result(result, "StartApplication")

    def start_solidcam(self) -> None:
        """Start the SolidCAM plugin inside an already-running CAD host.

        The CAD host application must already be open and have the SolidCAM
        plugin registered before calling this method. Use
        :meth:`start_application` first if the CAD host is not yet running.

        Raises:
            SolidCAMAPIError: When the COM call returns a falsy result,
                indicating that SolidCAM could not be started.
        """
        result = self._com.StartSolidCAM()
        self._require_result(result, "StartSolidCAM")
