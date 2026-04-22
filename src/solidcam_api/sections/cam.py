"""CAM section mixin — CAM part lifecycle and G-code generation."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass

from solidcam_api.sections._base import _SectionBase


class CAMSection(_SectionBase):
    """Mixin exposing the *CAM* section of the SolidCAM Automation COM API.

    Covers the full lifecycle of a SolidCAM part: opening, synchronisation,
    toolpath calculation, G-code generation, saving, and closing.

    This class is intended to be mixed into :class:`~solidcam_api.SolidCAMClient`
    alongside the other section mixins. It must not be instantiated directly.
    ``self._com`` is expected to be the live ``win32com`` dispatch object set by
    the concrete client class.
    """

    # ------------------------------------------------------------------
    # Open / close
    # ------------------------------------------------------------------

    def open(self, part_path: str, model_path: str = "") -> None:
        """Open a SolidCAM part file, optionally replacing its reference model.

        Loads the ``.cmp`` part at *part_path* into SolidCAM. When *model_path*
        is supplied, the part's reference CAD model is replaced with that file
        before the part is opened, which is useful for automated model-swap
        workflows.

        Args:
            part_path: Absolute path to the SolidCAM part file (``.cmp``).
            model_path: Absolute path to a replacement CAD model file.
                Pass an empty string (the default) to keep the existing
                reference model.

        Raises:
            SolidCAMAPIError: When the COM call returns a falsy result,
                indicating that the part could not be opened.
        """
        result = self._com.Open(part_path, model_path)
        self._require_result(result, "Open")

    def close(self) -> None:
        """Close the currently open SolidCAM part.

        Any unsaved changes are discarded. Call :meth:`save` or
        :meth:`save_as` first if the changes should be persisted.

        Raises:
            SolidCAMAPIError: When the COM API reports a non-zero ``LastError``
                after the call.
        """
        self._com.Close()
        self._raise_on_error("Close")

    def exit(self) -> None:
        """Close SolidCAM entirely and release the COM server.

        Shuts down the SolidCAM application. Any open parts are closed without
        saving. This should be the last call made through the API in a session.

        Raises:
            SolidCAMAPIError: When the COM API reports a non-zero ``LastError``
                after the call.
        """
        self._com.Exit()
        self._raise_on_error("Exit")

    # ------------------------------------------------------------------
    # Synchronisation
    # ------------------------------------------------------------------

    def check_synchronization(self) -> None:
        """Check whether the open part is synchronised with its reference model.

        Queries the synchronisation state without making any changes. Inspect
        :attr:`~solidcam_api.sections.GeneralSection.last_error` afterwards, or
        rely on the :exc:`~solidcam_api.exceptions.SolidCAMAPIError` raised here
        on failure.

        Raises:
            SolidCAMAPIError: When the COM API reports a non-zero ``LastError``
                after the call.
        """
        self._com.CheckSynchronization()
        self._raise_on_error("CheckSynchronization")

    def synchronize(self) -> None:
        """Synchronise the open part with its reference CAD model.

        Updates the SolidCAM part to reflect any geometry changes made to the
        associated CAD model since the part was last synchronised.

        Raises:
            SolidCAMAPIError: When the COM API reports a non-zero ``LastError``
                after the call.
        """
        self._com.Synchronize()
        self._raise_on_error("Synchronize")

    # ------------------------------------------------------------------
    # Calculation
    # ------------------------------------------------------------------

    def calculate(self, only_not_calculated: bool = False) -> None:
        """Calculate toolpaths for all operations in the open part.

        Args:
            only_not_calculated: When ``True``, only operations whose toolpath
                has not yet been calculated are processed; already-calculated
                operations are skipped. Defaults to ``False`` (recalculate all).

        Raises:
            SolidCAMAPIError: When the COM API reports a non-zero ``LastError``
                after the call.
        """
        self._com.Calculate(only_not_calculated)
        self._raise_on_error("Calculate")

    def calculate_operations(
        self,
        operations: list[str],
        only_not_calculated: bool = False,
    ) -> None:
        """Calculate toolpaths for a named subset of operations.

        Args:
            operations: List of operation names (as displayed in the SolidCAM
                operation tree) whose toolpaths should be calculated.
            only_not_calculated: When ``True``, operations in *operations* that
                already have a valid toolpath are skipped. Defaults to ``False``.

        Raises:
            SolidCAMAPIError: When the COM API reports a non-zero ``LastError``
                after the call.
        """
        self._com.CalculateOperations(operations, only_not_calculated)
        self._raise_on_error("CalculateOperations")

    def calculate_single_operation(self, number: int) -> None:
        """Calculate the toolpath for a single operation identified by its number.

        Args:
            number: One-based operation number as shown in the SolidCAM
                operation tree.

        Raises:
            SolidCAMAPIError: When the COM API reports a non-zero ``LastError``
                after the call.
        """
        self._com.CalculateSingleOperation(number)
        self._raise_on_error("CalculateSingleOperation")

    # ------------------------------------------------------------------
    # Post-processing / G-code
    # ------------------------------------------------------------------

    def change_post_processor_directory(self, path: str) -> None:
        """Override the directory from which SolidCAM loads post-processor files.

        Useful in automated environments where post-processor files reside in a
        non-default location (e.g. a network share or a job-specific folder).

        Args:
            path: Absolute path to the directory containing the post-processor
                (``.gpp`` / ``.gp_mac``) files.

        Raises:
            SolidCAMAPIError: When the COM API reports a non-zero ``LastError``
                after the call.
        """
        self._com.ChangePostProcessorDirectory(path)
        self._raise_on_error("ChangePostProcessorDirectory")

    def generate_gcode(self) -> None:
        """Run the post-processor and generate G-code for all operations.

        Output is written to the G-code output path configured in the open
        SolidCAM part. Ensure all operations have been calculated before
        calling this method; uncalculated operations may produce incomplete
        or erroneous output.

        Raises:
            SolidCAMAPIError: When the COM API reports a non-zero ``LastError``
                after the call.
        """
        self._com.GenerateGCode()
        self._raise_on_error("GenerateGCode")

    # ------------------------------------------------------------------
    # Save
    # ------------------------------------------------------------------

    def save(self, folder: str) -> str:
        """Save the open part to *folder* and return the resulting file path.

        SolidCAM derives the filename from the part name and writes the
        ``.cmp`` file into *folder*. The full path of the saved file is
        returned so that callers can record or forward the location without
        having to reconstruct it.

        Args:
            folder: Absolute path to the directory where the part should be
                saved.

        Returns:
            Full absolute path to the saved ``.cmp`` file.

        Raises:
            SolidCAMAPIError: When the COM call returns a falsy result,
                indicating that the save operation failed.
        """
        result = self._com.Save(folder)
        self._require_result(result, "Save")
        return str(result)

    def save_as(self, path: str) -> None:
        """Save the open part to an explicit file path.

        Unlike :meth:`save`, the caller supplies the complete destination path
        including the filename and extension. The part is saved at exactly that
        location.

        Args:
            path: Absolute destination path for the saved ``.cmp`` file,
                including the filename and extension.

        Raises:
            SolidCAMAPIError: When the COM call returns a falsy result,
                indicating that the save operation failed.
        """
        result = self._com.SaveAs(path)
        self._require_result(result, "SaveAs")

    def save_to_folder(self, folder: str) -> str:
        """Save the open part into *folder*, mirroring the source directory structure.

        Similar to :meth:`save`, but SolidCAM may replicate the original part's
        relative directory hierarchy inside *folder*. The full path of the saved
        file is returned.

        Args:
            folder: Absolute path to the root destination directory.

        Returns:
            Full absolute path to the saved ``.cmp`` file.

        Raises:
            SolidCAMAPIError: When the COM call returns a falsy result,
                indicating that the save operation failed.
        """
        result = self._com.SaveToFolder(folder)
        self._require_result(result, "SaveToFolder")
        return str(result)
