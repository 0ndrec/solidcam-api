from __future__ import annotations

from dataclasses import dataclass

from solidcam_api.enums import OperationType, try_parse_operation_type


@dataclass(frozen=True)
class Operation:
    """Represents a single NC operation in the active CAM part.

    Attributes:
        index:     Zero-based position of the operation in the operations list.
        name:      Display name of the operation as shown in the SolidCAM tree.
        type_code: Raw integer type code returned by the COM API.
    """

    index: int
    name: str
    type_code: int

    @property
    def type(self) -> OperationType | int:
        """Resolved operation type.

        Returns the matching :class:`~solidcam_api.enums.OperationType` member
        when the code is recognised, or the raw :attr:`type_code` integer when
        the code is unknown (e.g. introduced in a newer SolidCAM version).
        """
        return try_parse_operation_type(self.type_code)
