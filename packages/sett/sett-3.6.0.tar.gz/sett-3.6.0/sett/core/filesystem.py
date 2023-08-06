import math
import os
import shutil
import warnings
from contextlib import contextmanager
from itertools import count
from pathlib import Path
from typing import Iterable, Iterator, Generator, List, Union, Optional, Type
from types import TracebackType

from .error import UserError
from ..utils.log import create_logger

logger = create_logger(__name__)


def search_files_recursively(input_list: List[str]) -> Iterator[str]:
    """Recursively search for files and/or verify that files part of
    input_list really exist.

    :param input_list: list of files and directories to recursively search
        for files.
    :return: list of files and their absolute path.
    :raises UserError:
    """

    # Loop through all input path provided by the user. If the path is a
    # directory, search it recursively for files.
    for path in input_list:
        path_obj = Path(path).absolute()
        if path_obj.is_file():
            yield path_obj.as_posix()
        elif path_obj.is_dir():
            yield from (x.as_posix() for x in path_obj.rglob("*") if x.is_file())
        else:
            raise UserError(
                f"input path is not a valid file or directory: " f"{path_obj.name}"
            )


def check_file_read_permission(input_list: List[str]) -> None:
    """Verify the user has read permission on all files listed in input_list"""
    no_read_permission = [x for x in input_list if not os.access(x, os.R_OK)]
    if no_read_permission:
        raise UserError(
            f"no read permission on input files:" f"{', '.join(no_read_permission)}"
        )


def delete_files(*files: str) -> None:
    """Delete the specified file(s) and catch error if deletion fails.
    :param files: paths of files to delete from disk.
    :raises UserError:
    """
    failed = []
    for f in files:
        if os.path.exists(f):
            try:
                os.unlink(f)
            except OSError:
                failed.append(f)

    if failed:
        warnings.warn(
            f"Failed to delete file(s): {', '.join(failed)}. "
            f"You have to take care of the clean up"
        )


def unique_filename(
    filename: str, extension: str = "", separator: str = "_", first_number: int = 1
) -> str:
    def filename_candidates() -> Iterator[str]:
        yield f"{filename}{extension}"
        yield from (
            f"{filename}{separator}{i}{extension}" for i in count(start=first_number)
        )

    return next(
        candidate
        for candidate in filename_candidates()
        if not os.path.exists(candidate)
    )


class DeleteDirOnError:
    """Context Manager to delete the specified directory including all of its files
    in case of an exception.
    """

    def __init__(self, directory: Union[str, Path]):
        self.directory = directory

    def __enter__(self) -> Union[str, Path]:
        return self.directory

    def __exit__(
        self,
        exception_type: Optional[Type[BaseException]],
        value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        if traceback is not None:
            # Exception occurred
            if os.path.isdir(self.directory):
                logger.debug("Deleting directory: %s", self.directory)
                shutil.rmtree(self.directory)
            else:
                logger.debug("Directory doesn't exist: %s", self.directory)


@contextmanager
def delete_file_on_error(path: Union[str, Path]) -> Generator[None, None, None]:
    """Context manager that deletes a file if any exception is raised
    while in the context manager block.
    """
    try:
        yield
    except Exception as e:
        if os.path.exists(path):
            logger.debug("Deleting file: %s", path)
            os.remove(path)
        else:
            logger.debug("File doesn't exist: %s", path)
        raise e


class OutOfSpaceError(UserError):
    """UserError version of OSError(28, "No space left on device")"""


def get_total_size(files: Iterable[str]) -> int:
    """Compute total size (bytes) of input files"""
    return sum(os.path.getsize(path) for path in files)


def check_space(required_space: int, dest: str, force: bool = False) -> None:
    """Check if device has sufficient space."""
    available_space = shutil.disk_usage(dest).free
    if required_space >= available_space:
        msg = f"No space left on device\nrequired: {required_space}, available: {available_space}."
        if not force:
            raise OutOfSpaceError(msg)
        warnings.warn(msg + " Operation will most likely fail.")


def to_human_readable_size(size: int, precision: int = 2, sep: str = " ") -> str:
    """Converts a number of bytes into human readable units.

    The output units are selected depending on the size of the input.
    The function does not support byte values > 1000 YB.

    :param size: byte value to convert to a human readable string.
    :param precision: number of decimals to use in output.
    :param sep: separator string to use between the size value and the unit.
        e.g. if sep = " " -> "3.21 MB"
    :return: size as human readable string.
    """
    prefix = ("", "k", "M", "G", "T", "P", "E", "Z", "Y")
    log_value = int(math.log(size, 1024)) if size > 0 else 0
    return (
        f"{round(size / (1024 ** log_value), precision if log_value else None)}"
        f"{sep}{prefix[log_value]}B"
    )


def get_compression_stats(source: int, output: int, compression: bool = True) -> str:
    """Create a compression summary."""
    compression_ratio = (source / output) if compression else (output / source)
    return (
        f"source: {to_human_readable_size(source)}, "
        f"output: {to_human_readable_size(output)}, "
        f"compression ratio: {round(compression_ratio, 2)}"
    )


def reverse_expanduser(path: str) -> str:
    """Performs the reverse operation of os.path.expanduser(). It checks
    whether a path starts with a user's home directory, and if so, changes
    it to the "~" shortcut. It also removes any trailing path separator.

    Example:
      * On linux  : /home/user/foo/bar/ -> ~/foo/bar
      * On windows: /home/user/foo/bar/ -> ~\\foo\\bar
    """
    path_as_posix = Path(path).as_posix()
    home_as_posix = Path.home().as_posix()
    if path_as_posix.startswith(home_as_posix):
        return str(Path("~" + path_as_posix[len(home_as_posix) :]))

    # Note: conversion to Path and back is to remove trailing path separators.
    return str(Path(path))


def abspath_expanduser(path: Optional[str]) -> Optional[str]:
    return os.path.abspath(os.path.expanduser(path)) if path else path
