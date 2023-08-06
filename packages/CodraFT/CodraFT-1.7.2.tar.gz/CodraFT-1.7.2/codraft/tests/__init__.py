# -*- coding: utf-8 -*-
#
# Licensed under the terms of the CECILL License
# (see codraft/__init__.py for details)

"""
CodraFT unit tests
"""

from guidata.guitest import run_testlauncher

import codraft.config  # Loading icons


def run():
    """Run CodraFT test launcher"""
    run_testlauncher(codraft)


if __name__ == "__main__":
    run()
