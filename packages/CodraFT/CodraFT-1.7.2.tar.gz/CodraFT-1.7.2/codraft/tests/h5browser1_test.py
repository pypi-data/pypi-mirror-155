# -*- coding: utf-8 -*-
#
# Licensed under the terms of the CECILL License
# (see codraft/__init__.py for details)

"""
HDF5 browser test 1

Try and open all HDF5 test data available.
"""

from guidata.configtools import get_icon

from codraft.tests.data import get_test_fnames
from codraft.utils.qthelpers import qt_app_context
from codraft.widgets.h5browser import H5BrowserDialog

SHOW = True  # Show test in GUI-based test launcher


def h5browser_test():
    """HDF5 browser test"""
    with qt_app_context():
        for fname in get_test_fnames("*.h5"):
            print(f"Opening: {fname}")
            dlg = H5BrowserDialog(None)
            dlg.setWindowIcon(get_icon("codraft.svg"))
            dlg.setup(fname)
            dlg.exec()


if __name__ == "__main__":
    h5browser_test()
