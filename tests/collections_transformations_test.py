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
        self.assertEquals(list(transformations.recursive_iter(
            (set([('abc',)]),
            ([('def',)],)))),
            ['abc', 'def'])
        self.assertEquals(list(transformations.recursive_iter([[[[[1]]]], [FakeIterable([2])]])), [1, 2])

    def test_flatten_basics(self):
        self.assertEquals(transformations.flatten(1), [1])
        self.assertEquals(transformations.flatten('a'), ['a'])
        self.assertEquals(transformations.flatten('abc'), ['abc'])
        self.assertEquals(transformations.flatten(['abc', 'def']), ['abc', 'def'])
        self.assertEquals(transformations.flatten(('abc', 'def')), ['abc', 'def'])
        self.assertEquals(transformations.flatten({'a': 1}), [{'a': 1}])
        self.assertEquals(transformations.flatten((e for e in [1,2])), [1, 2])
        self.assertEquals(transformations.flatten(set(['abc', 'def'])), ['abc', 'def'])
        self.assertEquals(transformations.flatten(xrange(5)), [0, 1, 2, 3, 4])
        self.assertEquals(transformations.flatten(FakeIterable([1, 2])), [1, 2])

    def test_flatten_nested(self):
        self.assertEquals(transformations.flatten([[1]]), [1])
        self.assertEquals(transformations.flatten([['a']]), ['a'])
        self.assertEquals(transformations.flatten([['abc']]), ['abc'])
        self.assertEquals(transformations.flatten([['abc', 'def']]), ['abc', 'def'])
        self.assertEquals(transformations.flatten([['abc'], ['def']]), ['abc', 'def'])
        self.assertEquals(transformations.flatten([['abc'], 'def']), ['abc', 'def'])
        self.assertEquals(transformations.flatten([{'a': 1}, {'a': 2}]), [{'a': 1}, {'a': 2}])
        self.assertEquals(transformations.flatten((set(['abc']), ('def',))), ['abc', 'def'])
        self.assertEquals(transformations.flatten([i] for i in xrange(5)), [0, 1, 2, 3, 4])
        self.assertEquals(transformations.flatten([1, FakeIterable([2])]), [1, 2])

    def test_flatten_many_nested(self):
        self.assertEquals(transformations.flatten([[[[[1]]]]]), [1])
        self.assertEquals(transformations.flatten([[[['a']]]]), ['a'])
        self.assertEquals(transformations.flatten([[['abc']]]), ['abc'])
        self.assertEquals(transformations.flatten([[['abc'], 'def']]), ['abc', 'def'])
        self.assertEquals(transformations.flatten([[[['abc']]], [['def']]]), ['abc', 'def'])
        self.assertEquals(transformations.flatten([[[[['abc']]]], 'def']), ['abc', 'def'])
        self.assertEquals(transformations.flatten([[[[{'a': 1}, {'a': 2}]]]]), [{'a': 1}, {'a': 2}])
        self.assertEquals(transformations.flatten((set([('abc',)]), ([('def',)],))), ['abc', 'def'])
        self.assertEquals(transformations.flatten([[[i]]] for i in xrange(5)), [0, 1, 2, 3, 4])
        self.assertEquals(transformations.flatten([[[[[1]]]], [FakeIterable([2])]]), [1, 2])

    def test_merge_dicts_basics(self):
        self.assertDictEqual(transformations.merge_dicts({'a': 1}), {'a': 1})
        self.assertDictEqual(transformations.merge_dicts({'a': 1}, {'a': 2}), {'a': 2})
        self.assertDictEqual(transformations.merge_dicts(
            {'a': 1, 'b': 1}, {'a': 2, 'c': 1}), {'a': 2, 'b': 1, 'c': 1})

    def test_merge_dicts_copy(self):
        d = {'a': 1, 'b': 1}
        self.assertDictEqual(transformations.merge_dicts(d, copy=True), d)
        self.assertDictEqual(transformations.merge_dicts(d, d, copy=True), d)
        self.assertDictEqual(transformations.merge_dicts(d, {'a': 2}, copy=True), {'a': 2, 'b':1})
        self.assertDictEqual(d, {'a': 1, 'b': 1})

    def test_merge_dicts_no_copy(self):
        d = {'a': 1, 'b': 1}
        self.assertDictEqual(transformations.merge_dicts(d, copy=False), d)
        self.assertDictEqual(transformations.merge_dicts(d, d, copy=False), d)
        self.assertDictEqual(transformations.merge_dicts(d, {'a': 2}, copy=False), {'a': 2, 'b':1})
        self.assertEquals(d['a'], 2)

    def test_batch_basics(self):
        self.assertEquals(list(transformations.batch([], 2)), [()])
        self.assertEquals(list(transformations.batch([1], 0)), [[1]])
        self.assertEquals(list(transformations.batch([1], 1)), [[1]])
        self.assertEquals(list(transformations.batch([1], 2)), [[1]])
        self.assertEquals(list(transformations.batch([1, 2], 1)), [[1], [2]])
        self.assertEquals(list(transformations.batch([1, 2, 3, 4], 2)), [[1, 2], [3, 4]])
        self.assertEquals(list(transformations.batch([1, 2, 3, 4], 3)), [[1, 2, 3], [4]])

    def test_batch_types(self):
        self.assertEquals(list(transformations.batch(xrange(0), 2)), [tuple()])
        self.assertEquals(list(transformations.batch((1, 2), 1)), [(1,), (2,)])
        self.assertEquals(list(transformations.batch(set([1, 2, 3, 4]), 2)), [[1, 2], [3, 4]])
        self.assertEquals(list(transformations.batch(xrange(5), 3)), [(0, 1, 2), (3, 4)])

    def test_degenertor_gen_xrange(self):
        self.assertEquals(transformations.degenerate(xrange(0)), [])
        self.assertEquals(transformations.degenerate(xrange(3)), [0, 1, 2])

    def test_degenertor_gen_func(self):
        def yield_func(top):
            for i in range(top):
                yield i
        self.assertEquals(transformations.degenerate(yield_func(0)), [])
        self.assertEquals(transformations.degenerate(yield_func(3)), [0, 1, 2])

    def test_degenertor_gens(self):
        self.assertEquals(transformations.degenerate(_ for _ in []), [])
        self.assertEquals(transformations.degenerate(i for i in range(3)), [0, 1, 2])

if __name__ == "__main__":
    unittest.main()
