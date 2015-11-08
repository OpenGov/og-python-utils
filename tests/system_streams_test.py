from __future__ import print_function

# This import fixes sys.path issues
from .parentpath import *

import sys
import unittest
import StringIO
from ogutils.system import streams

class SystemStreamsTest(unittest.TestCase):
    def test_stdout_stream(self):
        stdout = StringIO.StringIO()
        with streams.StdRedirector(stdout):
            self.assertEquals(sys.stdout, stdout)
            sys.stdout.write('1\n')
            print('2')
        self.assertNotEqual(sys.stdout, stdout)
        self.assertEquals(stdout.getvalue(), '1\n2\n')

    def test_stderr_stream(self):
        stderr = StringIO.StringIO()
        with streams.StdRedirector(stderr=stderr):
            self.assertEquals(sys.stderr, stderr)
            sys.stderr.write('1\n')
            print('2', file=sys.stderr)
        self.assertNotEqual(sys.stderr, stderr)
        self.assertEquals(stderr.getvalue(), '1\n2\n')

if __name__ == "__main__":
    unittest.main()
