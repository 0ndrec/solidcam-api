from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CoordSys:
    """A coordinate system entry in the CAM part."""

    index: int
    name: str


@dataclass(frozen=True)
class HomeEntry:
    """A home position entry in the CAM part."""

    index: int
    name: str


@dataclass(frozen=True)
class GeomEntry:
    """A geometry entry in the CAM part."""

    index: int
    name: str
