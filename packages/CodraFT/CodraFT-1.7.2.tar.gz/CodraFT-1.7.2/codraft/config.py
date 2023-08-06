# -*- coding: utf-8 -*-
#
# Licensed under the terms of the CECILL License
# (see codraft/__init__.py for details)

"""
codraft.config
--------------

The `config` module handles `codraft` configuration
(options, images and icons).
"""

import os
import os.path as osp

from guidata import configtools
from guidata.config import CONF

from codraft.utils import tests

_ = configtools.get_translation("codraft")

APP_NAME = _("CodraFT")
APP_DESC = _(
    """<b>Codra</b> <b>F</b>iltering <b>T</b>ool<br>
Generic signal and image processing software based on Python and Qt"""
)
APP_PATH = osp.dirname(__file__)
DEBUG = len(os.environ.get("DEBUG", "")) > 0

configtools.add_image_module_path("codraft", osp.join("data", "logo"))
configtools.add_image_module_path("codraft", osp.join("data", "icons"))

DEFAULTS = {}
CONF.update_defaults(DEFAULTS)
CONF.set_application(APP_NAME, "1.0.0", load=not DEBUG)

tests.add_test_module_path("codraft", osp.join("data", "tests"))
