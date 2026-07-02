"""Path handling utilities for the SolidCAM API.

This module provides type aliases and helpers for handling file paths in a
cross-platform manner, with support for both ``str`` and ``os.PathLike`` inputs.
"""

from __future__ import annotations

import os

StrPath = str | os.PathLike[str]


def as_str(path: StrPath) -> str:
    """Normalize a path to ``str`` for passing to COM.

    Args:
        path: A string or ``os.PathLike`` path to normalize.

    Returns:
        The path as a string suitable for COM API calls.

    """
    return os.fspath(path)
