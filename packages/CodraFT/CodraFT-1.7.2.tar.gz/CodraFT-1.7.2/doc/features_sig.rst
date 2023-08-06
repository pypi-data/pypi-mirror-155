Signal processing features
==========================

.. figure:: /images/shots/s_simple_example.png

    Simple example


"File" menu
-----------

.. image:: /images/shots/s_file.png

New signal
    |createfrom| various models:

    .. list-table::
        :header-rows: 1
        :widths: 20, 80

        * - Model
          - Equation
        * - Zeros
          - :math:`y[i] = 0`
        * - Random
          - :math:`y[i] \in [-0.5, 0.5]`
        * - Gaussian
          - :math:`y = y_{0}+\dfrac{A}{\sqrt{2*\pi}.\sigma}.exp(-\dfrac{1}{2}.(\dfrac{x-x_{0}}{\sigma})^2)`
        * - Lorentzian
          - :math:`y = y_{0}+\dfrac{A}{\sigma.\pi}.\dfrac{1}{1+(\dfrac{x-x_{0}}{\sigma})^2}`
        * - Voigt
          - :math:`y = y_{0}+A.\dfrac{Re(exp(-z^2).erfc(-j.z))}{\sqrt{2*\pi}.\sigma}` with :math:`z = \dfrac{x-x_{0}-j.\sigma}{\sqrt{2}.\sigma}`

Open signal
    |createfrom| the following supported filetypes:

    .. list-table::
        :header-rows: 1

        * - File type
          - Extensions
        * - Text files
          - .txt, .csv
        * - NumPy arrays
          - .npy

Save signal
    Save current signal to the following supported filetypes:

    .. list-table::
        :header-rows: 1

        * - File type
          - Extensions
        * - Text files
          - .csv

Open HDF5 file
    Import data from a HDF5 file using the :ref:`h5browser`.

Save to HDF5 file
    Export the whole CodraFT session (all signals and images) into a HDF5 file.

------------

"Edit" menu
-----------

.. image:: /images/shots/s_edit.png

Duplicate
    |create| identical to the currently selected object.

Remove
    Remove currently selected signal.

Delete object metadata
    Delete metadata from currently selected signal.
    Metadata contains additionnal information such as Region of Interest
    or results of computations

Delete all
    Delete all signals.

------------

"Operation" menu
----------------

.. image:: /images/shots/s_operation.png

Sum
    |create| the sum |ofallobj|:

    :math:`y_{M} = \sum_{k=0}^{M-1}{y_{k}}`

Average
    |create| the average |ofallobj|:

    :math:`y_{M} = \dfrac{1}{M}\sum_{k=0}^{M-1}{y_{k}}`

Difference
    |create| the difference |ofalltwo|:

    :math:`y_{2} = y_{1} - y_{0}`

Product
    |create| the product |ofallobj|:

    :math:`y_{M} = \prod_{k=0}^{M-1}{y_{k}}`

Division
    |create| the division |ofalltwo|:

    :math:`y_{2} = \dfrac{y_{1}}{y_{0}}`

Absolute value
    |create| the absolute value |ofeachobj|:

    :math:`y_{k} = |y_{k-1}|`

Log10(y)
    |create| the base 10 logarithm |ofeachobj|:

    :math:`z_{k} = \log_{10}(z_{k-1})`

Peak detection
    |createfrom| semi-automatic peak detection |ofeachobj|.

    .. figure:: /images/shots/s_peak_detection.png

        Peak detection dialog: threshold is adjustable by moving the
        horizontal marker, peaks are detected automatically (see vertical
        markers with labels indicating peak position)

ROI extraction
    |createfrom| a user-defined Region of Interest (ROI).

    .. figure:: /images/shots/s_roi_extraction.png

        ROI extraction dialog: the ROI is defined by moving the position
        and adjusting the width of an horizontal range.

Swap X/Y axes
    |create| the result of swapping X/Y data.

------------

"Processing" menu
-----------------

.. image:: /images/shots/s_processing.png

Normalize
    |create| the normalization |ofeachobj|
    by maximum, amplitude, sum or energy:

    .. list-table::
        :header-rows: 1
        :widths: 25, 75

        * - Parameter
          - Normalization
        * - Maximum
          - :math:`y_{1}= \dfrac{y_{0}}{max(y_{0})}`
        * - Amplitude
          - :math:`y_{1}= \dfrac{y_{0}'}{max(y_{0}')}` with :math:`y_{0}'=y_{0}-min(y_{0})`
        * - Sum
          - :math:`y_{1}= \dfrac{y_{0}}{\sum_{n=0}^{N}y_{0}[n]}`
        * - Energy
          - :math:`y_{1}= \dfrac{y_{0}}{\sum_{n=0}^{N}|y_{0}[n]|^2}`

Derivative
    |create| the derivative |ofeachobj|.

Integral
    |create| the integral |ofeachobj|.

Linear calibration
    |create| a linear calibration |ofeachobj| with respect to X or Y axis:

    .. list-table::
        :header-rows: 1
        :widths: 40, 60

        * - Parameter
          - Linear calibration
        * - X-axis
          - :math:`x_{1} = a.x_{0} + b`
        * - Y-axis
          - :math:`y_{1} = a.y_{0} + b`

Lorentzian filter
    Compute 1D-Lorentzian filter |ofeachobj|
    (implementation based on `scipy.ndimage.gaussian_filter1d <https://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.gaussian_filter1d.html>`_).

Moving average
    Compute moving average on :math:`M`
    points |ofeachobj|, without border effect:
    :math:`y_{1}[i]=\dfrac{1}{M}\sum_{j=0}^{M-1}y_{0}[i+j]`

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

Lorentzian, Lorentzian, Voigt, Polynomial and Multi-Gaussian fit
    Open an interactive curve fitting tool in a modal dialog box.

    .. list-table::
        :header-rows: 1
        :widths: 20, 80

        * - Model
          - Equation
        * - Gaussian
          - :math:`y = y_{0}+\dfrac{A}{\sqrt{2*\pi}.\sigma}.exp(-\dfrac{1}{2}.(\dfrac{x-x_{0}}{\sigma})^2)`
        * - Lorentzian
          - :math:`y = y_{0}+\dfrac{A}{\sigma.\pi}.\dfrac{1}{1+(\dfrac{x-x_{0}}{\sigma})^2}`
        * - Voigt
          - :math:`y = y_{0}+A.\dfrac{Re(exp(-z^2).erfc(-j.z))}{\sqrt{2*\pi}.\sigma}` with :math:`z = \dfrac{x-x_{0}-j.\sigma}{\sqrt{2}.\sigma}`
        * - Multi-Gaussian
          - :math:`y = y_{0}+\sum_{i=0}^{K}\dfrac{A_{i}}{\sqrt{2*\pi}.\sigma_{i}}.exp(-\dfrac{1}{2}.(\dfrac{x-x_{0,i}}{\sigma_{i}})^2)`

------------

"Computing" menu
----------------

.. image:: /images/shots/s_computing.png

Define ROI
    Open a dialog box to setup a Region Of Interest (ROI).
    ROI is stored as metadata, and thus attached to signal.

    .. figure:: /images/shots/s_roi_definition.png

        ROI definition dialog: the ROI is defined by moving the position
        and adjusting the width of an horizontal range.

    .. figure:: /images/shots/s_roi_signal.png

        A signal with an ROI.

Full width at half-maximum
    Fit data to a Gaussian, Lorentzian or Voigt model using
    least-square method.
    Then, compute the full width at half-maximum value.

    .. figure:: /images/shots/s_fwhm.png

        The computed result is displayed as an annotated segment.

Full width at 1/e²
    Fit data to a Lorentzian model using least-square method.
    Then, compute the full width at 1/e².

.. note:: Computed scalar results are systematically stored as metadata.
    Metadata is attached to signal and serialized with it when exporting
    current session in a HDF5 file.

------------

"View" menu
-----------

.. image:: /images/shots/s_view.png

View in a new window
    Open a new window to visualize the selected signals.

Other menu entries
    Show/hide panels or toolbars.

------------

"?" menu
--------

.. image:: /images/shots/s_help.png

Online documentation
    Open the online documentation (english only):

    .. image:: /images/shots/doc_online.png

CHM documentation
    Open the CHM documentation (french/english and Windows only):

    .. image:: /images/shots/doc_chm.png

About
    Open the "About CodraFT" dialog box:

    .. image:: /images/shots/about.png

.. ==========================================================
.. Text substitutions:
.. |create| replace:: Create a new signal which is
.. |createfrom| replace:: Create a new signal from
.. |ofeachobj| replace:: of each selected signal
.. |ofallobj| replace:: of all selected signals
.. |ofalltwo| replace:: of the **two** selected signals
