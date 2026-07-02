from __future__ import annotations

from pathlib import Path

from solidcam_api._paths import StrPath, as_str


def test_as_str_with_string() -> None:
    assert as_str("path/to/file") == "path/to/file"


def test_as_str_with_pathlib_path() -> None:
    # On Windows, Path normalizes separators
    result = as_str(Path("path/to/file"))
    assert "path" in result and "to" in result and "file" in result


def test_as_str_with_posix_path() -> None:
    # On Windows, Path normalizes separators
    result = as_str(Path("C:/Users/test"))
    assert "Users" in result and "test" in result


def test_str_path_type_accepts_string() -> None:
    # StrPath is a type alias, this is just a compile-time check
    path: StrPath = "some/path"
    assert path == "some/path"


def test_str_path_type_accepts_pathlib() -> None:
    path: StrPath = Path("some/path")
    # On Windows, Path normalizes separators
    assert "some" in str(path) and "path" in str(path)
