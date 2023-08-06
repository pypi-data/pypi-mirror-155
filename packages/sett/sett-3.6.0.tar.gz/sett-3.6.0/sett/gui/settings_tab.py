from typing import Optional, Tuple, Union, Dict, Callable, Sequence, Any, cast
from dataclasses import Field, asdict, fields  # pylint: disable=unused-import

from .listener import Listener
from .ui_model_bind import (
    bind,
    TextControl,
    PathControl,
    BoolControl,
    NumericControl,
)
from .component import (
    PathInput,
    create_slider,
    LineEdit,
    SpinBox,
    grid_layout,
    GridLayoutCell,
)
from .model import AppData
from .pyside import QtCore, QtGui, QtWidgets
from .keys_refresh import load_authority_key_threaded
from ..utils import config
from ..utils.config import Config, FileType


class ConfigProxy(Listener):
    """Proxy between the Config dataclass and the UI."""

    def __init__(self, app_data: AppData):
        super().__init__()
        self.app_data = app_data

    def set_value(self, attr: str, val: Any) -> None:
        """Updates the specified sett config attribute (attr) with a new value."""
        cfg = self.app_data.config
        if val != getattr(cfg, attr):
            setattr(cfg, attr, val)
            if attr == "key_authority_fingerprint":
                # Only attempt to reload the key validation authority key if
                # a proper fingerprint was entered. Otherwise we get a warning
                # each time the user is entering a new character in the field.
                if len(val) == 40:
                    load_authority_key_threaded(self.app_data)
                else:
                    self.app_data.validation_authority_key = None

    def get_value(self, attr: str) -> Any:
        return getattr(self.app_data.config, attr)

    def refresh(self) -> None:
        for callbacks in self._listeners.values():
            for callback in callbacks:
                callback()

    def set_config(self, cfg: Config) -> None:
        """Sets/Updates the in-memory config values with the new values passed
        in "cfg". Then updates the Settings Tab widgets in the UI.
        """
        self.app_data.config = cfg
        self.refresh()

    def get_config(self) -> Config:
        """Returns the current in-memory config values."""
        cfg: Config = self.app_data.config
        return cfg


class SettingsTab(QtWidgets.QWidget):
    persist_btn_text = "Save to config file"

    def __init__(self, parent: QtWidgets.QMainWindow, app_data: AppData):
        super().__init__(parent=parent)
        self.app_data = app_data
        self.config_proxy = ConfigProxy(self.app_data)

        widget_register: Dict[str, QtWidgets.QWidget] = {}
        cfg_fields = {f.name: f for f in fields(Config)}

        def cfg_field(key: str) -> Tuple[QtWidgets.QWidget, ...]:
            return widget_row_from_field(
                self.config_proxy, cfg_fields[key], widget_register=widget_register
            )

        self.setLayout(
            grid_layout(
                self._header(),
                group_box(
                    "Data encryption / decryption settings",
                    cfg_field("compression_level"),
                    cfg_field("max_cpu"),
                    cfg_field("default_sender"),
                    cfg_field("sign_encrypted_data"),
                    cfg_field("always_trust_recipient_key"),
                    cfg_field("output_dir"),
                    cfg_field("offline"),
                    cfg_field("package_name_suffix"),
                ),
                group_box(
                    "PGP keys",
                    cfg_field("key_authority_fingerprint"),
                    cfg_field("gpg_home_dir"),
                    cfg_field("keyserver_url"),
                    cfg_field("gpg_key_autodownload"),
                ),
                group_box(
                    "Data transfer",
                    cfg_field("ssh_password_encoding"),
                    cfg_field("dcc_portal_url"),
                    cfg_field("verify_package_name"),
                ),
                group_box(
                    "sett updates", cfg_field("repo_url"), cfg_field("check_version")
                ),
                group_box(
                    "Miscellaneous and logs",
                    cfg_field("gui_quit_confirmation"),
                    cfg_field("log_dir"),
                    cfg_field("log_max_file_number"),
                    cfg_field("error_reports"),
                ),
                self._footer(),
            )
        )
        # Enable or disable the PGP key auto-download checkbox option based on
        # whether a keyserver URL value is provided or not.
        self.checkbox_gpg_key_autodownload = cast(
            QtWidgets.QCheckBox, widget_register["gpg_key_autodownload"]
        )
        self.field_keyserver_url = cast(
            QtWidgets.QLineEdit, widget_register["keyserver_url"]
        )
        self._enable_checkbox_key_autodownload()
        self.field_keyserver_url.textChanged.connect(  # type: ignore
            self._enable_checkbox_key_autodownload
        )
        self.config_proxy.refresh()

    def _save_config_to_disk(self) -> None:
        """Write the current in-app config values to a config file on disk."""
        config.save_config(config.config_to_dict(self.config_proxy.get_config()))

    def _header(
        self,
    ) -> Tuple[GridLayoutCell, QtWidgets.QPushButton, QtWidgets.QPushButton]:
        top_label = QtWidgets.QLabel(
            "Changes you make are applied instantly during the current session.\n"
            f"To persist changes across restarts, make sure to click the "
            f"'{self.persist_btn_text}' button at the bottom of the app."
        )
        top_label.setWordWrap(True)
        reset_btn = QtWidgets.QPushButton("Reset", self)
        reset_btn.setStatusTip("Resets to your last persisted settings")
        reset_btn.clicked.connect(  # type: ignore
            lambda: self.config_proxy.set_config(config.load_config())
        )

        defaults_btn = QtWidgets.QPushButton("Restore defaults", self)
        defaults_btn.setStatusTip("Reset all settings to their default values")
        defaults_btn.clicked.connect(  # type: ignore
            lambda: self.config_proxy.set_config(config.default_config())
        )
        return (GridLayoutCell(top_label, span=2), reset_btn, defaults_btn)

    def _footer(self) -> Tuple[GridLayoutCell]:
        persist_btn = QtWidgets.QPushButton(self.persist_btn_text, self)
        persist_btn.setIcon(QtGui.QIcon(":icon/feather/save.png"))
        persist_btn.setStatusTip("Saves your current settings to the config file")
        persist_btn.clicked.connect(self._save_config_to_disk)  # type: ignore
        return (GridLayoutCell(persist_btn, span=4),)

    def _enable_checkbox_key_autodownload(self) -> None:
        self.checkbox_gpg_key_autodownload.setEnabled(
            len(self.field_keyserver_url.text().strip()) > 0
        )


def group_box(
    name: str, *widgets: Sequence[Optional[Union[QtWidgets.QWidget, GridLayoutCell]]]
) -> Tuple[GridLayoutCell]:
    box = QtWidgets.QGroupBox(name)
    box.setLayout(grid_layout(*widgets, parent=box, min_col_width=(0, 180)))
    return (GridLayoutCell(box, span=4),)


def widget_str(
    config_proxy: ConfigProxy,
    config_key: str,
    status_tip: str,
    regex: Optional[str] = None,
) -> Tuple[QtWidgets.QWidget, ...]:
    widget = LineEdit()
    widget.setStatusTip(status_tip)
    bind(config_proxy, config_key, widget, TextControl)
    if regex:
        widget.setValidator(
            QtGui.QRegularExpressionValidator(QtCore.QRegularExpression(regex))
        )

    return (widget,)


def widget_path(
    config_proxy: ConfigProxy,
    config_key: str,
    status_tip: str,
    file_type: FileType,
) -> Tuple[QtWidgets.QWidget, ...]:
    widget = PathInput(directory=file_type is FileType.directory, path=None)
    widget.setStatusTip(status_tip)
    bind(config_proxy, config_key, widget, PathControl)

    return (widget.text, widget.btn, widget.btn_clear)


def widget_bool(
    config_proxy: ConfigProxy,
    config_key: str,
    status_tip: str,
) -> Tuple[QtWidgets.QWidget, ...]:
    widget = QtWidgets.QCheckBox()
    widget.setStatusTip(status_tip)
    bind(config_proxy, config_key, widget, BoolControl)

    return (widget,)


def widget_int(
    config_proxy: ConfigProxy,
    config_key: str,
    status_tip: str,
    minimum: Optional[int] = None,
    maximum: Optional[int] = None,
) -> Tuple[QtWidgets.QWidget, ...]:
    widget = SpinBox()
    widget.setStatusTip(status_tip)
    if minimum is not None:
        widget.setMinimum(minimum)
    if maximum is not None:
        widget.setMaximum(maximum)
    bind(config_proxy, config_key, widget, NumericControl)

    return (widget,)


def widget_int_range(
    config_proxy: ConfigProxy,
    config_key: str,
    status_tip: str,
    minimum: int,
    maximum: int,
) -> Tuple[QtWidgets.QWidget, ...]:
    slider, slider_value = create_slider(
        minimum=minimum,
        maximum=maximum,
        initial_value=config_proxy.get_value(config_key),
        status_tip=status_tip,
        on_change=None,
        show_ticks=True,
    )
    bind(config_proxy, config_key, slider, NumericControl)
    return (slider, slider_value)


widget_by_type: Dict[type, Callable[..., Tuple[QtWidgets.QWidget, ...]]] = {
    int: widget_int,
    bool: widget_bool,
    str: widget_str,
}


# TODO: when dropping support for python 3.7, remove quotes around "Field"
#       and Field will no longer need to be imported.
def widget_row_from_field(
    config_proxy: ConfigProxy,
    field: "Field[Any]",
    widget_register: Optional[Dict[str, QtWidgets.QWidget]] = None,
) -> Tuple[QtWidgets.QWidget, ...]:
    """Create a widget row consisting of a label, a main widget and possible
    auxiliary widgets based on field metadata of the Config dataclass.

    If widget_register is passed, register the main widget under the
    corresponding field name.
    """
    field_type = field.type
    if getattr(field_type, "__origin__", None) is Union:
        field_type = next(t for t in field_type.__args__ if not isinstance(None, t))
    try:
        metadata = field.metadata["metadata"]
    except KeyError:
        raise RuntimeError(
            "Field metadata is required in order to create a widget from a field."
        ) from None
    widget_factory = widget_by_type[field_type]
    # Special cases:
    if metadata.minimum and metadata.maximum:
        widget_factory = widget_int_range
    if metadata.file_type is not None:
        widget_factory = widget_path
    widget_args = {
        key: val
        for key, val in asdict(metadata).items()
        if key not in ("label", "description") and val is not None
    }
    widget_row = widget_factory(
        config_proxy,
        config_key=field.name,
        status_tip=metadata.description,
        **widget_args,
    )
    if widget_register is not None:
        widget_register[field.name] = widget_row[0]
    return (
        QtWidgets.QLabel(metadata.label),
        *widget_row,
    )
