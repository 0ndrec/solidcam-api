r"""Main SolidCAM client — assembles all section mixins into a single object.

The underlying COM object is created *lazily* inside :meth:`SolidCAMClient.connect`
(or on ``__enter__``), so the module can be safely imported on any platform
for documentation builds, static analysis, and unit-testing with mocks.
Platform and dependency checks only fire when a connection is actually attempted.
"""

from __future__ import annotations

from types import TracebackType
from typing import TYPE_CHECKING, Any

from solidcam_api.sections.cad import CADSection
from solidcam_api.sections.cam import CAMSection
from solidcam_api.sections.general import GeneralSection
from solidcam_api.sections.geometry import GeometrySection
from solidcam_api.sections.machine import MachineSection
from solidcam_api.sections.operation import OperationSection
from solidcam_api.sections.part import PartSection
from solidcam_api.sections.template import TemplateSection
from solidcam_api.sections.tool import ToolSection

if TYPE_CHECKING:
    pass

__all__ = ["SolidCAMClient"]

_PROG_ID = "SolidCAM.Automation"


class SolidCAMClient(
    GeneralSection,
    CADSection,
    CAMSection,
    MachineSection,
    PartSection,
    OperationSection,
    ToolSection,
    GeometrySection,
    TemplateSection,
):
    r"""High-level Python client for the SolidCAM Automation COM API.

    :class:`SolidCAMClient` composes all API sections — General, CAD, CAM,
    Machine, Part, Operation, Tool, Geometry, and Templates — into a single
    cohesive object.  Every public method and property defined by the section
    mixins is directly accessible on the client instance with no intermediate
    sub-objects.

    The underlying COM dispatch object (``SolidCAM.Automation``) is created
    lazily when :meth:`connect` is called (or when entering a ``with`` block).
    All platform and dependency checks are deferred to that point so the
    module can be imported freely on any OS.

    Typical usage — context manager (recommended)::

        with SolidCAMClient() as sc:
            sc.start_application(r"C:\Program Files\SolidWorks\SLDWORKS.exe")
            sc.open(r"C:\parts\my_part.prz")
            sc.calculate()
            sc.generate_gcode()
            sc.close()

    Manual lifecycle::

        sc = SolidCAMClient()
        sc.connect()
        try:
            sc.open(r"C:\parts\my_part.prz")
            sc.calculate()
            sc.generate_gcode()
        finally:
            sc.disconnect()

    Dependency injection / testing — pass a pre-built mock as *com_object*::

        import unittest.mock as mock

        fake_com = mock.MagicMock()
        sc = SolidCAMClient(com_object=fake_com)
        # sc._com is already set; connect() becomes a no-op
        assert sc.is_connected

    Attributes:
        prog_id: COM ProgID used when dispatching the automation object.
            Defaults to ``"SolidCAM.Automation"``.

    Raises:
        OSError: From :meth:`connect` when the host platform is not Windows.
        ImportError: From :meth:`connect` when ``pywin32`` is not installed.
        ~solidcam_api.exceptions.SolidCAMConnectionError: From :meth:`connect`
            when the COM object cannot be created (e.g. ``scautom.dll`` not
            registered).

    """

    def __init__(
        self,
        prog_id: str = _PROG_ID,
        *,
        com_object: Any = None,  # noqa: ANN401
    ) -> None:
        """Initialise the client without connecting to the COM object.

        The COM object is **not** created here unless *com_object* is supplied
        directly (e.g. for testing).  Call :meth:`connect` or use the client as
        a context manager to establish a live connection.

        Args:
            prog_id: COM ProgID to dispatch.  Override only when testing
                against a custom stub or a differently-registered DLL.
                Defaults to ``"SolidCAM.Automation"``.
            com_object: Optional pre-built COM dispatch object (or mock) to use
                instead of calling ``win32com.client.Dispatch``.  When supplied
                the client is considered connected immediately and :meth:`connect`
                becomes a no-op.

        """
        self.prog_id: str = prog_id
        self._com: Any = com_object  # None until connect(); or injected directly

    # ------------------------------------------------------------------
    # Connection lifecycle
    # ------------------------------------------------------------------

    def connect(self) -> None:
        """Create the underlying COM dispatch object and make the API available.

        After a successful call every method and property defined by the
        section mixins is usable.  Calling :meth:`connect` on an already-connected
        client (``is_connected`` is ``True``) is a safe no-op.

        Raises:
            OSError: When the current platform is not Windows.
            ImportError: When the ``pywin32`` package is not installed.
            ~solidcam_api.exceptions.SolidCAMConnectionError: If
                ``win32com.client.Dispatch`` raises any exception — typically
                because ``scautom.dll`` is not registered or SolidCAM is not
                installed.

        """
        if self._com is not None:
            return

        # Deferred platform + dependency checks via the internal _com module.
        from solidcam_api._com import create_com_object

        self._com = create_com_object(self.prog_id)

    def disconnect(self) -> None:
        """Release the reference to the underlying COM object.

        After this call all API methods will raise :exc:`AttributeError` until
        :meth:`connect` is called again.  Calling :meth:`disconnect` on a
        client that is not connected is a safe no-op.
        """
        self._com = None

    @property
    def is_connected(self) -> bool:
        """``True`` if the COM object is held and the client is ready to use.

        This property checks only that :meth:`connect` has been called and
        :meth:`disconnect` has not.  It does **not** verify that the SolidCAM
        process is still alive.  For a live liveness check use
        :meth:`is_solidcam_running`.
        """
        return self._com is not None

    # ------------------------------------------------------------------
    # Context-manager protocol
    # ------------------------------------------------------------------

    def __enter__(self) -> SolidCAMClient:
        """Connect to the COM object and return *self*.

        Enables the recommended pattern::

            with SolidCAMClient() as sc:
                sc.open(part_path)
                ...

        Raises:
            OSError: Propagated from :meth:`connect`.
            ImportError: Propagated from :meth:`connect`.
            ~solidcam_api.exceptions.SolidCAMConnectionError: Propagated from
                :meth:`connect`.

        """
        self.connect()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """Release the COM object regardless of whether an exception occurred.

        The COM reference is always dropped; any exception raised inside the
        ``with`` block propagates normally (this method returns ``None``,
        which is falsy, so exceptions are not suppressed).
        """
        self.disconnect()

    # ------------------------------------------------------------------
    # Dunder helpers
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        """Return a developer-friendly string representation of the client."""
        state = "connected" if self.is_connected else "disconnected"
        return f"SolidCAMClient(prog_id={self.prog_id!r}, state={state!r})"
