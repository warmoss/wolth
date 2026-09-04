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


def copy(source: str, dest: str, override=True):
    """Copy a file or directory to *dest*.

    Copies the file, or the whole directory tree, at *source* to *dest*.
    Missing parent folders of *dest* are created automatically.

    Args:
        source: Path of the file or directory to copy.
        dest: Destination path. If it is an existing directory, *source*
            is copied into it and keeps its base name.
        override: Whether to replace an existing destination (default
            ``True``). When ``False``, an existing *dest* raises an error.

    Returns:
        The path that the file or directory was copied to.

    Raises:
        FileNotFoundError: If *source* does not exist.
        FileExistsError: If *dest* already exists and *override* is False.
    """
    if not os.path.exists(source):
        raise FileNotFoundError(f"source path does not exist: {source}")

    # Copying a file onto an existing directory keeps its base name.
    if os.path.isfile(source) and os.path.isdir(dest):
        dest = os.path.join(dest, os.path.basename(source))

    parent = os.path.dirname(dest)
    if parent:
        mkdirs(parent)

    if os.path.isdir(source):
        if os.path.exists(dest) and not override:
            raise FileExistsError(f"destination already exists: {dest}")
        if os.path.exists(dest):
            if os.path.isdir(dest):
                rmdirs(dest)
            else:
                remove(dest)
        return shutil.copytree(source, dest)

    if os.path.exists(dest) and not override:
        raise FileExistsError(f"destination already exists: {dest}")
    return shutil.copy2(source, dest)
