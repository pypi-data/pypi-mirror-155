from typing import Callable, Optional, Any, Type, TypeVar, Generic, cast
from pathlib import Path

from .pyside import QtCore, QtWidgets
from .listener import Listener
from .component import PathInput

from ..core.secret import Secret, reveal

# Generic type for a variable.
T = TypeVar("T")
T_WIDGET = TypeVar("T_WIDGET")


class Control(Generic[T, T_WIDGET]):
    """Abstracts all functionality of a widget needed to bind the widget to
    a state.
    """

    @classmethod
    def signal_connect(cls, widget: Any) -> Callable[[Callable[[T], None]], None]:
        # NOTE: widget is typed as "Any" for lack of a better solution.
        pass

    @classmethod
    def setter(cls, widget: T_WIDGET) -> Callable[[T], None]:
        pass


class SignalControl(Control[T, T_WIDGET]):
    """Controls with a signal property (in contrast to controls with a
    on_changed callback).
    """

    @classmethod
    def signal(cls, widget: T_WIDGET) -> Callable[[T], None]:
        pass

    @classmethod
    def getter(cls, widget: T_WIDGET) -> Callable[[], Any]:
        pass

    @classmethod
    def signal_connect(cls, widget: T_WIDGET) -> Callable[[Callable[[T], None]], None]:
        # NOTE: cast is needed here so that mypy knows that the object returned
        #       by cls.signal() has a .connect method.
        signal_obj: QtCore.SignalInstance = cast(
            QtCore.SignalInstance, cls.signal(widget)
        )
        signal_connect = signal_obj.connect

        def _connect(callback_with_value: Callable[[T], None]) -> None:
            signal_connect(to_signal_callback(callback_with_value, cls.getter(widget)))

        return _connect


class BoolControl(Control[bool, QtWidgets.QCheckBox]):
    @classmethod
    def signal_connect(cls, widget: Any) -> Callable[[Callable[[bool], None]], None]:
        def _connect(callback: Callable[[bool], None]) -> None:
            widget.stateChanged.connect(
                callback_with_conversion(
                    callback, lambda state: state == QtCore.Qt.Checked
                )
            )

        return _connect

    # NOTE: the reason for not returning directly "widget.setChecked" is
    #       because mypy does not infer its type properly in that case.
    #       The same happens in subsequent functions (see below).
    @classmethod
    def setter(cls, widget: QtWidgets.QCheckBox) -> Callable[[bool], None]:
        widget_method: Callable[[bool], None] = widget.setChecked
        return widget_method


class NumericControl(Control[int, QtWidgets.QSpinBox]):
    @classmethod
    def signal_connect(cls, widget: Any) -> Callable[[Callable[[int], None]], None]:
        widget_method: Callable[
            [Callable[[int], None]], None
        ] = widget.valueChanged.connect
        return widget_method

    @classmethod
    def setter(cls, widget: QtWidgets.QSpinBox) -> Callable[[int], None]:
        widget_method: Callable[[int], None] = widget.setValue
        return widget_method


T_STR_OR_SECRET = TypeVar(
    "T_STR_OR_SECRET", Optional[str], Secret[str], Optional[Secret[str]]
)


class TextControl(SignalControl[str, QtWidgets.QLineEdit], Generic[T_STR_OR_SECRET]):
    @staticmethod
    def _to_ui(val: Any) -> str:
        ret: str = val
        return ret

    @staticmethod
    def _from_ui(val: Any) -> T_STR_OR_SECRET:
        ret: T_STR_OR_SECRET = val
        return ret

    @classmethod
    def signal(cls, widget: QtWidgets.QLineEdit) -> Callable[[str], None]:
        text_changed_method: Callable[[str], None] = widget.textChanged  # type: ignore
        return text_changed_method

    @classmethod
    def setter(cls, widget: QtWidgets.QLineEdit) -> Callable[[str], None]:
        def _set(val: str) -> None:
            widget.setText(cls._to_ui(val))

        return _set

    @classmethod
    def getter(cls, widget: QtWidgets.QLineEdit) -> Callable[[], T_STR_OR_SECRET]:
        def _get() -> T_STR_OR_SECRET:
            return cast(T_STR_OR_SECRET, cls._from_ui(widget.text()))

        return _get


class OptionalTextControl(TextControl[Optional[str]]):
    @staticmethod
    def _to_ui(val: Optional[str]) -> str:
        return val or ""

    @staticmethod
    def _from_ui(val: Optional[str]) -> Optional[str]:
        return val or None


class PasswordControl(TextControl[Secret[str]]):
    @staticmethod
    def _to_ui(val: Secret[str]) -> str:
        return val.reveal()

    @staticmethod
    def _from_ui(val: str) -> Secret[str]:
        return Secret(val)


class OptionalPasswordControl(TextControl[Optional[Secret[str]]]):
    @staticmethod
    def _to_ui(val: Optional[Secret[str]]) -> str:
        return reveal(val) or ""

    @staticmethod
    def _from_ui(val: Optional[str]) -> Optional[Secret[str]]:
        return None if not val else Secret(val)


class PathControl(Control[Optional[str], PathInput]):
    null_value: Optional[str] = ""

    @classmethod
    def signal_connect(
        cls, widget: Any
    ) -> Callable[[Callable[[Optional[str]], None]], None]:
        def _connect(callback: Callable[[Optional[str]], None]) -> None:
            widget.on_path_change(
                callback_with_conversion(
                    callback, lambda path: cls.null_value if path is None else str(path)
                )
            )

        return _connect

    @classmethod
    def setter(cls, widget: PathInput) -> Callable[[Optional[str]], None]:
        def _set(val: Optional[str]) -> None:
            widget.update_path(Path(val) if val else None)

        return _set


class OptionalPathControl(PathControl):
    null_value = None


def bind(
    state: Listener,
    attr: str,
    widget: QtWidgets.QWidget,
    widget_type: Type[Any],
) -> None:
    widget_type.signal_connect(widget)(lambda val: state.set_value(attr, val))
    state.add_listener(attr, lambda: widget_type.setter(widget)(state.get_value(attr)))


def to_signal_callback(
    callback_with_value: Callable[[Any], None],
    getter: Callable[[], None],
) -> Callable[[], None]:
    """Converts a callback with signature cb(val) -> None to a callback with
    signature cb() -> None, so it can be passed to a signal.connect() call.
    """

    def new_callback() -> None:
        callback_with_value(getter())

    return new_callback


def callback_with_conversion(
    callback: Callable[[Any], None], converter: Callable[[Any], Any]
) -> Callable[[Any], None]:
    def new_callback(val: Any) -> None:
        callback(converter(val))

    return new_callback
