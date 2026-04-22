"""Section mixin classes for the SolidCAM Automation COM API.

Each section is a mixin class whose methods delegate to ``self._com`` — the
raw ``win32com`` dispatch object that the concrete
:class:`~solidcam_api.SolidCAMClient` sets during initialisation.

Importing from this sub-package gives access to all nine section mixins:

.. code-block:: python

    from solidcam_api.sections import (
        GeneralSection,
        CADSection,
        CAMSection,
        MachineSection,
        PartSection,
        OperationSection,
        ToolSection,
        GeometrySection,
        TemplateSection,
    )
"""

from __future__ import annotations

from solidcam_api.sections._base import _SectionBase
from solidcam_api.sections.cad import CADSection
from solidcam_api.sections.cam import CAMSection
from solidcam_api.sections.general import GeneralSection
from solidcam_api.sections.geometry import GeometrySection
from solidcam_api.sections.machine import MachineSection
from solidcam_api.sections.operation import OperationSection
from solidcam_api.sections.part import PartSection
from solidcam_api.sections.template import TemplateSection
from solidcam_api.sections.tool import ToolSection

__all__: list[str] = [
    "_SectionBase",
    "GeneralSection",
    "CADSection",
    "CAMSection",
    "MachineSection",
    "PartSection",
    "OperationSection",
    "ToolSection",
    "GeometrySection",
    "TemplateSection",
]
