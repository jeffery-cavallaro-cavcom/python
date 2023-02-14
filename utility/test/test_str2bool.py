"""
String to Boolean Unit Tests
"""

import unittest

from utility.str2bool import str2bool

class TestStr2Bool(unittest.TestCase):
    """ String to Boolean Test Suite """
    def test_true(self):
        """ Check for True values """
        self.assertTrue(str2bool('true'))
        self.assertTrue(str2bool('TRUE'))
        self.assertTrue(str2bool('tRuE'))
        self.assertTrue(str2bool('t'))
        self.assertTrue(str2bool('T'))
        self.assertTrue(str2bool('yes'))
        self.assertTrue(str2bool('YES'))
        self.assertTrue(str2bool('YeS'))
        self.assertTrue(str2bool('y'))
        self.assertTrue(str2bool('Y'))
        self.assertTrue(str2bool('on'))
        self.assertTrue(str2bool('ON'))
        self.assertTrue(str2bool('On'))
        self.assertTrue(str2bool('1'))
        self.assertTrue(str2bool('42'))
        self.assertTrue(str2bool('-1'))

    def test_false(self):
        """ Check for False values """
        self.assertFalse(str2bool('false'))
        self.assertFalse(str2bool('FALSE'))
        self.assertFalse(str2bool('FaLsE'))
        self.assertFalse(str2bool('f'))
        self.assertFalse(str2bool('F'))
        self.assertFalse(str2bool('no'))
        self.assertFalse(str2bool('NO'))
        self.assertFalse(str2bool('No'))
        self.assertFalse(str2bool('n'))
        self.assertFalse(str2bool('N'))
        self.assertFalse(str2bool('off'))
        self.assertFalse(str2bool('OFF'))
        self.assertFalse(str2bool('Off'))
        self.assertFalse(str2bool('junk'))
        self.assertFalse(str2bool('0'))
        self.assertFalse(str2bool(None))
        self.assertFalse(str2bool(1))

if __name__ == '__main__':
    unittest.main()
