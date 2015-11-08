# This import fixes sys.path issues
from .parentpath import *

import unittest
from .fake_iterable import FakeIterable
from ogutils import checks

class ChecksTest(unittest.TestCase):
    def test_booleanize_false(self):
        self.assertEquals(checks.booleanize(False), False)
        self.assertEquals(checks.booleanize(0), False)
        self.assertEquals(checks.booleanize(''), False)
        self.assertEquals(checks.booleanize([]), False)
        self.assertEquals(checks.booleanize(set()), False)
        self.assertEquals(checks.booleanize({}), False)
        self.assertEquals(checks.booleanize(FakeIterable([])), False)
        self.assertEquals(checks.booleanize('false'), False)
        self.assertEquals(checks.booleanize('FaLsE'), False)
        self.assertEquals(checks.booleanize('FALSE'), False)
        self.assertEquals(checks.booleanize('0'), False)
        self.assertEquals(checks.booleanize(e for e in []), False)

    def test_booleanize_true(self):
        self.assertEquals(checks.booleanize(True), True)
        self.assertEquals(checks.booleanize(1), True)
        self.assertEquals(checks.booleanize('a'), True)
        self.assertEquals(checks.booleanize([0]), True)
        self.assertEquals(checks.booleanize(set([0])), True)
        self.assertEquals(checks.booleanize({'a': 0}), True)
        self.assertEquals(checks.booleanize(FakeIterable([1])), True)
        self.assertEquals(checks.booleanize('true'), True)
        self.assertEquals(checks.booleanize('TrUe'), True)
        self.assertEquals(checks.booleanize('TRUE'), True)
        self.assertEquals(checks.booleanize('1'), True)
        self.assertEquals(checks.booleanize(e for e in [0]), True)

if __name__ == "__main__":
    unittest.main()
