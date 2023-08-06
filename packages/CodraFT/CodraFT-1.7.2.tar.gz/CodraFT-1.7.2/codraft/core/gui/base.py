# -*- coding: utf-8 -*-
#
# Licensed under the terms of the CECILL License
# (see codraft/__init__.py for details)

"""
CodraFT Base GUI module
"""

# pylint: disable=invalid-name  # Allows short reference names like x, y, ...

import abc
import enum

from qtpy import QtWidgets as QW
from qtpy import QtGui as QG
from qtpy import QtCore as QC

import numpy as np

import guidata.dataset.datatypes as gdt
import guidata.dataset.dataitems as gdi
import guidata.dataset.qtwidgets as gdq
from guidata.configtools import get_icon
from guidata.qthelpers import create_action, add_actions
from guidata.utils import update_dataset
from guiqwt.builder import make
from guiqwt.plot import CurveDialog
from guiqwt.styles import style_generator

from codraft.config import _, APP_NAME
from codraft.core.model import SignalParam
from codraft.utils.qthelpers import create_progress_bar, qt_try_except


class ActionCategory(enum.Enum):
    """Action categories"""

    FILE = enum.auto()
    EDIT = enum.auto()
    VIEW = enum.auto()
    OPERATION = enum.auto()
    PROCESSING = enum.auto()
    COMPUTING = enum.auto()


class ObjectFTMeta(type(QW.QSplitter), abc.ABCMeta):
    """Mixed metaclass to avoid conflicts"""


class ObjectFT(QW.QSplitter, metaclass=ObjectFTMeta):
    """Object handling the item list, the selected item properties and plot"""

    PARAMCLASS = SignalParam  # Replaced by the right class in child object
    DIALOGCLASS = CurveDialog  # Idem
    PREFIX = ""  # e.g. "s"
    SIG_OBJECT_ADDED = QC.Signal()
    SIG_OBJECT_REMOVED = QC.Signal()
    SIG_STATUS_MESSAGE = QC.Signal(str)
    OBJECT_STR = ""  # e.g. "signal"

    def __init__(self, parent, plotwidget):
        super().__init__(QC.Qt.Vertical, parent)
        self.setObjectName(self.PREFIX)
        self.plotwidget = plotwidget.plotwidget
        self.plot = plotwidget.get_plot()

        self.objects = []  # signals or images
        self.items = []  # associated plot items
        self._computing_items = []
        self.listwidget = None
        self.properties = None
        self._hsplitter = None
        self._enable_cleanup_dataview = True
        self.feature_actions = {}
        self.operation_end_actions = None
        self.number = 0

        # Object selection dependent actions
        self.actlist_1more = []
        self.actlist_2more = []
        self.actlist_1 = []
        self.actlist_2 = []

    # ------Setup widget, menus, actions
    def setup(self, toolbar):  # pylint: disable=unused-argument
        """Setup QSplitter data object"""
        self.listwidget = QW.QListWidget()
        self.listwidget.setAlternatingRowColors(True)
        self.listwidget.setSelectionMode(QW.QListWidget.ExtendedSelection)
        self.properties = gdq.DataSetEditGroupBox(_("Properties"), self.PARAMCLASS)
        self.properties.SIG_APPLY_BUTTON_CLICKED.connect(self.properties_changed)
        self.properties.setEnabled(False)

        self.listwidget.currentRowChanged.connect(self.current_item_changed)
        self.listwidget.itemSelectionChanged.connect(self.selection_changed)
        self.listwidget.itemDoubleClicked.connect(self.item_double_clicked)

        properties_stretched = QW.QWidget()
        hlayout = QW.QHBoxLayout()
        hlayout.addWidget(self.properties)
        vlayout = QW.QVBoxLayout()
        vlayout.addLayout(hlayout)
        vlayout.addStretch()
        properties_stretched.setLayout(vlayout)

        self.addWidget(self.listwidget)
        self.addWidget(properties_stretched)

        featact = self.feature_actions
        featact[ActionCategory.FILE] = file_act = self.create_file_actions()
        featact[ActionCategory.EDIT] = edit_act = self.create_edit_actions()
        featact[ActionCategory.VIEW] = view_act = self.create_view_actions()
        featact[ActionCategory.OPERATION] = self.create_operation_actions()
        featact[ActionCategory.PROCESSING] = self.create_processing_actions()
        featact[ActionCategory.COMPUTING] = self.create_computing_actions()

        add_actions(toolbar, file_act + [None] + edit_act + [None] + view_act)

    def get_category_actions(self, category):
        """Return actions for category"""
        return self.feature_actions[category]

    def create_file_actions(self):
        """Create file actions"""
        new_action = create_action(
            self,
            _("New %s...") % self.OBJECT_STR,
            icon=get_icon(f"new_{self.OBJECT_STR}.svg"),
            tip=_("Create new %s") % self.OBJECT_STR,
            triggered=self.new_object,
            shortcut=QG.QKeySequence(QG.QKeySequence.New),
        )
        open_action = create_action(
            self,
            _("Open %s...") % self.OBJECT_STR,
            icon=get_icon("libre-gui-import.svg"),
            tip=_("Open %s") % self.OBJECT_STR,
            triggered=self.open_object,
            shortcut=QG.QKeySequence(QG.QKeySequence.Open),
        )
        save_action = create_action(
            self,
            _("Save %s...") % self.OBJECT_STR,
            icon=get_icon("libre-gui-export.svg"),
            tip=_("Save selected %s") % self.OBJECT_STR,
            triggered=self.save_object,
            shortcut=QG.QKeySequence(QG.QKeySequence.Save),
        )
        self.actlist_1more += [save_action]
        return [new_action, open_action, save_action]

    def create_edit_actions(self):
        """Create edit actions"""
        dup_action = create_action(
            self,
            _("Duplicate"),
            icon=get_icon("libre-gui-copy.svg"),
            triggered=self.duplicate_object,
            shortcut=QG.QKeySequence(QG.QKeySequence.Copy),
        )
        cleanup_action = create_action(
            self,
            _("Clean up data view"),
            icon=get_icon("libre-tools-vacuum-cleaner.svg"),
            tip=_("Clean up data view before updating plotting panels"),
            toggled=self.toggle_cleanup_dataview,
        )
        cleanup_action.setChecked(True)
        delm_action = create_action(
            self,
            _("Delete object metadata"),
            icon=get_icon("libre-gui-table-col-remove.svg"),
            tip=_("Delete all that is contained in object metadata"),
            triggered=self.delete_metadata,
        )
        delall_action = create_action(
            self,
            _("Delete all"),
            shortcut="Shift+Ctrl+Suppr",
            triggered=self.delete_all_objects,
        )
        del_action = create_action(
            self,
            _("Remove"),
            icon=get_icon("libre-gui-trash.svg"),
            triggered=self.remove_object,
            shortcut=QG.QKeySequence(QG.QKeySequence.Delete),
        )
        self.actlist_1more += [dup_action, del_action, delm_action]
        return [dup_action, del_action, delm_action, None, delall_action]

    def create_view_actions(self):
        """Create view actions"""
        view_action = create_action(
            self,
            _("View in a new window"),
            icon=get_icon("libre-gui-binoculars.svg"),
            triggered=self.open_separate_view,
        )
        self.actlist_1more += [view_action]
        return [view_action]

    @abc.abstractmethod
    def create_operation_actions(self):
        """Create operation actions"""
        cra = create_action
        sum_action = cra(self, _("Sum"), self.compute_sum)
        average_action = cra(self, _("Average"), self.compute_average)
        diff_action = cra(self, _("Difference"), self.compute_difference)
        prod_action = cra(self, _("Product"), self.compute_product)
        div_action = cra(self, _("Division"), self.compute_division)
        roi_action = cra(
            self,
            _("ROI extraction"),
            self.extract_roi,
            icon=get_icon(f"{self.OBJECT_STR}_roi.svg"),
        )
        swapaxes_action = cra(self, _("Swap X/Y axes"), self.swap_axes)
        abs_action = cra(self, _("Absolute value"), self.compute_abs)
        log_action = cra(self, "Log10(y)", self.compute_log10)
        self.actlist_1more += [roi_action, swapaxes_action, abs_action, log_action]
        self.actlist_2more += [sum_action, average_action, prod_action]
        self.actlist_2 += [diff_action, div_action]
        self.operation_end_actions = [roi_action, swapaxes_action]
        return [
            sum_action,
            average_action,
            diff_action,
            prod_action,
            div_action,
            None,
            abs_action,
            log_action,
        ]

    @abc.abstractmethod
    def create_processing_actions(self):
        """Create processing actions"""
        cra = create_action
        gaussian_action = cra(self, _("Gaussian filter"), self.compute_gaussian)
        movavg_action = cra(self, _("Moving average"), self.compute_moving_average)
        movmed_action = cra(self, _("Moving median"), self.compute_moving_median)
        wiener_action = cra(self, _("Wiener filter"), self.compute_wiener)
        fft_action = cra(self, _("FFT"), self.compute_fft)
        ifft_action = cra(self, _("Inverse FFT"), self.compute_ifft)
        for act in (fft_action, ifft_action):
            act.setToolTip(_("Warning: only real part is plotted"))
        actions = [
            gaussian_action,
            movavg_action,
            movmed_action,
            wiener_action,
            fft_action,
            ifft_action,
        ]
        self.actlist_1more += actions
        return actions

    @abc.abstractmethod
    def create_computing_actions(self):
        """Create computing actions"""
        return []

    # ------GUI refresh/setup
    def current_item_changed(self, row):
        """Current item changed"""
        if row != -1:
            update_dataset(self.properties.dataset, self.objects[row])
            self.properties.get()

    def item_double_clicked(self, listwidgetitem):
        """Item was double-clicked: open a pop-up plot dialog"""
        rows = [self.listwidget.row(listwidgetitem)]
        self.open_separate_view(rows)

    @abc.abstractmethod
    def open_separate_view(self, rows=None):
        """Open separate view for visualizing selected objects"""

    def cleanup_dataview(self):
        """Clean up data view"""
        for item in self.plot.items[:]:
            if item not in self.items:
                self.plot.del_item(item)

    def toggle_cleanup_dataview(self, state):
        """Toggle clean up data view option"""
        self._enable_cleanup_dataview = state

    @abc.abstractmethod
    def get_plot_options(self):
        """Return standard signal/image plot options"""

    def create_new_dialog(self, rows, edit=False, toolbar=True, title=None, tools=None):
        """Create new pop-up signal/image plot dialog"""
        if title is not None or len(rows) == 1:
            if title is None:
                title = self.objects[rows[0]].title
            title = f"{title} - {APP_NAME}"
        else:
            title = APP_NAME
        dlg = self.DIALOGCLASS(
            parent=self,
            wintitle=title,
            edit=edit,
            options=self.get_plot_options(),
            toolbar=toolbar,
        )
        dlg.setWindowIcon(get_icon("codraft.svg"))
        if tools is not None:
            for tool in tools:
                dlg.add_tool(tool)
        plot = dlg.get_plot()
        for row in rows:
            item = self.make_item(self.objects[row], update_from=self.items[row])
            plot.add_item(item, z=0)
        plot.set_active_item(item)
        plot.replot()
        return dlg

    def create_new_dialog_for_selection(self, title):
        """Create new pop-up dialog for the currently selected signal/image,
        return tuple (dialog, current_object)"""
        row = self.get_selected_rows()[0]
        obj = self.objects[row]
        dlg = self.create_new_dialog(
            [row], edit=True, toolbar=False, title=f"{title} - {obj.title}"
        )
        return dlg, obj

    def get_selected_rows(self):
        """Return selected rows"""
        return [
            index.row() for index in self.listwidget.selectionModel().selectedRows()
        ]

    def selection_changed(self):
        """Signal list: selection changed"""
        row = self.listwidget.currentRow()
        self.properties.setDisabled(row == -1)
        self.refresh_plot()
        nbrows = len(self.get_selected_rows())
        for act in self.actlist_1more:
            act.setEnabled(nbrows >= 1)
        for act in self.actlist_2more:
            act.setEnabled(nbrows >= 2)
        for act in self.actlist_1:
            act.setEnabled(nbrows == 1)
        for act in self.actlist_2:
            act.setEnabled(nbrows == 2)

    def add_item(self, row):
        """Add plot item to plot"""
        item = self.make_item(self.objects[row])
        item.set_readonly(True)
        self.items[row] = item
        self.plot.add_item(item)
        return item

    @abc.abstractmethod
    def make_item(self, obj, update_from=None):
        """Make plot item associated to data,
        eventually update item from another item (`update_from`)"""

    @abc.abstractmethod
    def update_item(self, row):
        """Update plot item associated to data"""

    def add_computing_items(self, row):
        """Add items associated to computed results"""
        obj = self.objects[row]
        if obj.metadata:
            for item in obj.iterate_computing_items():
                self.plot.add_item(item)
                self._computing_items.append(item)

    def remove_all_computing_items(self):
        """Remove all computing items"""
        if set(self._computing_items).issubset(set(self.plot.items)):
            self.plot.del_items(self._computing_items)
        self._computing_items = []

    def refresh_plot(self):
        """Refresh plot"""
        rows = self.get_selected_rows()
        self.remove_all_computing_items()
        if self._enable_cleanup_dataview and len(rows) == 1:
            self.cleanup_dataview()
        for item in self.items:
            if item is not None:
                item.hide()
        title_keys = ("title", "xlabel", "ylabel", "zlabel", "xunit", "yunit", "zunit")
        titles_dict = {}
        if rows:
            for i_row, row in enumerate(rows):
                for key in title_keys:
                    title = getattr(self.objects[row], key, "")
                    value = titles_dict.get(key)
                    if value is None:
                        titles_dict[key] = title
                    elif value != title:
                        titles_dict[key] = ""
                item = self.items[row]
                if item is None:
                    item = self.add_item(row)
                else:
                    if i_row == 0:
                        make.style = style_generator()
                    self.update_item(row)
                self.plot.set_item_visible(item, True, replot=False)
                self.plot.set_active_item(item)
                item.unselect()
                self.add_computing_items(row)
            self.plot.replot()
        else:
            for key in title_keys:
                titles_dict[key] = ""
        tdict = titles_dict
        tdict["ylabel"] = (tdict["ylabel"], tdict.pop("zlabel"))
        tdict["yunit"] = (tdict["yunit"], tdict.pop("zunit"))
        self.plot.set_titles(**titles_dict)
        self.plot.do_autoscale()

    def refresh_list(self, new_current_row="current"):
        """new_current_row: integer, 'first', 'last', 'current'"""
        row = self.listwidget.currentRow()
        self.listwidget.clear()
        self.listwidget.addItems(
            [f"{self.PREFIX}{i:03d}: {obj.title}" for i, obj in enumerate(self.objects)]
        )
        if new_current_row == "first":
            row = 0
        elif new_current_row == "last":
            row = self.listwidget.count() - 1
        elif isinstance(new_current_row, int):
            row = new_current_row
        else:
            assert new_current_row == "current"
        if row < self.listwidget.count():
            self.listwidget.setCurrentRow(row)

    def properties_changed(self):
        """The properties 'Apply' button was clicked: updating signal"""
        row = self.listwidget.currentRow()
        update_dataset(self.objects[row], self.properties.dataset)
        self.refresh_list(new_current_row="current")
        self.refresh_plot()

    def add_object(self, obj, refresh=True):
        """Add signal/image object"""
        self.objects.append(obj)
        self.items.append(None)
        row = len(self.objects) - 1
        item = self.add_item(row)
        if refresh:
            self.refresh_list(new_current_row="last")
        self.SIG_OBJECT_ADDED.emit()
        return item

    # ------I/O
    @abc.abstractmethod
    def new_object(self):
        """Create a new object (signal/image)"""

    @abc.abstractmethod
    def open_object(self):
        """Open object from file (signal/image)"""

    @abc.abstractmethod
    def save_object(self):
        """Save selected object to file (signal/image)"""

    # ------Edit operations
    def duplicate_object(self):
        """Duplication signal/image object"""
        rows = sorted(self.get_selected_rows(), reverse=True)
        row = None
        for row in rows:
            obj = self.objects[row]
            objcopy = self.PARAMCLASS()
            objcopy.title = obj.title
            objcopy.copy_data_from(obj)
            self.objects.insert(row + 1, objcopy)
            self.items.insert(row + 1, None)
        self.refresh_list(new_current_row=row + 1)
        self.refresh_plot()

    def remove_object(self):
        """Remove signal/image object"""
        rows = sorted(self.get_selected_rows(), reverse=True)
        for row in rows:
            self.objects.pop(row)
            item = self.items.pop(row)
            self.plot.del_item(item)
        self.refresh_list(new_current_row="first")
        self.refresh_plot()
        self.SIG_OBJECT_REMOVED.emit()

    def delete_all_objects(self):
        """Confirm before removing all objects"""
        if len(self.objects) == 0:
            return
        answer = QW.QMessageBox.warning(
            self,
            _("Delete all"),
            _("Do you want to delete all %ss currently opened in CodraFT?")
            % self.OBJECT_STR,
            QW.QMessageBox.Yes | QW.QMessageBox.No,
        )
        if answer == QW.QMessageBox.Yes:
            self.remove_all_objects()

    def remove_all_objects(self):
        """Remove all signal/image objects"""
        self.objects = []
        self.items = []
        self.plot.del_all_items()
        self.refresh_list(new_current_row="first")
        self.refresh_plot()
        self.SIG_OBJECT_REMOVED.emit()

    def delete_metadata(self):
        """Delete object metadata"""
        for row in self.get_selected_rows():
            self.objects[row].metadata = {}
        self.refresh_plot()

    # ------Operations
    @qt_try_except()
    def compute_sum(self):
        """Compute sum"""
        rows = self.get_selected_rows()
        outobj = self.PARAMCLASS()
        outobj.title = "+".join([f"{self.PREFIX}{row:03d}" for row in rows])
        for row in rows:
            obj = self.objects[row]
            if outobj.data is None:
                outobj.copy_data_from(obj)
            else:
                outobj.data += np.array(obj.data, dtype=outobj.data.dtype)
        self.add_object(outobj)

    @qt_try_except()
    def compute_average(self):
        """Compute average"""
        rows = self.get_selected_rows()
        outobj = self.PARAMCLASS()
        title = ", ".join([f"{self.PREFIX}{row:03d}" for row in rows])
        outobj.title = f'{_("Average")}({title})'
        original_dtype = self.objects[rows[0]].data.dtype
        for row in rows:
            obj = self.objects[row]
            if outobj.data is None:
                outobj.copy_data_from(obj, dtype=float)
            else:
                outobj.data += np.array(obj.data, dtype=outobj.data.dtype)
        outobj.data /= float(len(rows))
        outobj.set_data_type(dtype=original_dtype)
        self.add_object(outobj)

    @qt_try_except()
    def compute_product(self):
        """Compute product"""
        rows = self.get_selected_rows()
        outobj = self.PARAMCLASS()
        outobj.title = "*".join([f"{self.PREFIX}{row:03d}" for row in rows])
        for row in rows:
            obj = self.objects[row]
            if outobj.data is None:
                outobj.copy_data_from(obj)
            else:
                outobj.data *= np.array(obj.data, dtype=outobj.data.dtype)
        self.add_object(outobj)

    @qt_try_except()
    def compute_difference(self):
        """Compute difference"""
        rows = self.get_selected_rows()
        outobj = self.PARAMCLASS()
        outobj.title = "-".join([f"{self.PREFIX}{row:03d}" for row in rows])
        obj0, obj1 = self.objects[rows[0]], self.objects[rows[1]]
        outobj.copy_data_from(obj0)
        outobj.data -= np.array(obj1.data, dtype=outobj.data.dtype)
        if np.issubdtype(outobj.data.dtype, np.unsignedinteger):
            outobj.data[obj0.data < obj1.data] = 0
        self.add_object(outobj)

    @qt_try_except()
    def compute_division(self):
        """Compute division"""
        rows = self.get_selected_rows()
        outobj = self.PARAMCLASS()
        outobj.title = "/".join([f"{self.PREFIX}{row:03d}" for row in rows])
        obj0, obj1 = self.objects[rows[0]], self.objects[rows[1]]
        outobj.copy_data_from(obj0)
        outobj.data /= np.array(obj1.data, dtype=outobj.data.dtype)
        self.add_object(outobj)

    @abc.abstractmethod
    def extract_roi(self):
        """Extract Region Of Interest (ROI) from data"""

    @abc.abstractmethod
    def swap_axes(self):
        """Swap data axes"""

    @abc.abstractmethod
    def compute_abs(self):
        """Compute absolute value"""

    @abc.abstractmethod
    def compute_log10(self):
        """Compute Log10"""

    # ------Data Processing
    @abc.abstractmethod
    def apply_11_func(self, obj, orig, func, param, message):
        """Apply 11 function: 1 object in --> 1 object out"""

    def compute_11(
        self, name, func, param=None, one_param_for_all=True, suffix=None, func_obj=None
    ):
        """Compute 11 function: 1 object in --> 1 object out"""
        if param is not None and one_param_for_all:
            if not param.edit(parent=self.parent()):
                return
        rows = self.get_selected_rows()
        progress = create_progress_bar(self, name, max_=len(rows))
        for idx, row in enumerate(rows):
            progress.setValue(idx)
            QW.QApplication.processEvents()
            if progress.wasCanceled():
                break
            if param is not None and not one_param_for_all:
                if not param.edit(parent=self.parent()):
                    return
            orig = self.objects[row]
            obj = self.PARAMCLASS()
            obj.title = f"{name}({self.PREFIX}{row:03d})"
            if suffix is not None:
                obj.title += "|" + suffix(param)
            obj.copy_data_from(orig)
            message = _("Computing:") + " " + obj.title
            self.apply_11_func(obj, orig, func, param, message)
            if func_obj is not None:
                func_obj(obj)
            self.add_object(obj)
        progress.close()

    @abc.abstractmethod
    def apply_10_func(self, orig, func, param, message):
        """Apply 10 function: 1 object in --> 0 object out (scalar result)"""

    def compute_10(self, name, func, param=None, one_param_for_all=True, suffix=None):
        """Compute 10 function: 1 object in --> 0 object out
        (the result of this method is stored in original object's metadata)"""
        if param is not None and one_param_for_all:
            if not param.edit(parent=self.parent()):
                return
        rows = self.get_selected_rows()
        progress = create_progress_bar(self, name, max_=len(rows))
        results = []
        for idx, row in enumerate(rows):
            progress.setValue(idx)
            QW.QApplication.processEvents()
            if progress.wasCanceled():
                break
            if param is not None and not one_param_for_all:
                if not param.edit(parent=self.parent()):
                    return
            orig = self.objects[row]
            title = name
            if suffix is not None:
                title += "|" + suffix(param)
            message = _("Computing:") + " " + title
            result = self.apply_10_func(orig, func, param, message)
            if result is None:
                continue
            if np.iterable(result):
                prefix = "_"
                rdata = np.array(list(result))
            else:
                prefix = ""
                rdata = result
            orig.metadata[prefix + title] = rdata
            results.append((title, rdata))
            self.add_computing_items(row)
            self.current_item_changed(row)
            self.refresh_plot()
        progress.close()
        # TODO: show a message box presenting *results*
        # (with a "show this message next time" checkbox)
        # (with a mention of the fact that results have been added to metadata)

    @staticmethod
    @abc.abstractmethod
    def func_gaussian_filter(x, y, p):
        """Compute gaussian filter"""

    @qt_try_except()
    def compute_gaussian(self):
        """Compute gaussian filter"""

        class GaussianParam(gdt.DataSet):
            """Gaussian filter parameters"""

            sigma = gdi.FloatItem("σ", default=1.0)

        param = GaussianParam(_("Gaussian filter"))
        func = self.func_gaussian_filter
        self.compute_11(
            "GaussianFilter", func, param, suffix=lambda p: f"σ={p.sigma:.3f} pixels"
        )

    @staticmethod
    @abc.abstractmethod
    def func_moving_average(x, y, p):
        """Moving average computing function"""

    @qt_try_except()
    def compute_moving_average(self):
        """Compute moving average"""

        class MovingAverageParam(gdt.DataSet):
            """Moving average parameters"""

            n = gdi.IntItem(_("Size of the moving window"), default=3, min=1)

        param = MovingAverageParam(_("Moving average"))
        func = self.func_moving_average
        self.compute_11("MovAvg", func, param, suffix=lambda p: f"n={p.n}")

    @staticmethod
    @abc.abstractmethod
    def func_moving_median(x, y, p):
        """Moving median computing function"""

    @qt_try_except()
    def compute_moving_median(self):
        """Compute moving median"""

        class MovingMedianParam(gdt.DataSet):
            """Moving median parameters"""

            n = gdi.IntItem(
                _("Size of the moving window"), default=3, min=1, even=False
            )

        param = MovingMedianParam(_("Moving median"))
        func = self.func_moving_median
        self.compute_11("MovMed", func, param, suffix=lambda p: f"n={p.n}")

    @abc.abstractmethod
    @qt_try_except()
    def compute_wiener(self):
        """Compute Wiener filter"""

    @abc.abstractmethod
    @qt_try_except()
    def compute_fft(self):
        """Compute iFFT"""

    @abc.abstractmethod
    @qt_try_except()
    def compute_ifft(self):
        """Compute FFT"""

    # ------Computing
    @abc.abstractmethod
    def get_roi_dialog(self):
        """Get ROI from specific dialog box"""

    def define_roi(self):
        """Define Region Of Interest (ROI) for computing functions"""
        param = self.get_roi_dialog()
        if param is not None:
            if param.edit(parent=self):
                row = self.get_selected_rows()[0]
                obj = self.objects[row]
                obj.roi = param
                self.add_computing_items(row)
                self.current_item_changed(row)
                self.refresh_plot()
