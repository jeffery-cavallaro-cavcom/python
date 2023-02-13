"""
Option Unit Tests
"""

import unittest

from parameters.test.argument_test import ArgumentTest
from parameters.option import Option

class TestArgument(ArgumentTest):
    """ Option Unit Test Suite """
    def test_default_state(self):
        """ Check the default state """
        option = Option()

        self.assertIsNone(option.long_name)
        self.assertTrue(option.use_prefix)
        self.assertIsNone(option.short_name)
        self.assertIsNone(option.short_prefix)
        self.assertIsNone(option.help_or_mutex)
        self.assertEqual(option.kwargs, {})

    def test_long_name_with_prefix(self):
        """ Use parameter name with group prefix """
        name = 'name'
        group = 'group'
        value = 'value'

        argument = Option()
        argument.add_argument(name, group, self.parser)

        values = self.run_parser([f"--{group}_{name}", value])

        self.assertEqual(values.group_name, value)
        self.assertEqual(argument.get_value(name, group, values), value)

    def test_long_name_no_prefix(self):
        """ Use parameter name with no group prefix """
        name = 'name'
        value = 'value'

        option = Option()
        option.add_argument(name, None, self.parser)

        values = self.run_parser([f"--{name}", value])

        self.assertEqual(values.name, value)
        self.assertEqual(option.get_value(name, None, values), value)

    def test_long_name_with_disabled_prefix(self):
        """ Use parameter name with disabled group prefix """
        name = 'name'
        group = 'group'
        value = 'value'

        option = Option(use_prefix=False)
        option.add_argument(name, group, self.parser)

        values = self.run_parser([f"--{name}", value])

        self.assertEqual(values.name, value)
        self.assertEqual(option.get_value(name, group, values), value)

    def test_dest_override(self):
        """ Override name with dest argument """
        name = 'name'
        group = 'group'
        value = 'value'

        argument = Option(dest='here')
        argument.add_argument(name, group, self.parser)

        values = self.run_parser([f"--{group}_{name}", value])

        self.assertEqual(values.here, value)
        self.assertEqual(argument.get_value(name, group, values), value)

    def test_short_name_with_prefix(self):
        """ Short name with prefix """
        long_name = 'name'
        group = 'group'
        short_name = 'x'
        short_prefix = 's'
        value = 'value'

        argument = Option(short_name=short_name, short_prefix=short_prefix)
        argument.add_argument(long_name, group, self.parser)

        values = self.run_parser([f"-{short_prefix}{short_name}", value])

        self.assertEqual(values.group_name, value)
        self.assertEqual(argument.get_value(long_name, group, values), value)

    def test_short_name_with_no_prefix(self):
        """ Short name with no prefix """
        long_name = 'name'
        group = 'group'
        short_name = 'x'
        value = 'value'

        argument = Option(short_name=short_name)
        argument.add_argument(long_name, group, self.parser)

        values = self.run_parser([f"-{short_name}", value])

        self.assertEqual(values.group_name, value)
        self.assertEqual(argument.get_value(long_name, group, values), value)

    def test_option_converter(self):
        """ Convert option value """
        name = 'name'
        group = 'group'
        value = 42

        option = Option()
        option.add_argument(name, group, self.parser, converter=int)

        values = self.run_parser([f"--{group}_{name}", str(value)])

        self.assertEqual(values.group_name, value)
        self.assertEqual(option.get_value(name, group, values), value)

    def test_option_converter_override(self):
        """ Convert option value with explicit type argument """
        name = 'name'
        group = 'group'
        value = 42

        option = Option(type=int)
        option.add_argument(
            name, group, self.parser, converter=self.bad_value
        )

        values = self.run_parser([f"--{group}_{name}", str(value)])

        self.assertEqual(values.group_name, value)
        self.assertEqual(option.get_value(name, group, values), value)

    def test_option_action_override(self):
        """ Disable converter with action override """
        name = 'pi'
        group = 'math'
        value = 3.14

        option = Option(action='store_const', const=value)
        option.add_argument(
            name, group, self.parser, converter=self.bad_value
        )

        values = self.run_parser([f"--{group}_{name}"])

        self.assertEqual(values.math_pi, value)
        self.assertEqual(option.get_value(name, group, values), value)

    def test_missing(self):
        """ No option value returns None """
        name = 'name'
        group = 'group'

        option = Option()
        option.add_argument(name, group, self.parser, converter=int)

        values = self.run_parser([])

        self.assertIsNone(values.group_name)

if __name__ == '__main__':
    unittest.main()
