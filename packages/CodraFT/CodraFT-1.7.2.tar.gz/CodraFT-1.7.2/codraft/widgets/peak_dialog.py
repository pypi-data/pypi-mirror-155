# -*- coding: utf-8 -*-
#
# Licensed under the terms of the CECILL License
# (see codraft/__init__.py for details)

"""Peak detection feature"""

# pylint: disable=invalid-name  # Allows short reference names like x, y, ...


import numpy as np
from guidata.configtools import get_icon
from guiqwt.builder import make
from guiqwt.plot import CurveDialog

from codraft.config import _
from codraft.core.computation.signal import peak_indexes


class PeakDetectionDialog(CurveDialog):
    """Peak detection dialog"""

    def __init__(self, parent=None):
        super().__init__(wintitle=_("Peak detection"), edit=True, parent=parent)
        self.setWindowIcon(get_icon("codraft.svg"))
        self.peaks = None
        self.peak_indexes = None
        self.in_x = None
        self.in_y = None
        self.in_curve = None
        self.in_threshold = None
        self.in_threshold_cursor = None
        self.co_results = None
        self.co_positions = None
        self.co_markers = None
        legend = make.legend("TR")
        self.get_plot().add_item(legend)

    def get_peaks(self):
        """Return peaks coordinates"""
        return self.peaks

    def get_peak_indexes(self):
        """Return peak indexes"""
        return self.peak_indexes

    def get_threshold(self):
        """Return relative threshold"""
        y = self.in_y
        return (self.in_threshold - np.min(y)) / (np.max(y) - np.min(y))

    def compute_peaks(self):
        """Compute peak detection"""
        x, y = self.in_x, self.in_y
        plot = self.get_plot()
        self.peak_indexes = peak_indexes(y, thres=self.in_threshold, thres_abs=True)
        self.peaks = [(x[index], y[index]) for index in self.peak_indexes]
        markers = [
            make.marker(
                pos,
                movable=False,
                color="orange",
                markerstyle="|",
                linewidth=1,
                marker="NoShape",
                linestyle="DashLine",
            )
            for pos in self.peaks
        ]
        if self.co_markers is not None:
            plot.del_items(self.co_markers)
        self.co_markers = markers
        for item in self.co_markers:
            plot.add_item(item)
        positions = [str(marker.get_pos()[0]) for marker in markers]
        prefix = f'<b>{_("Peaks:")}</b><br>'
        self.co_results.set_text(prefix + "<br>".join(positions))

    def hcursor_changed(self, marker):
        """Horizontal cursor position has changed"""
        _x, y = marker.get_pos()
        self.in_threshold = y
        self.compute_peaks()

    def setup_data(self, x, y):
        """Setup dialog box"""
        self.in_curve = make.curve(x, y, "ab", "b")
        plot = self.get_plot()
        plot.add_item(self.in_curve)
        self.in_threshold = 0.3 * (np.max(y) - np.min(y)) + np.min(y)
        cursor = make.hcursor(self.in_threshold)
        self.in_threshold_cursor = cursor
        plot.add_item(self.in_threshold_cursor)
        self.co_results = make.label("", "TL", (0, 0), "TL")
        plot.add_item(self.co_results)
        plot.SIG_MARKER_CHANGED.connect(self.hcursor_changed)
        self.in_x, self.in_y = x, y
        self.compute_peaks()
