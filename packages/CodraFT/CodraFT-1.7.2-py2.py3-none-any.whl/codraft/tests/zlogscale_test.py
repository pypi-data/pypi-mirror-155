# -*- coding: utf-8 -*-
#
# Licensed under the terms of the CECILL License
# (see codraft/__init__.py for details)

"""
Z-log scale test
"""

import numpy as np
from guiqwt.builder import make
from guiqwt.plot import ImageDialog

from codraft import patch  # pylint: disable=unused-import
from codraft.tests.data import create_2d_steps_data
from codraft.utils.qthelpers import qt_app_context

SHOW = True  # Show test in GUI-based test launcher


def zlogscale_test():
    """Z-log scale test"""
    with qt_app_context():
        data = create_2d_steps_data((1024, 1024), width=256, dtype=np.int32)
        win = ImageDialog(edit=False, toolbar=True, wintitle="Z-log scale test")
        item = make.image(data)
        win.get_plot().add_item(item)
        item.set_zaxis_log_state(True)  # pylint: disable=no-member
        win.exec()


if __name__ == "__main__":
    zlogscale_test()
