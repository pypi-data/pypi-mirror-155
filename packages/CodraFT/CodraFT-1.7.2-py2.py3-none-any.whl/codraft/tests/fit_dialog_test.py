# -*- coding: utf-8 -*-
#
# Licensed under the terms of the CECILL License
# (see codraft/__init__.py for details)

"""Curve fitting dialog test"""

# pylint: disable=invalid-name  # Allows short reference names like x, y, ...


import numpy as np

from codraft.core.computation.signal import peak_indexes
from codraft.tests.data import get_test_fnames
from codraft.utils.qthelpers import qt_app_context
from codraft.widgets.fit_dialog import multigaussianfit

SHOW = True  # Show test in GUI-based test launcher


def test():
    """Test function"""
    with qt_app_context():
        x, y = np.loadtxt(get_test_fnames("paracetamol.txt")[0], delimiter=",").T
        peakindexes = peak_indexes(y)
        print(multigaussianfit(x, y, peakindexes))


if __name__ == "__main__":
    test()
