import warnings
from typing import Callable

from sett import (
    APP_NAME_LONG,
    URL_READTHEDOCS,
    URL_GITLAB_ISSUES,
    APP_NAME_SHORT,
    __version__,
    URL_GITLAB,
    VERSION_WITH_DEPS,
)
from .component import show_warning, is_macos
from .decrypt_tab import DecryptTab
from .encrypt_tab import EncryptTab
from .keys_tab import KeysTab
from .model import AppData
from .parallel import run_thread
from .pyside import QAction, QtCore, QtGui, QtWidgets, open_window
from .settings_tab import SettingsTab
from .transfer_tab import TransferTab
from ..core.versioncheck import check_version
from ..utils.config import Config, load_config, save_config, config_to_dict

QtCore.QThreadPool.globalInstance().setExpiryTimeout(-1)


class MainWindow(QtWidgets.QMainWindow):
    """Class that initializes the main QtWidget (window) of the application,
    onto which all other components will be added.
    """

    def __init__(self) -> None:
        super().__init__()
        self.app_data = AppData(config=self.load_config_from_disk())
        self.setWindowTitle(APP_NAME_LONG)
        self.add_menu()
        self.add_tabs()
        self.add_status_bar()
        self.check_version()

    def load_config_from_disk(self) -> Config:
        """Load user config settings from the default config file."""
        with warnings.catch_warnings(record=True) as w:
            config = load_config()
            if w:
                show_warning(
                    "Configuration Error",
                    "\n".join(format(warning.message) for warning in w),
                    self,
                )
        return config

    def add_tabs(self) -> None:
        # FIXME: tab_keys is created first to populate gpg keys.
        tab_keys = KeysTab(parent=self, app_data=self.app_data)
        tab_encrypt = EncryptTab(parent=self, app_data=self.app_data)
        tab_decrypt = DecryptTab(parent=self, app_data=self.app_data)
        tab_transfer = TransferTab(parent=self, app_data=self.app_data)
        tab_settings = SettingsTab(parent=self, app_data=self.app_data)

        tabs = QtWidgets.QTabWidget()
        tabs.addTab(tab_encrypt, QtGui.QIcon(":icon/feather/lock.png"), "&Encrypt")
        tabs.addTab(tab_transfer, QtGui.QIcon(":icon/feather/send.png"), "&Transfer")
        tabs.addTab(tab_decrypt, QtGui.QIcon(":icon/feather/unlock.png"), "&Decrypt")
        tabs.addTab(tab_keys, QtGui.QIcon(":icon/feather/key.png"), "&Keys")
        tabs.addTab(
            tab_settings, QtGui.QIcon(":icon/feather/settings.png"), "&Settings"
        )

        self.setCentralWidget(tabs)

    def add_status_bar(self) -> None:
        self.status = QtWidgets.QStatusBar()
        self.setStatusBar(self.status)

    def add_menu(self) -> None:
        action_exit = QAction(QtGui.QIcon(":icon/feather/log-out.png"), "&Exit", self)
        action_exit.setShortcut(QtGui.QKeySequence("Ctrl+Q"))
        action_exit.setStatusTip("Exit application")
        action_exit.triggered.connect(self.close)  # type: ignore

        menu = self.menuBar()
        menu.setNativeMenuBar(not is_macos())
        menu_file = menu.addMenu("&File")
        menu_file.addAction(action_exit)

        action_help = QAction(
            QtGui.QIcon(":icon/feather/book-open.png"), "&Documentation", self
        )
        action_help.setStatusTip("Open online documentation")
        action_help.setShortcut(QtGui.QKeySequence(QtGui.QKeySequence.HelpContents))
        action_help.triggered.connect(open_url(URL_READTHEDOCS))  # type: ignore

        action_bug_report = QAction(
            QtGui.QIcon(":icon/feather/alert-triangle.png"), "&Report an Issue", self
        )
        action_bug_report.setStatusTip("Open online bug report form")
        action_bug_report.triggered.connect(open_url(URL_GITLAB_ISSUES))  # type: ignore

        action_about = QAction(QtGui.QIcon(":icon/feather/info.png"), "&About", self)
        action_about.setStatusTip("Show info about application")
        action_about.triggered.connect(self.show_about)  # type: ignore

        menu_help = menu.addMenu("&Help")
        menu_help.addAction(action_help)
        menu_help.addAction(action_bug_report)
        menu_help.addAction(action_about)

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        """Code that is run when the application is closed by the user."""

        # Compare the current in-memory config values to those present on disk
        # (in the user's config file). If they differ, ask the user whether
        # they want to save their config value modifications to disk.
        if self.app_data.config != self.load_config_from_disk():
            reply = QtWidgets.QMessageBox.question(
                self,
                "Persist changed settings?",
                "You made changes to settings you did not persist yet.\n"
                "Do you want to permanently persist them to your sett "
                "configuration file?",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                QtWidgets.QMessageBox.No,
            )
            if reply == QtWidgets.QMessageBox.Yes:
                save_config(config_to_dict(self.app_data.config))

        if self.app_data.config.gui_quit_confirmation:
            reply = QtWidgets.QMessageBox.question(
                self,
                "Quit",
                "Do you really want to quit?",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                QtWidgets.QMessageBox.No,
            )
            if reply == QtWidgets.QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()

    def check_version(self) -> None:
        if self.app_data.config.offline or not self.app_data.config.check_version:
            return

        def get_warnings() -> str:
            with warnings.catch_warnings(record=True) as w:
                check_version(self.app_data.config.repo_url, gui_formatting=True)
                return "\n".join(format(warning.message) for warning in w)

        run_thread(
            get_warnings,
            f_kwargs={},
            report_config=self.app_data.config,
            signals=dict(
                result=lambda x: show_warning("Version check", x, self) if x else x
            ),
        )

    def show_about(self) -> None:
        msg = QtWidgets.QMessageBox(parent=self)
        msg.setWindowTitle("About")
        msg.setIconPixmap(QtGui.QPixmap(":icon/biomedit_logo.png"))
        msg.setTextFormat(QtCore.Qt.RichText)
        msg.setText(
            f"{APP_NAME_LONG}<br>"
            f"{VERSION_WITH_DEPS}<br><br>"
            f"For documentation go to "
            f"<a href='{URL_READTHEDOCS}'>{URL_READTHEDOCS}</a><br>"
            f"To report an issue go to "
            f"<a href='{URL_GITLAB_ISSUES}'>{URL_GITLAB_ISSUES}</a><br>"
            f"Source code is available at "
            f"<a href='{URL_GITLAB}'>{URL_GITLAB}</a><br><br>"
            f"{APP_NAME_SHORT} is developed as part of the "
            f"<a href='https://www.biomedit.ch/'>BioMedIT "
            f"project</a>"
        )
        msg.show()


def open_url(url: str) -> Callable[[], None]:
    """Returns a function that will open the specified URL in the user's
    default browser when called. The returned function has no arguments.

    :param url: URL to open.
    :returns: function that opens the specified URL.
    """

    def open_url_template() -> None:
        if not QtGui.QDesktopServices.openUrl(QtCore.QUrl(url)):
            msg_warn = QtWidgets.QMessageBox()
            msg_warn.setWindowTitle("Warning")
            msg_warn.setText(f"Unable to open URL at \n{url}.")
            msg_warn.setIcon(QtWidgets.QMessageBox.Warning)
            open_window(msg_warn)

    return open_url_template
