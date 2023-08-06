# -*- coding: utf-8 -*-
#
# Licensed under the terms of the CECILL License
# (see codraft/__init__.py for details)

"""
Application launcher test 3

Create signal and image objects (with circles, rectangles, segments and markers),
then open CodraFT to show them.
"""

# pylint: disable=invalid-name  # Allows short reference names like x, y, ...

from codraft.app import run
from codraft.tests.app2_test import create_test_signal1
from codraft.tests.data import create_test_image1, create_test_image2

SHOW = True  # Show test in GUI-based test launcher


def test():
    """Simple test"""
    shape = (2000, 2000)
    sig1 = create_test_signal1()
    ima1 = create_test_image1(shape)
    ima2 = create_test_image2(shape, with_metadata=True)
    objects = [sig1, ima1, ima2]
    run(objects=objects, size=(1200, 550))


if __name__ == "__main__":
    test()
