# -*- coding: utf-8 -*-
#
# Licensed under the terms of the CECILL License
# (see codraft/__init__.py for details)

"""
Peak detection test
"""

# pylint: disable=invalid-name  # Allows short reference names like x, y, ...

from pprint import pprint

import numpy as np

from codraft.utils.qthelpers import qt_app_context
from codraft.utils.tests import get_test_fnames
from codraft.widgets.peak_dialog import PeakDetectionDialog

SHOW = True  # Show test in GUI-based test launcher


def test():
    """Peak dialog test"""
    with qt_app_context() as app:
        data = np.loadtxt(get_test_fnames("paracetamol.txt")[0], delimiter=",")
        x, y = data.T
        dlg = PeakDetectionDialog()
        dlg.setup_data(x, y)
        dlg.show()
        app.exec()
        print("peaks:")
        pprint(dlg.get_peaks())


if __name__ == "__main__":
    test()
