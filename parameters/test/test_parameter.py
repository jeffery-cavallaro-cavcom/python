"""
Parameter Unit tests
"""

import unittest

from configparser import ConfigParser
from os import environ
from typing import ClassVar

from parameters.argument import Argument
from parameters.env_variable import EnvVariable
from parameters.option import Option
from parameters.parameter import Parameter
from parameters.test.argument_test import ArgumentTest

class TestParameter(ArgumentTest):
    """ Parameter Unit Test Suite """
    CONFIG : ClassVar[str] = '''
[DEFAULT]

    name = value

[group1]

    answer = 42

[group2]

    pi = 3.14
'''

    def setUp(self) -> None:
        """ Setup parameter context """
        super().setUp()
        self.config = ConfigParser()
        self.config.read_string(self.CONFIG)

    def test_default_state(self):
        """ Check the default state """
        name = 'name'

        parameter = Parameter(name)

        self.assertEqual(parameter.name, name)
        self.assertIsNone(parameter.group)
        self.assertIsNone(parameter.arg)
        self.assertIsNone(parameter.env)
        self.assertFalse(parameter.config)
        self.assertIsNone(parameter.converter)
        self.assertIsNone(parameter.default)
        self.assertIsNone(parameter.help_text)

        self.assertEqual(parameter.get_full_name(), name)

    def test_with_group(self):
        """ Check for group prefix in name """
        name = 'name'
        group = 'group'

        parameter = Parameter(name, group=group)

        self.assertEqual(parameter.get_full_name(), f"{group}_{name}")

    def test_parameter_default_and_help(self):
        """ Parameter supplies default value and help text """
        name = 'name'
        group = 'group'
        value = 42
        text = 'a dummy argument'
        full_text = f"{text} (def: {str(value)})"

        parameter = Parameter(
            name,
            group,
            arg=Argument(),
            converter=int,
            default=value,
            help_text=text
        )

        self.assertEqual(parameter.default, value)
        self.assertNotIn('default', parameter.arg.kwargs)

        self.assertEqual(parameter.help_text, full_text)
        self.assertEqual(parameter.arg.kwargs['help'], full_text)

    def test_argument_default_and_help(self):
        """ Argument supplies default value and help text """
        name = 'name'
        group = 'group'
        value = 'hello'
        text = 'a dummy argument'
        full_text = f"{text} (def: {str(value)})"

        parameter = Parameter(
            name,
            group,
            arg=Argument(default=value, help=text),
            default='xyzzy',
            help_text='some dummy text'
        )

        self.assertEqual(parameter.default, value)
        self.assertNotIn('default', parameter.arg.kwargs)

        self.assertEqual(parameter.help_text, full_text)
        self.assertEqual(parameter.arg.kwargs['help'], full_text)

    def test_argument_no_converter(self):
        """ Get string argument value """
        parameter = Parameter(
            name='name',
            group='group',
            arg=Argument(),
            default='bad'
        )
        parameter.add_argument(self.parser)
        values = self.run_parser(['hello'])
        value = parameter.get_value(values, self.config)
        self.assertEqual(value, 'hello')

    def test_option_no_converter(self):
        """ Get string option value """
        parameter = Parameter(
            name='name',
            group='group',
            arg=Option(short_name='x'),
            default='bad'
        )
        parameter.add_argument(self.parser)
        values = self.run_parser(['-x', 'world'])
        value = parameter.get_value(values, self.config)
        self.assertEqual(value, 'world')

    def test_argument_parameter_converter(self):
        """ Get converted argument value with parameter converter """
        parameter = Parameter(
            name='name',
            group='group',
            arg=Argument(),
            converter=int,
            default=-1
        )
        parameter.add_argument(self.parser)
        values = self.run_parser(['42'])
        value = parameter.get_value(values, self.config)
        self.assertEqual(value, 42)

    def test_option_parameter_converter(self):
        """ Get converted option value with parameter converter """
        parameter = Parameter(
            name='name',
            group='group',
            arg=Option(short_name='x'),
            converter=int,
            default=-1
        )
        parameter.add_argument(self.parser)
        values = self.run_parser(['-x', '42'])
        value = parameter.get_value(values, self.config)
        self.assertEqual(value, 42)

    def test_argument_converter(self):
        """ Get converted argument value with argument converter """
        parameter = Parameter(
            name='name',
            group='group',
            arg=Argument(type=int),
            converter=self.bad_value,
            default=-1
        )
        parameter.add_argument(self.parser)
        values = self.run_parser(['42'])
        value = parameter.get_value(values, self.config)
        self.assertEqual(value, 42)

    def test_option_converter(self):
        """ Get converted option value with option converter """
        parameter = Parameter(
            name='name',
            group='group',
            arg=Option(short_name='x', type=int),
            converter=self.bad_value,
            default=-1
        )
        parameter.add_argument(self.parser)
        values = self.run_parser(['-x', '42'])
        value = parameter.get_value(values, self.config)
        self.assertEqual(value, 42)

    def test_not_found(self):
        """ Missing value with None default value """
        parameter = Parameter(
            name='hello',
            group='world',
            arg=Option(),
            env=EnvVariable(),
            config=True
        )
        parameter.add_argument(self.parser)
        values = self.run_parser([])
        value = parameter.get_value(values, self.config)
        self.assertIsNone(value)

    def test_default_value(self):
        """ Accept a default value """
        parameter = Parameter(
            name='pi',
            group='group1',
            arg=Option(),
            env=EnvVariable(),
            config=True,
            default='not found'
        )
        parameter.add_argument(self.parser)
        values = self.run_parser([])
        value = parameter.get_value(values, self.config)
        self.assertEqual(value, 'not found')

    def test_default_config_value(self):
        """ Accept a value from the default configuration section """
        parameter = Parameter(
            name='name',
            arg=Option(),
            env=EnvVariable(),
            config=True,
            default='not found'
        )
        parameter.add_argument(self.parser)
        values = self.run_parser([])
        value = parameter.get_value(values, self.config)
        self.assertEqual(value, 'value')

    def test_config_value(self):
        """ Accept a value from a configuration section """
        parameter = Parameter(
            name='answer',
            group='group1',
            arg=Option(),
            env=EnvVariable(),
            config=True,
            converter=int,
            default='not found'
        )
        parameter.add_argument(self.parser)
        values = self.run_parser([])
        value = parameter.get_value(values, self.config)
        self.assertEqual(value, 42)

    def test_alternate_config_value(self):
        """ Accept a value from a configuration alternate section """
        section = Parameter(name='section', arg=Argument())
        section.add_argument(self.parser)

        parameter = Parameter(
            name='pi',
            group='group1',
            arg=Option(),
            env=EnvVariable(),
            config=section,
            converter=float,
            default='not found'
        )
        parameter.add_argument(self.parser)

        values = self.run_parser(['group2'])
        value = parameter.get_value(values, self.config)
        self.assertEqual(value, 3.14)

    def test_environment_value(self):
        """ Accept a value from an environment variable """
        environ['GROUP1_ANSWER'] = '100'

        parameter = Parameter(
            name='answer',
            group='group1',
            arg=Option(),
            env=EnvVariable(),
            config=True,
            converter=int,
            default=-1
        )
        parameter.add_argument(self.parser)

        values = self.run_parser([])
        value = parameter.get_value(values, self.config)
        self.assertEqual(value, 100)

    def test_option_value(self):
        """ Accept a value from a command line option """
        environ['GROUP1_ANSWER'] = '100'

        parameter = Parameter(
            name='answer',
            group='group1',
            arg=Option(),
            env=EnvVariable(),
            config=True,
            converter=int,
            default=-1
        )
        parameter.add_argument(self.parser)

        values = self.run_parser(['--group1_answer', '1234'])
        value = parameter.get_value(values, self.config)
        self.assertEqual(value, 1234)

if __name__ == '__main__':
    unittest.main()
