from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Machine:
    """Represents a single machine entry from the SolidCAM machine database.

    Attributes:
        index: Zero-based index of the machine in the machines list.
        name:  Display name of the machine as reported by the COM API.
    """

    index: int
    name: str
