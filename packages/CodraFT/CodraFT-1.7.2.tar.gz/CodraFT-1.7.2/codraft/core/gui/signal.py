# -*- coding: utf-8 -*-
#
# Licensed under the terms of the CECILL License
# (see codraft/__init__.py for details)

"""
CodraFT Signal GUI module
"""

# pylint: disable=invalid-name  # Allows short reference names like x, y, ...

import sys
import os.path as osp
import os
import re
import traceback

from qtpy import QtWidgets as QW
from qtpy.compat import getopenfilenames, getsavefilename

import numpy as np
import scipy.ndimage as spi
import scipy.integrate as spt
import scipy.signal as sps
import scipy.optimize as spo

from guidata.dataset.datatypes import DataSet
from guidata.dataset.dataitems import IntItem, ChoiceItem, FloatItem
from guidata.configtools import get_icon
from guidata.qthelpers import create_action
from guidata.utils import update_dataset

from guiqwt.label import ObjectInfo
from guiqwt.plot import CurveDialog
from guiqwt.builder import make
from guiqwt.tools import LabelTool, VCursorTool, HCursorTool, XCursorTool
from guiqwt.styles import update_style_attr

from codraft.config import _, APP_NAME
from codraft.core.model import SignalParam, create_signal, ShapeTypes
from codraft.core.gui.new import create_signal_gui
from codraft.core.gui.base import ObjectFT
from codraft.utils.qthelpers import qt_try_except, qt_try_opening_file
from codraft.core.computation import fit
from codraft.core.computation.signal import (
    derivative,
    moving_average,
    normalize,
    peak_indexes,
    xpeak,
    xy_fft,
    xy_ifft,
)
from codraft.widgets import peak_dialog
from codraft.widgets import fit_dialog


class SignalFT(ObjectFT):
    """Object handling the item list, the selected item properties and plot,
    specialized for Signal objects"""

    PARAMCLASS = SignalParam
    DIALOGCLASS = CurveDialog
    PREFIX = "s"
    OBJECT_STR = _("signal")

    # ------ObjectFT API
    def create_operation_actions(self):
        """Create operation actions"""
        base_actions = super().create_operation_actions()
        peakdetect_action = create_action(
            self,
            _("Peak detection"),
            self.detect_peaks,
            icon=get_icon("peak_detect.svg"),
        )
        self.actlist_1more += [peakdetect_action]
        roi_actions = self.operation_end_actions
        return base_actions + [None, peakdetect_action, None] + roi_actions

    def create_processing_actions(self):
        """Create processing actions"""
        base_actions = super().create_processing_actions()
        cra = create_action
        normalize_action = cra(self, _("Normalize"), self.normalize)
        deriv_action = cra(self, _("Derivative"), self.compute_derivative)
        integ_action = cra(self, _("Integral"), self.compute_integral)
        lincal_action = cra(self, _("Linear calibration"), self.calibrate)
        polyfit_action = cra(self, _("Polynomial fit"), self.compute_polyfit)
        mgfit_action = cra(self, _("Multi-Gaussian fit"), self.compute_multigaussianfit)

        def cra_fit(title, fitdlgfunc):
            """Create curve fitting action"""
            return cra(self, title, lambda: self.compute_fit(title, fitdlgfunc))

        gaussfit_action = cra_fit(_("Gaussian fit"), fit_dialog.gaussianfit)
        lorentzfit_action = cra_fit(_("Lorentzian fit"), fit_dialog.lorentzianfit)
        voigtfit_action = cra_fit(_("Voigt fit"), fit_dialog.voigtfit)
        actions1 = [normalize_action, deriv_action, integ_action, lincal_action]
        actions2 = [
            gaussfit_action,
            lorentzfit_action,
            voigtfit_action,
            polyfit_action,
            mgfit_action,
        ]
        self.actlist_1more += actions1 + actions2
        return actions1 + [None] + base_actions + [None] + actions2

    def create_computing_actions(self):
        """Create computing actions"""
        defineroi_action = create_action(
            self, _("Define ROI"), triggered=self.define_roi, icon=get_icon("roi.svg")
        )
        fwhm_action = create_action(
            self,
            _("Full width at half-maximum"),
            triggered=self.compute_fwhm,
            tip=_("Compute Full Width at Half-Maximum (FWHM)"),
        )
        fw1e2_action = create_action(
            self,
            _("Full width at") + " 1/e²",
            triggered=self.compute_fw1e2,
            tip=_("Compute Full Width at Maximum") + "/e²",
        )
        self.actlist_1 += [defineroi_action]
        self.actlist_1more += [fwhm_action, fw1e2_action]
        return [defineroi_action, None, fwhm_action, fw1e2_action]

    def make_item(self, obj, update_from=None):
        """Make plot item associated to data,
        eventually update item from another item (`update_from`)"""
        data = obj.xydata
        if len(data) == 2:  # x, y signal
            x, y = data
            item = make.mcurve(x, y.real, label=obj.title)
        elif len(data) == 4:  # x, y, dx, dy error bar signal
            x, y, dx, dy = data
            item = make.merror(x, y.real, dx, dy, label=obj.title)
        else:
            raise RuntimeError("data not supported")
        if update_from is not None:
            update_dataset(item.curveparam, update_from.curveparam)
        update_dataset(item.curveparam, obj.metadata)
        item.update_params()
        return item

    def update_item(self, row):
        """Update plot item associated to data"""
        signal = self.objects[row]
        item = self.items[row]
        data = signal.xydata
        if len(data) == 2:  # x, y signal
            x, y = data
            item.set_data(x, y.real)
        elif len(data) == 4:  # x, y, dx, dy error bar signal
            x, y, dx, dy = data
            item.set_data(x, y.real, dx, dy)
        item.curveparam.label = signal.title
        update_style_attr(next(make.style), item.curveparam)

    def open_separate_view(self, rows=None):
        """Open separate view for visualizing selected objects"""
        if rows is None:
            rows = self.get_selected_rows()
        tools = (LabelTool, VCursorTool, HCursorTool, XCursorTool)
        dlg = self.create_new_dialog(rows, tools=tools)
        dlg.plot_widget.itemlist.setVisible(True)
        dlg.exec()

    def get_plot_options(self):
        """Return standard signal plot options"""
        return dict(
            xlabel=self.plot.get_axis_title("bottom"),
            ylabel=self.plot.get_axis_title("left"),
            xunit=self.plot.get_axis_unit("bottom"),
            yunit=self.plot.get_axis_unit("left"),
        )

    # ------I/O
    def new_object(self):
        """Create a new signal"""
        size = None
        rows = self.get_selected_rows()
        if rows:
            size = len(self.objects[rows[-1]].data)
        signal = create_signal_gui(self, size=size)
        if signal is not None:
            self.add_object(signal)

    def open_object(self):
        """Open signal file"""
        saved_in, saved_out, saved_err = sys.stdin, sys.stdout, sys.stderr
        sys.stdout = None
        filters = f'{_("Text files")} (*.txt *.csv)\n{_("NumPy arrays")} (*.npy)'
        filenames, _filter = getopenfilenames(self.parent(), _("Open"), "", filters)
        sys.stdin, sys.stdout, sys.stderr = saved_in, saved_out, saved_err
        filenames = list(filenames)
        for filename in filenames:
            os.chdir(osp.dirname(filename))
            signal = create_signal(osp.basename(filename))
            with qt_try_opening_file(self.parent(), filename):
                if osp.splitext(filename)[1] == ".npy":
                    xydata = np.load(filename)
                else:
                    for delimiter in ("\t", ",", " ", ";"):
                        try:
                            xydata = np.loadtxt(filename, delimiter=delimiter)
                            break
                        except ValueError:
                            continue
                    else:
                        raise ValueError
                assert len(xydata.shape) in (1, 2), "Data not supported"
                if len(xydata.shape) == 1:
                    signal.set_xydata(np.arange(xydata.size), xydata)
                else:
                    rows, cols = xydata.shape
                    for colnb in (2, 3, 4):
                        if cols == colnb and rows > colnb:
                            xydata = xydata.T
                            break
                    if cols == 3:
                        # x, y, dy
                        xarr, yarr, dyarr = xydata
                        signal.set_xydata(xarr, yarr, dx=None, dy=dyarr)
                    else:
                        signal.xydata = xydata
                self.add_object(signal)

    def save_object(self):
        """Save selected signal"""
        rows = self.get_selected_rows()
        for row in rows:
            filename, _filter = getsavefilename(
                self, _("Save as"), "", _("CSV files") + " (*.csv)"
            )
            if not filename:
                return
            os.chdir(osp.dirname(filename))
            obj = self.objects[row]
            try:
                np.savetxt(filename, obj.xydata, delimiter=",")
            except Exception as msg:  # pylint: disable=broad-except
                traceback.print_exc()
                QW.QMessageBox.critical(
                    self.parent(),
                    APP_NAME,
                    (_("%s could not be written:") % osp.basename(filename))
                    + "\n"
                    + str(msg),
                )
                return

    # ------Signal operations
    def extract_roi(self):
        """Extract Region Of Interest (ROI) from data"""
        param = self.get_roi_dialog()
        if param is not None:
            # TODO: Instead of removing computing metadata, fix it following roi extract
            self.compute_11(
                "ROI",
                lambda x, y, p: (x.copy()[p.row1 : p.row2], y.copy()[p.row1 : p.row2]),
                param,
                suffix=lambda p: f"rows={p.row1:d}:{p.row2:d}",
                func_obj=lambda obj: obj.remove_computing_metadata(),
            )

    def swap_axes(self):
        """Swap data axes"""
        self.compute_11(
            "SwapAxes",
            lambda x, y: (y, x),
            func_obj=lambda obj: obj.remove_computing_metadata(),
        )

    def compute_abs(self):
        """Compute absolute value"""
        self.compute_11("Abs", lambda x, y: (x, np.abs(y)))

    def compute_log10(self):
        """Compute Log10"""
        self.compute_11("Log10", lambda x, y: (x, np.log10(y)))

    def detect_peaks(self):
        """Detect peaks from data"""
        row = self.get_selected_rows()[0]
        obj = self.objects[row]
        dlg = peak_dialog.PeakDetectionDialog(self)
        dlg.setup_data(obj.x, obj.y)
        if dlg.exec():
            thres = dlg.get_threshold()

            class PeakDetectionParam(DataSet):
                """Peak detection parameters"""

                threshold = IntItem(
                    _("Threshold") + " (%)",
                    default=int(thres * 100),
                    min=0,
                    max=100,
                    slider=True,
                )

            param = PeakDetectionParam(_("Peak detection"))

            def func(x, y, p):
                """Peak detection"""
                indexes = peak_indexes(y, thres=p.threshold * 0.01)
                return x[indexes], y[indexes]

            def func_obj(obj):
                """Customize signal object"""
                obj.metadata["curvestyle"] = "Sticks"

            self.compute_11(
                "Peaks",
                func,
                param,
                suffix=lambda p: f"threshold={p.threshold}%%",
                func_obj=func_obj,
            )

    # ------Signal Processing
    def apply_11_func(self, obj, orig, func, param, message):
        """Apply 11 function: 1 object in --> 1 object out"""

        # (self is used by @qt_try_except)
        # pylint: disable=unused-argument
        @qt_try_except(message)
        def apply_11_func_callback(self, obj, orig, func, param):
            """Apply 11 function callback: 1 object in --> 1 object out"""
            data = orig.xydata
            if len(data) == 2:  # x, y signal
                x, y = data
                if param is None:
                    obj.xydata = func(x, y)
                else:
                    obj.xydata = func(x, y, param)
            elif len(data) == 4:  # x, y, dx, dy error bar signal
                x, y, dx, dy = data
                if param is None:
                    x2, y2 = func(x, y)
                    _x3, dy2 = func(x, dy)
                else:
                    x2, y2 = func(x, y, param)
                    _x3, dy2 = func(x, dy, param)
                obj.xydata = x2, y2, dx, dy2

        return apply_11_func_callback(self, obj, orig, func, param)

    @qt_try_except()
    def normalize(self):
        """Normalize data"""
        methods = (
            (_("maximum"), "maximum"),
            (_("amplitude"), "amplitude"),
            (_("sum"), "sum"),
            (_("energy"), "energy"),
        )

        class NormalizeParam(DataSet):
            """Normalize parameters"""

            method = ChoiceItem(_("Normalize with respect to"), methods)

        param = NormalizeParam(_("Normalize"))

        def func(x, y, p):
            return (x, normalize(y, p.method))

        self.compute_11("Normalize", func, param, suffix=lambda p: f"ref={p.method}")

    @qt_try_except()
    def compute_derivative(self):
        """Compute derivative"""
        self.compute_11("Derivative", lambda x, y: (x, derivative(x, y)))

    @qt_try_except()
    def compute_integral(self):
        """Compute integral"""
        self.compute_11("Integral", lambda x, y: (x, spt.cumtrapz(y, x)))

    @qt_try_except()
    def calibrate(self):
        """Compute data linear calibration"""
        axes = (("x", _("X-axis")), ("y", _("Y-axis")))

        class CalibrateParam(DataSet):
            """Calibration parameters"""

            axis = ChoiceItem(_("Calibrate"), axes, default="y")
            a = FloatItem("a", default=1.0)
            b = FloatItem("b", default=0.0)

        param = CalibrateParam(_("Linear calibration"), "y = a.x + b")

        def func(x, y, p):
            """Compute linear calibration"""
            if p.axis == "x":
                return p.a * x + p.b, y
            return x, p.a * y + p.b

        self.compute_11(
            "LinearCal",
            func,
            param,
            suffix=lambda p: f"{p.axis}={p.a}*{p.axis}+{p.b}",
        )

    @staticmethod
    def func_gaussian_filter(x, y, p):
        """Compute gaussian filter"""
        return (x, spi.gaussian_filter1d(y, p.sigma))

    @staticmethod
    def func_moving_average(x, y, p):
        """Moving average computing function"""
        return (x, moving_average(y, p.n))

    @staticmethod
    def func_moving_median(x, y, p):
        """Moving median computing function"""
        return (x, sps.medfilt(y, kernel_size=p.n))

    @qt_try_except()
    def compute_wiener(self):
        """Compute Wiener filter"""
        self.compute_11("WienerFilter", lambda x, y: (x, sps.wiener(y)))

    @qt_try_except()
    def compute_fft(self):
        """Compute iFFT"""
        self.compute_11("FFT", xy_fft)

    @qt_try_except()
    def compute_ifft(self):
        """Compute FFT"""
        self.compute_11("iFFT", xy_ifft)

    @qt_try_except()
    def compute_fit(self, name, fitdlgfunc):
        """Compute fitting curve"""
        rows = self.get_selected_rows()
        for row in rows:
            self.__row_compute_fit(row, name, fitdlgfunc)

    @qt_try_except()
    def compute_polyfit(self):
        """Compute polynomial fitting curve"""
        txt = _("Polynomial fit")

        class PolynomialFitParam(DataSet):
            """Polynomial fitting parameters"""

            degree = IntItem(_("Degree"), 3, min=1, max=10, slider=True)

        param = PolynomialFitParam(txt)
        if param.edit(self):
            fitdlgfunc = fit_dialog.polynomialfit
            self.compute_fit(
                txt,
                lambda x, y, degree=param.degree, parent=self.parent(): fitdlgfunc(
                    x, y, degree, parent=parent
                ),
            )

    def __row_compute_fit(self, row, name, fitdlgfunc):
        """Curve fitting computing sub-method"""
        obj = self.objects[row]
        output = fitdlgfunc(obj.x, obj.y, parent=self.parent())
        if output is not None:
            y, params = output
            results = {}
            for param in params:
                if re.match(r"[\S\_]*\d{2}$", param.name):
                    shname = param.name[:-2]
                    value = results.get(shname, np.array([]))
                    results[shname] = np.array(list(value) + [param.value])
                else:
                    results[param.name] = param.value
            # Creating new signal
            signal = create_signal(f"{name}({obj.title})", obj.x, y, metadata=results)
            # Creating new plot item
            self.add_object(signal, refresh=False)
            # Refreshing list
            self.refresh_list(new_current_row="last")

    @qt_try_except()
    def compute_multigaussianfit(self):
        """Compute multi-Gaussian fitting curve"""
        rows = self.get_selected_rows()
        fitdlgfunc = fit_dialog.multigaussianfit
        for row in rows:
            dlg = peak_dialog.PeakDetectionDialog(self)
            obj = self.objects[row]
            dlg.setup_data(obj.x, obj.y)
            if dlg.exec():
                # Computing x, y
                peaks = dlg.get_peak_indexes()
                self.__row_compute_fit(
                    row,
                    _("Multi-Gaussian fit"),
                    lambda x, y, peaks=peaks, parent=self.parent(): fitdlgfunc(
                        x, y, peaks, parent=parent
                    ),
                )

    # ------Signal Computing
    def apply_10_func(self, orig, func, param, message):
        """Apply 10 function: 1 object in --> 0 object out (scalar result)"""

        # (self is used by @qt_try_except)
        # pylint: disable=unused-argument
        @qt_try_except(message)
        def apply_10_func_callback(self, orig, func, param):
            """Apply 10 function cb: 1 object in --> 0 object out (scalar result)"""
            data = orig.xydata
            if len(data) == 2:  # x, y signal
                x0, y0 = data
            else:  # x, y, dx, dy error bar signal
                x0, y0, dx, dy = data  # pylint: disable=unused-variable
            if orig.roi is None:
                x, y = x0, y0
            else:
                i0, i1 = orig.roi
                x, y = x0[i0:i1], y0[i0:i1]
            if param is None:
                return func(x, y, orig.metadata)
            return func(x, y, param, orig.metadata)

        return apply_10_func_callback(self, orig, func, param)

    @qt_try_except()
    def compute_fwhm(self):
        """Compute FWHM"""
        title = _("FWHM")
        fittypes = (
            ("GaussianModel", _("Gaussian")),
            ("LorentzianModel", _("Lorentzian")),
            ("VoigtModel", "Voigt"),
        )

        class FWHMParam(DataSet):
            """FWHM parameters"""

            fittype = ChoiceItem(_("Fit type"), fittypes, default="GaussianModel")

        def fwhm(x, y, param, metadata):
            """Compute FWHM"""
            dx = np.max(x) - np.min(x)
            dy = np.max(y) - np.min(y)
            base = np.min(y)
            sigma, mu = dx * 0.1, xpeak(x, y)
            FitModel = getattr(fit, param.fittype)
            amp = FitModel.get_amp_from_amplitude(dy, sigma)
            p_in = np.array([amp, sigma, mu, base])

            def func(params):
                """Fitting model function"""
                return y - FitModel.func(x, *params)

            (amp, sigma, mu, base), _ier = spo.leastsq(func, p_in)
            x0, y0, x1, y1 = FitModel.half_max_segment(amp, sigma, mu, base)
            metadata["_" + title] = np.array([x0, y0, x1, y1, ShapeTypes.SEGMENT])
            return FitModel.fwhm(amp, sigma)

        param = FWHMParam(title)
        self.compute_10(title, fwhm, param)

    @qt_try_except()
    def compute_fw1e2(self):
        """Compute FW at 1/e²"""
        title = _("FW") + "1/e²"

        def fw1e2(x, y, metadata):
            """Compute FW at 1/e²"""
            dx = np.max(x) - np.min(x)
            dy = np.max(y) - np.min(y)
            base = np.min(y)
            sigma, mu = dx * 0.1, xpeak(x, y)
            amp = fit.GaussianModel.get_amp_from_amplitude(dy, sigma)
            p_in = np.array([amp, sigma, mu, base])

            def func(params):
                """Fitting model function"""
                return y - fit.GaussianModel.func(x, *params)

            p_out, _ier = spo.leastsq(func, p_in)
            amp, sigma, mu, base = p_out
            hw = 2 * sigma
            amplitude = fit.GaussianModel.amplitude(amp, sigma)
            yhm = amplitude / np.e**2 + base
            metadata["_" + title] = np.array(
                [mu - hw, yhm, mu + hw, yhm, ShapeTypes.SEGMENT]
            )
            return 2 * hw

        self.compute_10(title, fw1e2)

    # ------Computing
    def get_roi_dialog(self):
        """Get ROI from specific dialog box"""
        roi_s = _("Region of interest")
        dlg, obj = self.create_new_dialog_for_selection(roi_s)
        data = obj.xydata
        if len(data) == 2:  # x, y signal
            x, y = data  # pylint: disable=unused-variable
        elif len(data) == 4:  # x, y, dx, dy error bar signal
            x, y, dx, dy = data  # pylint: disable=unused-variable
        if obj.roi is not None:
            i0, i1 = obj.roi
            xmin, xmax = x[i0], x[i1]
        else:
            xmin, xmax = x.min(), x.max()
        range_sel = make.range(xmin, xmax)

        class RangeInfo(ObjectInfo):
            """ObjectInfo for ROI selection"""

            def __init__(self, xrangeselection):
                self.range = xrangeselection

            def get_text(self):
                x0, x1 = self.range.get_range()
                return f"{x0} ≤ x ≤ {x1}"

        info = RangeInfo(range_sel)
        disp = make.info_label("BL", info, title=roi_s)
        plot = dlg.get_plot()
        plot.add_item(range_sel)
        plot.add_item(disp)
        plot.set_active_item(range_sel)
        if dlg.exec():
            imax = len(obj.x) - 1
            x0, x1 = range_sel.get_range()
            i0 = np.where(x >= x0)[0][0]
            i1 = min([np.where(x <= x1)[0][-1] + 1, imax])
            return obj.get_roi_param(i0, i1)
