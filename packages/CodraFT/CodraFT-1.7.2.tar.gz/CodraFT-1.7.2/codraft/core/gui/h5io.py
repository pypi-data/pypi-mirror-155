# -*- coding: utf-8 -*-
#
# Licensed under the terms of the CECILL License
# (see codraft/__init__.py for details)

"""
CodraFT HDF5 open/save module
"""

# pylint: disable=invalid-name  # Allows short reference names like x, y, ...

import os
import os.path as osp

import h5py
import numpy as np
from qtpy import QtWidgets as QW

from codraft.config import _
from codraft.core.model import create_image, create_signal
from codraft.widgets.h5browser import H5BrowserDialog, to_string
from codraft.utils.qthelpers import create_progress_bar, qt_try_opening_file


def fix_ldata(fuzzy):
    """Fix label data"""
    if fuzzy is not None:
        if fuzzy and isinstance(fuzzy, np.void) and len(fuzzy) > 1:
            #  Shouldn't happen (invalid LMJ fmt)
            fuzzy = fuzzy[0]
        if isinstance(fuzzy, np.string_):
            fuzzy = to_string(fuzzy)
        if isinstance(fuzzy, str):
            return fuzzy
    return None


def process_label(dataset, name):
    """Process dataset label `name`"""
    ldata = dataset[name][()]
    xldata, yldata, zldata = None, None, None
    if ldata is not None:
        if len(ldata) == 2:
            xldata, yldata = ldata
        elif len(ldata) == 3:
            xldata, yldata, zldata = ldata
    return fix_ldata(xldata), fix_ldata(yldata), fix_ldata(zldata)


class H5InputOutput:
    """Object handling HDF5 file open/save into/from CodraFT data model/main window"""

    H5_SIG_PREFIX = "CodraFT_Sig"
    H5_IMA_PREFIX = "CodraFT_Ima"

    def __init__(self, mainwindow):
        self.mainwindow = mainwindow
        self.h5browser = None
        self.uint32_wng = None

    @property
    def signalft(self):
        """Return signal handler instance"""
        return self.mainwindow.signalft

    @property
    def imageft(self):
        """Return image handler instance"""
        return self.mainwindow.imageft

    def save(self, filename):
        """Save all signals and images from CodraFT model into a HDF5 file"""
        os.chdir(osp.dirname(filename))
        h5file = h5py.File(filename, "w")
        sig_group = h5file.create_group(self.H5_SIG_PREFIX)
        for idx, obj in enumerate(self.signalft.objects):
            name = f"{self.signalft.PREFIX}{idx:03d}: {obj.title}"
            dataset = sig_group.create_dataset(name, data=obj.xydata)
            if obj.metadata:
                for key, value in obj.metadata.items():
                    dataset.attrs[key] = value
        ima_group = h5file.create_group(self.H5_IMA_PREFIX)
        for idx, obj in enumerate(self.imageft.objects):
            name = f"{self.imageft.PREFIX}{idx:03d}: {obj.title}"
            dataset = ima_group.create_dataset(name, data=obj.data)
            if obj.metadata:
                for key, value in obj.metadata.items():
                    dataset.attrs[key] = value
        h5file.close()
        self.mainwindow.set_modified(False)

    @classmethod
    def remove_prefix(cls, name):
        """Remove name prefix if necessary"""
        for prefix in ("/" + cls.H5_SIG_PREFIX + "/", "/" + cls.H5_IMA_PREFIX + "/"):
            if name.startswith(prefix):
                return name[len(prefix) + 6 :]
        return name

    def open(self, filename, import_all, reset_all):
        """Open HDF5 file"""
        os.chdir(osp.dirname(filename))
        if self.h5browser is None:
            self.h5browser = H5BrowserDialog(self.mainwindow)

        with qt_try_opening_file(self.mainwindow, filename):
            self.h5browser.setup(filename)
            if not import_all and not self.h5browser.exec():
                self.h5browser.cleanup()
                return
            if import_all:
                datasets = self.h5browser.get_all_datasets()
            else:
                datasets = self.h5browser.get_datasets()
            if datasets is None:
                self.h5browser.cleanup()
                return
            if reset_all:
                self.mainwindow.reset_all()
            progress = create_progress_bar(
                self.mainwindow, _("Loading data from HDF5 file..."), len(datasets)
            )

            self.uint32_wng = False
            for idx, dataset in enumerate(datasets):
                progress.setValue(idx)
                QW.QApplication.processEvents()
                if progress.wasCanceled():
                    break
                self.import_dataset(dataset)
            progress.close()
            self.h5browser.cleanup()
            if self.uint32_wng:
                QW.QMessageBox.warning(
                    self.mainwindow, _("Warning"), _("Clipping uint32 data to int32.")
                )

    def import_dataset(self, dataset):
        """Import dataset to CodraFT"""
        rm_prefix = H5InputOutput.remove_prefix
        xunit, yunit, zunit = None, None, None
        xlabel, ylabel, zlabel = None, None, None
        try:
            data = dataset["valeur"][()]
            xunit, yunit, zunit = process_label(dataset, "unite")
            xlabel, ylabel, zlabel = process_label(dataset, "label")
        except (KeyError, ValueError):
            data = dataset[()]
        if len(data.shape) == 1:
            obj = create_signal(
                rm_prefix(dataset.name),
                xunit=xunit,
                yunit=yunit,
                xlabel=xlabel,
                ylabel=ylabel,
            )
            obj.set_xydata(np.arange(data.size), data)
            obj.metadata = {}
            for key, value in dataset.attrs.items():
                obj.metadata[key] = value
            self.signalft.add_object(obj)
        else:
            rows, cols = data.shape
            if rows in (1, 2) or cols in (1, 2):
                obj = create_signal(
                    rm_prefix(dataset.name),
                    xunit=xunit,
                    yunit=yunit,
                    xlabel=xlabel,
                    ylabel=ylabel,
                )
                for colnb in (2, 3, 4):
                    if cols == colnb and rows > colnb:
                        data = data.T
                        break
                obj.xydata = np.array(data, dtype=float)
                obj.metadata = {}
                for key, value in dataset.attrs.items():
                    obj.metadata[key] = value
                self.signalft.add_object(obj)
            else:
                if data.dtype == np.uint32:
                    self.uint32_wng = data.max() > np.iinfo(np.int32).max
                    clipped_data = data.clip(0, np.iinfo(np.int32).max)
                    data = np.array(clipped_data, dtype=np.int32)
                obj = create_image(
                    rm_prefix(dataset.name),
                    data,
                    xunit=xunit,
                    yunit=yunit,
                    zunit=zunit,
                    xlabel=xlabel,
                    ylabel=ylabel,
                    zlabel=zlabel,
                )
                obj.metadata = {}
                for key, value in dataset.attrs.items():
                    obj.metadata[key] = value
                self.imageft.add_object(obj)
