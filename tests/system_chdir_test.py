# This import fixes sys.path issues
from .parentpath import *

import os
import unittest
from ogutils.system import chdir

class SystemChDirTest(unittest.TestCase):
    def test_chdir(self):
        cd = os.getcwd()
        with chdir.ChDir('..'):
            self.assertNotEqual(os.getcwd(), cd)
            self.assertEquals(os.path.abspath(os.getcwd()), os.path.abspath(os.path.join(cd, '..')))
        self.assertEquals(os.getcwd(), cd)

    def test_chdir_finally(self):
        cd = os.getcwd()
        changer = chdir.ChDir('..')
        try:
            changer.ch_dir()
            self.assertNotEqual(os.getcwd(), cd)
            self.assertEquals(os.path.abspath(os.getcwd()), os.path.abspath(os.path.join(cd, '..')))
        finally:
            changer.undo_ch()
        self.assertEquals(os.getcwd(), cd)

if __name__ == "__main__":
    unittest.main()
