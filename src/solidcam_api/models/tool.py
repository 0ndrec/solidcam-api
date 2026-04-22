from __future__ import annotations

from dataclasses import dataclass

from solidcam_api.enums import ToolType


@dataclass(frozen=True)
class Tool:
    """Represents a single tool entry from the SolidCAM tool library.

    Attributes:
        index: Zero-based position of the tool in the part's tool list.
        name: Display name of the tool as shown in SolidCAM.
        type_code: Raw integer tool-type code returned by the COM API.
    """

    index: int
    name: str
    type_code: int

    @property
    def type(self) -> ToolType | int:
        """Resolved :class:`~solidcam_api.enums.ToolType` for this tool.

        Returns the matching enum member when the code is recognised, or
        the raw ``int`` value unchanged for any future/unknown tool types
        so that calling code does not unexpectedly raise an exception.
        """
        try:
            return ToolType(self.type_code)
        except ValueError:
            return self.type_code
