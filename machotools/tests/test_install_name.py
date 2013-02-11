import shutil
import tempfile
import unittest

import os.path as op

import machotools.misc

DYLIB_DIRECTORY = op.join(op.dirname(__file__), "data")

FILES_TO_INSTALL_NAME = {
    op.join(DYLIB_DIRECTORY, "foo.dylib"): "foo.dylib",
    op.join(DYLIB_DIRECTORY, "foo2.dylib"): "yoyo.dylib",
}

class TestInstallName(unittest.TestCase):
    def test_simple_read(self):
        for f, install_name in FILES_TO_INSTALL_NAME.iteritems():
            self.assertEqual(len(machotools.misc.install_name(f)), 1)
            self.assertEqual(machotools.misc.install_name(f)[0], install_name)

    def test_simple_write(self):
        r_install_name = "youpla.dylib"

        temp_fp = tempfile.NamedTemporaryFile()
        dylib = op.join(DYLIB_DIRECTORY, "foo.dylib")
        with open(dylib, "rb") as fp:
            shutil.copyfileobj(fp, temp_fp)

        machotools.misc.change_install_name(temp_fp.name, r_install_name)

        self.assertEqual(machotools.misc.install_name(temp_fp.name)[0], r_install_name)
