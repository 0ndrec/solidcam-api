from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TemplateEntry:
    """A single operation template entry returned by the SolidCAM COM API.

    Attributes:
        index: Zero-based position of the template in the template list.
        name:  Display name of the template as reported by SolidCAM.

    """

    index: int
    name: str


@dataclass(frozen=True)
class ProcessTemplateEntry:
    """A single process-template entry returned by the SolidCAM COM API.

    Process templates (sometimes called *machining process templates*) group
    multiple operations together and differ from plain operation templates.

    Attributes:
        index: Zero-based position of the process template in the list.
        name:  Display name of the process template as reported by SolidCAM.

    """

    index: int
    name: str
