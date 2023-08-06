# -*- coding: utf-8 -*-
#
# Licensed under the terms of the CECILL License
# (see codraft/__init__.py for details)

"""
CodraFT Qt utilities
"""

import functools
import os
import os.path as osp
import traceback
from contextlib import contextmanager

import guidata
from guidata.configtools import get_module_data_path
from qtpy import QtCore as QC
from qtpy import QtGui as QG
from qtpy import QtWidgets as QW

from codraft.config import APP_NAME, _


@contextmanager
def qt_app_context():
    """Context manager handling Qt application creation and persistance"""
    try:
        app = guidata.qapplication()
        yield app
    finally:
        pass


def create_progress_bar(parent, label, max_):
    """Create modal progress bar"""
    prog = QW.QProgressDialog(label, _("Cancel"), 0, max_, parent, QC.Qt.SplashScreen)
    prog.setWindowModality(QC.Qt.WindowModal)
    prog.show()
    QW.QApplication.processEvents()
    return prog


def qt_handle_error_message(widget, message):
    """Handles application (QWidget) error message"""
    traceback.print_exc()
    txt = str(message)
    msglines = txt.splitlines()
    if len(msglines) > 10:
        txt = os.linesep.join(msglines[:10] + ["..."])
    title = widget.window().objectName()
    QW.QMessageBox.critical(widget, title, _("Error:") + f"\n{txt}")


def qt_try_except(message=None):
    """Try...except Qt widget method decorator"""

    def qt_try_except_decorator(func):
        """Try...except Qt widget method decorator"""

        @functools.wraps(func)
        def method_wrapper(*args, **kwargs):
            """Decorator wrapper function"""
            self = args[0]
            if message is not None:
                self.SIG_STATUS_MESSAGE.emit(message)
                QW.QApplication.setOverrideCursor(QG.QCursor(QC.Qt.WaitCursor))
                self.repaint()
            output = None
            try:
                output = func(*args, **kwargs)
            except Exception as msg:  # pylint: disable=broad-except
                qt_handle_error_message(self.parent(), msg)
            finally:
                self.SIG_STATUS_MESSAGE.emit("")
                QW.QApplication.restoreOverrideCursor()
            return output

        return method_wrapper

    return qt_try_except_decorator


@contextmanager
def qt_try_opening_file(widget, filename):
    """Try and open file"""
    try:
        yield filename
    except Exception as msg:  # pylint: disable=broad-except
        traceback.print_exc()
        QW.QMessageBox.critical(
            widget,
            APP_NAME,
            (_("%s could not be opened:") % osp.basename(filename)) + "\n" + str(msg),
        )
    finally:
        pass


SHOTPATH = osp.join(
    get_module_data_path("codraft"), os.pardir, "doc", "images", "shots"
)


def grab_save_window(widget, name):
    """Grab window screenshot and save it"""
    QW.QApplication.processEvents()
    pixmap = QW.QApplication.primaryScreen().grabWindow(widget.winId())
    pixmap.save(osp.join(SHOTPATH, f"{name}.png"))
