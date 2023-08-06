import logging
import platform
import sys
import traceback
import warnings
from contextlib import contextmanager
from typing import Generator, Sequence, Callable, Optional, Dict, cast, Any

from .pyside import QtCore, get_application_global_instance
from ..core.secret import enforce_secret_by_signature
from ..utils.config import Config
from ..utils.error_handling import (
    suppress_exceptions,
    log_exceptions,
    error_report_on_exception,
)
from ..utils.log import EmojiLevelFormatter, LOG_FORMAT, LOG_FORMAT_WITH_EMOJI


class LoggerHandler(logging.Handler):
    """Set color scheme for logging handler output."""

    def __init__(
        self,
        level: int = logging.NOTSET,
        callback: Optional[Callable[..., Any]] = None,
    ):
        super().__init__(level)
        self.callback = callback
        core_application: Optional[
            QtCore.QCoreApplication
        ] = get_application_global_instance()
        color = (
            # Note: for some reason the second call to "core_application.palette()"
            # does not raise a mypy error, but the first one does.
            core_application.palette().color(core_application.palette().ColorRole.Text)  # type: ignore
            if core_application is not None
            else "black"
        )
        self.log_style = {
            logging.DEBUG: "gray",
            logging.INFO: color,
            logging.WARNING: "orange",
            logging.ERROR: "red",
            logging.CRITICAL: "red",
        }

    def emit(self, record: logging.LogRecord) -> None:
        if self.callback:
            color = self.log_style.get(record.levelno)
            self.callback(
                f'<span style="color: {color}">{self.format(record)}</span>'
                if color
                else self.format(record)
            )


class WorkerSignals(QtCore.QObject):
    finished = QtCore.Signal()
    error = QtCore.Signal(tuple)
    result = QtCore.Signal(object)
    progress = QtCore.Signal(int)
    logging = cast(QtCore.SignalInstance, QtCore.Signal(str))
    warning = QtCore.Signal(str)


class Worker(QtCore.QRunnable):
    """Worker can run an arbitrary function in a separate thread.

    :param fn: function to run in a thread.
    :param args: arguments passed to the function.
    :param kwargs: keyword arguments passed to the function.
    :param logger: logs from those loggers are passed to the logging signal.
    """

    def __init__(
        self,
        fn: Callable[..., Any],
        *args: Any,
        capture_loggers: Sequence[logging.Logger] = (),
        ignore_exceptions: bool = False,
        forward_errors: Optional[Callable[[str], None]] = None,
        report_config: Config,
        **kwargs: Any,
    ):
        super().__init__()

        # If no specific logger was passed to the worker, create a default
        # logger that will print warnings and errors to the app's log file.
        logger = (
            capture_loggers[0] if capture_loggers else cast(logging.Logger, logging)
        )
        self.fn = log_exceptions(logger=logger, reraise_warnings=not capture_loggers)(
            fn
        )

        # Somehow pylint does not know that @contextmanager is also a decorator.
        sanitized_args, sanitized_kwargs = enforce_secret_by_signature(fn, args, kwargs)
        workflow_args_info = ",\n  ".join(
            [repr(arg) for arg in sanitized_args]
            + [f"{key}={repr(val)}" for key, val in sanitized_kwargs.items()]
        )

        if report_config.error_reports:
            self.fn = error_report_on_exception(  # pylint: disable=not-callable
                report_config,
                context=f"{fn.__name__}({workflow_args_info})",
            )(self.fn)
        if ignore_exceptions:
            self.fn = suppress_exceptions(self.fn)
        self.args = args
        self.kwargs = kwargs
        self.capture_loggers = capture_loggers
        self.signals = WorkerSignals()  # progress signal is not implemented
        if forward_errors is not None:
            self.signals.error.connect(lambda err: forward_errors(err[1]))

    def run(self) -> None:
        with attach_loggers_to_signals(
            self.capture_loggers, self.signals
        ), warnings.catch_warnings(record=True) as user_warnings:
            try:
                result = self.fn(*self.args, **self.kwargs)
            except Exception:  # pylint: disable=broad-except
                exception_type, value, _ = sys.exc_info()
                self.signals.error.emit((exception_type, value, traceback.format_exc()))
            else:
                self.signals.result.emit(result)

        if user_warnings:
            self.signals.warning.emit(
                "\n".join(format(w.message) for w in user_warnings)
            )
        self.signals.finished.emit()


@contextmanager
def attach_loggers_to_signals(
    loggers: Sequence[logging.Logger], signals: WorkerSignals
) -> Generator[None, None, None]:
    logger_handler = LoggerHandler(callback=signals.logging.emit)
    logger_handler.setFormatter(
        logging.Formatter(LOG_FORMAT)
        if platform.system() == "Windows"
        else EmojiLevelFormatter(LOG_FORMAT_WITH_EMOJI)
    )
    logger_handler.setLevel(logging.INFO)
    for logger in loggers:
        logger.addHandler(logger_handler)
    yield None

    for logger in loggers:
        logger.removeHandler(logger_handler)


def run_thread(
    f: Callable[..., Any],
    f_kwargs: Any,
    signals: Optional[Dict[str, Callable[..., Any]]] = None,
    **worker_kwargs: Any,
) -> None:
    pool = QtCore.QThreadPool.globalInstance()
    worker = Worker(f, **f_kwargs, **worker_kwargs)
    if signals is None:
        signals = {}
    for sig_name, sig_callback in signals.items():
        getattr(worker.signals, sig_name).connect(sig_callback)
    pool.start(worker)
