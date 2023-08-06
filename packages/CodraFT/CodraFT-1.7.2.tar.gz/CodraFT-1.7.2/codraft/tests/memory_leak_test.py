# -*- coding: utf-8 -*-
#
# Licensed under the terms of the CECILL License
# (see codraft/__init__.py for details)

"""
Memory leak test
"""

import os

import psutil
from guiqwt import pyplot as plt

from codraft.tests.embedded1_test import MainView
from codraft.utils.qthelpers import qt_app_context

SHOW = True  # Show test in GUI-based test launcher


def memory_leak_test():
    """Test for memory leak"""
    with qt_app_context():
        proc = psutil.Process(os.getpid())
        test = MainView()
        test.show()
        memlist = []
        for i in range(100):
            test.open_codraft()
            test.codraft.close()
            # test.codraft.destroy()
            # test.codraft = None
            # QApplication.processEvents()
            # import time; time.sleep(2)
            # QApplication.processEvents()
            memdata = proc.memory_info().vms / 1024**2
            memlist.append(memdata)
            print(i + 1, ":", memdata, "MB")
        plt.plot(memlist)
        plt.title("Memory leak test for CodraFT application")
        plt.ylabel("Memory (MB)")
        plt.show()


if __name__ == "__main__":
    memory_leak_test()
