# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2026-07-02

### Added

- Support for `os.PathLike[str]` in all path-accepting methods (`open`, `save`, `save_as`,
  `save_to_folder`, `open_host_file`, `render_preview`, `change_post_processor_directory`,
  `change_reference_model`, `create_new_part`).
- `open_part()` context manager for guaranteed part cleanup.
- Logging support with `logging.getLogger("solidcam_api")` for debugging COM calls.
- `ScAutom` Protocol for static type checking of COM interface.

### Changed

- `save()`, `save_as()`, `save_to_folder()` now accept `str | os.PathLike[str]`.
- `save()` and `save_to_folder()` now return `pathlib.Path` instead of `str`.
- `calculate()` and `calculate_operations()` now require keyword-only arguments.
- `start_application()` now requires keyword-only `wait_for_plugin` argument.
- `pid` property now returns `int` instead of `float`.
- Minimum Python version lowered from 3.13 to 3.10.

### Fixed

- Version now read dynamically from package metadata instead of hardcoded.
- Removed obsolete `ANN101`/`ANN102` ruff rules from config.
- Fixed `type: ignore[import]` to `type: ignore[import-untyped]` in `_com.py`.

### Removed

- Hardcoded version string in `__init__.py`.

## [0.1.0] - 2025-01-01

### Added

- Initial release with full SolidCAM Automation API coverage.
- Typed interface with `mypy --strict` compliance.
- 447 unit tests with 90% coverage.
- Support for all major API sections: General, CAD, CAM, Machine, Part, Operation, Tool, Geometry, Template.