"""Typed Protocol describing the SolidCAM Automation COM interface.

This module defines a ``Protocol`` that describes the expected interface of the
SolidCAM Automation COM object (``scautom.dll``). Using a Protocol enables
static type checking (mypy) to catch typos in COM method names at development
time, while still allowing ``MagicMock`` objects to satisfy the protocol in tests.

The Protocol is intentionally incomplete — only the methods and properties used
by the solidcam-api package are defined. Additional members can be added as
needed.
"""

from __future__ import annotations

from typing import Protocol


class ScAutom(Protocol):
    """Static description of the SolidCAM.Automation COM interface.

    This Protocol captures the attributes and methods used by solidcam-api.
    It enables mypy to catch typos like ``Sychronize`` vs ``Synchronize`` at
    static analysis time.
    """

    # Read-only properties
    LastError: int
    LastErrorDescription: str
    LogFile: str
    pid: float
    Type: int
    Path: str
    ReferenceModel: str
    MachineCount: int
    OperationCount: int
    ToolCount: int

    # Methods
    def Open(self, part_path: str, model_path: str) -> int: ...
    def Close(self) -> None: ...
    def Exit(self) -> None: ...
    def Synchronize(self) -> None: ...
    def Calculate(self, only_not_calculated: bool) -> None: ...
    def GenerateGCode(self) -> None: ...
    def Save(self, folder: str) -> str: ...
    def IsSolidCamRunning(self) -> int: ...
    def StartApplication(self, path: str, wait_for_plugin: int) -> int: ...
    def StartSolidCAM(self) -> int: ...
    def CheckSynchronization(self) -> None: ...
    def CalculateOperations(self, operations: list[str], only_not_calculated: bool) -> None: ...
    def CalculateSingleOperation(self, number: int) -> None: ...
    def ChangePostProcessorDirectory(self, path: str) -> None: ...
    def SaveAs(self, path: str) -> int: ...
    def SaveToFolder(self, folder: str) -> str: ...
