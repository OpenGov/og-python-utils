# This import fixes sys.path issues
from .parentpath import *

import unittest
from .fake_iterable import FakeIterable
from ogutils.collections import transformations

class CollectionTransformationsTest(unittest.TestCase):
    def test_recursive_iter_basics(self):
        self.assertEquals(list(transformations.recursive_iter(1)), [1])
        self.assertEquals(list(transformations.recursive_iter('a')), ['a'])
        self.assertEquals(list(transformations.recursive_iter('abc')), ['abc'])
        self.assertEquals(list(transformations.recursive_iter(['abc', 'def'])), ['abc', 'def'])
        self.assertEquals(list(transformations.recursive_iter(('abc', 'def'))), ['abc', 'def'])
        self.assertEquals(list(transformations.recursive_iter((e for e in [1,2]))), [1, 2])
        self.assertEquals(list(transformations.recursive_iter(set(['abc', 'def']))), ['abc', 'def'])
        self.assertEquals(list(transformations.recursive_iter(FakeIterable([1, 2]))), [1, 2])

    def test_recursive_iter_nested(self):
        self.assertEquals(list(transformations.recursive_iter([[1]])), [1])
        self.assertEquals(list(transformations.recursive_iter([['a']])), ['a'])
        self.assertEquals(list(transformations.recursive_iter([['abc']])), ['abc'])
        self.assertEquals(list(transformations.recursive_iter([['abc', 'def']])), ['abc', 'def'])
        self.assertEquals(list(transformations.recursive_iter([['abc'], ['def']])), ['abc', 'def'])
        self.assertEquals(list(transformations.recursive_iter([['abc'], 'def'])), ['abc', 'def'])
        self.assertEquals(list(transformations.recursive_iter((set(['abc']), ('def',)))), ['abc', 'def'])
        self.assertEquals(list(transformations.recursive_iter([1, FakeIterable([2])])), [1, 2])

    def test_recursive_iter_many_nested(self):
        self.assertEquals(list(transformations.recursive_iter([[[[[1]]]]])), [1])
        self.assertEquals(list(transformations.recursive_iter([[[['a']]]])), ['a'])
        self.assertEquals(list(transformations.recursive_iter([[['abc']]])), ['abc'])
        self.assertEquals(list(transformations.recursive_iter([[['abc'], 'def']])), ['abc', 'def'])
        self.assertEquals(list(transformations.recursive_iter([[[['abc']]], [['def']]])), ['abc', 'def'])
        self.assertEquals(list(transformations.recursive_iter([[[[['abc']]]], 'def'])), ['abc', 'def'])
        self.assertEquals(list(transformations.recursive_iter((set([('abc',)]), ([('def',)],)))), ['abc', 'def'])
        self.assertEquals(list(transformations.recursive_iter([[[[[1]]]], [FakeIterable([2])]])), [1, 2])

    def test_flatten_basics(self):
        self.assertEquals(transformations.flatten(1), [1])
        self.assertEquals(transformations.flatten('a'), ['a'])
        self.assertEquals(transformations.flatten('abc'), ['abc'])
        self.assertEquals(transformations.flatten(['abc', 'def']), ['abc', 'def'])
        self.assertEquals(transformations.flatten(('abc', 'def')), ['abc', 'def'])
        self.assertEquals(transformations.flatten((e for e in [1,2])), [1, 2])
        self.assertEquals(transformations.flatten(set(['abc', 'def'])), ['abc', 'def'])
        self.assertEquals(transformations.flatten(FakeIterable([1, 2])), [1, 2])

    def test_flatten_nested(self):
        self.assertEquals(transformations.flatten([[1]]), [1])
        self.assertEquals(transformations.flatten([['a']]), ['a'])
        self.assertEquals(transformations.flatten([['abc']]), ['abc'])
        self.assertEquals(transformations.flatten([['abc', 'def']]), ['abc', 'def'])
        self.assertEquals(transformations.flatten([['abc'], ['def']]), ['abc', 'def'])
        self.assertEquals(transformations.flatten([['abc'], 'def']), ['abc', 'def'])
        self.assertEquals(transformations.flatten((set(['abc']), ('def',))), ['abc', 'def'])
        self.assertEquals(transformations.flatten([1, FakeIterable([2])]), [1, 2])

    def test_flatten_many_nested(self):
        self.assertEquals(transformations.flatten([[[[[1]]]]]), [1])
        self.assertEquals(transformations.flatten([[[['a']]]]), ['a'])
        self.assertEquals(transformations.flatten([[['abc']]]), ['abc'])
        self.assertEquals(transformations.flatten([[['abc'], 'def']]), ['abc', 'def'])
        self.assertEquals(transformations.flatten([[[['abc']]], [['def']]]), ['abc', 'def'])
        self.assertEquals(transformations.flatten([[[[['abc']]]], 'def']), ['abc', 'def'])
        self.assertEquals(transformations.flatten((set([('abc',)]), ([('def',)],))), ['abc', 'def'])
        self.assertEquals(transformations.flatten([[[[[1]]]], [FakeIterable([2])]]), [1, 2])

if __name__ == "__main__":
    unittest.main()
