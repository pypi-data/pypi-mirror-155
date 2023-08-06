# -*- coding: utf-8 -*-
#
# Licensed under the terms of the CECILL License
# (see codraft/__init__.py for details)

"""
New signal/image test
"""

# pylint: disable=invalid-name  # Allows short reference names like x, y, ...

from codraft.config import _
from codraft.core.gui.new import ImageParamNew, SignalParamNew
from codraft.utils.qthelpers import qt_app_context

SHOW = True  # Show test in GUI-based test launcher


def new_signal_image_test():
    """Test new signal/image feature"""
    with qt_app_context():
        signalnew = SignalParamNew(title=_("Create a new signal"))
        if signalnew.edit():
            print(signalnew)
        imagenew = ImageParamNew(title=_("Create a new image"))
        if imagenew.edit():
            print(imagenew)


if __name__ == "__main__":
    new_signal_image_test()
