# This import fixes sys.path issues
from .parentpath import *

import unittest
import re
from ogutils.text import regex

class TextRegexTest(unittest.TestCase):
    def test_bad_input_chained_regex(self):
        with self.assertRaises(ValueError):
            regex.chain_sub_regexes('', '.')
        with self.assertRaises(TypeError):
            regex.chain_sub_regexes(5, ('.', 'a'))
        self.assertEquals(regex.chain_sub_regexes('foobar'), 'foobar')

    def test_single_chained_regex(self):
        self.assertEquals(regex.chain_sub_regexes('foobar', (re.compile('[a]+'), 'o')), 'foobor')
        self.assertEquals(regex.chain_sub_regexes('foobar', ('na', 'o')), 'foobar')
        self.assertEquals(regex.chain_sub_regexes('', ('.', 'o')), '')
        self.assertEquals(regex.chain_sub_regexes('foobar', ('.', '1')), '111111')
        self.assertEquals(regex.chain_sub_regexes('foobar', ('.+', '1')), '1')

    def test_many_chained_regex(self):
        self.assertEquals(regex.chain_sub_regexes('foobar', ('[a]+', 'o'), ('o', 'a')), 'faabar')
        self.assertEquals(regex.chain_sub_regexes(
            'foobar',
            ('.$', 'z'),
            (re.compile('^.'), 'b')),
            'boobaz')
        self.assertEquals(regex.chain_sub_regexes(
            'foobar',
            ('a', 'b'),
            ('b', 'c'),
            ('c', 'd'),
            ('d', 'e'),
            ('e', 'f')),
            'fooffr')

if __name__ == "__main__":
    unittest.main()
