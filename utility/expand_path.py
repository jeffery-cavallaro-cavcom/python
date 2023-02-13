"""
Resolve File Paths

This method accepts a path or string and expands it to an absolute path.  Any
leading '~' is expanded as expected.
"""

from pathlib import Path
from typing import Optional, Union

def expand_path(
    path : Optional[Union[Path, str]] = None,
    must_exist : bool = False
):
    """
    Expand file path

    Arguments:
        path:
            File path to be expanded.  Defaults to None (the current working
            directory).
        must_exist:
            The strict argument to resolve().  If True then the resulting
            absolute file path must exist.  Defaults to False.

    Returns:
        Path:
            Fully resolved (no links) file path with any leading '~' expanded
            as expected.
    """
    if not path:
        path = Path.cwd()

    return Path(path).expanduser().resolve(strict=bool(must_exist))
