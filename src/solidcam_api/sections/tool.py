"""Tool section mixin — part tool library queries and tool-sheet generation."""

from __future__ import annotations

from solidcam_api.models import Tool
from solidcam_api.sections._base import _SectionBase


class ToolSection(_SectionBase):
    """Mixin exposing the *Tool* section of the SolidCAM Automation COM API.

    Covers querying the tool library attached to the currently open CAM part,
    retrieving individual tool names, type codes, and tags, assigning tools
    to operations, and generating tool sheets.

    This class is intended to be mixed into :class:`~solidcam_api.SolidCAMClient`
    alongside the other section mixins.  It must not be instantiated directly.
    ``self._com`` is expected to be the live ``win32com`` dispatch object set by
    the concrete client class.
    """

    # ------------------------------------------------------------------
    # Read-only count properties
    # ------------------------------------------------------------------

    @property
    def tool_count(self) -> int:
        """Total number of tools defined in the currently open CAM part.

        Returns:
            Non-negative integer count of tool entries present in the part's
            tool library.

        """
        return int(self._com.ToolCount)

    @property
    def tool_sheet_count(self) -> int:
        """Total number of tool-sheet templates available.

        Returns:
            Non-negative integer count of tool-sheet template entries (e.g.
            ``Sheet_Full_HTML``, ``Sheet_Full_RTF``) known to SolidCAM.

        """
        return int(self._com.ToolSheetCount)

    # ------------------------------------------------------------------
    # Tool query methods
    # ------------------------------------------------------------------

    def get_tool_name(self, index: int) -> str:
        """Return the display name of the tool at *index*.

        Args:
            index: Zero-based index of the tool in the part's tool library.
                Must be in the range ``[0, tool_count - 1]``.

        Returns:
            Display name of the tool as shown in SolidCAM.

        """
        return str(self._com.GetToolName(index))

    def get_tool_type(self, index: int) -> int:
        """Return the raw integer type code of the tool at *index*.

        The raw code corresponds to :class:`~solidcam_api.enums.ToolType`:

        * ``0`` — :attr:`~solidcam_api.enums.ToolType.NONE`
        * ``1`` — :attr:`~solidcam_api.enums.ToolType.MILLING`
        * ``2`` — :attr:`~solidcam_api.enums.ToolType.TURNING`
        * ``3`` — :attr:`~solidcam_api.enums.ToolType.WIRE_CUT`

        Args:
            index: Zero-based index of the tool in the part's tool library.
                Must be in the range ``[0, tool_count - 1]``.

        Returns:
            Raw integer tool-type code as returned by the COM API.

        """
        return int(self._com.GetToolType(index))

    def get_tool_tag(
        self,
        number: int,
        position: int,
        station: int = 0,
        turret: int = 0,
    ) -> int:
        """Return the unique tag (ID) of a tool identified by its address.

        The tag returned by this method is used as the *tool_tag* argument in
        :meth:`set_operation_tool` and :meth:`get_operation_tool_tag`.

        Args:
            number: Tool number as shown in the tool table.
            position: Sub-position of the tool (e.g. insert position for
                multi-edge turning tools).
            station: Position in the turret magazine.  Pass ``0`` if not
                applicable.
            turret: Turret tag identifying which turret the tool belongs to.
                Pass ``0`` if not applicable or for single-turret machines.

        Returns:
            Integer tool tag (unique identifier) that can be passed to
            :meth:`set_operation_tool`.

        Raises:
            SolidCAMAPIError: When the COM API reports a non-zero
                ``LastError`` after the call.

        """
        tag = int(self._com.GetToolTag(number, position, station, turret))
        self._raise_on_error("GetToolTag")
        return tag

    def get_tool(self, index: int) -> Tool:
        """Return a :class:`~solidcam_api.models.Tool` for the entry at *index*.

        Fetches the name and type code for the tool at the given index and
        constructs a fully populated :class:`~solidcam_api.models.Tool`
        dataclass instance.

        Args:
            index: Zero-based index of the tool in the part's tool library.
                Must be in the range ``[0, tool_count - 1]``.

        Returns:
            :class:`~solidcam_api.models.Tool` instance with ``index``,
            ``name``, and ``type_code`` populated.

        """
        return Tool(
            index=index,
            name=self.get_tool_name(index),
            type_code=self.get_tool_type(index),
        )

    def list_tools(self) -> list[Tool]:
        """Return all tools defined in the currently open CAM part.

        Iterates over every index from ``0`` to :attr:`tool_count` - 1,
        fetching each tool's name and type code, and constructs a
        :class:`~solidcam_api.models.Tool` dataclass for each entry.

        Returns:
            Ordered list of :class:`~solidcam_api.models.Tool` instances,
            one per tool in the part's tool library, sorted by their
            zero-based index.

        """
        return [self.get_tool(i) for i in range(self.tool_count)]

    # ------------------------------------------------------------------
    # Tool-operation assignment
    # ------------------------------------------------------------------

    def set_operation_tool(self, operation_name: str, tool_tag: int) -> None:
        """Assign a tool to a named operation.

        Associates the tool identified by *tool_tag* (obtained from
        :meth:`get_tool_tag`) with the operation identified by
        *operation_name*.  After this call the operation will use the
        specified tool when calculating toolpaths and generating G-code.

        Args:
            operation_name: Name of the operation as it appears in the
                SolidCAM operation tree.
            tool_tag: Unique tool identifier returned by :meth:`get_tool_tag`.

        Raises:
            SolidCAMAPIError: When the COM API reports a non-zero
                ``LastError`` after the call.

        """
        self._com.SetOperationTool(operation_name, tool_tag)
        self._raise_on_error("SetOperationTool")

    def get_operation_tool_tag(self, operation_name: str) -> int:
        """Return the tag of the tool currently assigned to an operation.

        Args:
            operation_name: Name of the operation as it appears in the
                SolidCAM operation tree.

        Returns:
            Integer tool tag identifying the tool currently used by the
            named operation.  This tag can be passed back to
            :meth:`set_operation_tool` or compared against values from
            :meth:`get_tool_tag`.

        Raises:
            SolidCAMAPIError: When the COM API reports a non-zero
                ``LastError`` after the call.

        """
        tag = int(self._com.GetOperationToolTag(operation_name))
        self._raise_on_error("GetOperationToolTag")
        return tag

    # ------------------------------------------------------------------
    # Tool-sheet generation
    # ------------------------------------------------------------------

    def get_tool_sheet_name(self, index: int) -> str:
        """Return the name of the tool-sheet template at *index*.

        Common template names include ``Sheet_Full_HTML`` and
        ``Sheet_Full_RTF``.

        Args:
            index: Zero-based index of the tool-sheet template.  Must be in
                the range ``[0, tool_sheet_count - 1]``.

        Returns:
            Template name string as known to SolidCAM.

        """
        return str(self._com.GetToolSheetName(index))

    def list_tool_sheet_names(self) -> list[str]:
        """Return the names of all available tool-sheet templates.

        Convenience wrapper that iterates over every index from ``0`` to
        :attr:`tool_sheet_count` - 1 and collects the template names.

        Returns:
            Ordered list of template name strings.

        """
        return [self.get_tool_sheet_name(i) for i in range(self.tool_sheet_count)]

    def generate_tool_sheet(self, template_name: str) -> None:
        """Generate a tool sheet using the specified template.

        Produces a tool-sheet document for the currently open CAM part using
        the named template (e.g. ``"Sheet_Full_HTML"`` or
        ``"Sheet_Full_RTF"``).  Use :meth:`list_tool_sheet_names` to discover
        available template names.

        Args:
            template_name: Name of the tool-sheet template to use when
                generating the document.

        Raises:
            SolidCAMAPIError: When the COM API reports a non-zero
                ``LastError`` after the call.

        """
        self._com.GenerateToolSheet(template_name)
        self._raise_on_error("GenerateToolSheet")
