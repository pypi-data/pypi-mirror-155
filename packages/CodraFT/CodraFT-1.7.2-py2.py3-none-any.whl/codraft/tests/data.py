# -*- coding: utf-8 -*-
#
# Licensed under the terms of the CECILL License
# (see codraft/__init__.py for details)

"""
Test data functions

Functions creating test data: curves, images, ...
"""

# pylint: disable=invalid-name  # Allows short reference names like x, y, ...

import numpy as np

from codraft.core import io
from codraft.core.computation import fit
from codraft.core.model import create_image, create_signal
from codraft.utils.tests import get_test_fnames


def create_test_2d_data(shape, dtype):
    """Creating 2D test data"""
    x, y = np.meshgrid(np.linspace(0, 10, shape[1]), np.linspace(0, 10, shape[0]))
    raw_data = 0.5 * (np.sin(x) + np.cos(y)) + 0.5
    dmin = np.iinfo(dtype).min * 0.95
    dmax = np.iinfo(dtype).max * 0.95
    return np.array(raw_data * (dmax - dmin) + dmin, dtype=dtype)


def create_2d_steps_data(shape, width, dtype):
    """Creating 2D steps data for testing purpose"""
    data = np.zeros(shape, dtype=dtype)
    value = 1
    for col in range(0, shape[1] - width + 1, width):
        data[:, col : col + width] = value
        value *= 10
    data2 = np.zeros_like(data)
    value = 1
    for row in range(0, shape[0] - width + 1, width):
        data2[row : row + width, :] = value
        value *= 10
    data += data2
    return data


def create_noisy_2d_gaussian(shape, dtype, x0=0, y0=0, noiselvl=0.2):
    """Creating 2D Noisy Gaussian"""
    xlim = [-10, 10]
    ylim = [-10, 10]
    relative_amplitude = 0.5
    mu = 0.0
    sigma = 2.0
    x, y = np.meshgrid(
        np.linspace(xlim[0], xlim[1], shape[1]), np.linspace(ylim[0], ylim[1], shape[0])
    )
    amp = np.iinfo(dtype).max * relative_amplitude
    zgauss = amp * np.exp(
        -((np.sqrt((x - x0) ** 2 + (y - y0) ** 2) - mu) ** 2) / (2.0 * sigma**2)
    )
    noise = np.random.rand(*shape) * noiselvl * amp
    return np.array(zgauss + noise, dtype=dtype)


def get_laser_spot_data():
    """Return a list of NumPy arrays containing images which are relevant for
    testing laser spot image processing features"""
    noisy_gaussian = create_noisy_2d_gaussian((2000, 2000), np.uint16, x0=2.0, y0=-3.0)
    return [noisy_gaussian] + [
        io.imread_scor(fname) for fname in get_test_fnames("*.scor-data")
    ]


def create_test_signal1():
    """Create test signal (Paracetamol molecule spectrum)"""
    data = np.loadtxt(get_test_fnames("paracetamol.txt")[0], delimiter=",")
    obj = create_signal("Paracetamol")
    obj.xydata = data.T
    return obj


def create_test_signal2():
    """Create test signal (Gaussian curve)"""
    obj = create_signal("Gaussienne")
    x = np.linspace(-10, 10)
    y = fit.GaussianModel.func(x, 500.0, 2.0, 0.0, 0.0)
    obj.set_xydata(x, y)
    return obj


def create_test_image1(shape=None):
    """Create test image (sin(x)+cos(y))"""
    if shape is None:
        shape = (2000, 2000)
    return create_image("sin(x)+cos(y)", create_test_2d_data(shape, dtype=np.uint16))


# TODO: Define shape objects: Circle, Rectangle, CustomXXX
# Serialization: --> ("ClassName", param1, param2, ...)
# create_image parameters: (circles, rectangles, ...) ==> (objects=(obj1, obj2, ...))
def create_test_image2(shape=None, with_metadata=True):
    """Create test image (2D noisy gaussian)"""
    title = "2D Gaussian"
    data = create_noisy_2d_gaussian(shape, dtype=np.uint16, x0=2.0, y0=3.0)
    if with_metadata:
        return create_image(
            title,
            data,
            circles=(
                ("Circle1", (100, 100, 400, 400)),
                ("Circle2", (150, 150, 350, 350)),
            ),
            rectangles=(("Rect1", (300, 200, 700, 700)),),
            segments=(("Segment", (100, 100, 400, 400)),),
            markers=(("Marker1", (500, 500)),),
        )
    return create_image(title, data)
