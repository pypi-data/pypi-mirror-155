# -*- coding: utf-8 -*-
#
# Licensed under the terms of the CECILL License
# (see codraft/__init__.py for details)

"""
Enclosing circle test
"""

# pylint: disable=invalid-name  # Allows short reference names like x, y, ...

from guiqwt.builder import make

from codraft.config import _
from codraft.core.computation.image import get_centroid_fourier, get_enclosing_circle
from codraft.tests.data import get_laser_spot_data
from codraft.utils.qthelpers import qt_app_context
from codraft.utils.vistools import view_image_items

SHOW = True  # Show test in GUI-based test launcher


def test_enclosingcircle(data):
    """Enclosing circle test function"""
    items = []
    items += [make.image(data, interpolation="nearest", eliminate_outliers=1.0)]

    # Computing centroid coordinates
    row, col = get_centroid_fourier(data)
    label = _("Centroid") + " (%d, %d)"
    print(label % (row, col))
    cursor = make.xcursor(col, row, label=label)
    cursor.set_resizable(False)
    cursor.set_movable(False)
    items.append(cursor)

    x, y, radius = get_enclosing_circle(data)
    circle = make.circle(x - radius, y - radius, x + radius, y + radius)
    circle.set_readonly(True)
    circle.set_resizable(False)
    circle.set_movable(False)
    items.append(circle)
    print(x, y, radius)
    print("")

    view_image_items(items)


def enclosing_circle_test():
    """Test"""
    with qt_app_context():
        for data in get_laser_spot_data():
            test_enclosingcircle(data)


if __name__ == "__main__":
    enclosing_circle_test()
