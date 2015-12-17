# This import fixes sys.path issues
from .parentpath import *

import unittest
from ogutils.functions import decorators

class FunctionDecoratorsTest(unittest.TestCase):
    def test_listify_yield(self):
        @decorators.listify
        def yield_func(top):
            for i in range(top):
                yield i
        self.assertEquals(yield_func(3), [0, 1, 2])
        self.assertEquals(yield_func(top=0), [])

    def test_listify_generator(self):
        @decorators.listify
        def generator_func(top):
            return xrange(top)
        self.assertEquals(generator_func(3), [0, 1, 2])
        self.assertEquals(generator_func(top=0), [])

if __name__ == "__main__":
    unittest.main()
