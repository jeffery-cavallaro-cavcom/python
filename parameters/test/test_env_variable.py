"""
Environment Variable Unit Tests
"""

import unittest

from os import environ

from parameters.env_variable import EnvVariable

class TestEnvVariable(unittest.TestCase):
    """ Environment Variable Unit Test Suite """
    def test_default_state(self):
        """ Check the default state """
        env = EnvVariable()
        self.assertIsNone(env.name)
        self.assertTrue(env.use_prefix)

    def test_name_with_prefix(self):
        """ Use parameter name with group prefix """
        name = 'name'
        group = 'group'
        value = 'value'

        env_name = f"{group}_{name}".upper()
        environ[env_name] = value

        env = EnvVariable()
        env_value = env.get_value(name, group)
        self.assertEqual(env_value, value)

    def test_name_with_no_prefix(self):
        """ Use parameter name with no group prefix """
        name = 'name'
        value = 'value'

        env_name = name.upper()
        environ[env_name] = value

        env = EnvVariable()
        env_value = env.get_value(name, None)
        self.assertEqual(env_value, value)

    def test_name_with_disabled_prefix(self):
        """ Use parameter name with disabled group prefix """
        name = 'name'
        group = 'group'
        value = 'value'

        env_name = name.upper()
        environ[env_name] = value

        env = EnvVariable(use_prefix=False)
        env_value = env.get_value(name, group)
        self.assertEqual(env_value, value)

    def test_alternate_name(self):
        """ Use an altername name """
        name = 'name'
        alt_name = 'other'
        group = 'group'
        value = 'value'

        env_name = f"{group}_{alt_name}".upper()
        environ[env_name] = value

        env = EnvVariable(name=alt_name)
        env_value = env.get_value(name, group)
        self.assertEqual(env_value, value)

    def test_converted_value(self):
        """ Get a converted value """
        name = 'name'
        group = 'group'
        value = 42

        env_name = f"{group}_{name}".upper()
        environ[env_name] = str(value)

        env = EnvVariable()
        env_value = env.get_value(name, group, converter=int)
        self.assertEqual(env_value, value)

    def test_missing(self):
        """ Missing environment variable returns None """
        name = 'name'
        group = 'group'

        env_name = f"{group}_{name}".upper()
        environ.pop(env_name)

        env = EnvVariable()
        env_value = env.get_value(name, group, converter=int)
        self.assertIsNone(env_value)

if __name__ == '__main__':
    unittest.main()
