"""CAD section mixin — host-file and document helpers."""

from __future__ import annotations

from typing import TYPE_CHECKING

from solidcam_api._paths import StrPath, as_str
from solidcam_api.sections._base import _SectionBase

if TYPE_CHECKING:
    pass


class CADSection(_SectionBase):
    """Mixin exposing the *CAD* section of the SolidCAM Automation COM API.

    Covers opening host CAD files, querying the active document type, and
    generating preview images for PDM integrations.

    This class is intended to be mixed into :class:`~solidcam_api.SolidCAMClient`
    alongside the other section mixins. It must not be instantiated directly.
    ``self._com`` is expected to be the live ``win32com`` dispatch object set by
    the concrete client class.
    """

    # ------------------------------------------------------------------
    # Read-only properties
    # ------------------------------------------------------------------

    @property
    def is_active_doc_cam_part(self) -> bool:
        """Whether the currently active document in the CAD host is a CAM part.

        Returns:
            ``True`` if the active document is a SolidCAM part, ``False``
            otherwise (e.g. the active document is a plain CAD assembly or
            drawing, or no document is open).

        """
        return bool(self._com.IsActiveDocCamPart)

    # ------------------------------------------------------------------
    # Methods
    # ------------------------------------------------------------------

    def open_host_file(self, path: StrPath) -> None:
        """Open a file in the CAD host application.

        Instructs the running CAD host to open the document at *path*. The
        call blocks until the document has finished loading.

        Args:
            path: Absolute path to the CAD document to open (e.g. a
                ``.sldprt`` or ``.sldasm`` file for SolidWorks).

        Raises:
            SolidCAMAPIError: When the COM API reports a non-zero ``LastError``
                after the call, indicating that the file could not be opened.

        """
        self._com.OpenHostFile(as_str(path))
        self._raise_on_error("OpenHostFile")

    def render_preview(self, path: StrPath) -> None:
        """Generate a preview image of the active document via the CAD host.

        Invokes the CAD host to render and save a preview image to *path*.
        This is primarily intended for PDM (Product Data Management)
        integrations that require thumbnail images of CAM parts.

        Args:
            path: Absolute path where the rendered preview image should be
                saved. The image format is determined by the file extension
                (host-dependent).

        Raises:
            SolidCAMAPIError: When the COM API reports a non-zero ``LastError``
                after the call, indicating that the preview could not be
                generated.

        """
        self._com.RenderPreview(as_str(path))
        self._raise_on_error("RenderPreview")
