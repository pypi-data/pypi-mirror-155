# -*- coding: utf-8 -*-
#
# Licensed under the terms of the CECILL License
# (see codraft/__init__.py for details)

"""
Application launcher test 1

Create signal objects and open CodraFT to show them.
"""

# pylint: disable=invalid-name  # Allows short reference names like x, y, ...

from codraft.app import run
from codraft.tests.data import create_test_signal1, create_test_signal2

SHOW = True  # Show test in GUI-based test launcher


if __name__ == "__main__":
    run(objects=[create_test_signal1(), create_test_signal2()])
