import os
from typing import Optional, Union, Any

try:
    if os.environ.get("SETT_LEGACY", "") == "true":
        raise ImportError("Enforce legacy mode")  # pylint: disable=misplaced-bare-raise
    from PySide6 import QtCore as _QtCore
    from PySide6 import QtGui as _QtGui
    from PySide6 import QtWidgets as _QtWidgets
    from PySide6.QtGui import QAction as _QAction

    # Re-exports
    QtCore = _QtCore
    QtGui = _QtGui
    QtWidgets = _QtWidgets
    QAction = _QAction

    def open_window(
        window: Union[QtWidgets.QApplication, QtWidgets.QMessageBox, QtWidgets.QDialog]
    ) -> Any:
        return window.exec()

    def get_application_global_instance() -> Optional[QtCore.QCoreApplication]:
        return QtWidgets.QApplication.instance()

except ImportError:
    # If PySide6 is absent from the system, fall back on PySide2.
    from PySide2 import QtCore as _QtCore_PySide2
    from PySide2 import QtGui as _QtGui_PySide2
    from PySide2 import QtWidgets as _QtWidgets_PySide2
    from PySide2.QtWidgets import QAction as _QAction_PySide2

    # Re-exports.
    QtCore = _QtCore_PySide2  # type: ignore
    QtGui = _QtGui_PySide2  # type: ignore
    QtWidgets = _QtWidgets_PySide2  # type: ignore
    QAction = _QAction_PySide2  # type: ignore

    def open_window(
        window: Union[QtWidgets.QApplication, QtWidgets.QMessageBox, QtWidgets.QDialog]
    ) -> Any:
        return window.exec_()

    def get_application_global_instance() -> Optional[QtCore.QCoreApplication]:
        return QtWidgets.QApplication.instance()
