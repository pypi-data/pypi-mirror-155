# -*- coding: utf-8 -*-
#
# Licensed under the terms of the CECILL License
# (see codraft/__init__.py for details)

"""Curve fitting dialog widgets"""

# pylint: disable=invalid-name  # Allows short reference names like x, y, ...


import numpy as np
from guiqwt.widgets.fit import FitDialog, FitParam

from codraft.config import _
from codraft.core.computation import fit
from codraft.core.computation.signal import xpeak


def guifit(
    x,
    y,
    fitfunc,
    fitparams,
    fitargs=None,
    fitkwargs=None,
    wintitle=None,
    title=None,
    xlabel=None,
    ylabel=None,
    param_cols=1,
    auto_fit=True,
    winsize=None,
    winpos=None,
    parent=None,
):
    """GUI-based curve fitting tool"""
    win = FitDialog(
        edit=True,
        wintitle=wintitle,
        icon=None,
        toolbar=True,
        options=dict(title=title, xlabel=xlabel, ylabel=ylabel),
        parent=parent,
        param_cols=param_cols,
        auto_fit=auto_fit,
    )
    win.set_data(x, y, fitfunc, fitparams, fitargs, fitkwargs)
    win.autofit()  # TODO: make this optional
    if winsize is not None:
        win.resize(*winsize)
    if winpos is not None:
        win.move(*winpos)
    if win.exec():
        return win.get_values()
    return None


# --- Polynomial fitting curve -------------------------------------------------
def polynomialfit(x, y, degree, parent=None):
    """Compute polynomial fit

    Returns (yfit, params), where yfit is the fitted curve and params are
    the fitting parameters"""
    ivals = np.polyfit(x, y, degree)

    params = []
    for index in range(degree + 1):
        val = ivals[index]
        vmax = max(1.0, np.abs(val))
        param = FitParam(f"c{(len(ivals) - index - 1):d}", val, -2 * vmax, 2 * vmax)
        params.append(param)

    def fitfunc(x, params):
        return np.polyval(params, x)

    values = guifit(x, y, fitfunc, params, parent=parent)
    if values:
        return fitfunc(x, values), params


# --- Gaussian fitting curve ---------------------------------------------------
def gaussianfit(x, y, parent=None):
    """Compute Gaussian fit

    Returns (yfit, params), where yfit is the fitted curve and params are
    the fitting parameters"""
    dx = np.max(x) - np.min(x)
    dy = np.max(y) - np.min(y)
    sigma = dx * 0.1
    amp = fit.GaussianModel.get_amp_from_amplitude(dy, sigma)

    a = FitParam(_("Amplitude"), amp, 0.0, amp * 1.2)
    b = FitParam(_("Base line"), np.min(y), np.min(y) - 0.1 * dy, np.max(y))
    sigma = FitParam(_("Std-dev") + " (σ)", sigma, sigma * 0.2, sigma * 10)
    mu = FitParam(_("Mean") + " (μ)", xpeak(x, y), np.min(x), np.max(x))

    params = [a, sigma, mu, b]

    def fitfunc(x, params):
        return fit.GaussianModel.func(x, *params)

    values = guifit(x, y, fitfunc, params, parent=parent)
    if values:
        return fitfunc(x, values), params


# --- Lorentzian fitting curve -------------------------------------------------
def lorentzianfit(x, y, parent=None):
    """Compute Lorentzian fit

    Returns (yfit, params), where yfit is the fitted curve and params are
    the fitting parameters"""
    dx = np.max(x) - np.min(x)
    dy = np.max(y) - np.min(y)
    sigma = dx * 0.1
    amp = fit.LorentzianModel.get_amp_from_amplitude(dy, sigma)

    a = FitParam(_("Amplitude"), amp, 0.0, amp * 1.2)
    b = FitParam(_("Base line"), np.min(y), np.min(y) - 0.1 * dy, np.max(y))
    sigma = FitParam(_("Std-dev") + " (σ)", sigma, sigma * 0.2, sigma * 10)
    mu = FitParam(_("Mean") + " (μ)", xpeak(x, y), np.min(x), np.max(x))

    params = [a, sigma, mu, b]

    def fitfunc(x, params):
        return fit.LorentzianModel.func(x, *params)

    values = guifit(x, y, fitfunc, params, parent=parent)
    if values:
        return fitfunc(x, values), params


# --- Voigt fitting curve ------------------------------------------------------
def voigtfit(x, y, parent=None):
    """Compute Voigt fit

    Returns (yfit, params), where yfit is the fitted curve and params are
    the fitting parameters"""
    dx = np.max(x) - np.min(x)
    dy = np.max(y) - np.min(y)
    sigma = dx * 0.1
    amp = fit.VoigtModel.get_amp_from_amplitude(dy, sigma)

    a = FitParam(_("Amplitude"), amp, 0.0, amp * 1.2)
    b = FitParam(_("Base line"), np.min(y), np.min(y) - 0.1 * dy, np.max(y))
    sigma = FitParam(_("Std-dev") + " (σ)", sigma, sigma * 0.2, sigma * 10)
    mu = FitParam(_("Mean") + " (μ)", xpeak(x, y), np.min(x), np.max(x))

    params = [a, sigma, mu, b]

    def fitfunc(x, params):
        return fit.VoigtModel.func(x, *params)

    values = guifit(x, y, fitfunc, params, parent=parent)
    if values:
        return fitfunc(x, values), params


# --- Multi-Gaussian fitting curve ---------------------------------------------
def multigaussian(x, *values, **kwargs):
    """Return a 1-dimensional multi-Gaussian function."""
    a_amp = values[0::2]
    a_sigma = values[1::2]
    y0 = values[-1]
    a_x0 = kwargs["a_x0"]
    y = np.zeros_like(x) + y0
    for amp, sigma, x0 in zip(a_amp, a_sigma, a_x0):
        y += amp * np.exp(-0.5 * ((x - x0) / sigma) ** 2)
    return y


def multigaussianfit(x, y, peak_indexes, parent=None):
    """Compute Multi-Gaussian fit

    Returns (yfit, params), where yfit is the fitted curve and params are
    the fitting parameters"""
    params = []
    for index, i0 in enumerate(peak_indexes):
        iprev = 0
        inext = len(x) - 1
        if i0 != 0:
            iprev = i0 - 1
        if i0 < inext:
            inext = i0 + 1
        dx = x[inext] - x[iprev]
        dy = np.max(y[iprev:inext]) - np.min(y[iprev:inext])
        stri = f"{index + 1:02d}"
        params += [
            FitParam(("A") + stri, y[i0], 0.0, dy * 1.2),
            FitParam("σ" + stri, dx * 0.8, dx * 0.02, dx),
        ]

    params.append(
        FitParam(
            _("Y0"), np.min(y), np.min(y) - 0.1 * (np.max(y) - np.min(y)), np.max(y)
        )
    )

    kwargs = dict(a_x0=x[peak_indexes])

    def fitfunc(xi, params):
        return multigaussian(xi, *params, **kwargs)

    param_cols = 1
    if len(params) > 8:
        param_cols = 4
    values = guifit(
        x, y, fitfunc, params, param_cols=param_cols, winsize=(900, 600), parent=parent
    )
    if values:
        return fitfunc(x, values), params
