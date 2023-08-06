Image processing features
=========================

.. figure:: /images/shots/i_simple_example.png

    Simple example

"File" menu
-----------

.. image:: /images/shots/i_file.png

New image
    |createfrom| various models
    (supported datatypes: uint8, uint16, float32, float64):

    .. list-table::
        :header-rows: 1
        :widths: 20, 80

        * - Model
          - Equation
        * - Zeros
          - :math:`z[i] = 0`
        * - Empty
          - Data is directly taken from memory as it is
        * - Random
          - :math:`z[i] \in [0, z_{max})` where :math:`z_{max}` is the datatype maximum value
        * - 2D Gaussian
          - :math:`z = A.exp(-\dfrac{(\sqrt{(x-x0)^2+(y-y0)^2}-\mu)^2}{2\sigma^2})`

Open image
    |createfrom| the following supported filetypes:

    .. list-table::
        :header-rows: 1

        * - File type
          - Extensions
        * - PNG files
          - .png
        * - TIFF files
          - .tif, .tiff
        * - 8-bit images
          - .jpg, .gif
        * - NumPy arrays
          - .npy
        * - Text files
          - .txt, .csv, .asc
        * - Andor SIF files
          - .sif
        * - SPIRICON files
          - .scor-data
        * - FXD files
          - .fxd
        * - Bitmap images
          - .bmp

Save image
    Save current image (see "Open image" supported filetypes).

"Edit" menu
-----------

.. image:: /images/shots/i_edit.png

Duplicate
    |create| identical to the currently selected object.

Remove
    Remove currently selected image.

Delete object metadata
    Delete metadata from currently selected image.
    Metadata contains additionnal information such as Region of Interest
    or results of computations

Delete all
    Delete all images.

"Operation" menu
----------------

.. image:: /images/shots/i_operation.png

Sum
    |create| the sum |ofallobj|:

    :math:`z_{M} = \sum_{k=0}^{M-1}{z_{k}}`

Average
    |create| the average |ofallobj|:

    :math:`z_{M} = \dfrac{1}{M}\sum_{k=0}^{M-1}{z_{k}}`

Difference
    |create| the difference |ofalltwo|:

    :math:`z_{2} = z_{1} - z_{0}`

Product
    |create| the product |ofallobj|:

    :math:`z_{M} = \prod_{k=0}^{M-1}{z_{k}}`

Division
    |create| the division |ofalltwo|:

    :math:`z_{2} = \dfrac{z_{1}}{z_{0}}`

Absolute value
    |create| the absolute value |ofeachobj|:

    :math:`z_{k} = |z_{k-1}|`

Log10(z)
    |create| the base 10 logarithm |ofeachobj|:

    :math:`z_{k} = \log_{10}(z_{k-1})`

Log10(z+n)
    |create| the Log10(z+n) |ofeachobj| (avoid Log10(0) on image background):

    :math:`z_{k} = \log_{10}(z_{k-1}+n)`

Flat-field correction
    |create| flat-field correction |ofalltwo|:

    :math:`z_{1} = \dfrac{z_{0}}{z_{f}}.`
    :math:`\dfrac{1}{N_{row}.N_{col}}.\sum_{i=0}^{N_{row}}\sum_{j=0}^{N_{col}}{z_{f}[i,j]}`
    where :math:`z_{0}` is the raw image
    and :math:`z_{f}` is the flat field image

    .. note::

        Raw image and flat field image are supposedly already
        corrected by performing a dark frame subtraction.

Rotation
    |create| the result of rotating (90°, 270° or arbitrary angle) or
    flipping (horizontally or vertically) data.

Resize
    |create| a resized version |ofeachobj|.

ROI extraction
    |createfrom| a user-defined Region of Interest.

    .. figure:: /images/shots/i_roi_extraction.png

        ROI extraction dialog: the ROI is defined by moving the position
        and adjusting the size of a rectangle shape.

Swap X/Y axes
    |create| the result of swapping X/Y data.

"Processing" menu
-----------------

.. image:: /images/shots/i_processing.png

Linear calibration
    |create| a linear calibration |ofeachobj| with respect to Z axis:

    .. list-table::
        :header-rows: 1
        :widths: 40, 60

        * - Parameter
          - Linear calibration
        * - Z-axis
          - :math:`z_{1} = a.z_{0} + b`

Thresholding
    Apply the thresholding to each selected image.

Clipping
    Apply the clipping to each selected image.

Moving average
    Compute moving average |ofeachobj|
    (implementation based on `scipy.ndimage.uniform_filter <https://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.uniform_filter.html>`_).

Moving median
    Compute moving median |ofeachobj|
    (implementation based on `scipy.signal.medfilt <https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.medfilt.html>`_).

Wiener filter
    Compute Wiener filter |ofeachobj|
    (implementation based on `scipy.signal.wiener <https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.wiener.html>`_).

FFT
    |create| the Fast Fourier Transform (FFT) |ofeachobj|.

Inverse FFT
    |create| the inverse FFT |ofeachobj|.


"Computing" menu
----------------

.. image:: /images/shots/i_computing.png

Define ROI
    Open a dialog box to setup a Region Of Interest (ROI).
    ROI is stored as metadata, and thus attached to image.

    .. figure:: /images/shots/i_roi_definition.png

        An image with an ROI.

Centroid
    Compute image centroid using a Fourier transform method
    (as discussed by `Weisshaar et al. <http://www.mnd-umwelttechnik.fh-wiesbaden.de/pig/weisshaar_u5.pdf>`_).
    This method is quite insensitive to background noise.

Minimum enclosing circle center
    Compute the circle contour enclosing image values above
    a threshold level defined as the FWHM.

    .. warning::
        This feature requires `OpenCV for Python <https://pypi.org/project/opencv-python/>`_.

.. note:: Computed scalar results are systematically stored as metadata.
    Metadata is attached to image and serialized with it when exporting
    current session in a HDF5 file.

"View" menu
-----------

.. image:: /images/shots/i_view.png


.. ==========================================================
.. Text substitutions:
.. |create| replace:: Create a new image which is
.. |createfrom| replace:: Create a new image from
.. |ofeachobj| replace:: of each selected image
.. |ofallobj| replace:: of all selected images
.. |ofalltwo| replace:: of the **two** selected images
