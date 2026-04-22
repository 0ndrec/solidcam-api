"""Operation section mixin — NC operation queries and manipulation."""

from __future__ import annotations

from solidcam_api.models import Operation
from solidcam_api.sections._base import _SectionBase


class OperationSection(_SectionBase):
    """Mixin exposing the *Operation* section of the SolidCAM Automation COM API.

    Covers querying the list of NC operations in the currently open CAM part,
    retrieving individual operation names and type codes, suppressing operations,
    and generating G-code for individual operations.

    This class is intended to be mixed into :class:`~solidcam_api.SolidCAMClient`
    alongside the other section mixins.  It must not be instantiated directly.
    ``self._com`` is expected to be the live ``win32com`` dispatch object set by
    the concrete client class.
    """

    # ------------------------------------------------------------------
    # Read-only properties
    # ------------------------------------------------------------------

    @property
    def operation_count(self) -> int:
        """Total number of NC operations in the currently open CAM part.

        Returns:
            Non-negative integer count of operations in the part's operation
            tree.
        """
        return int(self._com.OperationCount)

    @property
    def number_of_jobs_with_exclamation_sign(self) -> int:
        """Number of operations currently opened with an exclamation-sign warning.

        Operations that have an exclamation sign are typically in an invalid or
        uncalculated state and may require recalculation or manual review.

        Returns:
            Non-negative integer count of operations bearing an exclamation
            sign in the SolidCAM operation tree.
        """
        return int(self._com.NumberOfJobsOpenedWithExclamationSign)

    # ------------------------------------------------------------------
    # Single-operation accessors
    # ------------------------------------------------------------------

    def get_operation_name(self, index: int) -> str:
        """Return the display name of the operation at *index*.

        Args:
            index: Zero-based index of the operation in the operation tree.
                Must be in the range ``[0, operation_count - 1]``.

        Returns:
            Display name of the operation as shown in the SolidCAM operation
            tree.
        """
        return str(self._com.GetOperationName(index))

    def get_operation_type(self, index: int) -> int:
        """Return the raw integer type code of the operation at *index*.

        The raw code can be resolved to an
        :class:`~solidcam_api.enums.OperationType` member via
        :func:`~solidcam_api.enums.try_parse_operation_type`, or by accessing
        the :attr:`~solidcam_api.models.Operation.type` property on the
        :class:`~solidcam_api.models.Operation` returned by :meth:`get_operation`
        or :meth:`list_operations`.

        Args:
            index: Zero-based index of the operation in the operation tree.
                Must be in the range ``[0, operation_count - 1]``.

        Returns:
            Raw integer operation-type code as returned by the COM API.
        """
        return int(self._com.GetOperationType(index))

    def get_operation(self, index: int) -> Operation:
        """Return an :class:`~solidcam_api.models.Operation` for the entry at *index*.

        Fetches the name and type code for the operation at *index* and
        constructs a fully populated :class:`~solidcam_api.models.Operation`
        dataclass instance.

        Args:
            index: Zero-based index of the operation in the operation tree.
                Must be in the range ``[0, operation_count - 1]``.

        Returns:
            :class:`~solidcam_api.models.Operation` instance with ``index``,
            ``name``, and ``type_code`` populated.
        """
        return Operation(
            index=index,
            name=self.get_operation_name(index),
            type_code=self.get_operation_type(index),
        )

    def list_operations(self) -> list[Operation]:
        """Return all NC operations in the currently open CAM part.

        Iterates over every index from ``0`` to :attr:`operation_count` - 1,
        fetching each operation's name and type code, and constructs an
        :class:`~solidcam_api.models.Operation` dataclass for each entry.

        Returns:
            Ordered list of :class:`~solidcam_api.models.Operation` instances,
            one per operation in the part's operation tree, sorted by their
            zero-based index.
        """
        return [self.get_operation(i) for i in range(self.operation_count)]

    # ------------------------------------------------------------------
    # Operation manipulation
    # ------------------------------------------------------------------

    def suppress_operation(self, operation_name: str, suppress: bool) -> None:
        """Suppress or unsuppress a named operation.

        A suppressed operation is skipped during calculation and G-code
        generation without being deleted from the part.

        Args:
            operation_name: Exact name of the operation as it appears in the
                SolidCAM operation tree (case-sensitive).
            suppress: ``True`` to suppress the operation, ``False`` to
                unsuppress (re-enable) it.

        Raises:
            SolidCAMAPIError: If the COM API reports a non-zero ``LastError``
                after the call.
        """
        self._com.SuppressOperation(operation_name, suppress)
        self._raise_on_error("SuppressOperation")

    def generate_gcode_for_operation(
        self,
        operation_name: str,
        file_name: str,
    ) -> None:
        """Generate G-code for a single named operation and write it to *file_name*.

        Args:
            operation_name: Exact name of the operation as it appears in the
                SolidCAM operation tree (case-sensitive).
            file_name: Full path to the output G-code file.  The directory
                must already exist.

        Raises:
            SolidCAMAPIError: If the COM API reports a non-zero ``LastError``
                after the call, indicating that code generation failed.
        """
        self._com.GenerateGCodeForOperation(operation_name, file_name)
        self._raise_on_error("GenerateGCodeForOperation")
