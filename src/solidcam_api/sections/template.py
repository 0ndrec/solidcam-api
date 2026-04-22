"""Template section mixin — operation templates and process templates."""

from __future__ import annotations

from solidcam_api.models import ProcessTemplateEntry, TemplateEntry
from solidcam_api.sections._base import _SectionBase


class TemplateSection(_SectionBase):
    """Mixin exposing the *Template* section of the SolidCAM Automation COM API.

    Covers querying and instantiating the two kinds of templates available in
    SolidCAM:

    * **Operation templates** — single-operation templates stored in the
      SolidCAM template library, represented as
      :class:`~solidcam_api.models.TemplateEntry` instances.
    * **Process templates** — multi-operation machining process templates that
      group several operations together, represented as
      :class:`~solidcam_api.models.ProcessTemplateEntry` instances.

    This class is intended to be mixed into :class:`~solidcam_api.SolidCAMClient`
    alongside the other section mixins.  It must not be instantiated directly.
    ``self._com`` is expected to be the live ``win32com`` dispatch object set by
    the concrete client class.
    """

    # ------------------------------------------------------------------
    # Operation-template properties and methods
    # ------------------------------------------------------------------

    @property
    def template_count(self) -> int:
        """Total number of operation templates available in the template library.

        Returns:
            Non-negative integer count of operation template entries reported
            by the COM API.
        """
        return int(self._com.TemplateCount)

    def get_template_name(self, index: int) -> str:
        """Return the display name of the operation template at *index*.

        Args:
            index: Zero-based index of the operation template.
                Must be in the range ``[0, template_count - 1]``.

        Returns:
            Display name of the operation template as reported by the COM API.
        """
        return str(self._com.GetTemplateName(index))

    def get_template(self, index: int) -> TemplateEntry:
        """Return a :class:`~solidcam_api.models.TemplateEntry` for the entry at *index*.

        Args:
            index: Zero-based index of the operation template.
                Must be in the range ``[0, template_count - 1]``.

        Returns:
            :class:`~solidcam_api.models.TemplateEntry` with ``index`` and
            ``name`` populated.
        """
        return TemplateEntry(index=index, name=self.get_template_name(index))

    def list_templates(self) -> list[TemplateEntry]:
        """Return all operation templates available in the template library.

        Returns:
            Ordered list of :class:`~solidcam_api.models.TemplateEntry`
            instances sorted by their zero-based index.
        """
        return [self.get_template(i) for i in range(self.template_count)]

    def create_job_from_template(
        self,
        template_name: str,
        geometry_name: str,
        sub_machine_index: int,
        index_of_jobs_with_combinations: int = 0,
    ) -> None:
        """Create a new NC operation from a single-operation template.

        Instantiates the operation defined by *template_name* and binds it to
        the specified geometry entry in the currently open CAM part.

        Args:
            template_name: Name of the operation template to instantiate (as
                returned by :meth:`get_template_name`).
            geometry_name: Name of the geometry to associate with the new
                operation (e.g. a stock or target name as seen in the
                SolidCAM geometry tree).
            sub_machine_index: Sub-machine index for multi-spindle or
                multi-turret setups.  Must be ``>= 1``.
            index_of_jobs_with_combinations: Index used when the template
                contains operation combinations.  Pass ``0`` when not
                applicable.

        Raises:
            :class:`~solidcam_api.exceptions.SolidCAMAPIError`: When the COM
                API reports a non-zero ``LastError`` after the call.
        """
        self._com.CreateJobFromTemplate(
            template_name,
            geometry_name,
            sub_machine_index,
            index_of_jobs_with_combinations,
        )
        self._raise_on_error("CreateJobFromTemplate")

    # ------------------------------------------------------------------
    # Process-template properties and methods
    # ------------------------------------------------------------------

    @property
    def process_template_count(self) -> int:
        """Total number of process templates available in the template library.

        Process templates differ from plain operation templates in that they
        encapsulate an entire machining *process* consisting of multiple
        coordinated operations.

        Returns:
            Non-negative integer count of process template entries reported
            by the COM API.
        """
        return int(self._com.ProcessTemplateCount)

    def get_process_template_name(self, index: int) -> str:
        """Return the display name of the process template at *index*.

        Args:
            index: Zero-based index of the process template.
                Must be in the range ``[0, process_template_count - 1]``.

        Returns:
            Display name of the process template as reported by the COM API.
        """
        return str(self._com.GetProcessTemplateName(index))

    def get_process_template(self, index: int) -> ProcessTemplateEntry:
        """Return a :class:`~solidcam_api.models.ProcessTemplateEntry` for *index*.

        Args:
            index: Zero-based index of the process template.
                Must be in the range ``[0, process_template_count - 1]``.

        Returns:
            :class:`~solidcam_api.models.ProcessTemplateEntry` with ``index``
            and ``name`` populated.
        """
        return ProcessTemplateEntry(
            index=index,
            name=self.get_process_template_name(index),
        )

    def list_process_templates(self) -> list[ProcessTemplateEntry]:
        """Return all process templates available in the template library.

        Returns:
            Ordered list of :class:`~solidcam_api.models.ProcessTemplateEntry`
            instances sorted by their zero-based index.
        """
        return [
            self.get_process_template(i) for i in range(self.process_template_count)
        ]

    def create_jobs_from_process_template(
        self,
        process_template_name: str,
        geometry_name: str,
        sub_machine_index: int,
        index_of_jobs_with_combinations: int = 0,
    ) -> None:
        """Create a set of NC operations from a process template.

        Instantiates all operations defined by *process_template_name* and
        binds them to the specified geometry entry in the currently open CAM
        part.  Process templates typically generate several coordinated
        operations in a single call.

        Args:
            process_template_name: Name of the process template to instantiate
                (as returned by :meth:`get_process_template_name`).
            geometry_name: Name of the geometry to associate with the new
                operations (e.g. a stock or target name as seen in the
                SolidCAM geometry tree).
            sub_machine_index: Sub-machine index for multi-spindle or
                multi-turret setups.  Must be ``>= 1``.
            index_of_jobs_with_combinations: Index used when the template
                contains operation combinations.  Pass ``0`` when not
                applicable.

        Raises:
            :class:`~solidcam_api.exceptions.SolidCAMAPIError`: When the COM
                API reports a non-zero ``LastError`` after the call.
        """
        self._com.CreateJobsFromProcessTemplate(
            process_template_name,
            geometry_name,
            sub_machine_index,
            index_of_jobs_with_combinations,
        )
        self._raise_on_error("CreateJobsFromProcessTemplate")
