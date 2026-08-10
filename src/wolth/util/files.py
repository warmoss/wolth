"""File and directory I/O utilities.

Provides convenience wrappers around :mod:`os` and :mod:`shutil`
for common file-system operations.
"""

import os
import shutil


def read_lines(filename):
    """Read a text file and return its lines as a list.

    Args:
        filename: Path to the file.

    Returns:
        A list of lines (including trailing newlines), or *None* if the
        file does not exist.
    """
    if not os.path.isfile(filename):
        return None
    with open(filename, "r", encoding="utf-8") as f:
        return f.readlines()


def read_all(filename):
    """Read the entire content of a text file.

    Args:
        filename: Path to the file.

    Returns:
        The full file content as a single string, or *None* if the file
        does not exist.
    """
    if not os.path.isfile(filename):
        return None
    with open(filename, "r", encoding="utf-8") as f:
        return f.read()


def write_all(filename, data, mode="w"):
    """Write string data to a file.

    Args:
        filename: Path to the file.
        data: The string content to write.
        mode: File-open mode (default ``"w"``). Use ``"a"`` to append.
    """
    with open(filename, mode, encoding="utf-8") as f:
        f.write(data)


def path_join(*path_parts: str):
    """Join path components with the OS-appropriate separator.

    Args:
        *path_parts: One or more path segments.

    Returns:
        The joined path string.
    """
    return os.path.join(*path_parts)


def exists(target):
    """Check whether a path exists.

    Args:
        target: File or directory path.

    Returns:
        ``True`` if the path exists, ``False`` otherwise.
    """
    return os.path.exists(target)


def rmdirs(target):
    """Recursively delete a directory tree.

    Does nothing if *target* does not exist.

    Args:
        target: Directory path to remove.
    """
    if os.path.exists(target):
        shutil.rmtree(target)


def mkdirs(target):
    """Create a directory (and any missing parents).

    No-op if the directory already exists.

    Args:
        target: Directory path to create.
    """
    os.makedirs(target, exist_ok=True)


def remove(filename):
    """Delete a single file.

    Args:
        filename: Path to the file to remove.

    Raises:
        FileNotFoundError: If the file does not exist.
        OSError: If the path is a directory (use :func:`rmdirs` instead).
    """
    os.remove(filename)


def archive(source: str, dest: str, format="zip"):
    """Create an archive of a directory.

    Args:
        source: Path to the directory to archive.
        dest: Base name of the archive to create (without extension).
        format: Archive format (default ``"zip"``).
    """
    shutil.make_archive(dest, format, source)


def extract(source: str, dest: str, format="zip"):
    """Extract an archive to a directory.

    Args:
        source: Path to the archive file to extract.
        dest: Path to the directory where files will be extracted.
        format: Archive format (default ``"zip"``).
    """
    shutil.unpack_archive(source, dest, format)
