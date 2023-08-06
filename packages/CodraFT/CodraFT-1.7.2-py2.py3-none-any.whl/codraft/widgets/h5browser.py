# -*- coding: utf-8 -*-
#
# Licensed under the terms of the CECILL License
# (see codraft/__init__.py for details)

"""
CodraFT HDF5 browser module
"""

# pylint: disable=invalid-name  # Allows short reference names like x, y, ...

import abc
import os.path as osp

import h5py
import numpy as np
from guidata.qthelpers import add_actions, create_action, create_toolbutton, get_icon
from guiqwt.builder import make
from guiqwt.plot import CurveWidget, ImageWidget
from qtpy.QtCore import QSize, Qt, QTimer, Signal
from qtpy.QtGui import QKeySequence
from qtpy.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QHBoxLayout,
    QMenu,
    QMessageBox,
    QSplitter,
    QStackedWidget,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
)

from codraft.config import _


def to_string(obj):
    """Convert to string, trying utf-8 then latin-1 codec"""
    if isinstance(obj, bytes):
        try:
            return obj.decode()
        except UnicodeDecodeError:
            return obj.decode("latin-1")
    try:
        return str(obj)
    except UnicodeDecodeError:
        return str(obj, encoding="latin-1")


def get_item_user_text(item):
    """Get QTreeWidgetItem user role string"""
    return item.data(0, Qt.UserRole)


class BaseTreeWidgetMeta(type(QTreeWidget), abc.ABCMeta):
    """Mixed metaclass to avoid conflicts"""


class BaseTreeWidget(QTreeWidget, metaclass=BaseTreeWidgetMeta):
    """One-column tree widget with context menu, ..."""

    def __init__(self, parent):
        QTreeWidget.__init__(self, parent)
        self.setItemsExpandable(True)
        self.itemActivated.connect(self.activated)
        self.itemClicked.connect(self.clicked)
        # Setup context menu
        self.menu = QMenu(self)
        self.collapse_all_action = None
        self.collapse_selection_action = None
        self.expand_all_action = None
        self.expand_selection_action = None
        self.common_actions = self.setup_common_actions()

        self.__expanded_state = None

        self.itemSelectionChanged.connect(self.item_selection_changed)
        self.item_selection_changed()

    @abc.abstractmethod
    def activated(self, item):
        """Double-click event"""

    @abc.abstractmethod
    def clicked(self, item):
        """Item was clicked"""

    def setup_common_actions(self):
        """Setup context menu common actions"""
        self.collapse_all_action = create_action(
            self,
            _("Collapse all"),
            icon=get_icon("collapse.png"),
            triggered=self.collapseAll,
        )
        self.expand_all_action = create_action(
            self, _("Expand all"), icon=get_icon("expand.png"), triggered=self.expandAll
        )
        self.restore_action = create_action(
            self,
            _("Restore"),
            tip=_("Restore original tree layout"),
            icon=get_icon("restore.png"),
            triggered=self.restore,
        )
        self.collapse_selection_action = create_action(
            self,
            _("Collapse selection"),
            icon=get_icon("collapse_selection.png"),
            triggered=self.collapse_selection,
        )
        self.expand_selection_action = create_action(
            self,
            _("Expand selection"),
            icon=get_icon("expand_selection.png"),
            triggered=self.expand_selection,
        )
        return [
            self.collapse_all_action,
            self.expand_all_action,
            self.restore_action,
            None,
            self.collapse_selection_action,
            self.expand_selection_action,
        ]

    def update_menu(self):
        """Update context menu"""
        self.menu.clear()
        items = self.selectedItems()
        actions = self.get_actions_from_items(items)
        if actions:
            actions.append(None)
        actions += self.common_actions
        add_actions(self.menu, actions)

    def get_actions_from_items(self, items):  # pylint: disable=W0613,R0201
        """Get actions from item"""
        # Right here: add other actions if necessary (reimplement this method)
        return []

    def restore(self):
        """Restore tree state"""
        self.collapseAll()
        for item in self.get_top_level_items():
            self.expandItem(item)

    def is_item_expandable(self, item):  # pylint: disable=W0613,R0201
        """To be reimplemented in child class
        See example in project explorer widget"""
        return True

    def __expand_item(self, item):
        """Expand item tree branch"""
        if self.is_item_expandable(item):
            self.expandItem(item)
            for index in range(item.childCount()):
                child = item.child(index)
                self.__expand_item(child)

    def expand_selection(self):
        """Expand selection"""
        items = self.selectedItems()
        if not items:
            items = self.get_top_level_items()
        for item in items:
            self.__expand_item(item)
        if items:
            self.scrollToItem(items[0])

    def __collapse_item(self, item):
        """Collapse item tree branch"""
        self.collapseItem(item)
        for index in range(item.childCount()):
            child = item.child(index)
            self.__collapse_item(child)

    def collapse_selection(self):
        """Collapse selection"""
        items = self.selectedItems()
        if not items:
            items = self.get_top_level_items()
        for item in items:
            self.__collapse_item(item)
        if items:
            self.scrollToItem(items[0])

    def item_selection_changed(self):
        """Item selection has changed"""
        is_selection = len(self.selectedItems()) > 0
        self.expand_selection_action.setEnabled(is_selection)
        self.collapse_selection_action.setEnabled(is_selection)

    def get_top_level_items(self):
        """Iterate over top level items"""
        return [self.topLevelItem(_i) for _i in range(self.topLevelItemCount())]

    def get_items(self):
        """Return items (excluding top level items)"""
        itemlist = []

        def add_to_itemlist(item):
            for index in range(item.childCount()):
                citem = item.child(index)
                itemlist.append(citem)
                add_to_itemlist(citem)

        for tlitem in self.get_top_level_items():
            add_to_itemlist(tlitem)
        return itemlist

    def get_scrollbar_position(self):
        """Get scrollbar position"""
        return (self.horizontalScrollBar().value(), self.verticalScrollBar().value())

    def set_scrollbar_position(self, position):
        """Set scrollbar position"""
        hor, ver = position
        self.horizontalScrollBar().setValue(hor)
        self.verticalScrollBar().setValue(ver)

    def get_expanded_state(self):
        """Get tree expanded state"""
        self.save_expanded_state()
        return self.__expanded_state

    def set_expanded_state(self, state):
        """Set tree expanded state"""
        self.__expanded_state = state
        self.restore_expanded_state()

    def save_expanded_state(self):
        """Save all items expanded state"""
        self.__expanded_state = {}

        def add_to_state(item):
            user_text = get_item_user_text(item)
            self.__expanded_state[hash(user_text)] = item.isExpanded()

        def browse_children(item):
            add_to_state(item)
            for index in range(item.childCount()):
                citem = item.child(index)
                user_text = get_item_user_text(citem)
                self.__expanded_state[hash(user_text)] = citem.isExpanded()
                browse_children(citem)

        for tlitem in self.get_top_level_items():
            browse_children(tlitem)

    def restore_expanded_state(self):
        """Restore all items expanded state"""
        if self.__expanded_state is None:
            return
        for item in self.get_items() + self.get_top_level_items():
            user_text = get_item_user_text(item)
            is_expanded = self.__expanded_state.get(hash(user_text))
            if is_expanded is not None:
                item.setExpanded(is_expanded)

    def sort_top_level_items(self, key):
        """Sorting tree wrt top level items"""
        self.save_expanded_state()
        items = sorted(
            [self.takeTopLevelItem(0) for index in range(self.topLevelItemCount())],
            key=key,
        )
        for index, item in enumerate(items):
            self.insertTopLevelItem(index, item)
        self.restore_expanded_state()

    def contextMenuEvent(self, event):
        """Override Qt method"""
        self.update_menu()
        self.menu.popup(event.globalPos())


def is_group(data):
    """Return True if data is an HDF5 group"""
    return isinstance(data, h5py.Group)


def is_supported_num_dtype(data):
    """Return True if data type is a numerical type supported by CodraFT"""
    return data.dtype.name.startswith(("int", "uint", "float"))


def is_single_str_array(data):
    """Return True if data is a single-item string array"""
    return data.shape == (1,) and isinstance(data[0], str)


def is_supported_str_dtype(data):
    """Return True if data type is a string type supported by preview"""
    return data.dtype.name.startswith("string") or is_single_str_array(data)


class H5TreeWidget(BaseTreeWidget):
    """HDF5 Browser Tree Widget"""

    SIG_SELECTED = Signal(QTreeWidgetItem)

    def __init__(self, parent):
        BaseTreeWidget.__init__(self, parent)
        title = _("HDF5 Browser")
        self.setColumnCount(4)
        self.setWindowTitle(title)
        self.setHeaderLabels([_("Name"), _("Size"), _("Type"), _("Textual preview")])
        self.fname = None
        self.h5file = None

    def setup(self, fname):
        """Setup H5TreeWidget"""
        self.fname = osp.abspath(fname)
        self.h5file = h5py.File(self.fname, "r")
        self.clear()
        self.populate_tree()
        self.expandAll()
        for col in range(3):
            self.resizeColumnToContents(col)

    def cleanup(self):
        """Clean up widget"""
        self.h5file.close()
        self.h5file = None

    def get_dataset(self, item):
        """Get HDF5 dataset associated to item"""
        name = get_item_user_text(item)
        if name:
            return self.h5file[name]
        return None

    def get_datasets(self, only_checked_items=True):
        """Get all datasets associated to checked items"""
        datasets = []
        for item in self.find_all_items():
            if item.flags() & Qt.ItemIsUserCheckable:
                if only_checked_items and item.checkState(0) == 0:
                    continue
                if item is not self.topLevelItem(0):
                    name = get_item_user_text(item)
                    datasets.append(self.h5file[name])
        return datasets

    def activated(self, item):
        """Double-click event"""
        if item is not self.topLevelItem(0):
            self.SIG_SELECTED.emit(item)

    def clicked(self, item):
        """Click event"""
        self.activated(item)

    def find_all_items(self):
        """Find all items"""
        return self.findItems("", Qt.MatchContains | Qt.MatchRecursive)

    def is_empty(self):
        """Return True if tree is empty"""
        return len(self.find_all_items()) == 1

    def get_item_from_id(self, item_id):
        """Return QListWidgetItem from id"""
        for item in self.find_all_items():
            if id(item) == item_id:
                return item
        return None

    def is_any_item_checked(self):
        """Return True if any item is checked"""
        for item in self.find_all_items():
            if item.checkState(0) > 0:
                return True
        return False

    def select_all(self, state):
        """Select all items"""
        for item in self.findItems("", Qt.MatchContains | Qt.MatchRecursive):
            if item.flags() & Qt.ItemIsUserCheckable:
                item.setSelected(state)
                if state:
                    self.clicked(item)

    def toggle_all(self, state):
        """Toggle all item state from 'unchecked' to 'checked'
        (or vice-versa)"""
        for item in self.findItems("", Qt.MatchContains | Qt.MatchRecursive):
            if item.flags() & Qt.ItemIsUserCheckable:
                item.setCheckState(0, Qt.Checked if state else Qt.Unchecked)

    @staticmethod
    def __create_node(parent, data, shape_str, dtype_str, text, desc=None):
        if parent.name == "/":
            offset = 1
        else:
            offset = len(parent.name) + 1
        node = QTreeWidgetItem([data.name[offset:], shape_str, dtype_str, text])
        node.setData(0, Qt.UserRole, data.name)
        if desc is not None:
            for col in range(node.columnCount()):
                node.setToolTip(col, desc)
        return node

    @staticmethod
    def __get_data_str(data):
        shape_str = dtype_str = ""
        if len(data.shape) in (1, 2):  # , 3):
            shape_str = " x ".join([str(size) for size in data.shape])
        if is_single_str_array(data) or isinstance(data[()], str):
            dtype_str = "string"
        else:
            dtype_str = str(data.dtype)
        if (
            not is_group(data)
            and not is_supported_num_dtype(data)
            and not is_supported_str_dtype(data)
        ):
            return None
        text = ""
        if is_single_str_array(data):
            text = data[0]
        elif not isinstance(data[()], np.ndarray):
            text = to_string(data[()])
        return shape_str, dtype_str, text

    @staticmethod
    def __get_data_icon(value):
        if is_supported_num_dtype(value):
            if len(value.shape) == 1:
                return "signal.svg"
            if len(value.shape) == 2:
                for colnb in (2, 3, 4):
                    if value.shape[1] == colnb and value.shape[0] > colnb:
                        return "signal.svg"
                for rownb in (2, 3, 4):
                    if value.shape[0] == rownb and value.shape[1] > rownb:
                        return "signal.svg"
                return "image.svg"
        return None

    @staticmethod
    def __recursive_popfunc_lmj(parent_node, data):
        """Recursive HDF5 analysis -- LMJ-specific"""
        if not is_group(data):
            return
        shape_str, dtype_str, text, desc = "", "", "", None
        value = data.get("valeur")
        is_lmj_data = value is not None
        if is_lmj_data:
            data_str = H5TreeWidget.__get_data_str(value)
            if data_str is not None:
                shape_str, dtype_str, text = data_str
            try:
                obj = data["unite"][()][0]
                obj = obj["UNITE_X"]
            except KeyError:
                obj = ""
            except TypeError:
                pass
            unite = to_string(obj)
            if unite == "NULL":
                unite = ""
            try:
                desc = to_string(data["description"][()])
            except KeyError:
                pass
            npval = value[()]
            if not isinstance(npval, np.ndarray) or len(npval.shape) == 1:
                text = to_string(npval)
                if unite and not text.lower().endswith((unite.lower(), "bit")):
                    text += " " + unite
        tree_node = H5TreeWidget.__create_node(
            data.parent, data, shape_str, dtype_str, text, desc
        )
        if not is_lmj_data:
            tree_node.setFlags(Qt.ItemIsEnabled)
            icon = get_icon("libre-gui-table.svg")
        else:
            icon_name = H5TreeWidget.__get_data_icon(value)
            if icon_name is None:
                icon_name = "libre-gui-view-details.svg"
                tree_node.setFlags(Qt.ItemIsEnabled)
            else:
                tree_node.setCheckState(0, Qt.Unchecked)
            icon = get_icon(icon_name)
        tree_node.setIcon(0, icon)
        parent_node.addChild(tree_node)
        if not is_lmj_data:
            for item in data.values():
                H5TreeWidget.__recursive_popfunc_lmj(tree_node, item)

    @staticmethod
    def __recursive_popfunc(parent_node, data):
        """Recursive HDF5 analysis"""
        shape_str = dtype_str = text = ""
        if not is_group(data):
            data_str = H5TreeWidget.__get_data_str(data)
            if data_str is not None:
                shape_str, dtype_str, text = data_str
            else:
                return
        tree_node = H5TreeWidget.__create_node(
            data.parent, data, shape_str, dtype_str, text
        )
        if is_group(data):
            tree_node.setFlags(Qt.ItemIsEnabled)
            icon = get_icon("libre-gui-table.svg")
        else:
            icon_name = H5TreeWidget.__get_data_icon(data)
            if icon_name is None:
                icon_name = "libre-gui-view-details.svg"
                tree_node.setFlags(Qt.ItemIsEnabled)
            else:
                tree_node.setCheckState(0, Qt.Unchecked)
            icon = get_icon(icon_name)
        tree_node.setIcon(0, icon)
        parent_node.addChild(tree_node)
        if is_group(data):
            for item in data.values():
                H5TreeWidget.__recursive_popfunc(tree_node, item)

    def populate_tree(self):
        """Populate tree"""
        topnode = QTreeWidgetItem([osp.basename(self.h5file.filename)])
        root = self.h5file["/"]
        topnode.setData(0, Qt.UserRole, root)
        topnode.setFlags(Qt.ItemIsEnabled)
        topnode.setIcon(0, get_icon("libre-gui-file.svg"))
        self.addTopLevelItem(topnode)
        for item in root.values():
            if root.get("ENTETE") is None:
                self.__recursive_popfunc(topnode, item)
            else:
                #  LMJ-formatted HDF5 file
                self.__recursive_popfunc_lmj(topnode, item)


class H5Browser(QSplitter):
    """HDF5 Browser Widget"""

    def __init__(self, parent=None):
        QSplitter.__init__(self, parent=parent)
        self.tree = H5TreeWidget(self)
        self.tree.SIG_SELECTED.connect(self.view_selected_item)
        self.addWidget(self.tree)
        self.stack = QStackedWidget(self)
        self.addWidget(self.stack)
        self.curvewidget = CurveWidget(self.stack)
        self.curvewidget.register_all_curve_tools()
        self.stack.addWidget(self.curvewidget)
        self.imagewidget = ImageWidget(self.stack, show_contrast=True)
        self.imagewidget.register_all_image_tools()
        self.stack.addWidget(self.imagewidget)

    def setup(self, fname):
        """Setup widget"""
        self.tree.setup(fname)

    def cleanup(self):
        """Clean up widget"""
        for widget in (self.imagewidget, self.curvewidget):
            widget.plot.del_all_items()
        self.tree.cleanup()

    def get_dataset(self, item=None):
        """Return (selected) dataset"""
        if item is None:
            item = self.tree.currentItem()
        return self.tree.get_dataset(item)

    def view_selected_item(self, item):
        """View selected item"""
        dataset = self.get_dataset(item)
        if (
            not isinstance(dataset, h5py.Dataset) and dataset.get("valeur") is not None
        ):  # LMJ-formatted HDF5 file
            dataset = dataset["valeur"]
        elif is_group(dataset):
            return
        data = dataset[()]
        if isinstance(data, np.ndarray) and is_supported_num_dtype(data):
            self.update_visual_preview(dataset.name, data)

    def update_visual_preview(self, name, data):
        """Update visual preview widget"""
        if len(data.shape) == 1:
            widget = self.curvewidget
            if data.dtype != float:
                data = np.array(data, dtype=float)
            x = np.arange(data.size, dtype=data.dtype)
            item = make.curve(x, data, title=name)
        elif len(data.shape) == 2:
            rows, cols = data.shape
            xydata = None
            for colnb in (2, 3, 4):
                if cols == colnb and rows > colnb:
                    xydata = data.T.copy()
                    break
            for rownb in (2, 3, 4):
                if rows == rownb and cols > rownb:
                    xydata = data.copy()
                    break
            if xydata is None:
                # Image
                widget = self.imagewidget
                visdata = data.real
                if np.any(np.isnan(visdata)):
                    visdata = np.nan_to_num(visdata)
                if visdata.dtype == np.uint32:
                    visdata = np.array(visdata, dtype=np.int32)
                item = make.image(
                    data=visdata,
                    title=name,
                    colormap="jet",
                    eliminate_outliers=0.1,
                    interpolation="nearest",
                )
            else:
                # Signal
                if xydata.dtype != float:
                    xydata = np.array(xydata, dtype=float)
                widget = self.curvewidget
                item = make.curve(xydata[0, :], xydata[1, :], title=name)
        else:  # len(data.shape) == 3
            widget = self.imagewidget
            item = make.rgbimage(data=data, title=name, interpolation="nearest")
        plot = widget.plot
        plot.del_all_items()
        plot.add_item(item)
        plot.set_active_item(item)
        item.unselect()
        plot.do_autoscale()
        self.stack.setCurrentWidget(widget)


class H5BrowserDialog(QDialog):
    """HDF5 Browser Dialog"""

    def __init__(self, parent=None, size=(1550, 600)):
        QDialog.__init__(self, parent=parent)
        self.setWindowTitle(_("HDF5 Browser"))
        vlayout = QVBoxLayout()
        self.setLayout(vlayout)
        self.button_layout = None
        self.bbox = None
        self.datasets = None

        self.browser = H5Browser(self)
        vlayout.addWidget(self.browser)

        self.browser.tree.itemChanged.connect(lambda item: self.refresh_buttons())

        self.install_button_layout()

        self.resize(QSize(*size))
        self.browser.setSizes([int(size[1] / 2)] * 2)
        self.refresh_buttons()

    def accept(self):
        """Accept changes"""
        self.datasets = self.browser.tree.get_datasets()
        QDialog.accept(self)

    def cleanup(self):
        """Cleanup dialog"""
        self.browser.cleanup()

    def refresh_buttons(self):
        """Refresh buttons"""
        state = self.browser.tree.is_any_item_checked()
        self.bbox.button(QDialogButtonBox.Ok).setEnabled(state)

    def setup(self, fname):
        """Setup dialog"""
        self.browser.setup(fname)
        if self.browser.tree.is_empty():
            QMessageBox.warning(
                self.parent(),
                self.windowTitle(),
                _("Warning:") + "\n" + _("No supported data available in HDF5 file."),
            )
            QTimer.singleShot(0, self.reject)

    def get_all_datasets(self):
        """Return all supported datasets"""
        return self.browser.tree.get_datasets(only_checked_items=False)

    def get_datasets(self):
        """Return datasets"""
        return self.datasets

    def install_button_layout(self):
        """Install button layout"""
        bbox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        bbox.accepted.connect(self.accept)
        bbox.rejected.connect(self.reject)

        btn_check_all = create_toolbutton(
            self,
            text=_("Check all"),
            autoraise=False,
            shortcut=QKeySequence.SelectAll,
            triggered=lambda checked=True: self.browser.tree.toggle_all(checked),
        )
        btn_uncheck_all = create_toolbutton(
            self,
            text=_("Uncheck all"),
            autoraise=False,
            triggered=lambda checked=False: self.browser.tree.toggle_all(checked),
        )

        self.button_layout = QHBoxLayout()
        self.button_layout.addWidget(btn_check_all)
        self.button_layout.addWidget(btn_uncheck_all)
        self.button_layout.addStretch()
        self.button_layout.addWidget(bbox)
        self.bbox = bbox

        vlayout = self.layout()
        vlayout.addSpacing(10)
        vlayout.addLayout(self.button_layout)
