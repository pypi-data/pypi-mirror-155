import concurrent.futures
import io
import os
import hashlib
from pathlib import Path
from typing import Optional, Sequence, Tuple, Iterable, IO
from .error import UserError


def compute_checksum_sha256(file_object: IO[bytes], block_size: int = 65536) -> str:
    """Compute a sha256 checksum on a file by reading it by chunks of
    'block_size' bytes at a time.

    :param file_object: input file as a FileIO object.
    :param block_size: size of blocks (in bytes) to be returned by the
        generator function. The default block size is 2^16 = 65536 bytes.
    :return: checksum
    """
    hash_value = hashlib.sha256()
    block = file_object.read(block_size)
    while block:
        hash_value.update(block)
        block = file_object.read(block_size)
    return hash_value.hexdigest()


def compute_checksum_on_write(
    stream: IO[bytes],
    fout: io.FileIO,
    checksum_buffer: io.StringIO,
    block_size: int = 65536,
) -> None:
    """Compute a sha256 checksum on stream while writing it to a file at the
    same time.

    :param stream: a stream of bytes to checksum and write to disk.
    :param fout: output file object.
    :param checksum_buffer: a buffer to store the checksum.
    :param block_size: size of blocks (in bytes) to be returned by the
        generator function. The default block size is 2^16 = 65536 bytes.
    """
    hash_value = hashlib.sha256()
    block = stream.read(block_size)
    while block:
        hash_value.update(block)
        fout.write(block)
        block = stream.read(block_size)
    checksum_buffer.write(hash_value.hexdigest())
    checksum_buffer.seek(0)


def compute_file_checksum_sha256(path: str) -> str:
    """Compute a sha256 checksum on a file.

    :param path: path to the file.
    :return: checksum.
    """
    with open(path, "rb") as f:
        return compute_checksum_sha256(f)


def generate_checksums_file_content(
    entries: Iterable[Tuple[str, str]],
    max_workers: Optional[int] = None,
) -> bytes:
    """Compute sha256 checksums for one or more files.

    Return a bytes string where each line has the format:
    `<checksum> <relative path/file name>`.
    These strings can directly be used by shasum:
    sha256sum --check *.sha256

    Return a bytes string containing lines in the format
    `<checksum> <file name>`
    (can directly be used by shasum: sha256sum --check *.sha256)

    DOS path separators will be replaced by Unix ones.

    Examples:
    a7186ae7ff993b379qcf3567775cfc71a212rf217e4dd testDir/file1.fastq
    f8d2d394264823e711fgc34e4ac83f8cbc253c6we034f testDir/file2.fastq
    78f3b23fe49cf5f7f245ddf43v9788d9e62c0971fe5fb testDir/subdir2/file4.fastq

    Checksum computation is parallelized and can make use of multiple
    CPU cores (see max_workers).

    :param entries: tuples of the form (archive path, file path).
        - archive path: the path of the file inside the archive. This is the
          path of the file as written in the string returned by the function.
        - file path: path of the original file whose checksum is to be computed.
    :param max_workers: max number of CPU cores to use for the task. If 'None',
        all available CPUs are used.
    :return: bytes string containing file names and hashes.

    """
    archive_paths, file_paths = zip(*entries)
    with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
        return b"".join(
            f"{checksum} {Path(archive_path).as_posix()}\n".encode()
            for checksum, archive_path in zip(
                executor.map(compute_file_checksum_sha256, file_paths), archive_paths
            )
        )


def verify_checksum(entry: Tuple[str, str]) -> Optional[str]:
    """Check whether the checksum of a given file matches the specified checksum.

    :param entry: tuple of (checksum value, file to verify path)
    :return: None if the checksums match, or the file's actual checksum if
        it does not match the specified checksum.
    """
    with open(entry[1], "rb") as f:
        computed = compute_checksum_sha256(f)
        return computed if entry[0].lower() != computed else None


def verify_checksums(
    # Sequence is preferable over Iterable, since ProcessPoolExecutor.map
    # collects the iterable immediately
    entries: Sequence[Tuple[str, str]],
    max_workers: Optional[int] = None,
) -> None:
    """Verify that the (checksum, file) pairs listed in entries are correct.

    Pairs are verified by checking if the file's checksum matches with the
    provided checksum. An error is raised if a mismatch is detected.
    The computing of checksums is parallelized and can make use of multiple
    CPU cores (see max_workers).

    :param entries: tuples of type (checksum value, file path), where the
        checksum value is the expected checksum to file path.
    :param max_workers: max number of CPU cores to use for the task. If 'None',
        all available CPUs are used.
    :raises UserError:
    """
    with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers) as executor:
        for (checksum, file_name), result in zip(
            entries, executor.map(verify_checksum, entries)
        ):
            if result is not None:
                raise UserError(
                    f"Checksum mismatch for: {file_name} (expected: {checksum}, "
                    f"got: {result})"
                )


def read_checksum_file(checksum_file: IO[bytes]) -> Iterable[Tuple[str, str]]:
    """Read lines from a checksum file object.

    Expected file format:

    a7186ae7ff993b379qcf3567775cfc71a212rf217e4dd testDir/file1.fastq
    f8d2d394264823e711fgc34e4ac83f8cbc253c6we034f testDir/file2.fastq
    78f3b23fe49cf5f7f245ddf43v9788d9e62c0971fe5fb testDir/subdir2/file4.fastq

    The reason the input argument is a file object and not a file path is so
    that the function is more flexible and also allows to read input from
    a stream rather than an actual file.

    :param checksum_file: file object.
    :return: generator of tuples of the form (checksum value, file path).
    :raises UserError:
    """
    for line in checksum_file:
        # Split line into checksum and file name values. Each line must have
        # exactly 2 elements.
        try:
            checksum, file_name = line.decode().rstrip("\n\r").split(maxsplit=1)
        except ValueError:
            raise UserError("Input must have exactly 2 elements per line.") from None
        if os.path.isabs(file_name):
            raise UserError("Absolute path in checksum file")
        yield checksum, file_name
