"""
This module overrides Python's import system
https://docs.python.org/3/library/importlib.html
https://stackoverflow.com/a/43573798/3481480
"""


import sys
import os
from typing import Optional, Sequence, Union
from importlib.machinery import ModuleSpec
from importlib.abc import MetaPathFinder
from importlib.util import spec_from_file_location
import types
import soil as _soil  # NOQA pylint:disable=unused-import

UNITTEST_MOCKS_FOLDER = "test/unit/unittest_mocks"


class Finder(MetaPathFinder):
    # pylint:disable=no-self-use
    """
    Load files that should come from the DB from unittest_mocks
    """

    def find_spec(
        self,
        fullname: str,
        path: Optional[Sequence[Union[bytes, str]]],
        _target: Optional[types.ModuleType] = None,
    ) -> Optional[ModuleSpec]:
        """Find the module in UNITTEST_MOCKS_FOLDER"""
        if "." in fullname:
            *parents, name = fullname.split(".")
        else:
            name = fullname
            parents = []

        if not (
            len(parents) > 1
            and parents[0] == "soil"
            and (parents[1] == "modules" or parents[1] == "data_structures")
        ):
            # If the module is not from soil.modules or soil.data_structures use the default loader
            return None

        path = UNITTEST_MOCKS_FOLDER
        folder = parents[2:]
        filename = os.path.abspath(os.path.join(path, *folder, f"{name}.py"))

        if os.path.exists(filename):
            return spec_from_file_location(fullname, filename)
        return None


def install() -> None:
    """Inserts the finder into the import machinery"""
    sys.meta_path.insert(0, Finder())
