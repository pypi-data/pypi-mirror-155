# -*- coding: utf-8 -*-
#
# Licensed under the terms of the CECILL License
# (see codraft/__init__.py for details)

"""
CodraFT Visualization tools (based on guiqwt)
"""

import os.path as osp
import sys

import guiqwt.image
import guiqwt.plot
import guiqwt.tools
from guiqwt.builder import make

from codraft.config import _


def create_image_window(title=None, show_itemlist=True, show_contrast=True, tools=None):
    """Create Image Dialog"""
    if title is None:
        script_name = osp.basename(sys.argv[0])
        title = f'{_("Test dialog")} `{script_name}`'
    win = guiqwt.plot.ImageDialog(
        edit=False,
        toolbar=True,
        wintitle=title,
        options=dict(show_itemlist=show_itemlist, show_contrast=show_contrast),
    )
    if tools is None:
        tools = (
            guiqwt.tools.LabelTool,
            guiqwt.tools.VCursorTool,
            guiqwt.tools.HCursorTool,
            guiqwt.tools.XCursorTool,
            guiqwt.tools.AnnotatedRectangleTool,
            guiqwt.tools.AnnotatedCircleTool,
            guiqwt.tools.AnnotatedEllipseTool,
            guiqwt.tools.AnnotatedSegmentTool,
            guiqwt.tools.AnnotatedPointTool,
        )
    for toolklass in tools:
        win.add_tool(toolklass, switch_to_default_tool=True)
    return win


def view_image_items(
    items, title=None, show_itemlist=True, show_contrast=True, tools=None
):
    """Create an image dialog and show items"""
    win = create_image_window(
        title=title,
        show_itemlist=show_itemlist,
        show_contrast=show_contrast,
        tools=tools,
    )
    plot = win.get_plot()
    for item in items:
        plot.add_item(item)
    win.exec()


def view_images(
    data_or_datalist, title=None, show_itemlist=True, show_contrast=True, tools=None
):
    """Create an image dialog and show images"""
    if isinstance(data_or_datalist, (tuple, list)):
        datalist = data_or_datalist
    else:
        datalist = [data_or_datalist]
    items = []
    for data in datalist:
        item = make.image(data, interpolation="nearest", eliminate_outliers=0.1)
        items.append(item)
    view_image_items(
        items,
        title=title,
        show_itemlist=show_itemlist,
        show_contrast=show_contrast,
        tools=tools,
    )
