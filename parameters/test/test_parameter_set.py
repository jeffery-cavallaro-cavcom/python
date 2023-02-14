"""
Parameter Set Unit Tests
"""

import unittest

from os import environ
from pathlib import Path
from sys import getdefaultencoding
from typing import ClassVar

from parameters.option import Option
from parameters.env_variable import EnvVariable
from parameters.parameter import Parameter
from parameters.parameter_set import ParameterSet

from utility.str2list import Str2List
from utility.str2bool import str2bool

class TestParameterSet(unittest.TestCase):
    """ Parameter Set Test Suite """
    PARAMETERS : ClassVar[list[Parameter]] = [
        Parameter(
            name='input_file',
            arg=Option(short_name='f'),
            env=EnvVariable()
        ),
        Parameter(
            name='answer',
            arg=Option(short_name='A'),
            env=EnvVariable(name='EVERYTHING'),
            config=True,
            converter=int,
            default=-1
        ),
        Parameter(
            name='remote',
            group='backup',
            arg=Option(use_prefix=False, short_name='r'),
            env=EnvVariable(),
            config=True,
        ),
        Parameter(
            name='tape',
            group='backup',
            arg=Option(use_prefix=False, short_name='t'),
            env=EnvVariable(),
            config=True,
            default='/dev/nst0'
        ),
        Parameter(
            name='blocking',
            group='backup',
            arg=Option(use_prefix=False, short_name='b'),
            env=EnvVariable(),
            converter=int,
            config=True,
            default=1
        ),
        Parameter(
            name='targets',
            group='backup',
            arg=Option(short_name='T'),
            config=True,
            converter=Str2List()
        ),
        Parameter(
            name='changer',
            group='backup',
            arg=Option(
                use_prefix=False,
                short_name='C',
                action='store_const',
                const=True
            ),
            config=True,
            converter=str2bool,
            default=False
        ),
        Parameter(
            name='verify',
            group='backup',
            arg=Option(
                use_prefix=False,
                short_name='V',
                action='store_const',
                const=True
            ),
            config=True,
            converter=str2bool,
            default=True
        ),
        Parameter(
            name='pi',
            group='math',
            config=True,
            converter=float,
            default=3.14159
        ),
        Parameter(
            name='euler',
            group='math',
            config=True,
            converter=float,
            default=2.71828
        ),
    ]

    def setUp(self) -> None:
        """ Create parameter set """
        self.parameters = ParameterSet(description='Test Parameters')
        self.parameters.add_parameters(self.PARAMETERS)
        self.filename = Path(__file__).parent / 'test.ini'

    def read_ini_file(self) -> str:
        """ Read the test configuration file """
        with open(self.filename, encoding=getdefaultencoding()) as source:
            config = source.read()

        return config

    def test_arguments(self):
        """ All values from the command line """
        values = self.parameters.collect_values(
            [
                '-f', str(self.filename),
                '-A', '1962',
                '--remote', 'backup.ngc.com',
                '--tape', '/dev/st1',
                '-b', '10',
                '-T', 'var, local',
                '--changer',
                '-V'
            ],
            config=self.PARAMETERS[0]
        )

        self.assertEqual(values['input_file'], str(self.filename))
        self.assertEqual(values['answer'], 1962)
        self.assertEqual(values['backup_remote'], 'backup.ngc.com')
        self.assertEqual(values['backup_tape'], '/dev/st1')
        self.assertEqual(values['backup_blocking'], 10)
        self.assertEqual(values['backup_targets'], ['var', 'local'])
        self.assertTrue(values['backup_changer'])
        self.assertTrue(values['backup_verify'])
        self.assertEqual(values['math_pi'], 3.14)
        self.assertEqual(values['math_euler'], 2.72)

    def test_environment(self):
        """ All values from the environment variables """
        environ['EVERYTHING'] = '99'
        environ['INPUT_FILE'] = str(self.filename)
        environ['BACKUP_REMOTE'] = 'somewhere.google.com'
        environ['BACKUP_TAPE'] = '/dev/st2'
        environ['BACKUP_BLOCKING'] = '100'

        values = self.parameters.collect_values([], config=self.PARAMETERS[0])

        self.assertEqual(values['input_file'], str(self.filename))
        self.assertEqual(values['answer'], 99)
        self.assertEqual(values['backup_remote'], 'somewhere.google.com')
        self.assertEqual(values['backup_tape'], '/dev/st2')
        self.assertEqual(values['backup_blocking'], 100)
        self.assertEqual(values['backup_targets'], ['home', 'etc', 'usr'])
        self.assertTrue(values['backup_changer'])
        self.assertFalse(values['backup_verify'])
        self.assertEqual(values['math_pi'], 3.14)
        self.assertEqual(values['math_euler'], 2.72)

        environ.pop('EVERYTHING')
        environ.pop('INPUT_FILE')
        environ.pop('BACKUP_REMOTE')
        environ.pop('BACKUP_TAPE')
        environ.pop('BACKUP_BLOCKING')

    def test_config(self):
        """ All values from the configuration file """
        values = self.parameters.collect_values(
            [],
            config=self.read_ini_file()
        )

        self.assertIsNone(values['input_file'])
        self.assertEqual(values['answer'], 42)
        self.assertEqual(values['backup_remote'], 'server.ngc.com')
        self.assertEqual(values['backup_tape'], '/dev/st0')
        self.assertEqual(values['backup_blocking'], 20)
        self.assertEqual(values['backup_targets'], ['home', 'etc', 'usr'])
        self.assertTrue(values['backup_changer'])
        self.assertFalse(values['backup_verify'])
        self.assertEqual(values['math_pi'], 3.14)
        self.assertEqual(values['math_euler'], 2.72)

    def test_defaults(self):
        """ All values from the default values """
        values = self.parameters.collect_values([])

        self.assertIsNone(values['input_file'])
        self.assertEqual(values['answer'], -1)
        self.assertIsNone(values['backup_remote'])
        self.assertEqual(values['backup_tape'], '/dev/nst0')
        self.assertEqual(values['backup_blocking'], 1)
        self.assertIsNone(values['backup_targets'])
        self.assertFalse(values['backup_changer'])
        self.assertTrue(values['backup_verify'])
        self.assertEqual(values['math_pi'], 3.14159)
        self.assertEqual(values['math_euler'], 2.71828)

if __name__ == '__main__':
    unittest.main()
