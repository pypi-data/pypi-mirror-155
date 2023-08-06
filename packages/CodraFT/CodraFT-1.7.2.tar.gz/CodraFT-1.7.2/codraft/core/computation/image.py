# -*- coding: utf-8 -*-
#
# Licensed under the terms of the CECILL License
# (see codraft/__init__.py for details)

"""
CodraFT Computation / Image module
"""

# pylint: disable=invalid-name  # Allows short reference names like x, y, ...

import numpy as np


def flatfield(rawdata, flatdata):
    """Compute flat-field correction"""
    dtemp = np.array(rawdata, dtype=np.float64, copy=True) * flatdata.mean()
    dunif = np.array(flatdata, dtype=np.float64, copy=True)
    dunif[dunif == 0] = 1.0
    return np.array(dtemp / dunif, dtype=rawdata.dtype)


def get_centroid_fourier(data):
    """Return image centroid using Fourier algorithm"""
    # Fourier transform method as discussed by Weisshaar et al.
    # (http://www.mnd-umwelttechnik.fh-wiesbaden.de/pig/weisshaar_u5.pdf)
    rows, cols = data.shape
    if rows == 1 or cols == 1:
        return 0, 0

    i = np.matrix(np.arange(0, rows))
    sin_a = np.sin((i - 1) * 2 * np.pi / (rows - 1))
    cos_a = np.cos((i - 1) * 2 * np.pi / (rows - 1))

    j = np.matrix(np.arange(0, cols)).transpose()
    sin_b = np.sin((j - 1) * 2 * np.pi / (cols - 1))
    cos_b = np.cos((j - 1) * 2 * np.pi / (cols - 1))

    a = (cos_a * data).sum()
    b = (sin_a * data).sum()
    c = (data * cos_b).sum()
    d = (data * sin_b).sum()

    rphi = (0 if b > 0 else 2 * np.pi) if a > 0 else np.pi
    cphi = (0 if d > 0 else 2 * np.pi) if c > 0 else np.pi

    if a * c == 0.0:
        return 0, 0

    row = (np.arctan(b / a) + rphi) * (rows - 1) / (2 * np.pi) + 1
    col = (np.arctan(d / c) + cphi) * (cols - 1) / (2 * np.pi) + 1
    return int(row), int(col)


def get_enclosing_circle(data, level=0.5):
    """Return (x, y, radius) for the circle contour enclosing image
    values above threshold relative level (.5 means FWHM)

    Raise ValueError if no contour was found"""
    if not isinstance(level, float) or level < 0.0 or level > 1.0:
        raise ValueError("Level must be a float between 0. and 1.")
    try:
        import cv2  # pylint: disable=import-outside-toplevel
    except ImportError as exc:
        raise ImportError("This feature requires OpenCV library") from exc
    data_th = data.copy()
    data_th[data <= data.max() * level] = 0.0
    data_8bits = np.array(data_th, dtype=np.uint8, copy=True)
    contours = cv2.findContours(data_8bits, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[
        -2
    ]
    if not contours:
        raise ValueError("No contour was found")
    (x, y), radius = cv2.minEnclosingCircle(max(contours, key=cv2.contourArea))
    return (int(x), int(y), radius)
