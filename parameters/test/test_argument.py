"""
Argument Unit Tests
"""

import unittest

from parameters.argument import Argument
from parameters.test.argument_test import ArgumentTest

class TestArgument(ArgumentTest):
    """ Argument Unit Test Suite """
    def test_default_state(self):
        """ Check the default state """
        argument = Argument()

        self.assertIsNone(argument.long_name)
        self.assertTrue(argument.use_prefix)
        self.assertEqual(argument.kwargs, {})

    def test_name_with_prefix(self):
        """ Use parameter name with group prefix """
        name = 'name'
        group = 'group'
        value = 'value'

        argument = Argument()
        argument.add_argument(name, group, self.parser)

        values = self.run_parser([value])

        self.assertEqual(values.group_name, value)
        self.assertEqual(argument.get_value(name, group, values), value)

    def test_name_no_prefix(self):
        """ Use parameter name with no group prefix """
        name = 'name'
        value = 'value'

        argument = Argument()
        argument.add_argument(name, None, self.parser)

        values = self.run_parser([value])

        self.assertEqual(values.name, value)
        self.assertEqual(argument.get_value(name, None, values), value)

    def test_name_with_disabled_prefix(self):
        """ Use parameter name with disabled group prefix """
        name = 'name'
        group = 'group'
        value = 'value'

        argument = Argument(use_prefix=False)
        argument.add_argument(name, group, self.parser)

        values = self.run_parser([value])

        self.assertEqual(values.name, value)
        self.assertEqual(argument.get_value(name, group, values), value)

    def test_argument_converter(self):
        """ Convert argument value """
        name = 'name'
        group = 'group'
        value = 42

        argument = Argument()
        argument.add_argument(name, group, self.parser, converter=int)

        values = self.run_parser([str(value)])

        self.assertEqual(values.group_name, value)
        self.assertEqual(argument.get_value(name, group, values), value)

    def test_argument_converter_override(self):
        """ Convert argument value with explicit type argument """
        name = 'name'
        group = 'group'
        value = 42

        argument = Argument(type=int)
        argument.add_argument(
            name, group, self.parser, converter=self.bad_value
        )

        values = self.run_parser([str(value)])

        self.assertEqual(values.group_name, value)
        self.assertEqual(argument.get_value(name, group, values), value)

if __name__ == '__main__':
    unittest.main()
