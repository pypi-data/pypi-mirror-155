# -*- coding: utf-8 -*-
#
# Licensed under the terms of the CECILL License
# (see codraft/__init__.py for details)

"""
CodraFT New Signal/Image GUI module
"""

# pylint: disable=invalid-name  # Allows short reference names like x, y, ...

import numpy as np

from guidata.dataset.datatypes import DataSet
from guidata.dataset.dataitems import IntItem, StringItem, ChoiceItem, FloatItem
from guiqwt import io

from codraft.config import _
from codraft.core.model import create_signal, create_image
from codraft.core.computation import fit


# --- New Signal ---------------------------------------------------------------
class SignalParamNew(DataSet):
    """New signal dataset"""

    title = StringItem(_("Title"), default=_("Untitled"))
    xmin = FloatItem("Xmin", default=-10.0)
    xmax = FloatItem("Xmax", default=10.0)
    size = IntItem(
        _("Size"), help=_("Signal size (total number of points)"), min=1, default=500
    )
    type = ChoiceItem(
        _("Type"),
        (
            ("zeros", _("zeros")),
            ("gauss", _("gaussian")),
            ("lorentz", _("lorentzian")),
            ("voigt", "Voigt"),
            ("rand", _("random")),
        ),
    )


SIG_NB = 0


class GaussLorentzVoigtParam(DataSet):
    """Parameters for Gaussian and Lorentzian functions"""

    a = FloatItem("A", default=1.0)
    ymin = FloatItem("Ymin", default=0.0).set_pos(col=1)
    sigma = FloatItem("σ", default=1.0)
    mu = FloatItem("μ", default=0.0).set_pos(col=1)


def create_signal_gui(parent, size=None):
    """Create a new Signal object from a dialog box"""
    global SIG_NB  # pylint: disable=global-statement
    signalnew = SignalParamNew(title=_("Create a new signal"))
    if size is not None:
        signalnew.size = size
    signalnew.title = f"{signalnew.title} {SIG_NB + 1:d}"
    if signalnew.edit(parent=parent):
        SIG_NB += 1
        signal = create_signal(signalnew.title)
        xarr = np.linspace(signalnew.xmin, signalnew.xmax, signalnew.size)
        if signalnew.type == "zeros":
            signal.set_xydata(xarr, np.zeros(signalnew.size))
        elif signalnew.type == "rand":
            signal.set_xydata(xarr, np.random.rand(signalnew.size) - 0.5)
        elif signalnew.type == "gauss":
            param = GaussLorentzVoigtParam(_("New gaussian function"))
            if not param.edit(parent=parent):
                return None
            yarr = fit.GaussianModel.func(
                xarr, param.a, param.sigma, param.mu, param.ymin
            )
            signal.set_xydata(xarr, yarr)
        elif signalnew.type == "lorentz":
            param = GaussLorentzVoigtParam(_("New lorentzian function"))
            if not param.edit(parent=parent):
                return None
            yarr = fit.LorentzianModel.func(
                xarr, param.a, param.sigma, param.mu, param.ymin
            )
            signal.set_xydata(xarr, yarr)
        elif signalnew.type == "voigt":
            param = GaussLorentzVoigtParam(_("New Voigt function"))
            if not param.edit(parent=parent):
                return None
            yarr = fit.VoigtModel.func(xarr, param.a, param.sigma, param.mu, param.ymin)
            signal.set_xydata(xarr, yarr)
        return signal
    return None


# --- New Image ----------------------------------------------------------------
class ImageParamNew(DataSet):
    """New image dataset"""

    title = StringItem(_("Title"), default=_("Untitled"))
    height = IntItem(
        _("Height"), help=_("Image height (total number of rows)"), min=1, default=500
    )
    width = IntItem(
        _("Width"), help=_("Image width (total number of columns)"), min=1, default=500
    )
    dtype = ChoiceItem(
        _("Data type"),
        (
            (np.uint8, "uint8"),
            (np.int16, "uint16"),
            (np.float32, "float32"),
            (np.float64, "float64"),
        ),
    )
    type = ChoiceItem(
        _("Type"),
        (
            ("zeros", _("zeros")),
            ("empty", _("empty")),
            ("gauss", _("gaussian")),
            ("rand", _("random")),
        ),
    )


IMG_NB = 0


def create_image_gui(parent, width=None, height=None):
    """Create a new Image object from dialog box"""
    global IMG_NB  # pylint: disable=global-statement
    imagenew = ImageParamNew(title=_("Create a new image"))
    if width is not None:
        imagenew.width = width
    if height is not None:
        imagenew.height = height
        imagenew.title = f"{imagenew.title} {IMG_NB + 1:d}"
    if imagenew.edit(parent=parent):
        IMG_NB += 1
        image = create_image(imagenew.title)
        shape = (imagenew.height, imagenew.width)
        dtype = imagenew.dtype
        if imagenew.type == "zeros":
            image.data = np.zeros(shape, dtype=dtype)
        elif imagenew.type == "empty":
            image.data = np.empty(shape, dtype=dtype)
        elif imagenew.type == "gauss":
            try:
                maxval = np.iinfo(dtype).max / 2.0
            except ValueError:
                maxval = 10.0

            class GaussParam(DataSet):
                """2D Gaussian parameters"""

                a = FloatItem("Norm", default=maxval)
                xmin = FloatItem("Xmin", default=-10).set_pos(col=1)
                sigma = FloatItem("σ", default=1.0)
                xmax = FloatItem("Xmax", default=10).set_pos(col=1)
                mu = FloatItem("μ", default=0.0)
                ymin = FloatItem("Ymin", default=-10).set_pos(col=1)
                x0 = FloatItem("X0", default=0)
                ymax = FloatItem("Ymax", default=10).set_pos(col=1)
                y0 = FloatItem("Y0", default=0).set_pos(col=0, colspan=1)

            param = GaussParam(_("New 2D-gaussian image"))
            if not param.edit(parent=parent):
                return None
            x, y = np.meshgrid(
                np.linspace(param.xmin, param.xmax, shape[1]),
                np.linspace(param.ymin, param.ymax, shape[0]),
            )
            x0, y0 = param.x0, param.y0
            zgauss = param.a * np.exp(
                -((np.sqrt((x - x0) ** 2 + (y - y0) ** 2) - param.mu) ** 2)
                / (2.0 * param.sigma**2)
            )
            image.data = np.array(zgauss, dtype=dtype)
        elif imagenew.type == "rand":
            data = np.random.rand(*shape)
            image.data = io.scale_data_to_dtype(data, dtype)
        return image
    return None
