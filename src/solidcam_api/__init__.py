"""solidcam-api — Python middleware for the SolidCAM Automation COM API.

This package provides a fully-typed, Pythonic interface to the SolidCAM
Automation API (``scautom.dll``), a Windows COM component that ships with
SolidCAM and exposes batch-processing capabilities such as opening CAM parts,
changing reference models, calculating toolpaths, and generating G-code.

Typical usage
-------------

.. code-block:: python

    from solidcam_api import SolidCAMClient

    with SolidCAMClient() as sc:
        sc.start_application(r"C:\\Program Files\\SolidWorks\\SLDWORKS.exe")
        sc.open(r"C:\\parts\\my_part.sldprt")
        sc.synchronize()
        sc.calculate()
        sc.generate_gcode()
        sc.close()

Public surface
--------------

:class:`~solidcam_api.client.SolidCAMClient`
    The main entry-point.  Inherits every section mixin so all API methods and
    properties are available directly on the client instance.

Enumerations (``solidcam_api.enums``)
    :class:`~solidcam_api.enums.PartType`,
    :class:`~solidcam_api.enums.NewPartType`,
    :class:`~solidcam_api.enums.HomeOriginPosition`,
    :class:`~solidcam_api.enums.StockDefineBy`,
    :class:`~solidcam_api.enums.TargetDefineBy`,
    :class:`~solidcam_api.enums.ToolType`,
    :class:`~solidcam_api.enums.OperationType`,
    :class:`~solidcam_api.enums.WireCutOperationType`

Data models (``solidcam_api.models``)
    :class:`~solidcam_api.models.Machine`,
    :class:`~solidcam_api.models.Operation`,
    :class:`~solidcam_api.models.Tool`,
    :class:`~solidcam_api.models.CoordSys`,
    :class:`~solidcam_api.models.HomeEntry`,
    :class:`~solidcam_api.models.GeomEntry`,
    :class:`~solidcam_api.models.TemplateEntry`,
    :class:`~solidcam_api.models.ProcessTemplateEntry`

Exceptions (``solidcam_api.exceptions``)
    :class:`~solidcam_api.exceptions.SolidCAMError`,
    :class:`~solidcam_api.exceptions.SolidCAMConnectionError`,
    :class:`~solidcam_api.exceptions.SolidCAMNotRunningError`,
    :class:`~solidcam_api.exceptions.SolidCAMNotOpenError`,
    :class:`~solidcam_api.exceptions.SolidCAMAPIError`
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Package metadata
# ---------------------------------------------------------------------------

__version__: str = "0.1.0"
__author__: str = "0ndrec"
__email__: str = "byeexs@gmail.com"
__license__: str = "MIT"

# ---------------------------------------------------------------------------
# Client
# ---------------------------------------------------------------------------

from solidcam_api.client import SolidCAMClient

# ---------------------------------------------------------------------------
# Enumerations
# ---------------------------------------------------------------------------
from solidcam_api.enums import (
    HomeOriginPosition,
    NewPartType,
    OperationType,
    PartType,
    StockDefineBy,
    TargetDefineBy,
    ToolType,
    WireCutOperationType,
    try_parse_operation_type,
)

# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------
from solidcam_api.exceptions import (
    SolidCAMAPIError,
    SolidCAMConnectionError,
    SolidCAMError,
    SolidCAMNotOpenError,
    SolidCAMNotRunningError,
)

# ---------------------------------------------------------------------------
# Data models
# ---------------------------------------------------------------------------
from solidcam_api.models import (
    CoordSys,
    GeomEntry,
    HomeEntry,
    Machine,
    Operation,
    ProcessTemplateEntry,
    TemplateEntry,
    Tool,
)

# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

__all__: list[str] = [
    # Client
    "SolidCAMClient",
    # Exceptions
    "SolidCAMError",
    "SolidCAMConnectionError",
    "SolidCAMNotRunningError",
    "SolidCAMNotOpenError",
    "SolidCAMAPIError",
    # Enumerations
    "PartType",
    "NewPartType",
    "HomeOriginPosition",
    "StockDefineBy",
    "TargetDefineBy",
    "ToolType",
    "OperationType",
    "WireCutOperationType",
    "try_parse_operation_type",
    # Data models
    "Machine",
    "Operation",
    "Tool",
    "CoordSys",
    "HomeEntry",
    "GeomEntry",
    "TemplateEntry",
    "ProcessTemplateEntry",
]
