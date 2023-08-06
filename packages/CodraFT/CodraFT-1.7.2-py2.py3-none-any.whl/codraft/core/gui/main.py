# -*- coding: utf-8 -*-
#
# Licensed under the terms of the CECILL License
# (see codraft/__init__.py for details)

"""
CodraFT main window
"""

# pylint: disable=invalid-name  # Allows short reference names like x, y, ...

import locale
import os
import os.path as osp
import platform
import sys
import time
import webbrowser

import numpy as np
import scipy.ndimage as spi
import scipy.signal as sps
from guidata import __version__ as guidata_ver
from guidata.configtools import get_icon, get_module_data_path, get_module_path
from guidata.qthelpers import add_actions, create_action, win32_fix_title_bar_background
from guidata.widgets.console import DockableConsole
from guiqwt import __version__ as guiqwt_ver
from guiqwt.builder import make
from guiqwt.plot import CurveWidget, ImageWidget
from qtpy import QtCore as QC
from qtpy import QtGui as QG
from qtpy import QtWidgets as QW
from qtpy.compat import getopenfilename, getsavefilename
from qwt import __version__ as qwt_ver

from codraft import __version__, __docurl__
from codraft.config import APP_DESC, APP_NAME, _
from codraft.core.gui.base import ActionCategory
from codraft.core.gui.docks import DockablePlotWidget, DockableTabWidget
from codraft.core.gui.h5io import H5InputOutput
from codraft.core.gui.image import ImageFT
from codraft.core.gui.signal import SignalFT
from codraft.core.model import ImageParam, SignalParam
from codraft.utils import dephash
from codraft.utils.qthelpers import grab_save_window


DATAPATH = get_module_data_path("codraft", "data")


def get_htmlhelp():
    """Return HTML Help documentation link adapted to locale, if it exists"""
    if os.name == "nt":
        for suffix in ("_" + locale.getlocale()[0][:2], ""):
            path = osp.join(DATAPATH, f"CodraFT{suffix}.chm")
            if osp.isfile(path):
                return path
    return None


class AppProxy:
    """Proxy to CodraFT application: object used from the embedded console
    to access CodraFT internal objects"""

    def __init__(self, win):
        self.win = win
        self.s = self.win.signalft.objects
        self.i = self.win.imageft.objects


def is_frozen(module_name):
    """Test if module has been frozen (py2exe/cx_Freeze)"""
    datapath = get_module_path(module_name)
    parentdir = osp.normpath(osp.join(datapath, osp.pardir))
    return not osp.isfile(__file__) or osp.isfile(parentdir)  # library.zip


class CodraFTMainWindow(QW.QMainWindow):
    """CodraFT main window"""

    __instance = None

    @staticmethod
    def get_instance(console=True, hide_on_close=False):
        """Return singleton instance"""
        if CodraFTMainWindow.__instance is None:
            return CodraFTMainWindow(console, hide_on_close)
        return CodraFTMainWindow.__instance

    def __init__(self, console=True, hide_on_close=False):
        """Initialize main window"""
        CodraFTMainWindow.__instance = self
        super().__init__()
        win32_fix_title_bar_background(self)
        self.setObjectName(APP_NAME)
        self.setWindowIcon(get_icon("codraft.svg"))

        self.hide_on_close = hide_on_close
        self.__old_size = None

        self.console = None
        self.app_proxy = None
        self.signal_toolbar = None
        self.image_toolbar = None
        self.signalft = None
        self.imageft = None
        self.tabwidget = None
        self.signal_image_docks = None
        self.h5import = H5InputOutput(self)

        self.openh5_action = None
        self.saveh5_action = None
        self.quit_action = None

        self.file_menu = None
        self.edit_menu = None
        self.operation_menu = None
        self.processing_menu = None
        self.computing_menu = None
        self.view_menu = None
        self.help_menu = None

        self.__is_modified = None
        self.set_modified(False)

        # Setup actions and menus
        self.setup(console)

    def check_dependencies(self):
        """Check dependencies"""
        if is_frozen("codraft"):
            # No need to check dependencies if CodraFT has been frozen
            return
        try:
            state = dephash.check_dependencies_hash(DATAPATH)
        except IOError:
            fname = osp.join(DATAPATH, dephash.DEPFILENAME)
            txt = _("Unable to open file") + " " + fname
            QW.QMessageBox.critical(self, APP_NAME, txt)
            return
        bad_deps = [name for name in state if not state[name]]
        if bad_deps:
            txt0 = _("Invalid dependency:")
            if len(bad_deps) > 1:
                txt0 = _("Invalid dependencies:")
            txt = "<br>".join(
                [
                    "<u>" + txt0 + "</u> " + ", ".join(bad_deps),
                    "",
                    "",
                    _("At least one dependency has been altered."),
                    _("Application may not behave as expected."),
                ]
            )
            QW.QMessageBox.critical(self, APP_NAME, txt)

    def take_screenshot(self, name):
        """Take main window screenshot"""
        grab_save_window(self, f"{name}")

    def take_menu_screenshots(self):
        """Take menu screenshots"""
        for index in range(2):
            self.tabwidget.setCurrentIndex(index)
            panelname = self.tabwidget.currentWidget().objectName()
            for name in (
                "file",
                "edit",
                "view",
                "operation",
                "processing",
                "computing",
                "help",
            ):
                menu = getattr(self, f"{name}_menu")
                menu.popup(self.pos())
                grab_save_window(menu, f"{panelname}_{name}")
                menu.close()

    # ------GUI setup
    def setup(self, console=True):
        """Setup main window"""
        self.statusBar().showMessage(_("Welcome to %s!") % APP_NAME, 5000)
        self.setup_commmon_actions()
        curvewidget = self.add_signal_panel()
        imagewidget = self.add_image_panel()
        self.add_tabwidget(curvewidget, imagewidget)
        self.add_menus()
        if console:
            self.setup_console()
        # Update selection dependent actions
        self.update_actions()
        self.signal_image_docks[0].raise_()

    def setup_commmon_actions(self):
        """Setup common actions"""
        self.openh5_action = create_action(
            self,
            _("Open HDF5 file..."),
            icon=get_icon("libre-gui-folder-open.svg"),
            tip=_("Open an HDF5 file"),
            triggered=lambda checked=False: self.open_hdf5_file(),
        )
        self.saveh5_action = create_action(
            self,
            _("Save to HDF5 file..."),
            icon=get_icon("libre-gui-save.svg"),
            tip=_("Save to HDF5 file"),
            triggered=self.save_to_hdf5_file,
        )
        h5_toolbar = self.addToolBar(_("HDF5 I/O Toolbar"))
        add_actions(h5_toolbar, [self.openh5_action, self.saveh5_action])
        # Quit action for "File menu" (added when populating menu on demand)
        if self.hide_on_close:
            quit_text = _("Hide window")
            quit_tip = _("Hide CodraFT window")
        else:
            quit_text = _("Quit")
            quit_tip = _("Quit application")
        self.quit_action = create_action(
            self,
            quit_text,
            shortcut=QG.QKeySequence(QG.QKeySequence.Quit),
            icon=get_icon("libre-gui-close.svg"),
            tip=quit_tip,
            triggered=self.close,
        )

    def add_signal_panel(self):
        """Setup signal toolbar, widgets and panel"""
        self.signal_toolbar = self.addToolBar(_("Signal Processing Toolbar"))
        curveplot_toolbar = self.addToolBar(_("Curve Plotting Toolbar"))
        curvewidget = DockablePlotWidget(self, CurveWidget, curveplot_toolbar)
        curveplot = curvewidget.get_plot()
        curveplot.add_item(make.legend("TR"))
        self.signalft = SignalFT(self, curvewidget)
        self.signalft.setup(self.signal_toolbar)
        self.signalft.SIG_STATUS_MESSAGE.connect(self.statusBar().showMessage)
        return curvewidget

    def add_image_panel(self):
        """Setup image toolbar, widgets and panel"""
        self.image_toolbar = self.addToolBar(_("Image Processing Toolbar"))
        imagevis_toolbar = self.addToolBar(_("Image Visualization Toolbar"))
        imagewidget = DockablePlotWidget(self, ImageWidget, imagevis_toolbar)
        self.imageft = ImageFT(self, imagewidget)
        self.imageft.setup(self.image_toolbar)
        # -----------------------------------------------------------------------------
        # # Before eventually disabling the "peritem" mode by default, wait for the
        # # guiqwt bug to be fixed (peritem mode is not compatible with multiple image
        # # items):
        # for cspanel in (
        #     self.imageft.plotwidget.get_xcs_panel(),
        #     self.imageft.plotwidget.get_ycs_panel(),
        # ):
        #     cspanel.peritem_ac.setChecked(False)
        # -----------------------------------------------------------------------------
        self.imageft.SIG_STATUS_MESSAGE.connect(self.statusBar().showMessage)
        return imagewidget

    def add_tabwidget(self, curvewidget, imagewidget):
        """Setup tabwidget with signals and images"""
        self.tabwidget = DockableTabWidget()
        self.tabwidget.setMaximumWidth(500)
        self.tabwidget.addTab(self.signalft, get_icon("signal.svg"), _("Signals"))
        self.tabwidget.addTab(self.imageft, get_icon("image.svg"), _("Images"))
        self._add_dockwidget(self.tabwidget, _("Main panel"))
        curve_dock = self._add_dockwidget(curvewidget, title=_("Curve panel"))
        image_dock = self._add_dockwidget(imagewidget, title=_("Image panel"))
        self.tabifyDockWidget(curve_dock, image_dock)
        self.signal_image_docks = curve_dock, image_dock
        self.tabwidget.currentChanged.connect(self._tab_index_changed)
        self.signalft.SIG_OBJECT_ADDED.connect(
            lambda: self.tabwidget.setCurrentIndex(0)
        )
        self.imageft.SIG_OBJECT_ADDED.connect(lambda: self.tabwidget.setCurrentIndex(1))
        for view in (self.signalft, self.imageft):
            view.SIG_OBJECT_ADDED.connect(lambda state=True: self.set_modified(state))
            view.SIG_OBJECT_REMOVED.connect(lambda state=True: self.set_modified(state))

    def add_menus(self):
        """Adding menus"""
        self.file_menu = self.menuBar().addMenu(_("File"))
        self.file_menu.aboutToShow.connect(self._update_file_menu)
        self.edit_menu = self.menuBar().addMenu(_("&Edit"))
        self.operation_menu = self.menuBar().addMenu(_("Operations"))
        self.processing_menu = self.menuBar().addMenu(_("Processing"))
        self.computing_menu = self.menuBar().addMenu(_("Computing"))
        self.view_menu = self.menuBar().addMenu(_("&View"))
        self.view_menu.aboutToShow.connect(self._update_view_menu)
        self.help_menu = self.menuBar().addMenu("?")
        for menu in (
            self.edit_menu,
            self.operation_menu,
            self.processing_menu,
            self.computing_menu,
        ):
            menu.aboutToShow.connect(self._update_generic_menu)
        about_action = create_action(
            self,
            _("About..."),
            icon=get_icon("libre-gui-about.svg"),
            triggered=self.about,
        )
        onlinedoc_action = create_action(
            self,
            _("Online documentation"),
            icon=get_icon("libre-gui-help.svg"),
            triggered=lambda: webbrowser.open(__docurl__),
        )
        chmdoc_action = create_action(
            self,
            _("CHM documentation"),
            icon=get_icon("chm.svg"),
            triggered=lambda: os.startfile(get_htmlhelp()),
        )
        chmdoc_action.setVisible(get_htmlhelp() is not None)
        about_action = create_action(
            self,
            _("About..."),
            icon=get_icon("libre-gui-about.svg"),
            triggered=self.about,
        )
        add_actions(
            self.help_menu,
            (
                onlinedoc_action,
                chmdoc_action,
                None,
                about_action,
            ),
        )

    def setup_console(self):
        """Add an internal console"""
        self.app_proxy = AppProxy(self)
        ns = {
            "app": self.app_proxy,
            "np": np,
            "sps": sps,
            "spi": spi,
            "os": os,
            "sys": sys,
            "osp": osp,
            "time": time,
        }
        msg = (
            "Example: app.s[0] returns signal object #0\n"
            "Modules imported at startup: "
            "os, sys, os.path as osp, time, "
            "numpy as np, scipy.signal as sps, scipy.ndimage as spi"
        )
        debug = os.environ.get("DEBUG") == "1"
        self.console = DockableConsole(self, namespace=ns, message=msg, debug=debug)
        console_dock = self._add_dockwidget(self.console, _("Console"))
        console_dock.hide()
        self.console.interpreter.widget_proxy.sig_new_prompt.connect(
            lambda txt: self.refresh_lists()
        )

    # ------GUI refresh
    def set_modified(self, state):
        """Set mainwindow modified state"""
        state = state and len(self.signalft.objects + self.imageft.objects) > 0
        self.__is_modified = state
        self.setWindowTitle(APP_NAME + ("*" if state else ""))

    def _add_dockwidget(self, child, title):
        """Add QDockWidget and toggleViewAction"""
        dockwidget, location = child.create_dockwidget(title)
        self.addDockWidget(location, dockwidget)
        return dockwidget

    def refresh_lists(self):
        """Refresh signal/image lists"""
        self.signalft.refresh_list()
        self.imageft.refresh_list()

    def update_actions(self):
        """Update selection dependent actions"""
        is_signal = self.tabwidget.currentWidget() is self.signalft
        objectft = self.signalft if is_signal else self.imageft
        objectft.selection_changed()
        self.signal_toolbar.setVisible(is_signal)
        self.image_toolbar.setVisible(not is_signal)

    def _tab_index_changed(self, index):
        """Switch from signal to image mode, or vice-versa"""
        dock = self.signal_image_docks[index]
        dock.raise_()
        self.update_actions()

    def _update_generic_menu(self, menu=None):
        """Update menu before showing up -- Generic method"""
        if menu is None:
            menu = self.sender()
        menu.clear()
        objectft = self.tabwidget.currentWidget()
        category = {
            self.file_menu: ActionCategory.FILE,
            self.edit_menu: ActionCategory.EDIT,
            self.view_menu: ActionCategory.VIEW,
            self.operation_menu: ActionCategory.OPERATION,
            self.processing_menu: ActionCategory.PROCESSING,
            self.computing_menu: ActionCategory.COMPUTING,
        }[menu]
        actions = objectft.get_category_actions(category)
        add_actions(menu, actions)

    def _update_file_menu(self):
        """Update file menu before showing up"""
        self.saveh5_action.setEnabled(
            len(self.signalft.objects) + len(self.imageft.objects)
        )
        self._update_generic_menu(self.file_menu)
        add_actions(
            self.file_menu,
            [None, self.openh5_action, self.saveh5_action, None, self.quit_action],
        )

    def _update_view_menu(self):
        """Update view menu before showing up"""
        self._update_generic_menu(self.view_menu)
        add_actions(self.view_menu, [None] + self.createPopupMenu().actions())

    # ------Common features
    def reset_all(self):
        """Reset all application data"""
        for view in (self.signalft, self.imageft):
            view.remove_all_objects()

    def save_to_hdf5_file(self):
        """Save into an HDF5 file"""
        saved_in, saved_out, saved_err = sys.stdin, sys.stdout, sys.stderr
        sys.stdout = None
        filters = f'{_("HDF5 files")} (*.h5)'
        filename, _filter = getsavefilename(self, _("Save"), "", filters)
        sys.stdin, sys.stdout, sys.stderr = saved_in, saved_out, saved_err
        if not filename:
            return
        self.h5import.save(filename)

    def open_hdf5_file(self, filename=None, import_all=False):
        """Open an HDF5 file"""
        reset_all = False
        if self.signalft.objects or self.imageft.objects:
            answer = QW.QMessageBox.question(
                self,
                _("Warning"),
                _(
                    "Do you want to remove all signals and images "
                    "before importing data from an HDF5 file?"
                ),
                QW.QMessageBox.Yes | QW.QMessageBox.No,
            )
            if answer == QW.QMessageBox.Yes:
                reset_all = True
        if filename is None:
            saved_in, saved_out, saved_err = sys.stdin, sys.stdout, sys.stderr
            sys.stdout = None
            filters = f'{_("HDF5 files")} (*.h5)'
            filename, _filter = getopenfilename(self, _("Open"), "", filters)
            sys.stdin, sys.stdout, sys.stderr = saved_in, saved_out, saved_err
            if not filename:
                return
        else:
            filename = osp.abspath(filename)
            bname = osp.basename(filename)
            if not osp.isfile(filename):
                raise IOError(f'File not found "{bname}"')
            if not filename.endswith(".h5"):
                raise IOError(f'Invalid HDF5 file "{bname}"')
        self.h5import.open(filename, import_all, reset_all)

    def add_object(self, obj, refresh=True):
        """Add object - signal or image"""
        if isinstance(obj, SignalParam):
            self.signalft.add_object(obj, refresh=refresh)
        elif isinstance(obj, ImageParam):
            self.imageft.add_object(obj, refresh=refresh)
        else:
            raise TypeError(f"Unsupported object type {type(obj)}")

    # ------?
    def about(self):
        """About dialog box"""

        QW.QMessageBox.about(
            self,
            _("About ") + APP_NAME,
            f"""<b>{APP_NAME}</b> v{__version__}<br>{APP_DESC}<p>
              {_("Developped by")} Pierre Raybaut
              <br>Copyright &copy; 2010 CEA<br>Copyright &copy; 2018 CODRA
              <p>PythonQwt {qwt_ver}, guidata {guidata_ver}
              , guiqwt {guiqwt_ver}<br>Python {platform.python_version()}
              , Qt {QC.__version__}, PyQt {QC.PYQT_VERSION_STR}
               {_("on")} {platform.system()}""",
        )

    def show(self):
        """Reimplement QMainWindow method"""
        super().show()
        if self.__old_size is not None:
            self.resize(self.__old_size)

    def closeEvent(self, event):
        """Reimplement QMainWindow method"""
        if self.hide_on_close:
            self.__old_size = self.size()
            self.hide()
        else:
            if self.__is_modified:
                answer = QW.QMessageBox.warning(
                    self,
                    _("Quit"),
                    _(
                        "Do you want to save all signals and images "
                        "to an HDF5 file before quitting CodraFT?"
                    ),
                    QW.QMessageBox.Yes | QW.QMessageBox.No | QW.QMessageBox.Cancel,
                )
                if answer == QW.QMessageBox.Yes:
                    self.save_to_hdf5_file()
                    if self.__is_modified:
                        event.ignore()
                        return
                elif answer == QW.QMessageBox.Cancel:
                    event.ignore()
                    return
            if self.console is not None:
                self.console.close()
            self.reset_all()
            event.accept()
