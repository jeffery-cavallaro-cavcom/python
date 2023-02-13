"""
Expand Path Unit Tests
"""

import unittest

import os
from pathlib import Path
from typing import ClassVar

from utility import is_windows
from utility.expand_path import expand_path

class TestExpandPath(unittest.TestCase):
    """ Expand Path Test Suite """
    PARENT : ClassVar[Path] = Path(__file__).parent

    def test_current_directory(self):
        """ Return the current working directory by default """
        cwd = Path.cwd()
        self.assertEqual(expand_path(), cwd)

    def test_expand_home(self):
        """ Expand ~ syntax """
        home = expand_path('~', must_exist=True)
        name = 'USERPROFILE' if is_windows else 'HOME'
        self.assertEqual(home, Path(os.environ[name]))

    def test_expand_absolute(self):
        """ Expand absolute existing path """
        expanded = expand_path(self.PARENT, must_exist=True)
        self.assertEqual(expanded, self.PARENT)

    def test_expand_relative(self):
        """ Expand a relative existing path """
        path =  self.PARENT / '../..' / 'utility' / '.' / 'expand_path.py'
        resolved = expand_path(path, must_exist=True)
        self.assertEqual(resolved, self.PARENT.parent / 'expand_path.py')

    def test_expand_no_exist(self):
        """ Expand to a non-existent path """
        path = self.PARENT / '..' / 'xyzzy'

        with self.assertRaises(FileNotFoundError):
            resolved = expand_path(path, must_exist=True)

        resolved = expand_path(path)
        self.assertEqual(resolved, self.PARENT.parent / 'xyzzy')

if __name__ == '__main__':
    unittest.main()
