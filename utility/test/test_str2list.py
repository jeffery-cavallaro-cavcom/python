"""
String to List Unit Tests
"""

import unittest

from utility.str2list import Str2List

class TestStr2List(unittest.TestCase):
    """ String to List Test Suite """
    def test_comma_list(self):
        """ Comma delimiters, stripping, no blanks, no converter """
        converter = Str2List()
        values = converter('  abc  ,defg,  1234  ')
        self.assertEqual(values, ['abc', 'defg', '1234'])

    def test_integer_list(self):
        """ Comma delimiters, stripping, no blanks, with converter """
        converter = Str2List(converter=int)
        values = converter('123,  42,  99,  -1   ')
        self.assertEqual(values, [123, 42, 99, -1])

    def test_empty_list(self):
        """ Comma delimiters, stripping, no blanks, no converter, empty list """
        converter = Str2List()

        values = converter(None)
        self.assertEqual(values, [])

        values = converter('')
        self.assertEqual(values, [])

        values = converter('   ,    ,,      ')
        self.assertEqual(values, [])

    def test_alternate_delimiter(self):
        """ Bar delimiters, stripping, no blanks, no converter """
        converter = Str2List(delimiter='|')
        values = converter('one, two, three | four, five | six')
        self.assertEqual(values, ['one, two, three', 'four, five', 'six'])

    def test_no_stripping(self):
        """ Comma delimiters, no stripping, no blanks, no converter """
        converter = Str2List(strip=False)
        values = converter('  abc  ,defg,, ,1234  ')
        self.assertEqual(values, ['  abc  ', 'defg', ' ', '1234  '])

        values = converter(None)
        self.assertEqual(values, [])

        values = converter('')
        self.assertEqual(values, [])

        values = converter('   ,    ,,      ')
        self.assertEqual(values, ['   ', '    ', '      '])

    def test_blanks(self):
        """ Comma delimiters, stripping, blanks, no converter """
        converter = Str2List(allow_blank=True)
        values = converter('  abc  ,defg,, ,1234  ')
        self.assertEqual(values, ['abc', 'defg', '', '', '1234'])

        values = converter(None)
        self.assertEqual(values, [])

        values = converter('')
        self.assertEqual(values, [''])

        values = converter('   ,    ,,      ')
        self.assertEqual(values, ['', '', '', ''])

    def test_no_stripping_blanks(self):
        """ Comma delimiters, no stripping, blanks, no converter """
        converter = Str2List(strip=False, allow_blank=True)
        values = converter('  abc  ,defg,, ,1234  ')
        self.assertEqual(values, ['  abc  ', 'defg', '', ' ', '1234  '])

        values = converter(None)
        self.assertEqual(values, [])

        values = converter('')
        self.assertEqual(values, [''])

        values = converter('   ,    ,,      ')
        self.assertEqual(values, ['   ', '    ', '', '      '])

if __name__ == '__main__':
    unittest.main()
