"""Tests for the file I/O utilities module."""

import os
import zipfile
from unittest.mock import patch, mock_open

import pytest

from wolth.util.files import (
    read_lines,
    read_all,
    write_all,
    path_join,
    exists,
    rmdirs,
    mkdirs,
    remove,
    unzip,
)


# ──────────────────────────────────────────────
# read_lines
# ──────────────────────────────────────────────


class TestReadLines:
    """Tests for read_lines."""

    @patch("wolth.util.files.os.path.isfile")
    @patch("builtins.open", new_callable=mock_open, read_data="line1\nline2\nline3\n")
    def test_read_lines_returns_list(self, mock_file, mock_isfile):
        mock_isfile.return_value = True
        result = read_lines("/tmp/test.txt")
        assert result == ["line1\n", "line2\n", "line3\n"]

    @patch("wolth.util.files.os.path.isfile")
    def test_read_lines_file_not_found(self, mock_isfile):
        mock_isfile.return_value = False
        result = read_lines("/tmp/nonexistent.txt")
        assert result is None

    @patch("wolth.util.files.os.path.isfile")
    @patch("builtins.open", new_callable=mock_open, read_data="")
    def test_read_lines_empty_file(self, mock_file, mock_isfile):
        mock_isfile.return_value = True
        result = read_lines("/tmp/empty.txt")
        assert result == []


# ──────────────────────────────────────────────
# read_all
# ──────────────────────────────────────────────


class TestReadAll:
    """Tests for read_all."""

    @patch("wolth.util.files.os.path.isfile")
    @patch("builtins.open", new_callable=mock_open, read_data="Hello, World!")
    def test_read_all_returns_string(self, mock_file, mock_isfile):
        mock_isfile.return_value = True
        result = read_all("/tmp/test.txt")
        assert result == "Hello, World!"

    @patch("wolth.util.files.os.path.isfile")
    def test_read_all_file_not_found(self, mock_isfile):
        mock_isfile.return_value = False
        result = read_all("/tmp/nonexistent.txt")
        assert result is None

    @patch("wolth.util.files.os.path.isfile")
    @patch("builtins.open", new_callable=mock_open, read_data="")
    def test_read_all_empty_file(self, mock_file, mock_isfile):
        mock_isfile.return_value = True
        result = read_all("/tmp/empty.txt")
        assert result == ""


# ──────────────────────────────────────────────
# write_all
# ──────────────────────────────────────────────


class TestWriteAll:
    """Tests for write_all."""

    @patch("builtins.open", new_callable=mock_open)
    def test_write_all_writes_data(self, mock_file):
        write_all("/tmp/test.txt", "Hello, World!")
        mock_file.assert_called_once_with("/tmp/test.txt", "w")
        mock_file().write.assert_called_once_with("Hello, World!")

    @patch("builtins.open", new_callable=mock_open)
    def test_write_all_append_mode(self, mock_file):
        write_all("/tmp/test.txt", "more data", mode="a")
        mock_file.assert_called_once_with("/tmp/test.txt", "a")
        mock_file().write.assert_called_once_with("more data")

    @patch("builtins.open", new_callable=mock_open)
    def test_write_all_empty_string(self, mock_file):
        write_all("/tmp/test.txt", "")
        mock_file().write.assert_called_once_with("")

    @patch("builtins.open", new_callable=mock_open)
    def test_write_all_multiple_calls(self, mock_file):
        write_all("/tmp/a.txt", "first")
        write_all("/tmp/b.txt", "second")
        assert mock_file.call_count == 2


# ──────────────────────────────────────────────
# path_join
# ──────────────────────────────────────────────


class TestPathJoin:
    """Tests for path_join."""

    def test_path_join_two_parts(self):
        result = path_join("a", "b")
        assert result == os.path.join("a", "b")

    def test_path_join_multiple_parts(self):
        result = path_join("a", "b", "c", "d")
        assert result == os.path.join("a", "b", "c", "d")

    def test_path_join_single_part(self):
        result = path_join("a")
        assert result == "a"


# ──────────────────────────────────────────────
# exists
# ──────────────────────────────────────────────


class TestExists:
    """Tests for exists."""

    @patch("wolth.util.files.os.path.exists")
    def test_exists_returns_true(self, mock_exists):
        mock_exists.return_value = True
        assert exists("/tmp/test.txt") is True

    @patch("wolth.util.files.os.path.exists")
    def test_exists_returns_false(self, mock_exists):
        mock_exists.return_value = False
        assert exists("/tmp/nonexistent.txt") is False

    @patch("wolth.util.files.os.path.exists")
    def test_exists_calls_os_path_exists(self, mock_exists):
        exists("/tmp/test.txt")
        mock_exists.assert_called_once_with("/tmp/test.txt")


# ──────────────────────────────────────────────
# rmdirs
# ──────────────────────────────────────────────


class TestRmdirs:
    """Tests for rmdirs."""

    @patch("wolth.util.files.shutil.rmtree")
    @patch("wolth.util.files.os.path.exists")
    def test_rmdirs_existing_directory(self, mock_exists, mock_rmtree):
        mock_exists.return_value = True
        rmdirs("/tmp/mydir")
        mock_rmtree.assert_called_once_with("/tmp/mydir")

    @patch("wolth.util.files.shutil.rmtree")
    @patch("wolth.util.files.os.path.exists")
    def test_rmdirs_non_existing_directory(self, mock_exists, mock_rmtree):
        mock_exists.return_value = False
        rmdirs("/tmp/nonexistent")
        mock_rmtree.assert_not_called()

    @patch("wolth.util.files.shutil.rmtree")
    @patch("wolth.util.files.os.path.exists")
    def test_rmdirs_calls_exists_first(self, mock_exists, mock_rmtree):
        rmdirs("/tmp/mydir")
        mock_exists.assert_called_once_with("/tmp/mydir")


# ──────────────────────────────────────────────
# mkdirs
# ──────────────────────────────────────────────


class TestMkdirs:
    """Tests for mkdirs."""

    @patch("wolth.util.files.os.makedirs")
    def test_mkdirs_creates_directory(self, mock_makedirs):
        mkdirs("/tmp/newdir")
        mock_makedirs.assert_called_once_with("/tmp/newdir", exist_ok=True)

    @patch("wolth.util.files.os.makedirs")
    def test_mkdirs_nested_directories(self, mock_makedirs):
        mkdirs("/tmp/a/b/c")
        mock_makedirs.assert_called_once_with("/tmp/a/b/c", exist_ok=True)

    @patch("wolth.util.files.os.makedirs")
    def test_mkdirs_exist_ok_true(self, mock_makedirs):
        """Should not raise if directory already exists."""
        mkdirs("/tmp/existing")
        mock_makedirs.assert_called_once_with("/tmp/existing", exist_ok=True)


# ──────────────────────────────────────────────
# remove
# ──────────────────────────────────────────────


class TestRemove:
    """Tests for remove."""

    @patch("wolth.util.files.os.remove")
    def test_remove_file(self, mock_remove):
        remove("/tmp/test.txt")
        mock_remove.assert_called_once_with("/tmp/test.txt")

    @patch("wolth.util.files.os.remove")
    def test_remove_file_not_found_raises(self, mock_remove):
        mock_remove.side_effect = FileNotFoundError()
        with pytest.raises(FileNotFoundError):
            remove("/tmp/nonexistent.txt")


# ──────────────────────────────────────────────
# unzip
# ──────────────────────────────────────────────


class TestUnzip:
    """Tests for unzip."""

    @patch("wolth.util.files.zipfile.ZipFile")
    def test_unzip_calls_extractall(self, mock_zip):
        mock_instance = mock_zip.return_value.__enter__.return_value
        unzip("/tmp/archive.zip", "/tmp/extract")
        mock_zip.assert_called_once_with("/tmp/archive.zip", "r")
        mock_instance.extractall.assert_called_once_with("/tmp/extract")

    @patch("wolth.util.files.zipfile.ZipFile")
    def test_unzip_uses_context_manager(self, mock_zip):
        """ZipFile should be used as a context manager."""
        unzip("/tmp/archive.zip", "/tmp/extract")
        mock_zip.return_value.__enter__.assert_called_once()
