# -*- coding: utf-8 -*-
#
# Copyright © 2022 Codra
# Pierre Raybaut

"""
Module providing test utilities
"""

import functools
import os
import pathlib

from guidata.configtools import get_module_data_path

TST_PATH = []


def add_test_path_from_env(envvar):
    """Appends test data path from environment variable (fails silently)"""
    path = os.environ.get(envvar)
    if path:
        TST_PATH.append(path)


def add_test_module_path(modname, relpath):
    """
    Appends test data path relative to a module name.
    Used to add module local data that resides in a module directory
    but will be shipped under sys.prefix / share/ ...

    modname must be the name of an already imported module as found in
    sys.modules
    """
    TST_PATH.append(get_module_data_path(modname, relpath=relpath))


def get_test_fnames(name_or_wildcard):
    """Return the absolute path list to test files with specified name/wildcard"""
    pathlist = []
    for pth in TST_PATH:
        pathlist += sorted(pathlib.Path(pth).rglob(name_or_wildcard))
    if not pathlist:
        raise FileNotFoundError(f"Test file(s) {name_or_wildcard} not found")
    return [str(path) for path in pathlist]


def try_open_test_data(title, name_or_wildcard):
    """Decorator handling test data opening"""

    def try_open_test_data_decorator(func):
        """Decorator handling test data opening"""

        @functools.wraps(func)
        def func_wrapper():
            """Decorator wrapper function"""
            print(title + ":")
            print("-" * len(title))
            try:
                for fname in get_test_fnames(name_or_wildcard):
                    print(f"=> Opening: {fname}")
                    func(fname)
            except FileNotFoundError:
                print(f"  No test data available for {name_or_wildcard}")
            finally:
                print(os.linesep)

        return func_wrapper

    return try_open_test_data_decorator
