import os
import sys
import json
import atexit
from logging import Logger
from functools import wraps
from contextlib import suppress, contextmanager
from datetime import datetime, timedelta
import warnings
from typing import Callable, Optional, TypeVar, Any, Generator
from glob import glob

from .. import URL_GITLAB_ISSUES
from ..core.error import UserError
from ..core.filesystem import delete_files
from .config import Config, config_to_dict
from .log import log_to_memory

EXCEPTION_TYPES = (
    UserError,
    FileNotFoundError,
    FileExistsError,
    PermissionError,
    OSError,
)

R = TypeVar("R")


def exit_on_exception(f: Callable[..., R]) -> Callable[..., R]:
    """A function decorator exiting the application on an exception of instance
    contained in or equal to `EXCEPTION_TYPES`, occurring while executing the
    decorated function. No stack trace will be printed, i.e. the errors are
    assumed to be handled/reported to the end users in a meaningful way.
    """

    @wraps(f)
    def wrapped_f(*args: Any, **kwargs: Any) -> R:
        try:
            return f(*args, **kwargs)
        except EXCEPTION_TYPES:
            sys.exit(1)

    return wrapped_f


def suppress_exceptions(f: Callable[..., R]) -> Callable[..., Optional[R]]:
    """Decorator implemention of the contextlib.suppress context manager"""

    @wraps(f)
    def wrapped_f(*args: Any, **kwargs: Any) -> Optional[R]:
        with suppress(*EXCEPTION_TYPES):
            return f(*args, **kwargs)
        return None

    return wrapped_f


ERROR_REPORT_PREFIX = "error_report-"


def write_error_report(config: Config, log: str, context: Optional[str] = None) -> str:
    """Writes a error report containing sys.argv, config and a log.
    Returns the filename of the report."""
    f_name = f"error_report-{datetime.now().strftime('%Y-%m-%dT%H-%M-%S')}.txt"
    with open(os.path.join(config.log_dir, f_name), "w", encoding="utf-8") as f:
        f.write("cmd: " + repr(sys.argv) + "\n")
        if context is not None:
            f.write("context: " + context + "\n")
        f.write("---\nlog\n===\n")
        f.write(log)
        f.write("\n---\nconfig\n======\n")
        json.dump(config_to_dict(config), f, indent=2)
        return f.name


def cleanup_error_reports(log_dir: str) -> None:
    old_crash_reports = (
        f
        for f in glob(os.path.join(log_dir, ERROR_REPORT_PREFIX) + "*.txt")
        if datetime.now() - datetime.fromtimestamp(os.path.getmtime(f))
        > timedelta(weeks=1)
    )
    delete_files(*old_crash_reports)


def log_exceptions(
    logger: Logger, reraise_warnings: bool = False
) -> Callable[[Callable[..., R]], Callable[..., R]]:
    """A function decorator catching the first exception of instance contained
    in or equal to `EXCEPTION_TYPES`, occurring while executing the decorated
    function, logging an error and reraises the exception for further error
    handling. It also turns warnings into log entries.
    """

    def decorator(f: Callable[..., R]) -> Callable[..., R]:
        @wraps(f)
        def wrapped_f(*args: Any, **kwargs: Any) -> R:
            try:
                with warnings.catch_warnings(record=True) as w:
                    warnings.simplefilter("always")
                    r = f(*args, **kwargs)
                    for warning in w:
                        # Note: the reason that "\n" are removed is so that
                        # each warning gets logged on a single line.
                        logger.warning(format(warning.message).replace("\n", " "))

                if reraise_warnings:
                    for warning in w:
                        warnings.warn(format(warning.message))
                return r

            except EXCEPTION_TYPES as e:
                logger.error(format(e))
                raise

        return wrapped_f

    return decorator


@contextmanager
def error_report_hint_at_exit(
    config: Config, **kwargs: Any
) -> Generator[None, None, None]:
    """Displays a message about a generated error report as a last action
    before exit.
    """

    try:
        with error_report_on_exception(config, **kwargs):
            yield None
    except ExceptionWithReport as e:
        msg = e.error_report_msg
        atexit.register(lambda: print("\n" + msg, file=sys.stderr))
        if e.__cause__ is None:
            raise e
        raise e.__cause__


class ExceptionWithReport(Exception):
    """Exception class holding the additional info about the error report
    file.
    """

    def __init__(self, error_report_file: str):
        self.error_report_msg = (
            f"An error occurred. If you think it is as bug, please report it "
            f"at {URL_GITLAB_ISSUES} and attach the following auto generated "
            f"error report: {error_report_file}. "
            f"Or contact the developers via another channel (please also "
            f"provide the error report)."
        )
        self.error_report_file = error_report_file
        super().__init__(self.error_report_msg)

    def __format__(self, format_spec: str) -> str:
        return format(self.__cause__) + "\n" + self.error_report_msg


@contextmanager
def error_report_on_exception(
    config: Config, context: Optional[str] = None, **kwargs: Any
) -> Generator[None, None, None]:
    """Function decorator / context manager generating a error report on any
    exception.

    In case of an exception, calls `handle_error_report` and re-raises the
    exception for further handling.
    """
    with log_to_memory(**kwargs) as mem_log:
        try:
            yield None
        except Exception as e:
            error_report_file = write_error_report(
                config, mem_log.getvalue(), context=context
            )
            cleanup_error_reports(config.log_dir)
            raise ExceptionWithReport(error_report_file) from e
