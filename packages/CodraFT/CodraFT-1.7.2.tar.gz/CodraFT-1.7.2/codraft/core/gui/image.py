# -*- coding: utf-8 -*-
#
# Licensed under the terms of the CECILL License
# (see codraft/__init__.py for details)

"""
CodraFT Image GUI module
"""

# pylint: disable=invalid-name  # Allows short reference names like x, y, ...

import os.path as osp
import os

from qtpy import QtWidgets as QW

import numpy as np
import scipy.ndimage as spi
import scipy.signal as sps

from guidata.dataset.datatypes import DataSet, ValueProp
from guidata.dataset.dataitems import IntItem, ChoiceItem, FloatItem, BoolItem
from guidata.configtools import get_icon
from guidata.qthelpers import create_action, add_actions
from guidata.utils import update_dataset

from guiqwt.plot import ImageDialog
from guiqwt.builder import make
from guiqwt.tools import (
    AnnotatedRectangleTool,
    AnnotatedEllipseTool,
    AnnotatedSegmentTool,
    AnnotatedCircleTool,
    LabelTool,
    AnnotatedPointTool,
    VCursorTool,
    HCursorTool,
    XCursorTool,
)
from guiqwt.widgets.resizedialog import ResizeDialog
from guiqwt.qthelpers import exec_images_open_dialog, exec_image_save_dialog

from codraft.config import _, APP_NAME
from codraft.core.model import ImageParam, create_image, make_roi_rectangle
from codraft.core.gui.new import create_image_gui
from codraft.core.gui.base import ObjectFT
from codraft.utils.qthelpers import qt_try_except
from codraft.core.computation.image import (
    flatfield,
    get_centroid_fourier,
    get_enclosing_circle,
)
from codraft.core.io import iohandler  # pylint: disable=W0611


class ImageFT(ObjectFT):
    """Object handling the item list, the selected item properties and plot,
    specialized for Image objects"""

    PARAMCLASS = ImageParam
    DIALOGCLASS = ImageDialog
    PREFIX = "i"
    OBJECT_STR = _("image")

    # ------ObjectFT API
    def create_operation_actions(self):
        """Create operation actions"""
        base_actions = super().create_operation_actions()
        rotate_menu = QW.QMenu(_("Rotation"), self)
        hflip_act = create_action(
            self,
            _("Flip horizontally"),
            triggered=self.flip_horizontally,
            icon=get_icon("flip_horizontally.svg"),
        )
        vflip_act = create_action(
            self,
            _("Flip vertically"),
            triggered=self.flip_vertically,
            icon=get_icon("flip_vertically.svg"),
        )
        rot90_act = create_action(
            self,
            _("Rotate 90° right"),
            triggered=self.rotate_270,
            icon=get_icon("rotate_right.svg"),
        )
        rot270_act = create_action(
            self,
            _("Rotate 90° left"),
            triggered=self.rotate_90,
            icon=get_icon("rotate_left.svg"),
        )
        rotate_act = create_action(
            self, _("Rotate arbitrarily..."), triggered=self.rotate_arbitrarily
        )
        resize_act = create_action(self, _("Resize"), triggered=self.resize_image)
        logp1_act = create_action(self, "Log10(z+n)", triggered=self.compute_logp1)
        flatfield_act = create_action(
            self, _("Flat-field correction"), triggered=self.flat_field_correction
        )
        self.actlist_2 += [flatfield_act]
        self.actlist_1more += [
            resize_act,
            hflip_act,
            vflip_act,
            logp1_act,
            rot90_act,
            rot270_act,
            rotate_act,
        ]
        add_actions(
            rotate_menu, [hflip_act, vflip_act, rot90_act, rot270_act, rotate_act]
        )
        roi_actions = self.operation_end_actions
        actions = [logp1_act, flatfield_act, None, rotate_menu, None, resize_act]
        return base_actions + actions + roi_actions

    def create_processing_actions(self):
        """Create processing actions"""
        base_actions = super().create_processing_actions()
        cra = create_action
        lincal_action = cra(self, _("Linear calibration"), self.calibrate)
        threshold_action = cra(self, _("Thresholding"), self.compute_threshold)
        clip_action = cra(self, _("Clipping"), self.compute_clip)
        actions = [lincal_action, threshold_action, clip_action]
        self.actlist_1more += actions
        return actions + [None] + base_actions

    def create_computing_actions(self):
        """Create computing actions"""
        defineroi_action = create_action(
            self, _("Define ROI"), self.define_roi, icon=get_icon("roi.svg")
        )
        centroid_action = create_action(
            self, _("Centroid"), self.compute_centroid, tip=_("Compute image centroid")
        )
        enclosing_action = create_action(
            self,
            _("Minimum enclosing circle center"),
            self.compute_enclosing_circle,
            tip=_("Compute smallest enclosing circle center"),
        )
        self.actlist_1 += [defineroi_action]
        self.actlist_1more += [centroid_action, enclosing_action]
        return [defineroi_action, None, centroid_action, enclosing_action]

    def make_item(self, obj, update_from=None):
        """Make plot item associated to data,
        eventually update item from another item (`update_from`)"""
        data = obj.data.real
        if np.any(np.isnan(data)):
            data = np.nan_to_num(data)
        item = make.image(
            data,
            title=obj.title,
            colormap="jet",
            eliminate_outliers=0.1,
            interpolation="nearest",
        )
        if update_from is not None:
            update_dataset(item.imageparam, update_from.imageparam)
        update_dataset(item.imageparam, obj.metadata)
        item.imageparam.update_image(item)
        return item

    def update_item(self, row):
        """Update plot item associated to data"""
        obj = self.objects[row]
        data = obj.data.real
        if np.any(np.isnan(data)):
            data = np.nan_to_num(data)
        item = self.items[row]
        lut_range = [item.min, item.max]
        item.set_data(data, lut_range=lut_range)
        item.imageparam.label = obj.title
        for axis in ("x", "y", "z"):
            unit = getattr(obj, axis + "unit")
            fmt = r"%.1f"
            if unit:
                fmt = r"%.1f (" + unit + ")"
            setattr(item.imageparam, axis + "format", fmt)
        item.plot().update_colormap_axis(item)

    def open_separate_view(self, rows=None):
        """Open separate view for visualizing selected objects"""
        if rows is None:
            rows = self.get_selected_rows()
        tools = (
            AnnotatedRectangleTool,
            AnnotatedEllipseTool,
            AnnotatedSegmentTool,
            AnnotatedCircleTool,
            LabelTool,
            AnnotatedPointTool,
            VCursorTool,
            HCursorTool,
            XCursorTool,
        )
        dlg = self.create_new_dialog(rows, tools=tools)
        dlg.plot_widget.itemlist.setVisible(True)
        dlg.exec()

    def cleanup_dataview(self):
        """Clean up data view"""
        for widget in (self.plotwidget.xcsw, self.plotwidget.ycsw):
            widget.hide()
        ObjectFT.cleanup_dataview(self)

    def get_plot_options(self):
        """Return standard image plot options"""
        return dict(
            xlabel=self.plot.get_axis_title("bottom"),
            ylabel=self.plot.get_axis_title("left"),
            zlabel=self.plot.get_axis_title("right"),
            xunit=self.plot.get_axis_unit("bottom"),
            yunit=self.plot.get_axis_unit("left"),
            zunit=self.plot.get_axis_unit("right"),
            show_contrast=True,
        )

    # ------I/O
    def new_object(self):
        """Create a new image"""
        width, height = None, None
        rows = self.get_selected_rows()
        if rows:
            width, height = self.objects[rows[-1]].size
        image = create_image_gui(self, width=width, height=height)
        if image is not None:
            self.add_object(image)

    def open_object(self):
        """Open image file"""
        for filename, data in exec_images_open_dialog(
            self, basedir="", app_name=APP_NAME, to_grayscale=False
        ):
            os.chdir(osp.dirname(filename))
            if filename.lower().endswith(".sif") and len(data.shape) == 3:
                for idx in range(data.shape[0]):
                    image = create_image(
                        osp.basename(filename) + "_Im" + str(idx), data[idx, ::]
                    )
                    self.add_object(image)
            else:
                if data.ndim == 3:
                    # Converting to grayscale
                    data = data[..., :4].mean(axis=2)
                image = create_image(osp.basename(filename), data)
                if osp.splitext(filename)[1].lower() == ".dcm":
                    import dicom  # pylint: disable=C0415,E0401

                    image.template = dicom.read_file(filename, stop_before_pixels=True)
                self.add_object(image)

    def save_object(self):
        """Save selected image"""
        rows = self.get_selected_rows()
        for row in rows:
            obj = self.objects[row]

            filename = exec_image_save_dialog(
                self, obj.data, template=obj.template, basedir="", app_name=APP_NAME
            )
            if filename:
                os.chdir(osp.dirname(filename))

    # ------Image operations
    def compute_logp1(self):
        """Compute base 10 logarithm"""

        class LogP1Param(DataSet):
            """Log10 parameters"""

            n = FloatItem("n")

        self.compute_11(
            "Log10(z+n)",
            lambda z, p: np.log10(z + p.n),
            LogP1Param("Log10(z+n)"),
            suffix=lambda p: f"n={p.n}",
        )

    def rotate_arbitrarily(self):
        """Rotate data arbitrarily"""
        boundaries = ("constant", "nearest", "reflect", "wrap")
        prop = ValueProp(False)

        class RotateParam(DataSet):
            """Rotate parameters"""

            angle = FloatItem(f"{_('Angle')} (°)")
            mode = ChoiceItem(
                _("Mode"), list(zip(boundaries, boundaries)), default=boundaries[0]
            )
            cval = FloatItem(
                _("cval"),
                default=0.0,
                help=_(
                    "Value used for points outside the "
                    "boundaries of the input if mode is "
                    "'constant'"
                ),
            )
            reshape = BoolItem(
                _("Reshape the output array"),
                default=True,
                help=_(
                    "Reshape the output array "
                    "so that the input array is "
                    "contained completely in the output"
                ),
            )
            prefilter = BoolItem(_("Prefilter the input image"), default=True).set_prop(
                "display", store=prop
            )
            order = IntItem(
                _("Order"),
                default=3,
                min=0,
                max=5,
                help=_("Spline interpolation order"),
            ).set_prop("display", active=prop)

        param = RotateParam(_("Rotation"))

        # TODO: Instead of removing computing metadata, fix it following rotation
        self.compute_11(
            "Rotate",
            lambda x, p: spi.rotate(
                x,
                p.angle,
                reshape=p.reshape,
                order=p.order,
                mode=p.mode,
                cval=p.cval,
                prefilter=p.prefilter,
            ),
            param,
            suffix=lambda p: f"α={p.angle:.3f}°, mode='{p.mode}'",
            func_obj=lambda obj: obj.remove_computing_metadata(),
        )

    def rotate_90(self):
        """Rotate data 90°"""
        # TODO: Instead of removing computing metadata, fix it following 90° rotation
        self.compute_11(
            "Rotate90", np.rot90, func_obj=lambda obj: obj.remove_computing_metadata()
        )

    def rotate_270(self):
        """Rotate data 270°"""
        # TODO: Instead of removing computing metadata, fix it following 270° rotation
        self.compute_11(
            "Rotate270",
            lambda x: np.rot90(x, 3),
            func_obj=lambda obj: obj.remove_computing_metadata(),
        )

    def flip_horizontally(self):
        """Flip data horizontally"""
        # TODO: Instead of removing computing metadata, fix it following horizontal flip
        self.compute_11(
            "HFlip", np.fliplr, func_obj=lambda obj: obj.remove_computing_metadata()
        )

    def flip_vertically(self):
        """Flip data vertically"""
        # TODO: Instead of removing computing metadata, fix it following vertical flip
        self.compute_11(
            "VFlip", np.flipud, func_obj=lambda obj: obj.remove_computing_metadata()
        )

    def resize_image(self):
        """Resize image"""
        rows = self.get_selected_rows()
        objs = self.objects
        for row in rows:
            if objs[row].size != objs[rows[0]].size:
                QW.QMessageBox.warning(
                    self.parent(),
                    APP_NAME,
                    _("Warning:")
                    + "\n"
                    + _("Selected images do not have the same size"),
                )
        original_size = objs[rows[0]].size

        dlg = ResizeDialog(
            self.plot,
            new_size=original_size,
            old_size=original_size,
            text=_("Destination size:"),
        )
        if not dlg.exec():
            return
        boundaries = ("constant", "nearest", "reflect", "wrap")
        prop = ValueProp(False)

        class ResizeParam(DataSet):
            """Resize parameters"""

            zoom = FloatItem(_("Zoom"), default=dlg.get_zoom())
            mode = ChoiceItem(
                _("Mode"), list(zip(boundaries, boundaries)), default=boundaries[0]
            )
            cval = FloatItem(
                _("cval"),
                default=0.0,
                help=_(
                    "Value used for points outside the "
                    "boundaries of the input if mode is "
                    "'constant'"
                ),
            )
            prefilter = BoolItem(_("Prefilter the input image"), default=True).set_prop(
                "display", store=prop
            )
            order = IntItem(
                _("Order"),
                default=3,
                min=0,
                max=5,
                help=_("Spline interpolation order"),
            ).set_prop("display", active=prop)

        param = ResizeParam(_("Resize"))

        def func_obj(obj):
            """Zooming function"""
            dx, dy = obj.pixel_spacing
            if dx is not None and dy is not None:
                obj.pixel_spacing = dx / param.zoom, dy / param.zoom
            # TODO: Instead of removing computing metadata, fix it following zoom
            obj.remove_computing_metadata()

        self.compute_11(
            "Zoom",
            lambda x, p: spi.interpolation.zoom(
                x,
                p.zoom,
                order=p.order,
                mode=p.mode,
                cval=p.cval,
                prefilter=p.prefilter,
            ),
            param,
            suffix=lambda p: f"zoom={p.zoom:.3f}",
            func_obj=func_obj,
        )

    def extract_roi(self):
        """Extract Region Of Interest (ROI) from data"""
        param = self.get_roi_dialog()
        if param is not None:

            def suffix_func(p):
                return f"rows={p.row1:d}:{p.row2:d},cols={p.col1:d}:{p.col2:d}"

            # TODO: Instead of removing computing metadata, fix it following ROI extract
            self.compute_11(
                "ROI",
                lambda x, p: x.copy()[p.row1 : p.row2, p.col1 : p.col2],
                param,
                suffix=suffix_func,
                func_obj=lambda obj: obj.remove_computing_metadata(),
            )

    def swap_axes(self):
        """Swap data axes"""
        self.compute_11(
            "SwapAxes",
            lambda z: z.T,
            func_obj=lambda obj: obj.remove_computing_metadata(),
        )

    def compute_abs(self):
        """Compute absolute value"""
        self.compute_11("Abs", np.abs)

    def compute_log10(self):
        """Compute Log10"""
        self.compute_11("Log10", np.log10)

    @qt_try_except()
    def flat_field_correction(self):
        """Compute flat field correction"""
        rows = self.get_selected_rows()
        robj = self.PARAMCLASS()
        robj.title = (
            "FlatField(" + (",".join([f"{self.PREFIX}{row:03d}" for row in rows])) + ")"
        )
        robj.data = flatfield(self.objects[rows[0]].data, self.objects[rows[1]].data)
        self.add_object(robj)

    # ------Image Processing
    def apply_11_func(self, obj, orig, func, param, message):
        """Apply 11 function: 1 object in --> 1 object out"""

        # (self is used by @qt_try_except)
        # pylint: disable=unused-argument
        @qt_try_except(message)
        def apply_11_func_callback(self, obj, orig, func, param):
            """Apply 11 function callback: 1 object in --> 1 object out"""
            if param is None:
                obj.data = func(orig.data)
            else:
                obj.data = func(orig.data, param)

        return apply_11_func_callback(self, obj, orig, func, param)

    @qt_try_except()
    def calibrate(self):
        """Compute data linear calibration"""

        class CalibrateParam(DataSet):
            """Linear calibration parameters"""

            a = FloatItem("a", default=1.0)
            b = FloatItem("b", default=0.0)

        param = CalibrateParam(_("Linear calibration"), "y = a.x + b")
        self.compute_11(
            "LinearCal",
            lambda x, p: p.a * x + p.b,
            param,
            suffix=lambda p: "z={p.a}*z+{p.b}",
        )

    @qt_try_except()
    def compute_threshold(self):
        """Compute threshold clipping"""

        class ThresholdParam(DataSet):
            """Threshold parameters"""

            value = FloatItem(_("Threshold"))

        self.compute_11(
            "Threshold",
            lambda x, p: np.clip(x, p.value, x.max()),
            ThresholdParam(_("Thresholding")),
            suffix=lambda p: f"min={p.value} lsb",
        )

    @qt_try_except()
    def compute_clip(self):
        """Compute maximum data clipping"""

        class ClipParam(DataSet):
            """Data clipping parameters"""

            value = FloatItem(_("Clipping value"))

        self.compute_11(
            "Clip",
            lambda x, p: np.clip(x, x.min(), p.value),
            ClipParam(_("Clipping")),
            suffix=lambda p: f"max={p.value} lsb",
        )

    @staticmethod
    def func_gaussian_filter(x, p):  # pylint: disable=arguments-differ
        """Compute gaussian filter"""
        return spi.gaussian_filter(x, p.sigma)

    @qt_try_except()
    def compute_fft(self):
        """Compute FFT"""
        self.compute_11("FFT", np.fft.fft2)

    @qt_try_except()
    def compute_ifft(self):
        "Compute iFFT" ""
        self.compute_11("iFFT", np.fft.ifft2)

    @staticmethod
    def func_moving_average(x, p):  # pylint: disable=arguments-differ
        """Moving average computing function"""
        return spi.uniform_filter(x, size=p.n, mode="constant")

    @staticmethod
    def func_moving_median(x, p):  # pylint: disable=arguments-differ
        """Moving median computing function"""
        return sps.medfilt(x, kernel_size=p.n)

    @qt_try_except()
    def compute_wiener(self):
        """Compute Wiener filter"""
        self.compute_11("WienerFilter", sps.wiener)

    # ------Image Computing
    def apply_10_func(self, orig, func, param, message):
        """Apply 10 function: 1 object in --> 0 object out (scalar result)"""

        # (self is used by @qt_try_except)
        # pylint: disable=unused-argument
        @qt_try_except(message)
        def apply_10_func_callback(self, orig, func, param):
            """Apply 10 function cb: 1 object in --> 0 object out (scalar result)"""
            if param is None:
                return func(orig)
            return func(orig, param)

        return apply_10_func_callback(self, orig, func, param)

    @qt_try_except()
    def compute_centroid(self):
        """Compute image centroid"""

        def centroid(image):
            """Compute centroid"""
            if image.roi is None:
                data = image.data
            else:
                x0, y0, x1, y1 = image.roi
                data = image.data[y0:y1, x0:x1]
            y, x = get_centroid_fourier(data)
            if image.roi is not None:
                x += x0
                y += y0
            return x, y

        self.compute_10(_("Centroid"), centroid)

    @qt_try_except()
    def compute_enclosing_circle(self):
        """Compute minimum enclosing circle"""

        def enclosing_circle(image):
            """Compute minimum enclosing circle"""
            if image.roi is None:
                data = image.data
            else:
                x0, y0, x1, y1 = image.roi
                data = image.data[y0:y1, x0:x1]
            x, y, radius = get_enclosing_circle(data)  # pylint: disable=unused-variable
            if image.roi is not None:
                x += x0
                y += y0
            return x, y

        # TODO: Find a way to add the circle to the computing results
        #  as in "enclosingcircle_test.py"
        self.compute_10(_("MinEnclosingCircle"), enclosing_circle)

    # ------Computing
    def get_roi_dialog(self):
        """Get ROI from specific dialog box"""
        roi_s = _("Region of interest")
        dlg, obj = self.create_new_dialog_for_selection(roi_s)
        if obj.roi is not None:
            x0, y0, x1, y1 = obj.roi
        else:
            x0, y0, x1, y1 = 0, 0, obj.size[0], obj.size[1]
        crect = make_roi_rectangle(x0, y0, x1, y1)
        plot = dlg.get_plot()
        plot.add_item(crect)
        plot.set_active_item(crect)
        if dlg.exec():
            parameters = [int(val) for val in crect.get_rect()]
            return obj.get_roi_param(*parameters)
        return None
