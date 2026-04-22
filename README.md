# solidcam-api

A fully-typed Python middleware library for the **SolidCAM Automation COM API** (`scautom.dll`).

`solidcam-api` wraps every section of the SolidCAM Automation API — General, CAD, CAM, Machine,
Part, Operation, Tool, Geometry, and Templates — in a clean, Pythonic interface with:

- Full **type annotations** and a `py.typed` marker (PEP 561)
- **Frozen dataclasses** for all result objects
- **`IntEnum`** constants for all integer codes
- A **context-manager**-friendly client
- Dependency injection / mock support for **unit testing without SolidCAM**

> **Platform note** — SolidCAM is a Windows application.  
> The COM layer is only active on Windows; the package can be *imported* on any OS for
> documentation builds, static analysis, and testing with mocks.

---

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Quick start](#quick-start)
- [Usage examples](#usage-examples)
  - [Open a part and generate G-code](#open-a-part-and-generate-g-code)
  - [Change the reference model and recalculate](#change-the-reference-model-and-recalculate)
  - [List machines, operations, and tools](#list-machines-operations-and-tools)
  - [Create stock and target geometry](#create-stock-and-target-geometry)
  - [Apply a process template](#apply-a-process-template)
  - [Generate a tool sheet](#generate-a-tool-sheet)
- [API overview](#api-overview)
- [Error handling](#error-handling)
- [Testing without SolidCAM](#testing-without-solidcam)
- [Contributing](#contributing)
- [License](#license)

---

## Requirements

| Requirement | Version |
|---|---|
| Python | ≥ 3.13 |
| pywin32 | ≥ 307 (Windows only) |
| SolidCAM | any version with `scautom.dll` registered |

Before using the library, the SolidCAM COM server must be registered:

```bat
regsvr32 "C:\Program Files\SolidCAM\scautom.dll"
```

This is done automatically by the SolidCAM installer.

---

## Installation

```bash
pip install solidcam-api
```

With development tools (linting, type checking, tests):

```bash
pip install "solidcam-api[dev]"
```

With documentation build dependencies:

```bash
pip install "solidcam-api[docs]"
```

---

## Quick start

```python
from solidcam_api import SolidCAMClient

with SolidCAMClient() as sc:
    sc.start_application(r"C:\Program Files\SolidWorks\SLDWORKS.exe")
    sc.open(r"C:\CAM\my_part.sldprt")
    sc.calculate()
    sc.generate_gcode()
    sc.close()
```

---

## Usage examples

### Open a part and generate G-code

```python
from solidcam_api import SolidCAMClient

with SolidCAMClient() as sc:
    # Start host CAD (SolidWorks) — wait for plugin to initialise
    sc.start_application(r"C:\Program Files\SolidWorks\SLDWORKS.exe")

    # Open a CAM part (no reference-model replacement)
    sc.open(r"D:\jobs\bracket.sldprt")

    # Check current part info
    print(sc.part_path)       # D:\jobs\bracket.sldprt
    print(sc.part_type)       # PartType.MILLING
    print(sc.reference_model) # D:\cad\bracket_v3.sldprt

    # Synchronise, calculate all operations, write G-code
    sc.synchronize()
    sc.calculate()
    sc.generate_gcode()

    # Save to a delivery folder
    saved_path = sc.save(r"D:\output")
    print(f"Saved to {saved_path}")

    sc.close()
```

### Change the reference model and recalculate

```python
from solidcam_api import SolidCAMClient

with SolidCAMClient() as sc:
    sc.start_application(r"C:\Program Files\SolidWorks\SLDWORKS.exe")
    sc.open(r"D:\jobs\bracket.sldprt")

    # Swap in the new revision of the CAD model
    sc.change_reference_model(r"D:\cad\bracket_v4.sldprt")

    sc.synchronize()
    sc.calculate()
    sc.generate_gcode()
    sc.close()
```

### List machines, operations, and tools

```python
from solidcam_api import SolidCAMClient

with SolidCAMClient() as sc:
    sc.start_application(r"C:\Program Files\SolidWorks\SLDWORKS.exe")
    sc.open(r"D:\jobs\bracket.sldprt")

    # --- Machines ---
    print(f"Available machines ({sc.machine_count}):")
    for machine in sc.list_machines():
        print(f"  [{machine.index}] {machine.name}")

    print(f"Current machine: {sc.current_machine_name}")

    # --- Operations ---
    print(f"\nOperations ({sc.operation_count}):")
    for op in sc.list_operations():
        print(f"  [{op.index}] {op.name!r:30s}  type={op.type}")

    # Suppress a roughing pass for a quick finish-only run
    sc.suppress_operation("Roughing_1", suppress=True)

    # --- Tools ---
    print(f"\nTools ({sc.tool_count}):")
    for tool in sc.list_tools():
        print(f"  [{tool.index}] {tool.name!r:25s}  type={tool.type}")

    sc.close()
```

### Create stock and target geometry

```python
from solidcam_api import SolidCAMClient, StockDefineBy, TargetDefineBy

with SolidCAMClient() as sc:
    sc.start_application(r"C:\Program Files\SolidWorks\SLDWORKS.exe")
    sc.open(r"D:\jobs\new_part.sldprt")

    # Create a box stock with 2 mm offsets on every face
    sc.create_stock_box(
        name="Stock_Box",
        x_plus=2.0, x_minus=2.0,
        y_plus=2.0, y_minus=2.0,
        z_plus=2.0, z_minus=0.0,  # no offset on the bottom face
        define_by=StockDefineBy.SOLID,
        generate_stock_envelope=True,
    )

    # Create a cylindrical stock for a turning part
    sc.create_stock_cylinder(
        name="Bar_Stock",
        right=3.0,
        left=3.0,
        external_diameter=2.0,
        define_by=StockDefineBy.SOLID,
    )

    # Create a target from the finished solid
    sc.create_target(
        name="Finished_Part",
        define_by=TargetDefineBy.SOLID,
        generate_envelope=True,
    )

    # Inspect resulting geometry entries
    for geom in sc.list_geometries():
        print(geom.name)

    sc.close()
```

### Apply a process template

```python
from solidcam_api import SolidCAMClient

with SolidCAMClient() as sc:
    sc.start_application(r"C:\Program Files\SolidWorks\SLDWORKS.exe")
    sc.open(r"D:\jobs\new_part.sldprt")

    # List available process templates
    for pt in sc.list_process_templates():
        print(pt.name)

    # Instantiate a process template against an existing geometry
    sc.create_jobs_from_process_template(
        process_template_name="Finish_Profile_Template",
        geometry_name="Finished_Part",
        sub_machine_index=1,
    )

    sc.calculate()
    sc.generate_gcode()
    sc.close()
```

### Generate a tool sheet

```python
from solidcam_api import SolidCAMClient

with SolidCAMClient() as sc:
    sc.start_application(r"C:\Program Files\SolidWorks\SLDWORKS.exe")
    sc.open(r"D:\jobs\bracket.sldprt")

    # Discover available templates
    print(sc.list_tool_sheet_names())
    # e.g. ['Sheet_Full_HTML', 'Sheet_Full_RTF', ...]

    sc.generate_tool_sheet("Sheet_Full_HTML")
    sc.close()
```

---

## API overview

All methods and properties are available directly on `SolidCAMClient`.

### Connection lifecycle

| Member | Description |
|---|---|
| `SolidCAMClient(prog_id, *, com_object)` | Initialise (no COM connection yet) |
| `.connect()` | Create the COM dispatch object |
| `.disconnect()` | Release the COM dispatch object |
| `.is_connected` | `True` if the COM object is held |
| `with SolidCAMClient() as sc:` | Preferred: auto connect/disconnect |

### General

| Member | Description |
|---|---|
| `.last_error` | Last error code (0 = no error) |
| `.last_error_description` | Human-readable last error message |
| `.log_file` | Path to the API log file (get/set) |
| `.pid` | Process ID of the target SolidCAM instance (get/set) |
| `.is_solidcam_running()` | `True` if SolidCAM process is active |
| `.start_application(path, wait_for_plugin)` | Start SolidWorks or standalone SolidCAM |
| `.start_solidcam()` | Start SolidCAM plugin (SolidWorks must be running) |

### CAD

| Member | Description |
|---|---|
| `.open_host_file(path)` | Open a CAD file in the host |
| `.is_active_doc_cam_part` | `True` if the active document is a CAM part |
| `.render_preview(path)` | Generate a PDM preview image |

### CAM

| Member | Description |
|---|---|
| `.open(part_path, model_path)` | Open a CAM part; optionally replace reference model |
| `.check_synchronization()` | Check sync status |
| `.synchronize()` | Synchronise the CAM part with its reference model |
| `.calculate(only_not_calculated)` | Calculate all (or only outdated) operations |
| `.calculate_operations(operations, only_not_calculated)` | Calculate a list of named operations |
| `.calculate_single_operation(number)` | Calculate one operation by number |
| `.change_post_processor_directory(path)` | Change the post-processor directory |
| `.generate_gcode()` | Generate G-code for the entire part |
| `.save(folder)` | Save to folder; returns the saved file path |
| `.save_as(path)` | Save to a new file path |
| `.save_to_folder(folder)` | Save to folder; returns the saved file path |
| `.close()` | Close the currently open CAM part |
| `.exit()` | Close SolidCAM entirely |

### Machine

| Member | Description |
|---|---|
| `.machine_count` | Number of available machines |
| `.current_machine` | Index of the active machine (get/set) |
| `.current_machine_name` | Name of the active machine |
| `.get_machine_name(index)` | Name of machine at *index* |
| `.list_machines()` | `list[Machine]` of all machines |

### Part

| Member | Description |
|---|---|
| `.part_path` | Path to the currently open CAM part |
| `.part_type` | `PartType` of the open part |
| `.reference_model` | Path to the reference CAD model |
| `.change_reference_model(model_path)` | Replace the reference model |
| `.create_new_part(name, path, part_type, machine_index, home_origin_position, inch)` | Create a new CAM part |

### Operation

| Member | Description |
|---|---|
| `.operation_count` | Number of NC operations |
| `.number_of_jobs_with_exclamation_sign` | Count of operations with warnings |
| `.get_operation_name(index)` | Name of operation at *index* |
| `.get_operation_type(index)` | Raw type code of operation at *index* |
| `.get_operation(index)` | `Operation` dataclass at *index* |
| `.list_operations()` | `list[Operation]` of all operations |
| `.suppress_operation(name, suppress)` | Suppress or unsuppress a named operation |
| `.generate_gcode_for_operation(name, file_name)` | G-code for one operation |

### Tool

| Member | Description |
|---|---|
| `.tool_count` | Number of tools in the tool table |
| `.tool_sheet_count` | Number of tool-sheet templates |
| `.get_tool_name(index)` | Name of tool at *index* |
| `.get_tool_type(index)` | Raw type code of tool at *index* |
| `.get_tool_tag(number, position, station, turret)` | Unique tool tag by address |
| `.get_tool(index)` | `Tool` dataclass at *index* |
| `.list_tools()` | `list[Tool]` of all tools |
| `.set_operation_tool(operation_name, tool_tag)` | Assign a tool to an operation |
| `.get_operation_tool_tag(operation_name)` | Tag of the tool used by an operation |
| `.get_tool_sheet_name(index)` | Name of tool-sheet template at *index* |
| `.list_tool_sheet_names()` | `list[str]` of all template names |
| `.generate_tool_sheet(template_name)` | Generate a tool sheet |

### Geometry

| Member | Description |
|---|---|
| `.cad_coord_sys_count` | Number of CAD coordinate systems |
| `.get_cad_coord_sys_name(index)` | Name of CAD coord sys at *index* |
| `.get_cad_coord_sys(index)` | `CoordSys` at *index* |
| `.list_cad_coord_sys()` | `list[CoordSys]` |
| `.home_count` | Number of home positions |
| `.get_home_name(index)` | Name of home at *index* |
| `.get_home(index)` | `HomeEntry` at *index* |
| `.list_home_positions()` | `list[HomeEntry]` |
| `.create_home(home_origin_position)` | Create a home at a given origin |
| `.create_home_by_cad(cad_home_name)` | Create a home from a CAD coord sys |
| `.geom_count` | Number of geometry entries |
| `.get_geom_name(index)` | Name of geometry entry at *index* |
| `.get_geom(index)` | `GeomEntry` at *index* |
| `.list_geometries()` | `list[GeomEntry]` |
| `.create_target(...)` | Create a target solid geometry |
| `.create_stock_box(...)` | Create a box stock geometry |
| `.create_stock_cylinder(...)` | Create a cylindrical stock geometry |

### Templates

| Member | Description |
|---|---|
| `.template_count` | Number of operation templates |
| `.get_template_name(index)` | Name of template at *index* |
| `.get_template(index)` | `TemplateEntry` at *index* |
| `.list_templates()` | `list[TemplateEntry]` |
| `.create_job_from_template(name, geometry, sub_machine, index)` | Instantiate one operation |
| `.process_template_count` | Number of process templates |
| `.get_process_template_name(index)` | Name of process template at *index* |
| `.get_process_template(index)` | `ProcessTemplateEntry` at *index* |
| `.list_process_templates()` | `list[ProcessTemplateEntry]` |
| `.create_jobs_from_process_template(name, geometry, sub_machine, index)` | Instantiate all operations |

---

## Error handling

All API methods raise **`SolidCAMAPIError`** on failure.  The exception carries three
attributes: `method` (the API call that failed), `code` (the integer error code from
`LastError`), and `description` (the human-readable description from `LastErrorDescription`).

```python
from solidcam_api import SolidCAMClient, SolidCAMAPIError, SolidCAMConnectionError

try:
    with SolidCAMClient() as sc:
        sc.start_application(r"C:\Program Files\SolidWorks\SLDWORKS.exe")
        sc.open(r"D:\jobs\bracket.sldprt")
        sc.calculate()
        sc.generate_gcode()
        sc.close()
except SolidCAMConnectionError as exc:
    print(f"Could not connect to SolidCAM: {exc}")
except SolidCAMAPIError as exc:
    print(f"API call '{exc.method}' failed (code {exc.code}): {exc.description}")
```

### Exception hierarchy

```
SolidCAMError
├── SolidCAMConnectionError   # COM object could not be created
├── SolidCAMNotRunningError   # SolidCAM process not detected
├── SolidCAMNotOpenError      # No CAM part is currently open
└── SolidCAMAPIError          # A specific API call returned failure
      .method  – str
      .code    – int
      .description – str
```

---

## Testing without SolidCAM

`SolidCAMClient` accepts a `com_object` keyword argument so you can inject a mock and test
automation scripts without a SolidCAM installation.

```python
import unittest.mock as mock
from solidcam_api import SolidCAMClient, PartType

def test_calculate_called_after_open():
    fake_com = mock.MagicMock()
    fake_com.LastError = 0
    fake_com.Open.return_value = 1
    fake_com.Type = int(PartType.MILLING)

    sc = SolidCAMClient(com_object=fake_com)
    assert sc.is_connected

    sc.open(r"C:\parts\test.sldprt")
    sc.calculate()

    fake_com.Open.assert_called_once_with(r"C:\parts\test.sldprt", "")
    fake_com.Calculate.assert_called_once_with(False)
```

---

## Contributing

1. **Fork** the repository and create a feature branch.
2. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```
3. Make your changes and add tests under `tests/`.
4. **Lint and format**:
   ```bash
   ruff check src tests
   ruff format src tests
   ```
5. **Type-check**:
   ```bash
   mypy src
   ```
6. **Run tests**:
   ```bash
   pytest --cov=solidcam_api --cov-report=term-missing
   ```
7. Open a pull request describing the change.

### Project structure

```
solidcam-api/
├── src/
│   └── solidcam_api/
│       ├── __init__.py          # Public API surface
│       ├── py.typed             # PEP 561 marker
│       ├── _com.py              # Internal COM wrapper (win32com)
│       ├── client.py            # SolidCAMClient — assembles all sections
│       ├── exceptions.py        # Exception hierarchy
│       ├── enums.py             # IntEnum constants (PartType, OperationType, …)
│       ├── models/              # Frozen dataclasses for result objects
│       │   ├── machine.py
│       │   ├── operation.py
│       │   ├── tool.py
│       │   ├── geometry.py
│       │   └── template.py
│       └── sections/            # Section mixins (one per API section)
│           ├── _base.py
│           ├── general.py
│           ├── cad.py
│           ├── cam.py
│           ├── machine.py
│           ├── part.py
│           ├── operation.py
│           ├── tool.py
│           ├── geometry.py
│           └── template.py
├── tests/
├── pyproject.toml
└── README.md
```

---

## License

[MIT](LICENSE) © 0ndrec