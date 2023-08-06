# -*- coding: utf-8 -*-
#
# Licensed under the terms of the CECILL License
# (see codraft/__init__.py for details)

"""
Application embedded test 2

CodraFT main window is simply hidden when closing application.
It is shown and raised above other windows when reopening application.
"""

from codraft.core.gui.main import CodraFTMainWindow
from codraft.tests import embedded1_test

SHOW = True  # Show test in GUI-based test launcher


class MainView(embedded1_test.BaseMainView):
    """Test main view"""

    def open_codraft(self):
        """Open CodraFT test"""
        if self.codraft is None:
            self.codraft = CodraFTMainWindow(console=False, hide_on_close=True)
            self.codraft.show()
        else:
            self.codraft.show()
            self.codraft.raise_()


if __name__ == "__main__":
    embedded1_test.test_embedded_feature(MainView)
