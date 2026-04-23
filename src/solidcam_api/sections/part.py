"""Part section mixin — CAM part metadata and creation."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass

from solidcam_api.enums import HomeOriginPosition, NewPartType, PartType
from solidcam_api.sections._base import _SectionBase


class PartSection(_SectionBase):
    """Mixin exposing the *Part* section of the SolidCAM Automation COM API.

    Covers reading metadata about the currently open CAM part (file path,
    part type, reference model), swapping the reference model, and creating
    brand-new CAM parts programmatically.

    This class is intended to be mixed into :class:`~solidcam_api.SolidCAMClient`
    alongside the other section mixins. It must not be instantiated directly.
    ``self._com`` is expected to be the live ``win32com`` dispatch object set by
    the concrete client class.
    """

    # ------------------------------------------------------------------
    # Read-only properties
    # ------------------------------------------------------------------

    @property
    def part_path(self) -> str:
        """Absolute file-system path of the currently open SolidCAM part.

        Named ``part_path`` rather than ``path`` to avoid shadowing
        :class:`pathlib.Path` in any mixed-in namespace.

        Returns:
            Absolute path to the open ``.prz`` file as a plain string.
        """
        return str(self._com.Path)

    @property
    def part_type(self) -> PartType | int:
        """Type of the currently open CAM part.

        Attempts to resolve the raw integer returned by the COM API to a
        :class:`~solidcam_api.enums.PartType` enum member. If the code is not
        recognised (e.g. introduced in a newer SolidCAM version), the raw
        ``int`` is returned unchanged so that calling code does not unexpectedly
        raise an exception.

        Returns:
            The matching :class:`~solidcam_api.enums.PartType` member, or the
            raw integer type code when the value is unknown.
        """
        raw = int(self._com.Type)
        try:
            return PartType(raw)
        except ValueError:
            return raw

    @property
    def reference_model(self) -> str:
        """Absolute file-system path of the CAD model referenced by the open part.

        The reference model is the CAD document (e.g. a SolidWorks part or
        assembly) from which the CAM part derives its geometry.

        Returns:
            Absolute path to the reference CAD model file as a plain string.
        """
        return str(self._com.ReferenceModel)

    # ------------------------------------------------------------------
    # Methods
    # ------------------------------------------------------------------

    def change_reference_model(self, model_path: str) -> None:
        """Replace the reference CAD model of the currently open part.

        Swaps the geometry source used by the open SolidCAM part to the
        document at *model_path*. This is useful in batch workflows where the
        same toolpath template is applied to a family of similar parts that
        differ only in their CAD geometry.

        Args:
            model_path: Absolute path to the replacement CAD model file.

        Raises:
            SolidCAMAPIError: When the COM call returns a falsy result,
                indicating that the reference model could not be changed.
        """
        result = self._com.ChangeReferenceModel(model_path)
        self._require_result(result, "ChangeReferenceModel")

    def create_new_part(
        self,
        name: str,
        path: str,
        part_type: NewPartType | int,
        machine_index: int,
        home_origin_position: HomeOriginPosition | int,
        inch: bool,
    ) -> None:
        """Create a new SolidCAM part and save it at the given path.

        Programmatically creates a ``.prz`` project file with the specified
        configuration. The active CAD document in the host application is used
        as the reference model for the new part.

        Args:
            name: Display name for the new CAM part as it will appear in the
                SolidCAM part tree.
            path: Absolute directory path where the new ``.prz`` file should
                be saved. The filename is derived from *name*.
            part_type: Machining type of the new part. Pass a
                :class:`~solidcam_api.enums.NewPartType` member or a raw
                integer for forward-compatibility with unknown part types.
            machine_index: Zero-based index of the machine to associate with
                the new part, as listed in the SolidCAM machine database.
            home_origin_position: Position of the home origin for milling
                parts. Pass a :class:`~solidcam_api.enums.HomeOriginPosition`
                member or a raw integer.
            inch: ``True`` to create the part using imperial (inch) units;
                ``False`` for metric (millimetre) units.

        Raises:
            SolidCAMAPIError: When the COM API reports a non-zero ``LastError``
                after the call, indicating that the part could not be created.
        """
        self._com.CreateNewPart(
            name,
            path,
            int(part_type),
            machine_index,
            int(home_origin_position),
            inch,
        )
        self._raise_on_error("CreateNewPart")
