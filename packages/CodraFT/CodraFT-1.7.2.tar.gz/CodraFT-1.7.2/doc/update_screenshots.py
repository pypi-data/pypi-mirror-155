# -*- coding: utf-8 -*-
#
# Licensed under the terms of the CECILL License
# (see codraft/__init__.py for details)

"""
Module for taking CodraFT screenshots
"""

from codraft.app import create
from codraft.tests.data import create_test_image1, create_test_signal1
from codraft.utils.qthelpers import qt_app_context


def take_menu_screenshots():
    """Run the CodraFT application and take screenshots"""
    sig1 = create_test_signal1()
    ima1 = create_test_image1()
    objects = (sig1, ima1)
    with qt_app_context():
        window = create(splash=False, objects=objects, size=(1000, 500))
        window.take_menu_screenshots()
        window.take_screenshot("i_simple_example")
        window.tabwidget.setCurrentWidget(window.signalft)
        window.take_screenshot("s_simple_example")
        window.set_modified(False)
        window.close()


if __name__ == "__main__":
    take_menu_screenshots()
