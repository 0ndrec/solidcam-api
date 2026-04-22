"""Geometry section mixin — coordinate systems, homes, geometry entries, stock, and targets."""

from __future__ import annotations

from solidcam_api.enums import HomeOriginPosition, StockDefineBy, TargetDefineBy
from solidcam_api.models import CoordSys, GeomEntry, HomeEntry
from solidcam_api.sections._base import _SectionBase


class GeometrySection(_SectionBase):
    """Mixin exposing the *Geometry* section of the SolidCAM Automation COM API.

    Covers:

    * **CAD coordinate systems** — named coordinate systems defined in the
      reference CAD model, used as machining origins.
    * **Home positions** — SolidCAM home / work-offset positions derived from
      the CAD model or created programmatically.
    * **Geometry entries** — named geometry elements (stock, targets, curves,
      surfaces) that drive NC operations.
    * **Stock and target creation** — programmatic creation of box/cylinder
      stock and target geometry.

    This class is intended to be mixed into :class:`~solidcam_api.SolidCAMClient`
    alongside the other section mixins.  It must not be instantiated directly.
    ``self._com`` is expected to be the live ``win32com`` dispatch object set by
    the concrete client class.
    """

    # ------------------------------------------------------------------
    # CAD coordinate-system properties and methods
    # ------------------------------------------------------------------

    @property
    def cad_coord_sys_count(self) -> int:
        """Number of coordinate systems defined in the reference CAD model.

        Returns:
            Non-negative integer count of CAD coordinate system entries.
        """
        return int(self._com.CADCoordSysCount)

    def get_cad_coord_sys_name(self, index: int) -> str:
        """Return the name of the CAD coordinate system at *index*.

        Args:
            index: Zero-based index of the CAD coordinate system.
                Must be in the range ``[0, cad_coord_sys_count - 1]``.

        Returns:
            Name of the CAD coordinate system as reported by the COM API.
        """
        return str(self._com.GetCADCoordSysName(index))

    def get_cad_coord_sys(self, index: int) -> CoordSys:
        """Return a :class:`~solidcam_api.models.CoordSys` for the CAD coord sys at *index*.

        Args:
            index: Zero-based index of the CAD coordinate system.
                Must be in the range ``[0, cad_coord_sys_count - 1]``.

        Returns:
            :class:`~solidcam_api.models.CoordSys` instance with ``index``
            and ``name`` populated.
        """
        return CoordSys(index=index, name=self.get_cad_coord_sys_name(index))

    def list_cad_coord_sys(self) -> list[CoordSys]:
        """Return all CAD coordinate systems defined in the reference CAD model.

        Returns:
            Ordered list of :class:`~solidcam_api.models.CoordSys` instances
            sorted by zero-based index.
        """
        return [self.get_cad_coord_sys(i) for i in range(self.cad_coord_sys_count)]

    # ------------------------------------------------------------------
    # Home-position properties and methods
    # ------------------------------------------------------------------

    @property
    def home_count(self) -> int:
        """Total number of home positions defined in the currently open CAM part.

        Returns:
            Non-negative integer count of home / work-offset entries.
        """
        return int(self._com.HomeCount)

    def get_home_name(self, index: int) -> str:
        """Return the name of the home position at *index*.

        Args:
            index: Zero-based index of the home position.
                Must be in the range ``[0, home_count - 1]``.

        Returns:
            Name of the home position as reported by the COM API.
        """
        return str(self._com.GetHomeName(index))

    def get_home(self, index: int) -> HomeEntry:
        """Return a :class:`~solidcam_api.models.HomeEntry` for the home at *index*.

        Args:
            index: Zero-based index of the home position.
                Must be in the range ``[0, home_count - 1]``.

        Returns:
            :class:`~solidcam_api.models.HomeEntry` instance with ``index``
            and ``name`` populated.
        """
        return HomeEntry(index=index, name=self.get_home_name(index))

    def list_home_positions(self) -> list[HomeEntry]:
        """Return all home positions defined in the currently open CAM part.

        Returns:
            Ordered list of :class:`~solidcam_api.models.HomeEntry` instances
            sorted by zero-based index.
        """
        return [self.get_home(i) for i in range(self.home_count)]

    def create_home(self, home_origin_position: HomeOriginPosition | int) -> None:
        """Create a new home at the specified origin position.

        Args:
            home_origin_position: Origin location for the new home.
                Use :class:`~solidcam_api.enums.HomeOriginPosition` values:
                ``TOP_CORNER`` (0), ``TOP_CENTER`` (1), or ``CAD_ORIGIN`` (2).

        Raises:
            SolidCAMAPIError: If the COM API reports a non-zero ``LastError``.
        """
        self._com.CreateHome(int(home_origin_position))
        self._raise_on_error("CreateHome")

    def create_home_by_cad(self, cad_home_name: str) -> None:
        """Create a new home based on a coordinate system defined in the CAD model.

        Args:
            cad_home_name: Name of the coordinate system in the CAD model to
                use as the new home origin.

        Raises:
            SolidCAMAPIError: If the COM API reports a non-zero ``LastError``
                or the operation returns a falsy result.
        """
        result = self._com.CreateHomeByCAD(cad_home_name)
        self._require_result(result, "CreateHomeByCAD")

    # ------------------------------------------------------------------
    # Geometry-entry properties and methods
    # ------------------------------------------------------------------

    @property
    def geom_count(self) -> int:
        """Total number of geometry entries defined in the currently open CAM part.

        Geometry entries include named stock bodies, target solids, curves, and
        surfaces that are referenced by NC operations.

        Returns:
            Non-negative integer count of geometry entries.
        """
        return int(self._com.GeomCount)

    def get_geom_name(self, index: int) -> str:
        """Return the name of the geometry entry at *index*.

        Args:
            index: Zero-based index of the geometry entry.
                Must be in the range ``[0, geom_count - 1]``.

        Returns:
            Name of the geometry entry as reported by the COM API.
        """
        return str(self._com.GetGeomName(index))

    def get_geom(self, index: int) -> GeomEntry:
        """Return a :class:`~solidcam_api.models.GeomEntry` for the entry at *index*.

        Args:
            index: Zero-based index of the geometry entry.
                Must be in the range ``[0, geom_count - 1]``.

        Returns:
            :class:`~solidcam_api.models.GeomEntry` instance with ``index``
            and ``name`` populated.
        """
        return GeomEntry(index=index, name=self.get_geom_name(index))

    def list_geometries(self) -> list[GeomEntry]:
        """Return all geometry entries defined in the currently open CAM part.

        Returns:
            Ordered list of :class:`~solidcam_api.models.GeomEntry` instances
            sorted by zero-based index.
        """
        return [self.get_geom(i) for i in range(self.geom_count)]

    # ------------------------------------------------------------------
    # Target creation
    # ------------------------------------------------------------------

    def create_target(
        self,
        name: str,
        define_by: TargetDefineBy | int = TargetDefineBy.ALL,
        model_without_envelope: bool = False,
        generate_envelope: bool = True,
        generate_section: bool = False,
        generate_mirror_envelope: bool = False,
        facet_tolerance: float = 0.0,
    ) -> None:
        """Create a target geometry from the currently active CAD solid(s).

        Args:
            name: Name to assign to the new target geometry entry.
            define_by: Which entities to include when defining the target.
                Use :class:`~solidcam_api.enums.TargetDefineBy` values:
                ``SOLID`` (0), ``SURFACE`` (1), or ``ALL`` (2).
                Defaults to ``ALL``.
            model_without_envelope: When ``True``, the 3-D model is used
                without generating an envelope.  Defaults to ``False``.
            generate_envelope: When ``True``, an envelope is generated for
                the target model.  Defaults to ``True``.
            generate_section: When ``True``, a cross-section is generated.
                Defaults to ``False``.
            generate_mirror_envelope: When ``True``, a mirrored envelope is
                generated.  Defaults to ``False``.
            facet_tolerance: Tessellation tolerance for the envelope mesh.
                Pass ``0.0`` (default) to use the value from SolidCAM settings.

        Raises:
            SolidCAMAPIError: If the COM API returns a falsy result or reports
                a non-zero ``LastError``.
        """
        result = self._com.CreateTarget(
            name,
            int(define_by),
            model_without_envelope,
            generate_envelope,
            generate_section,
            generate_mirror_envelope,
            facet_tolerance,
        )
        self._require_result(result, "CreateTarget")

    # ------------------------------------------------------------------
    # Stock creation
    # ------------------------------------------------------------------

    def create_stock_box(
        self,
        name: str,
        x_plus: float = 0.0,
        y_plus: float = 0.0,
        z_plus: float = 0.0,
        x_minus: float = 0.0,
        y_minus: float = 0.0,
        z_minus: float = 0.0,
        absolute: bool = False,
        define_by: StockDefineBy | int = StockDefineBy.ALL,
        add_3d_sketch: bool = False,
        generate_stock_envelope: bool = True,
        facet_tolerance: float = 0.0,
    ) -> None:
        """Create a rectangular box stock geometry.

        Args:
            name: Name to assign to the new stock geometry entry.
            x_plus: Box offset in the +X direction.
            y_plus: Box offset in the +Y direction.
            z_plus: Box offset in the +Z direction.
            x_minus: Box offset in the -X direction.
            y_minus: Box offset in the -Y direction.
            z_minus: Box offset in the -Z direction.
            absolute: When ``True``, offsets are treated as absolute
                coordinates; when ``False`` (default) they are relative
                offsets from the bounding box of the selected geometry.
            define_by: Which entities to include when defining the stock.
                Use :class:`~solidcam_api.enums.StockDefineBy` values:
                ``SOLID`` (0), ``SURFACE`` (1), or ``ALL`` (2).
                Defaults to ``ALL``.
            add_3d_sketch: When ``True``, a 3-D sketch of the stock box is
                added to the CAD model.  Defaults to ``False``.
            generate_stock_envelope: When ``True``, a stock envelope mesh is
                generated.  Defaults to ``True``.
            facet_tolerance: Tessellation tolerance for the stock mesh.
                Pass ``0.0`` (default) to use the value from SolidCAM settings.

        Raises:
            SolidCAMAPIError: If the COM API returns a falsy result or reports
                a non-zero ``LastError``.
        """
        result = self._com.CreateStockBox(
            name,
            x_plus,
            y_plus,
            z_plus,
            x_minus,
            y_minus,
            z_minus,
            absolute,
            int(define_by),
            add_3d_sketch,
            generate_stock_envelope,
            facet_tolerance,
        )
        self._require_result(result, "CreateStockBox")

    def create_stock_cylinder(
        self,
        name: str,
        right: float = 0.0,
        left: float = 0.0,
        internal_diameter: float = 0.0,
        external_diameter: float = 0.0,
        absolute: bool = False,
        define_by: StockDefineBy | int = StockDefineBy.ALL,
        add_3d_sketch: bool = False,
        generate_stock_envelope: bool = True,
        facet_tolerance: float = 0.0,
    ) -> None:
        """Create a cylindrical stock geometry.

        Primarily used for turning and mill-turn parts where the raw stock
        is a bar or tube of revolution.

        Args:
            name: Name to assign to the new stock geometry entry.
            right: Cylinder offset on the right (positive-Z) face.
            left: Cylinder offset on the left (negative-Z) face.
            internal_diameter: Inner diameter offset (for tube stock).
                Use ``0.0`` for solid bar stock.
            external_diameter: Outer diameter offset.
            absolute: When ``True``, dimensions are treated as absolute values;
                when ``False`` (default) they are offsets from the selected
                geometry's bounding cylinder.
            define_by: Which entities to include when defining the stock.
                Use :class:`~solidcam_api.enums.StockDefineBy` values:
                ``SOLID`` (0), ``SURFACE`` (1), or ``ALL`` (2).
                Defaults to ``ALL``.
            add_3d_sketch: When ``True``, a 3-D sketch of the cylinder is
                added to the CAD model.  Defaults to ``False``.
            generate_stock_envelope: When ``True``, a stock envelope mesh is
                generated.  Defaults to ``True``.
            facet_tolerance: Tessellation tolerance for the stock mesh.
                Pass ``0.0`` (default) to use the value from SolidCAM settings.

        Raises:
            SolidCAMAPIError: If the COM API returns a falsy result or reports
                a non-zero ``LastError``.
        """
        result = self._com.CreateStockCylinder(
            name,
            right,
            left,
            internal_diameter,
            external_diameter,
            absolute,
            int(define_by),
            add_3d_sketch,
            generate_stock_envelope,
            facet_tolerance,
        )
        self._require_result(result, "CreateStockCylinder")
