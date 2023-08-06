# -*- coding: utf-8 -*-
#
# Licensed under the terms of the CECILL License
# (see codraft/__init__.py for details)

"""
Application embedded test 1

CodraFT main window is destroyed when closing application.
It is rebuilt from scratch when reopening application.
"""

from qtpy.QtCore import Qt
from qtpy.QtWidgets import QMainWindow, QPushButton

from codraft.config import _
from codraft.core.gui.main import CodraFTMainWindow
from codraft.utils.qthelpers import qt_app_context

SHOW = True  # Show test in GUI-based test launcher


class BaseMainView(QMainWindow):
    """Main window"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle(_("Host Qt main window"))
        self.codraft = None
        btn = QPushButton(_("Open CodraFT"))
        btn.clicked.connect(self.open_codraft)
        self.setCentralWidget(btn)
        self.resize(300, 40)

    def open_codraft(self):
        """Open CodraFT test"""
        raise NotImplementedError


class MainView(BaseMainView):
    """Test main view"""

    def open_codraft(self):
        """Open CodraFT test"""
        if self.codraft is None:
            self.codraft = CodraFTMainWindow(console=False)
            self.codraft.setAttribute(Qt.WA_DeleteOnClose, True)
            self.codraft.show()
        else:
            try:
                self.codraft.show()
                self.codraft.raise_()
            except RuntimeError:
                self.codraft = None
                self.open_codraft()


def test_embedded_feature(klass):
    """Testing embedded feature"""
    with qt_app_context() as app:
        window = klass()
        window.show()
        app.exec()


if __name__ == "__main__":
    test_embedded_feature(MainView)
