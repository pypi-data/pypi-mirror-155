# -*- coding: utf-8 -*-
#
# Licensed under the terms of the CECILL License
# (see codraft/__init__.py for details)

"""
CodraFT
=======

CodraFT is a generic signal and image processing software based on Python scientific
libraries (such as NumPy, SciPy or OpenCV) and Qt graphical user interfaces (thanks to
guidata and guiqwt libraries).

CodraFT is Copyright © 2018 CEA-CODRA, Pierre Raybaut, and Licensed under the
terms of the CeCILL License v2.1.
"""

from distutils.core import setup

import setuptools  # analysis:ignore
from guidata.configtools import get_module_data_path
from guidata.utils import get_package_data, get_subpackages

from codraft import __docurl__
from codraft import __version__ as version
from codraft.utils import dephash

LIBNAME = "CodraFT"
MODNAME = LIBNAME.lower()

DESCRIPTION = "Signal and image processing software"
LONG_DESCRIPTION = f"""\
CodraFT: Signal and Image Processing Software
=============================================

.. image:: https://raw.githubusercontent.com/CODRA-Ingenierie-Informatique/CodraFT/master/doc/images/dark_light_modes.png

CodraFT is a generic signal and image processing software based on Python scientific
libraries (such as NumPy, SciPy or OpenCV) and Qt graphical user interfaces (thanks to
guidata and guiqwt libraries).

CodraFT stands for "CODRA Filtering Tool".

See `documentation`_ for more details on the library and `changelog`_ for
recent history of changes.

Copyright © 2018-2022 CODRA, Pierre Raybaut
Copyright © 2009-2015 CEA, Pierre Raybaut
Licensed under the terms of the `CECILL License`_.

.. _documentation: {__docurl__}
.. _changelog: https://github.com/CODRA-Ingenierie-Informatique/CodraFT/blob/master/CHANGELOG.md
.. _CECILL License: https://github.com/CODRA-Ingenierie-Informatique/CodraFT/blob/master/Licence_CeCILL_V2.1-en.txt
"""

KEYWORDS = ""
CLASSIFIERS = ["Topic :: Scientific/Engineering"]
if "beta" in version or "b" in version:
    CLASSIFIERS += ["Development Status :: 4 - Beta"]
elif "alpha" in version or "a" in version:
    CLASSIFIERS += ["Development Status :: 3 - Alpha"]
else:
    CLASSIFIERS += ["Development Status :: 5 - Production/Stable"]


dephash.create_dependencies_file(
    get_module_data_path("codraft", "data"), ("guidata", "guiqwt")
)

setup(
    name=LIBNAME,
    version=version,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=get_subpackages(MODNAME),
    package_data={
        MODNAME: get_package_data(
            MODNAME, (".png", ".svg", ".mo", ".chm", ".txt", ".h5", ".sig", ".csv")
        )
    },
    install_requires=[
        "NumPy>=1.21",
        "SciPy>=1.7",
        "guidata>=2.1",
        "guiqwt>=4.1",
        "QtPy>=1.9",
    ],
    entry_points={"gui_scripts": [f"{MODNAME} = {MODNAME}.app:run"]},
    author="Pierre Raybaut",
    author_email="p.raybaut@codra.fr",
    url=f"https://github.com/CODRA-Ingenierie-Informatique/{LIBNAME}",
    license="CeCILL V2",
    classifiers=CLASSIFIERS
    + [
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: OS Independent",
        "Operating System :: POSIX",
        "Operating System :: Unix",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
