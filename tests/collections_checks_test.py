# This import fixes sys.path issues
from .parentpath import *

import unittest
from .fake_iterable import FakeIterable
from ogutils.collections import checks

class CollectionChecksTest(unittest.TestCase):
    def test_is_collection(self):
        self.assertEquals(checks.is_collection(False), False)
        self.assertEquals(checks.is_collection(True), False)
        self.assertEquals(checks.is_collection(None), False)
        self.assertEquals(checks.is_collection(0), False)
        self.assertEquals(checks.is_collection(''), True)
        self.assertEquals(checks.is_collection([]), True)
        self.assertEquals(checks.is_collection(set()), True)
        self.assertEquals(checks.is_collection({}), True)
        self.assertEquals(checks.is_collection(FakeIterable([])), True)
        self.assertEquals(checks.is_collection(e for e in []), True)

    def test_is_empty_falsy(self):
        self.assertEquals(checks.is_empty(False), False)
        self.assertEquals(checks.is_empty(True), False)
        self.assertEquals(checks.is_empty(None), False)
        self.assertEquals(checks.is_empty(0), False)
        self.assertEquals(checks.is_empty(['first']), False)
        self.assertEquals(checks.is_empty(set(['first'])), False)
        self.assertEquals(checks.is_empty({'first': 'value'}), False)
        self.assertEquals(checks.is_empty(FakeIterable(['first'])), False)
        self.assertEquals(checks.is_empty(e for e in ['first']), False)

    def test_is_empty_truthy(self):
        self.assertEquals(checks.is_empty(''), True)
        self.assertEquals(checks.is_empty([]), True)
        self.assertEquals(checks.is_empty(set()), True)
        self.assertEquals(checks.is_empty({}), True)
        self.assertEquals(checks.is_empty(FakeIterable([])), True)
        self.assertEquals(checks.is_empty(e for e in []), True)

    def test_any_shared(self):
        enumerables = (
            [],
            {},
            set(),
            'abc',
            ['test'],
            ['a', 'b'],
            {'test': 'value', 'a': 'b'},
            FakeIterable(['b']))
        for enum_one in enumerables:
            for enum_two in enumerables:
                self.assertEquals(checks.any_shared(enum_one, enum_two),
                                  any(set(enum_one) & set(enum_two)))

    def test_any_shared_non_iterable(self):
        # Non-iterable elements always return false
        self.assertEquals(checks.any_shared(5, [5]), False)
        self.assertEquals(checks.any_shared([5], 5), False)
        self.assertEquals(checks.any_shared(5, 5), False)

if __name__ == "__main__":
    unittest.main()
