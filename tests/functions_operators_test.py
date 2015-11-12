# This import fixes sys.path issues
from .parentpath import *

import unittest
from ogutils.functions import operators

class FunctionOperatorsTest(unittest.TestCase):
    def test_restrict_args_basics(self):
        self.assertEquals(operators.restrict_args(lambda: '', 'a', 'b'), '')
        self.assertEquals(operators.restrict_args(lambda a: a, 'a'), 'a')
        self.assertEquals(operators.restrict_args(lambda a: a, 'a', 'b'), 'a')
        self.assertEquals(operators.restrict_args(lambda a, b: a + b, 'a', 'b'), 'ab')

    def test_restrict_args_with_kwargs(self):
        self.assertEquals(operators.restrict_args(lambda a: a, a='a'), 'a')
        self.assertEquals(operators.restrict_args(lambda a, b: a + b, 'a', b='b'), 'ab')
        self.assertEquals(operators.restrict_args(lambda a, b: a + b, a='a', b='b'), 'ab')
        with self.assertRaises(TypeError):
            operators.restrict_args(lambda: '', a='a')
        with self.assertRaises(TypeError):
            operators.restrict_args(lambda a: a, 'a', b='b')
        with self.assertRaises(TypeError):
            operators.restrict_args(lambda a: a, 'a', a='a')

    def test_restrict_args_with_too_few_args(self):
        with self.assertRaises(TypeError):
            operators.restrict_args(lambda a: a)
        with self.assertRaises(TypeError):
            operators.restrict_args(lambda a, b: a + b, 'a')
        with self.assertRaises(TypeError):
            operators.restrict_args(lambda a, b: a + b, a='a')
        with self.assertRaises(TypeError):
            operators.restrict_args(lambda a, b: a + b, b='b')

    def test_repeat_call(self):
        def fail_count_down():
            if fail_count_down.fail_count == 0:
                return 'success'
            else:
                fail_count_down.fail_count -= 1
                raise TypeError('fail')
        fail_count_down.fail_count = 0

        self.assertEquals(operators.repeat_call(lambda: 'success', 0), 'success')
        fail_count_down.fail_count = 1
        self.assertEquals(operators.repeat_call(fail_count_down, 1), 'success')
        with self.assertRaises(TypeError):
            fail_count_down.fail_count = 2
            self.assertEquals(operators.repeat_call(fail_count_down, 1), 'success')
        fail_count_down.fail_count = 5
        self.assertEquals(operators.repeat_call(fail_count_down, 5), 'success')

    def test_repeat_call_with_args(self):
        def fail_count_down(*args, **kwargs):
            if fail_count_down.fail_count == 0:
                return (args, kwargs)
            else:
                fail_count_down.fail_count -= 1
                raise TypeError('fail')
        fail_count_down.fail_count = 0

        self.assertEquals(operators.repeat_call(lambda a: a, 0, 'success'), 'success')
        fail_count_down.fail_count = 2
        self.assertEquals(operators.repeat_call(fail_count_down, 2, 'third', a='b'), (('third',), {'a': 'b'}))

if __name__ == "__main__":
    unittest.main()
