# This import fixes sys.path issues
from .parentpath import *

import unittest
from ogutils.collections import operators

class CollectionOperatorsTest(unittest.TestCase):
    def test_apply_dict_default(self):
        self.assertDictEqual(operators.apply_dict_default({}, 'test', 1), {'test': 1})
        self.assertDictEqual(operators.apply_dict_default({'test': 1}, 'test', 2), {'test': 1})

    def test_apply_dict_default_func_arg(self):
        self.assertDictEqual(operators.apply_dict_default({}, 'test', lambda: 1), {'test': 1})
        self.assertDictEqual(operators.apply_dict_default(
            {},
            'test',
            lambda a: a + '1'),
            {'test': 'test1'})

if __name__ == "__main__":
    unittest.main()
