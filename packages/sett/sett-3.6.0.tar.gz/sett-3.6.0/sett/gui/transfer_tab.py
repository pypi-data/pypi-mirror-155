import enum
import time
from functools import partial
from typing import Iterator, Optional, Sequence

from .component import (
    TabMixin,
    PathInput,
    GuiProgress,
    get_text_input,
    MandatoryLabel,
    create_verify_dtr_checkbox,
    create_verify_filename_checkbox,
    ToolBar,
    LineEdit,
    grid_layout,
    vbox_layout,
    hbox_layout,
)
from .file_selection_widget import ArchiveOnlyFileSelectionWidget
from .pyside import QtCore, QtGui, QtWidgets, QAction, open_window
from .ui_model_bind import (
    bind,
    TextControl,
    OptionalTextControl,
    OptionalPasswordControl,
    OptionalPathControl,
)
from .model import new_sftp_connection, AppData
from .. import protocols
from ..core.error import UserError
from ..protocols.liquid_files import Protocol as LiquidFiles
from ..protocols.s3 import Protocol as S3
from ..protocols.sftp import Protocol as Sftp
from ..utils.config import ConnectionStore
from ..workflows import transfer


class TransferTab(TabMixin):
    """Class that creates the "Transfer" Tab of the GUI application."""

    def __init__(self, parent: QtWidgets.QMainWindow, app_data: AppData):
        super().__init__(parent=parent)
        self.app_data = app_data
        self.connections_model = QtCore.QStringListModel()
        files_panel = self.create_files_panel()
        verify_dtr_group = QtWidgets.QGroupBox()
        vbox_layout(
            create_verify_dtr_checkbox(self.app_data, "transfer_verify_dtr"),
            create_verify_filename_checkbox(
                self.app_data, "transfer_verify_package_name"
            ),
            parent=verify_dtr_group,
        )

        options_panel = self.create_options_panel()
        self.create_run_panel("Transfer data", self.transfer, "Transfer selected files")
        self.app_data.add_listener("transfer_files", self._enable_buttons)
        self.create_console()
        self.create_progress_bar()

        vbox_layout(
            files_panel,
            verify_dtr_group,
            options_panel,
            self.run_panel,
            self.console,
            self.progress_bar,
            parent=self,
        )

    def _enable_buttons(self) -> None:
        self.set_buttons_enabled(len(self.app_data.transfer_files) > 0)

    def create_files_panel(self) -> QtWidgets.QGroupBox:
        box = ArchiveOnlyFileSelectionWidget(
            title="Encrypted files to transfer", parent=self
        )
        box.file_list_model.layoutChanged.connect(  # type: ignore
            lambda: setattr(self.app_data, "transfer_files", box.get_list())
        )
        return box

    def create_sftp_options_panel(self) -> QtWidgets.QGroupBox:
        sftp_args = self.app_data.transfer_protocol_args[Sftp]
        text_username = LineEdit()
        text_username.setStatusTip("Username on the SFTP server")
        bind(sftp_args, "username", text_username, TextControl)

        text_destination_dir = LineEdit()
        text_destination_dir.setStatusTip(
            "Relative or absolute path to the "
            "destination directory on the SFTP "
            "server"
        )
        bind(sftp_args, "destination_dir", text_destination_dir, TextControl)

        text_host = LineEdit()
        text_host.setStatusTip("URL of the SFTP server with an optional port number")
        bind(sftp_args, "host", text_host, TextControl)

        text_jumphost = LineEdit()
        text_jumphost.setStatusTip("(optional) URL of the jumphost server")
        bind(sftp_args, "jumphost", text_jumphost, OptionalTextControl)

        pkey_location = PathInput(directory=False, path=None)
        pkey_location.setStatusTip(
            "Path to the private SSH key used for authentication"
        )
        bind(sftp_args, "pkey", pkey_location, OptionalPathControl)

        pkey_password = LineEdit()
        pkey_password.setStatusTip("Passphrase for the SSH private key")
        pkey_password.setEchoMode(QtWidgets.QLineEdit.Password)
        bind(sftp_args, "pkey_password", pkey_password, OptionalPasswordControl)

        box = QtWidgets.QGroupBox()
        box.setFlat(True)
        grid_layout(
            (MandatoryLabel("User name"), text_username),
            (MandatoryLabel("Host URL"), text_host),
            (QtWidgets.QLabel("Jumphost URL"), text_jumphost),
            (MandatoryLabel("Destination directory"), text_destination_dir),
            (
                QtWidgets.QLabel("SSH key location"),
                pkey_location.text,
                pkey_location.btn,
                pkey_location.btn_clear,
            ),
            (QtWidgets.QLabel("SSH key password"), pkey_password),
            parent=box,
        )
        return box

    def create_liquidfiles_options_panel(self) -> QtWidgets.QGroupBox:
        lf_args = self.app_data.transfer_protocol_args[LiquidFiles]

        text_host = LineEdit()
        bind(lf_args, "host", text_host, TextControl)

        text_api_key = LineEdit()
        bind(lf_args, "api_key", text_api_key, TextControl)

        box = QtWidgets.QGroupBox()
        box.setFlat(True)
        grid_layout(
            (MandatoryLabel("Host URL"), text_host),
            (MandatoryLabel("API Key"), text_api_key),
            parent=box,
        )
        return box

    def create_s3_options_panel(self) -> QtWidgets.QGroupBox:
        s3_args = self.app_data.transfer_protocol_args[S3]

        text_host = LineEdit()
        bind(s3_args, "host", text_host, TextControl)

        text_bucket = LineEdit()
        bind(s3_args, "bucket", text_bucket, TextControl)

        text_access_key = LineEdit()
        bind(s3_args, "access_key", text_access_key, TextControl)

        text_secret_key = LineEdit()
        text_secret_key.setEchoMode(QtWidgets.QLineEdit.Password)
        bind(s3_args, "secret_key", text_secret_key, OptionalPasswordControl)

        box = QtWidgets.QGroupBox()
        box.setFlat(True)
        grid_layout(
            (MandatoryLabel("Host URL"), text_host),
            (MandatoryLabel("Bucket"), text_bucket),
            (MandatoryLabel("Access Key"), text_access_key),
            (MandatoryLabel("Secret Key"), text_secret_key),
            parent=box,
        )
        return box

    def create_conn_actions(
        self, connections_selection: QtWidgets.QComboBox
    ) -> Iterator[QAction]:
        connection_store = ConnectionStore()

        def confirm(text: str) -> bool:
            dialog = QtWidgets.QMessageBox(parent=self)
            dialog.setWindowTitle("Connection profile")
            dialog.setText(text)
            dialog.setStandardButtons(
                QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel
            )
            dialog.setDefaultButton(QtWidgets.QMessageBox.Cancel)
            return bool(open_window(dialog) == QtWidgets.QMessageBox.Ok)

        def rename() -> None:
            label_old = connections_selection.currentText()
            dialog = ConnectionDialog(
                parent=self,
                label=f"Rename connection profile '{label_old}' to:",
                forbidden=self.connections_model.stringList(),
                default_input=label_old,
            )
            if open_window(dialog):
                label_new = dialog.text_field.text()
                self.app_data.config.connections[
                    label_new
                ] = self.app_data.config.connections.pop(label_old)
                try:
                    connection_store.rename(old=label_old, new=label_new)
                except UserError:
                    # Connection profile is not saved in the config file.
                    pass
                self.connections_model.setStringList(
                    sorted(
                        label_new if x == label_old else x
                        for x in self.connections_model.stringList()
                    )
                )
                connections_selection.setCurrentText(label_new)

        def add() -> None:
            dialog = ConnectionDialog(
                parent=self,
                label="New connection profile label:",
                forbidden=self.connections_model.stringList(),
            )
            if open_window(dialog):
                label = dialog.text_field.text()
                self.app_data.config.connections[label] = new_sftp_connection()
                self.connections_model.setStringList(
                    sorted(self.connections_model.stringList() + [label])
                )
                connections_selection.setCurrentText(label)

        def delete() -> None:
            label = connections_selection.currentText()
            if confirm(f"Do you want to delete '{label}' profile?"):
                self.app_data.config.connections.pop(label)
                self.connections_model.removeRow(connections_selection.currentIndex())
                try:
                    connection_store.delete(label)
                except UserError:
                    # Connection profile is not saved in the config file.
                    pass

        def save() -> None:
            label = connections_selection.currentText()
            if confirm(f"Do you want to save '{label}' profile to your config file?"):
                connection = self.app_data.transfer_protocol_args[
                    self.app_data.transfer_protocol_type
                ].target
                self.app_data.config.connections[label] = connection
                connection_store.save(label, connection)

        def set_btn_enabled(btn: QtWidgets.QAbstractButton, text: str) -> None:
            btn.setEnabled(bool(text))

        for tip, fn, needs_selection, icon in (
            ("Create a new connection profile", add, False, "plus-square"),
            ("Rename the current connection profile", rename, True, "edit"),
            ("Delete the current connection profile", delete, True, "trash-2"),
            ("Save the current connection profile", save, True, "save"),
        ):
            action = QAction(QtGui.QIcon(f":icon/feather/{icon}.png"), tip, self)
            action.triggered.connect(fn)  # type: ignore
            if needs_selection:
                connections_selection.currentTextChanged.connect(  # type: ignore
                    partial(set_btn_enabled, action)
                )
                if not connections_selection.currentText():
                    action.setEnabled(False)
            yield action

    def create_options_panel(self) -> QtWidgets.QGroupBox:
        box = QtWidgets.QGroupBox("Connection")

        connections_selection = QtWidgets.QComboBox(box)
        connections_selection.setStatusTip(
            "Select a predefined connection profile. Check documentation for details."
        )
        connections_selection.setModel(self.connections_model)
        self.connections_model.setStringList(list(self.app_data.config.connections))

        protocol_btn_grp = QtWidgets.QButtonGroup(box)
        protocol_btn_grp.addButton(QtWidgets.QRadioButton("sftp"))
        protocol_btn_grp.addButton(QtWidgets.QRadioButton("s3"))
        protocol_btn_grp.addButton(QtWidgets.QRadioButton("liquid_files"))
        get_btn_from_group(protocol_btn_grp, "sftp").setChecked(True)

        protocol_boxes = {
            "sftp": self.create_sftp_options_panel(),
            "s3": self.create_s3_options_panel(),
            "liquid_files": self.create_liquidfiles_options_panel(),
        }
        protocol_boxes["s3"].hide()
        protocol_boxes["liquid_files"].hide()

        def load_connection() -> None:
            connection = self.app_data.config.connections.get(
                connections_selection.currentText()
            )
            if not connection:
                return
            protocol = protocols.protocol_name[type(connection)]
            get_btn_from_group(protocol_btn_grp, protocol).click()
            self.app_data.transfer_protocol_args[
                self.app_data.transfer_protocol_type
            ].target = connection

        connections_selection.currentTextChanged.connect(load_connection)  # type: ignore

        def toggle_protocol(btn: QtWidgets.QRadioButton, state: bool) -> None:
            if state:
                self.app_data.transfer_protocol_type = protocols.parse_protocol(
                    btn.text()
                )
            protocol_boxes[btn.text()].setVisible(state)

        protocol_btn_grp.buttonToggled.connect(toggle_protocol)  # type: ignore

        toolbar = ToolBar("Options", self)
        for action in self.create_conn_actions(connections_selection):
            toolbar.addAction(action)
        layout_connection = hbox_layout(connections_selection, toolbar)
        layout_protocol_buttons = hbox_layout(*protocol_btn_grp.buttons())

        layout_protocol = vbox_layout(layout_protocol_buttons, *protocol_boxes.values())
        vbox_layout(layout_connection, layout_protocol, parent=box)
        load_connection()
        return box

    def transfer(self, dry_run: bool = False) -> None:
        second_factor = None

        class Msg(enum.Enum):
            code = enum.auto()

        class MsgSignal(QtCore.QObject):
            msg = QtCore.Signal(object)

        msg_signal = MsgSignal()

        def second_factor_callback() -> None:
            msg_signal.msg.emit(Msg.code)
            time_start = time.time()
            timeout = 120
            while time.time() - time_start < timeout:
                time.sleep(1)
                if second_factor is not None:
                    break
            return second_factor

        def show_second_factor_dialog(msg: str) -> None:
            """Show a pop-up where the user can enter the verification code
            for their second factor authentication.
            """
            nonlocal second_factor
            second_factor = None
            if msg == str(Msg.code):
                output = get_text_input(self, "Verification code")
                second_factor = "" if output is None else output

        protocol = self.app_data.transfer_protocol_args[
            self.app_data.transfer_protocol_type
        ].target

        msg_signal.msg.connect(show_second_factor_dialog)
        self.run_workflow_thread(
            transfer.transfer,
            f_kwargs=dict(
                files=self.app_data.transfer_files,
                protocol=protocol,
                config=self.app_data.config,
                dry_run=dry_run,
                verify_dtr=self.app_data.transfer_verify_dtr,
                verify_pkg_name=self.app_data.transfer_verify_package_name,
                pkg_name_suffix=self.app_data.encrypt_package_name_suffix,
                progress=GuiProgress(self.progress_bar.setValue),
                two_factor_callback=second_factor_callback,
            ),
            capture_loggers=(
                transfer.logger,
                protocols.sftp.logger,
                protocols.s3.logger,
            ),
            ignore_exceptions=True,
            report_config=self.app_data.config,
        )


class ConnectionDialog(QtWidgets.QDialog):
    def __init__(
        self,
        parent: Optional[QtWidgets.QWidget],
        label: str,
        forbidden: Sequence[str] = (),
        default_input: str = "",
    ):
        super().__init__(parent=parent)
        self.setWindowTitle("Connection profile")
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)

        btn_box = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        )
        btn_box.accepted.connect(self.accept)  # type: ignore
        btn_box.rejected.connect(self.reject)  # type: ignore

        self.text_field = LineEdit()
        self.text_field.setValidator(
            QtGui.QRegularExpressionValidator(QtCore.QRegularExpression(r"[\w\-@]+"))
        )
        self.text_field.setText(default_input)

        def set_ok_enabled(text: str) -> None:
            btn_box.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(
                len(text) > 0 and text not in forbidden
            )

        set_ok_enabled(self.text_field.text())
        self.text_field.textChanged.connect(set_ok_enabled)  # type: ignore

        self.setLayout(vbox_layout(QtWidgets.QLabel(label), self.text_field, btn_box))


def get_btn_from_group(
    btn_grp: QtWidgets.QButtonGroup, text: str
) -> QtWidgets.QAbstractButton:
    btn = next(x for x in btn_grp.buttons() if x.text() == text)
    if not btn:
        raise KeyError(f"No button matching '{text}' found in the group.")
    return btn
