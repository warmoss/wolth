"""File and directory I/O utilities.

Provides convenience wrappers around :mod:`os`, :mod:`shutil`, and :mod:`zipfile`
for common file-system operations.
"""

import os
import shutil
import zipfile


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
    with open(filename, "r") as f:
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
    with open(filename, "r") as f:
        return "".join(f.readlines())


def write_all(filename, data, mode="w"):
    """Write string data to a file.

    Args:
        filename: Path to the file.
        data: The string content to write.
        mode: File-open mode (default ``"w"``). Use ``"a"`` to append.
    """
    with open(filename, mode) as f:
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


def unzip(filename: str, extract_to: str):
    """Extract a ZIP archive into a target directory.

    Args:
        filename: Path to the ZIP file.
        extract_to: Destination directory.
    """
    with zipfile.ZipFile(filename, "r") as zip_ref:
        zip_ref.extractall(extract_to)
