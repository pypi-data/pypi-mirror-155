# -*- coding: utf-8 -*-
#
# Licensed under the terms of the CECILL License
# (see codraft/__init__.py for details)

"""
Unit test scenario 1
"""

from codraft.app import create
from codraft.tests.data import create_test_image1, create_test_signal1
from codraft.utils.qthelpers import qt_app_context

SHOW = True  # Show test in GUI-based test launcher


def run_scenario1():
    """Run unit test scenario 1"""
    sig1 = create_test_signal1()
    ima1 = create_test_image1()
    objects = (sig1, ima1)
    with qt_app_context() as app:
        window = create(splash=False, objects=objects, size=(1000, 500))
        window.set_modified(False)
        # window.close()
        app.exec()


if __name__ == "__main__":
    run_scenario1()
