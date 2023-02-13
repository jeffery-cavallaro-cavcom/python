"""
Argument/Option Test Base Class
"""

import unittest

from argparse import ArgumentParser, Namespace

class ArgumentTest(unittest.TestCase):
    """ Argument/Option Testing """
    def setUp(self) -> None:
        """ Construct an argument parser """
        self.parser = ArgumentParser(
            description='Test Parser', exit_on_error=False
        )

    def run_parser(self, args : list[str]) -> Namespace:
        """
        Parse arguments

        Arguments:
            args:
                Command line arguments to use (as opposed to sys.argv).

        Returns:
            Resulting value namespace, or None on an error.
        """
        return self.parser.parse_args(args)

    @staticmethod
    def bad_value(value : str):
        """ Force a bad value """
        raise ValueError('invalid value')
