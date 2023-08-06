#!/usr/bin/env python3
"""Secure Encryption and Transfer Tool GUI."""

import sys
from typing import Any

from . import main_window
from .. import APP_NAME_SHORT, __version__
from .pyside import QtGui, QtWidgets, open_window

# Note: rc_icon is used implicitly by PySide. It must be imported into the
# namespace, even if never used, otherwise the icons don't display in the GUI.
from .resources import rc_icons  # pylint: disable=unused-import
from ..utils.log import log_to_rotating_file


def run() -> Any:
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName(APP_NAME_SHORT)
    app.setApplicationDisplayName(f"{APP_NAME_SHORT} ({__version__})")
    app.setApplicationVersion(__version__)
    app.setWindowIcon(QtGui.QIcon(":icon/sett_icon.png"))
    window = main_window.MainWindow()
    log_to_rotating_file(
        log_dir=window.app_data.config.log_dir,
        file_max_number=window.app_data.config.log_max_file_number,
    )
    window.show()
    return open_window(app)


if __name__ == "__main__":
    run()
