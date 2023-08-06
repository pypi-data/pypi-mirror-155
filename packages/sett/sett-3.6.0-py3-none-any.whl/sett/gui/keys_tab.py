import html
from pathlib import Path
from typing import (
    Iterable,
    Iterator,
    Optional,
    Sequence,
    Tuple,
    Callable,
    Any,
    cast,
)

from sett.core.error import UserError
from .component import (
    SelectionAction,
    SelectionButton,
    ToolBar,
    LineEdit,
    warning_callback,
    show_warning,
    grid_layout,
    GridLayoutCell,
)
from .model import AppData, KeyValueListModel
from .keys_refresh import load_authority_key_threaded
from .parallel import run_thread
from .pyside import QtCore, QtGui, QtWidgets, QAction, open_window
from ..core import crypt, gpg
from ..core.secret import Secret
from ..utils.config import Config
from ..workflows import (
    upload_keys as upload_keys_workflow,
    request_sigs as request_sigs_workflow,
)


class KeysTab(QtWidgets.QWidget):
    def __init__(self, parent: QtWidgets.QMainWindow, app_data: AppData):
        super().__init__(parent=parent)
        self.app_data = app_data

        # Update public and private key lists in AppData.
        self.update_private_keys()
        self.update_public_keys()

        # At listeners that refresh the 'Keys' tab of the GUI to reflect
        # changes in validation authority key.
        for callback in (self.update_public_keys, self.update_display_selected_pub_key):
            self.app_data.add_listener("validation_authority_key", callback)

        # Download/refresh the validation authority key.
        load_authority_key_threaded(self.app_data)

        self.text_panel = QtWidgets.QTextEdit()
        self.text_panel.setReadOnly(True)

        self.priv_keys_view = QtWidgets.QListView()
        self.priv_keys_view.setModel(self.app_data.priv_keys_model)
        self.priv_keys_view.selectionModel().currentChanged.connect(  # type: ignore
            self._update_display
        )

        self.pub_keys_view = QtWidgets.QListView()
        self.pub_keys_view.setModel(self.app_data.pub_keys_model)
        self.pub_keys_view.selectionModel().currentChanged.connect(self._update_display)  # type: ignore
        self.pub_keys_view.setSelectionMode(
            QtWidgets.QAbstractItemView.ExtendedSelection
        )

        # When item is selected in the public/private key list, clear
        # the selection in the other list.
        self.priv_keys_view.selectionModel().currentChanged.connect(  # type: ignore
            lambda: self.pub_keys_view.selectionModel().clear()
        )
        self.pub_keys_view.selectionModel().currentChanged.connect(  # type: ignore
            lambda: self.priv_keys_view.selectionModel().clear()
        )

        action_generate_key = QAction(
            QtGui.QIcon(":icon/feather/plus-square.png"),
            "Generate new private/public key",
            self,
        )
        action_generate_key.triggered.connect(lambda: KeyGenDialog(parent=self).show())  # type: ignore
        action_refresh_keys = QAction(
            QtGui.QIcon(":icon/feather/refresh-cw.png"),
            "Refresh keys from the local keyring",
            self,
        )

        def refresh_keys() -> None:
            self.update_private_keys()
            self.update_public_keys()
            self.update_display_selected_pub_key()

        action_refresh_keys.triggered.connect(refresh_keys)  # type: ignore

        toolbar = ToolBar("Key management", self)
        toolbar.addAction(action_generate_key)
        toolbar.addSeparator()
        for action in self.create_public_keys_actions():
            toolbar.addAction(action)
        toolbar.addSeparator()
        toolbar.addAction(action_refresh_keys)

        self.setLayout(
            grid_layout(
                (GridLayoutCell(toolbar, span=2),),
                (QtWidgets.QLabel("Private keys"), QtWidgets.QLabel("Public keys")),
                (self.priv_keys_view, self.pub_keys_view),
                (GridLayoutCell(self.text_panel, span=2),),
            )
        )

    def key_to_html(self, key: gpg.Key) -> str:
        """Represent a PGP key as an HTML string"""

        # Add key info (user ID, key ID, fingerprint, signatures).
        content = ["<table>"]
        rows = [
            ("User ID", html.escape(str(key.uids[0]))),
            ("Key ID", key.key_id),
            ("Key fingerprint", key.fingerprint),
            ("Key length", key.key_length),
        ]
        for k, v in rows:
            content.append(f"<tr><th>{k}</th><td>{v}</td></tr>")

        content.append("<tr><th>Signatures</th><td>")
        content.append(
            "<br>".join(
                [
                    f"{html.escape(str(sig.issuer_uid))} {sig.issuer_key_id} "
                    f"{sig.signature_class}"
                    for sig in key.valid_signatures
                ]
            )
        )
        content.append("</td></tr>")

        # Add key validation info: is the key signed or not.
        content.append("</table>")
        if key.key_type == gpg.KeyType.public:
            try:
                crypt.validate_pub_key(
                    key=key,
                    gpg_store=self.app_data.config.gpg_store,
                    signee_key=self.app_data.validation_authority_key,
                    keyserver_url=self.app_data.config.keyserver_url,
                )
                if self.app_data.validation_authority_key:
                    content.append('<p class="safe">This key has been verified</p>')
                elif self.app_data.config.key_authority_fingerprint:
                    content.append(
                        '<p class="info">This key could not be verified because the '
                        "key validation authority's key ["
                        + self.app_data.config.key_authority_fingerprint
                        + "] is not available on your machine or is invalid.</p>"
                    )
                else:
                    content.append(
                        '<p class="info">This key could not be verified because no '
                        "key validation authority is defined in the setting.</p>"
                    )
            except UserError as e:
                # Note: changing "<email>" to "[email]" in the error message
                # as the text between "< >" is not rendered.
                content.append(
                    f'<p class="danger">'
                    f"{str(e).replace('<', '[').replace('>', ']')}</p>"
                )
        else:
            content.append(
                "<p>This is a private key. Private keys cannot be signed.</p>"
            )
        return "".join(content)

    @staticmethod
    def key_to_text(key: gpg.Key) -> str:
        return f"User ID: {key.uids[0]}\nFingerprint: {key.fingerprint}"

    def create_public_keys_actions(self) -> Iterator[QAction]:
        selection_model = self.pub_keys_view.selectionModel()

        def offline_action(icon: str, tip: str, selection: bool = True) -> QAction:
            """Force disable button in offline mode."""

            icon_obj = f":icon/feather/{icon}.png"
            if self.app_data.config.offline:
                action = QAction(
                    QtGui.QIcon(icon_obj),
                    f"{tip} (not available in offline mode)",
                    self,
                )
                action.setEnabled(False)
            else:
                if selection:
                    action = SelectionAction(
                        QtGui.QIcon(icon_obj),
                        tip,
                        self,
                        selection_model=selection_model,
                    )
                else:
                    action = QAction(QtGui.QIcon(icon_obj), tip, self)
            return action

        # Create a dict of actions (functions) to associate to each
        # action button of the GUI.
        # The reason to create a dict object before looping over it is so
        # that mypy gets the correct typing information (for some reason
        # SelectionAction is not recognized as a subtype of QAction).
        functions_by_action: Sequence[Tuple[QAction, Callable[..., Any]]] = (
            (
                offline_action(
                    "download-cloud",
                    "Search and download keys from the keyserver",
                    False,
                ),
                lambda: KeyDownloadDialog(parent=self).show(),
            ),
            (
                offline_action("upload-cloud", "Upload selected keys to the keyserver"),
                self.upload_key,
            ),
            (
                offline_action("pen-tool", "Request signature for the selected keys"),
                self.send_signature_request,
            ),
            (
                offline_action("rotate-cw", "Update selected keys from the keyserver"),
                self.update_keys,
            ),
            (
                SelectionAction(
                    QtGui.QIcon(":icon/feather/trash-2.png"),
                    "Delete selected keys from your computer",
                    self,
                    selection_model=selection_model,
                ),
                self.delete_keys,
            ),
            (
                QAction(
                    QtGui.QIcon(":icon/feather/file-plus.png"),
                    "Import key from file",
                    self,
                ),
                self.import_key,
            ),
        )
        for action, fn in functions_by_action:
            action.triggered.connect(fn)  # type: ignore
            yield action

    def update_private_keys(self) -> None:
        """Retrieve/reload all private keys from the user's local keyring and
        store them in the application's memory."""
        keys_private = self.app_data.config.gpg_store.list_sec_keys()
        try:
            default_key = (
                self.app_data.config.default_sender
                or self.app_data.config.gpg_store.default_key()
            )
            self.app_data.default_key_index = next(
                index
                for index, entry in enumerate(keys_private)
                if entry.fingerprint == default_key
            )
            self.app_data.encrypt_sender = default_key
        except StopIteration:
            pass
        self.app_data.priv_keys_model.set_data(data=keys_as_tuple(keys=keys_private))

    def update_public_keys(self) -> None:
        """Retrieve/reload all public keys from the user's local keyring and
        store them in the application's memory."""
        keys_public = self.app_data.config.gpg_store.list_pub_keys(sigs=True)
        self.app_data.pub_keys_model.set_data(data=keys_as_tuple(keys=keys_public))

    def get_selected_keys(self) -> Tuple[gpg.Key, ...]:
        """Returns the gpg.Key objects corresponding to the keys currently
        selected in the GUI.
        """
        # Note: it's probably possible to get rid of the cast() here.
        selected_keys = (
            cast(KeyValueListModel, index.model()).get_value(index)
            for index in self.pub_keys_view.selectedIndexes()
        )
        return tuple(selected_keys)

    def update_keys(self) -> None:
        """Update/refresh selected keys from the keyserver."""
        show_ok = ok_message("Updated keys", "Keys have been successfully updated.")
        keys_to_update = self.get_selected_keys()
        if keys_to_update:

            def on_result() -> None:
                self.update_public_keys()
                self.update_display_selected_pub_key()
                show_ok()

            run_thread(
                crypt.download_keys,
                f_kwargs=dict(
                    fingerprints=[key.fingerprint for key in keys_to_update],
                    keyserver=self.app_data.config.keyserver_url,
                    gpg_store=self.app_data.config.gpg_store,
                ),
                report_config=self.app_data.config,
                forward_errors=warning_callback("GPG key update error"),
                signals=dict(result=on_result),
            )

    def import_key(self) -> None:
        """Import a GPG key from a local file."""
        path = QtWidgets.QFileDialog.getOpenFileName(
            self, "Select GPG key file", str(Path.home())
        )[0]
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle("GPG public key import")
        try:
            if path:
                with open(path, encoding="utf-8") as fin:
                    key_data = fin.read()
                crypt.import_keys(key_data, self.app_data.config.gpg_store)
                self.update_public_keys()
                self.update_display_selected_pub_key()
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.setText("Key has been imported.")
                open_window(msg)
        except (UnicodeDecodeError, UserError) as e:
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setText(format(e))
            open_window(msg)

    def delete_keys(self) -> None:
        """Delete the selected public keys from the user's local keyring. Only
        public keys with no associated private key can be deleted.
        """
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Question)
        msg.setWindowTitle("Delete public key")
        msg.setText("Do you really want to delete the following public key?")
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
        msg_warn = QtWidgets.QMessageBox()
        msg_warn.setWindowTitle("GPG key deletion error")
        msg_warn.setIcon(QtWidgets.QMessageBox.Warning)
        priv_keys = self.app_data.config.gpg_store.list_sec_keys()

        keys_to_delete = self.get_selected_keys()
        for key in keys_to_delete:
            if any(k for k in priv_keys if key.fingerprint == k.fingerprint):
                msg_warn.setText(
                    "Unable to delete key:\n\n"
                    f"{key.uids[0]}\n{key.fingerprint}\n\n"
                    "Deleting private keys (and by extension public keys "
                    "with an associated private key) is not supported by "
                    "this application. Please use an external software  "
                    "such as GnuPG (Linux, MacOS) or Kleopatra (Windows)."
                )
                open_window(msg_warn)
                continue
            msg.setDetailedText(self.key_to_text(key))
            if key is keys_to_delete[0]:
                click_show_details(msgbox=msg)
            status = open_window(msg)
            if status == QtWidgets.QMessageBox.Ok:
                try:
                    crypt.delete_pub_keys(
                        [key.fingerprint], self.app_data.config.gpg_store
                    )
                    self.pub_keys_view.selectionModel().clearSelection()
                except UserError as e:
                    msg_warn.setText(format(e))
                    open_window(msg_warn)
                self.text_panel.clear()
        self.update_public_keys()

    def upload_key(self) -> None:
        """Upload the selected keys to the keyserver specific in the user's
        config file.
        """
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle("Send public key")
        msg.setText("Do you want to upload the selected key to the key server?")
        msg.setIcon(QtWidgets.QMessageBox.Question)
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
        show_ok = ok_message(
            "Send public key", "Key has been successfully uploaded to the keyserver."
        )

        keys_to_upload = self.get_selected_keys()
        for key in keys_to_upload:
            msg.setDetailedText(self.key_to_text(key))
            if key is keys_to_upload[0]:
                click_show_details(msgbox=msg)
            status = open_window(msg)
            if status == QtWidgets.QMessageBox.Ok:
                run_thread(
                    upload_keys_workflow.upload_keys,
                    f_kwargs=dict(
                        key_ids=[key.fingerprint], config=self.app_data.config
                    ),
                    report_config=self.app_data.config,
                    capture_loggers=(upload_keys_workflow.logger,),
                    forward_errors=warning_callback("GPG key upload error"),
                    signals=dict(result=lambda _: show_ok()),
                )

    def send_signature_request(self) -> None:
        """Send a request to the key authority to sign the selected keys."""
        request_signature(self.get_selected_keys(), self.app_data.config, self)

    def _update_display(self, index: QtCore.QModelIndex) -> None:
        """Display key info summary in GUI text panel."""
        style = (
            "<style>"
            "th {text-align: left; padding: 0 20px 5px 0;}"
            ".danger { color: red;}"
            ".safe { color: green;}"
            "</style>"
        )
        if index.isValid():
            try:
                # Note: it's probably possible to get rid of the cast() here.
                self.text_panel.setHtml(
                    style
                    + self.key_to_html(
                        cast(KeyValueListModel, index.model()).get_value(index)
                    )
                )
            except IndexError:
                self.text_panel.setHtml("")

    def update_display_selected_pub_key(self) -> None:
        """Refresh the displayed key info of the currently selected public keys."""
        self._update_display(self.pub_keys_view.selectionModel().currentIndex())


class KeyDownloadDialog(QtWidgets.QDialog):
    def __init__(self, parent: KeysTab):
        super().__init__(parent=parent)
        self.parent_tab = parent
        self.setWindowTitle("Download public keys from keyserver")
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)

        self.search_string = LineEdit()
        self.btn_search = QtWidgets.QPushButton("Search")
        self.btn_search.clicked.connect(self.search_keys)  # type: ignore
        self.btn_search.setEnabled(False)
        self.search_string.textChanged.connect(  # type: ignore
            lambda text: self.btn_search.setEnabled(bool(text))
        )

        self.key_list_view = QtWidgets.QListView()
        key_list_model = QtCore.QStringListModel()
        self.key_list_view.setSelectionMode(
            QtWidgets.QAbstractItemView.ExtendedSelection
        )
        self.key_list_view.setModel(key_list_model)

        self.btn_download = SelectionButton(
            "Download", self.key_list_view.selectionModel()
        )
        self.btn_download.clicked.connect(self.download_selected)  # type: ignore

        self.label_results = QtWidgets.QLabel("")
        self.set_number_of_keys_found(None)

        btn_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Close)
        btn_box.rejected.connect(self.reject)  # type: ignore

        self.setLayout(
            grid_layout(
                (
                    QtWidgets.QLabel(
                        "Enter a search term (e.g. user name, email, key fingerprint)"
                    ),
                ),
                (self.search_string, self.btn_search),
                (QtWidgets.QLabel("Select a key to download"),),
                (self.key_list_view, self.btn_download),
                (self.label_results,),
                (None, btn_box),
            )
        )

    def set_number_of_keys_found(self, n: Optional[int]) -> None:
        self.label_results.setText(f"Number of keys found: {'-' if n is None else n}")

    def search_keys(self) -> None:
        self.btn_search.setEnabled(False)
        self.key_list_view.selectionModel().clear()

        # Note: using cast() here as self.key_list_view.model() seems to have
        # a bad return value type-hint.
        key_list_model = cast(QtCore.QStringListModel, self.key_list_view.model())
        key_list_model.setStringList([])
        self.set_number_of_keys_found(None)

        def on_result(keys: Sequence[gpg.KeyInfo]) -> None:
            key_list_model.setStringList([f"{k.uid} {k.fingerprint}" for k in keys])
            self.set_number_of_keys_found(len(keys))

        run_thread(
            crypt.search_keyserver,
            f_kwargs=dict(
                search_term=self.search_string.text(),
                keyserver=self.parent_tab.app_data.config.keyserver_url,
            ),
            report_config=self.parent_tab.app_data.config,
            forward_errors=warning_callback("GPG key search error"),
            signals=dict(result=on_result),
        )

    def download_selected(self) -> None:
        """Download keys selected in the key-search pop-up to the user's
        local keyring.
        """
        keys_to_download = [
            index.model().data(index) for index in self.key_list_view.selectedIndexes()
        ]
        if keys_to_download:

            def on_result() -> None:
                self.parent_tab.update_public_keys()
                self.parent_tab.update_display_selected_pub_key()

            self.btn_download.setEnabled(False)
            run_thread(
                crypt.download_keys,
                f_kwargs=dict(
                    fingerprints=[x.split()[-1] for x in keys_to_download],
                    keyserver=self.parent_tab.app_data.config.keyserver_url,
                    gpg_store=self.parent_tab.app_data.config.gpg_store,
                ),
                report_config=self.parent_tab.app_data.config,
                forward_errors=warning_callback("GPG key search error"),
                signals=dict(
                    result=on_result,
                    finished=lambda: self.btn_download.setEnabled(True),
                ),
            )


class KeyGenDialog(QtWidgets.QDialog):
    def __init__(self, parent: KeysTab):
        super().__init__(parent=parent)
        self.parent_tab = parent
        self.setWindowTitle("Generate new key pair")
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)

        self.text_name_full = LineEdit()
        self.text_name_extra = LineEdit()
        self.text_email = LineEdit()
        self.text_pass = LineEdit()
        self.text_pass_repeat = LineEdit()
        self.toggle_password_visibility(False)

        re_email = QtCore.QRegularExpression(r"[^@]+@[^@]+\.[^@]+")
        self.text_email.setValidator(QtGui.QRegularExpressionValidator(re_email))

        self.btn_run = QtWidgets.QPushButton("Generate key")
        self.btn_run.setDefault(True)
        self.btn_run.clicked.connect(self.create_private_key)  # type: ignore
        btn_cancel = QtWidgets.QPushButton("Close")
        btn_cancel.clicked.connect(self.close)  # type: ignore
        btn_show_pass = QtWidgets.QPushButton("Show")
        btn_show_pass.setCheckable(True)
        btn_show_pass.clicked.connect(self.toggle_password_visibility)  # type: ignore

        self.setLayout(
            grid_layout(
                (QtWidgets.QLabel("Full name"), self.text_name_full),
                (
                    QtWidgets.QLabel("(optional) institution/project"),
                    self.text_name_extra,
                ),
                (QtWidgets.QLabel("Institutional email"), self.text_email),
                (QtWidgets.QLabel("Password"), self.text_pass),
                (
                    QtWidgets.QLabel("Password (repeat)"),
                    self.text_pass_repeat,
                    btn_show_pass,
                ),
                (btn_cancel, self.btn_run),
                (
                    GridLayoutCell(
                        QtWidgets.QLabel("Key generation can take a few minutes"),
                        span=3,
                    ),
                ),
            )
        )

    def toggle_password_visibility(self, show: bool) -> None:
        mode = QtWidgets.QLineEdit.Normal if show else QtWidgets.QLineEdit.Password
        self.text_pass.setEchoMode(mode)
        self.text_pass_repeat.setEchoMode(mode)

    def clear_form(self) -> None:
        self.text_name_full.clear()
        self.text_name_extra.clear()
        self.text_email.clear()
        self.text_pass.clear()
        self.text_pass_repeat.clear()

    def post_key_creation(self, key: gpg.Key) -> None:
        msg = QtWidgets.QMessageBox(self)
        msg.setWindowTitle("GPG Key Generation")
        msg.setIcon(QtWidgets.QMessageBox.Information)
        try:
            revocation_cert = crypt.create_revocation_certificate(
                key.fingerprint,
                self.text_pass.text(),
                self.parent_tab.app_data.config.gpg_store,
            )
            msg.setText(
                "Your new key has been successfully generated.\n\n"
                "Additionally, a revocation certificate was also created. "
                "It can be used to revoke your key in the eventuality that it "
                "gets compromised, lost, or that you forget your password.\n"
                "Please store the revocation certificate below in a safe "
                "location, as anyone can use it to revoke your key."
            )
            msg.setDetailedText(revocation_cert.decode())
            # Programmatically click the "Show Details..." button so that the
            # certificate is shown by default.
            click_show_details(msgbox=msg)

        except UserError:
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            msg.setText(
                "Key has been successfully generated. However, it was not "
                "possible to create a revocation certificate for it. Please "
                "execute the following command to create the certificate:\n\n"
                f"gpg --gen-revoke {key.fingerprint}"
            )
        finally:
            open_window(msg)
            if (
                self.parent_tab.app_data.config.key_authority_fingerprint
                and not self.parent_tab.app_data.config.offline
            ):
                request_signature((key,), self.parent_tab.app_data.config, self)
            self.clear_form()
            self.parent_tab.update_private_keys()
            self.parent_tab.update_public_keys()
            self.close()

    def create_private_key(self) -> None:
        self.btn_run.setEnabled(False)
        name_full = self.text_name_full.text().strip()
        name_extra = self.text_name_extra.text().strip()
        if name_extra:
            if not name_extra.startswith("(") and not name_extra.endswith(")"):
                name_extra = f"({name_extra})"
            name_full = name_full + " " + name_extra
        if self.text_pass.text() != self.text_pass_repeat.text():
            show_warning(
                "GPG Key Generation Error",
                "Password and repeated password do not match.",
                self,
            )
            self.btn_run.setEnabled(True)
            return

        run_thread(
            crypt.create_key,
            f_kwargs=dict(
                full_name=name_full,
                email=self.text_email.text(),
                pwd=Secret(self.text_pass.text()),
                gpg_store=self.parent_tab.app_data.config.gpg_store,
            ),
            forward_errors=warning_callback("GPG Key Generation Error"),
            report_config=self.parent_tab.app_data.config,
            signals=dict(
                result=self.post_key_creation,
                finished=lambda: self.btn_run.setEnabled(True),
            ),
        )


def click_show_details(msgbox: QtWidgets.QMessageBox) -> None:
    for button in msgbox.buttons():
        if msgbox.buttonRole(button) is QtWidgets.QMessageBox.ButtonRole.ActionRole:
            button.click()


def request_signature(
    keys: Sequence[gpg.Key],
    config: Config,
    parent: Optional[QtWidgets.QWidget] = None,
) -> None:
    """Request the specified keys to be signed by the key validation authority.
    This triggers the following:
     * The specified keys are uploaded to the keyserver.
     * An email is sent to the key authority to request the signature.
    """
    msg = QtWidgets.QMessageBox(parent)
    msg.setWindowTitle("Key signing request")
    msg.setText("Do you want to request signature for this key?")
    msg.setIcon(QtWidgets.QMessageBox.Question)
    msg.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
    show_ok = ok_message(
        "Key signing request", "Key signing request has been sent.", parent=parent
    )

    for key in keys:
        msg.setDetailedText(KeysTab.key_to_text(key))
        if key is keys[0]:
            click_show_details(msgbox=msg)
        status = open_window(msg)
        if status == QtWidgets.QMessageBox.Yes:
            run_thread(
                request_sigs_workflow.request_sigs,
                f_kwargs=dict(
                    key_ids=[key.key_id],
                    config=config,
                ),
                capture_loggers=(request_sigs_workflow.logger,),
                forward_errors=warning_callback("Key signing request", parent=parent),
                report_config=config,
                signals=dict(result=lambda _: show_ok()),
            )


def ok_message(
    title: str, msg: str, parent: Optional[QtWidgets.QWidget] = None
) -> Callable[[], Any]:
    msg_ok = QtWidgets.QMessageBox(parent)
    msg_ok.setIcon(QtWidgets.QMessageBox.Information)
    msg_ok.setWindowTitle(title)
    msg_ok.setText(msg)
    return lambda: open_window(msg_ok)


def keys_as_tuple(keys: Sequence[gpg.Key]) -> Iterable[Tuple[str, gpg.Key]]:
    """Returns a generator of tuples of the form ("userID keyID", key)."""
    return ((f"{key.uids[0]} {key.key_id}", key) for key in keys)
