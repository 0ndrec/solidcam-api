"""Machine section mixin — machine database queries and selection."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass

from solidcam_api.models import Machine
from solidcam_api.sections._base import _SectionBase


class MachineSection(_SectionBase):
    """Mixin exposing the *Machine* section of the SolidCAM Automation COM API.

    Covers querying the machine database, reading the number of configured
    machines, retrieving machine names by index, and getting or setting the
    currently active machine.

    This class is intended to be mixed into :class:`~solidcam_api.SolidCAMClient`
    alongside the other section mixins. It must not be instantiated directly.
    ``self._com`` is expected to be the live ``win32com`` dispatch object set by
    the concrete client class.
    """

    # ------------------------------------------------------------------
    # Read-only properties
    # ------------------------------------------------------------------

    @property
    def machine_count(self) -> int:
        """Total number of machines registered in the SolidCAM machine database.

        Returns:
            Non-negative integer count of available machines.
        """
        return int(self._com.MachineCount)

    @property
    def current_machine_name(self) -> str:
        """Display name of the currently active machine.

        Returns:
            Name string of the active machine as reported by the COM API.
        """
        return str(self._com.CurrentMachineName)

    # ------------------------------------------------------------------
    # Read/write properties
    # ------------------------------------------------------------------

    @property
    def current_machine(self) -> int:
        """Zero-based index of the currently active machine.

        Setting this property switches the active machine used for subsequent
        CAM operations in the open part.

        Returns:
            Zero-based index of the active machine in the machine database.
        """
        return int(self._com.CurrentMachine)

    @current_machine.setter
    def current_machine(self, value: int) -> None:
        """Set the currently active machine by its zero-based index.

        Args:
            value: Zero-based index of the machine to activate. Must be in the
                range ``[0, machine_count - 1]``.
        """
        self._com.CurrentMachine = value

    # ------------------------------------------------------------------
    # Methods
    # ------------------------------------------------------------------

    def get_machine_name(self, index: int) -> str:
        """Return the display name of the machine at *index*.

        Args:
            index: Zero-based index of the machine in the SolidCAM machine
                database. Must be in the range ``[0, machine_count - 1]``.

        Returns:
            Display name of the machine as reported by the COM API.
        """
        return str(self._com.GetMachineName(index))

    def list_machines(self) -> list[Machine]:
        """Return all machines registered in the SolidCAM machine database.

        Iterates over every index from ``0`` to :attr:`machine_count` - 1,
        fetching each machine's name via :meth:`get_machine_name`, and
        constructs a :class:`~solidcam_api.models.Machine` dataclass for each
        entry.

        Returns:
            Ordered list of :class:`~solidcam_api.models.Machine` instances,
            one per registered machine, sorted by their zero-based index.
        """
        return [
            Machine(index=i, name=self.get_machine_name(i))
            for i in range(self.machine_count)
        ]
