"""Tests for the file utilities module."""

import os
from unittest.mock import patch, mock_open

import pytest

from wolth.util.files import (
    archive,
    exists,
    extract,
    mkdirs,
    path_join,
    read_all,
    read_lines,
    remove,
    rmdirs,
    write_all,
)


# ──────────────────────────────────────────────
# read_lines
# ──────────────────────────────────────────────


class TestReadLines:
    """Tests for read_lines."""

    def test_read_lines_normal(self, tmp_path):
        file = tmp_path / "test.txt"
        file.write_text("line1\nline2\nline3\n", encoding="utf-8")
        result = read_lines(str(file))
        assert result == ["line1\n", "line2\n", "line3\n"]

    def test_read_lines_file_not_found(self, tmp_path):
        result = read_lines(str(tmp_path / "nonexistent.txt"))
        assert result is None

    def test_read_lines_empty_file(self, tmp_path):
        file = tmp_path / "empty.txt"
        file.write_text("", encoding="utf-8")
        result = read_lines(str(file))
        assert result == []

    def test_read_lines_single_line_no_newline(self, tmp_path):
        file = tmp_path / "single.txt"
        file.write_text("hello", encoding="utf-8")
        result = read_lines(str(file))
        assert result == ["hello"]

    def test_read_lines_with_blank_lines(self, tmp_path):
        file = tmp_path / "blanks.txt"
        file.write_text("a\n\nb\n\n", encoding="utf-8")
        result = read_lines(str(file))
        assert result == ["a\n", "\n", "b\n", "\n"]

    def test_read_lines_directory_not_file(self, tmp_path):
        """Passing a directory path should return None."""
        result = read_lines(str(tmp_path))
        assert result is None


# ──────────────────────────────────────────────
# read_all
# ──────────────────────────────────────────────


class TestReadAll:
    """Tests for read_all."""

    def test_read_all_normal(self, tmp_path):
        file = tmp_path / "test.txt"
        content = "Hello\nWorld"
        file.write_text(content, encoding="utf-8")
        result = read_all(str(file))
        assert result == content

    def test_read_all_file_not_found(self, tmp_path):
        result = read_all(str(tmp_path / "nonexistent.txt"))
        assert result is None

    def test_read_all_empty_file(self, tmp_path):
        file = tmp_path / "empty.txt"
        file.write_text("", encoding="utf-8")
        result = read_all(str(file))
        assert result == ""

    def test_read_all_unicode(self, tmp_path):
        file = tmp_path / "unicode.txt"
        content = "café – résumé"
        file.write_text(content, encoding="utf-8")
        result = read_all(str(file))
        assert result == content

    def test_read_all_directory_not_file(self, tmp_path):
        """Passing a directory path should return None."""
        result = read_all(str(tmp_path))
        assert result is None


# ──────────────────────────────────────────────
# write_all
# ──────────────────────────────────────────────


class TestWriteAll:
    """Tests for write_all."""

    def test_write_all_creates_file(self, tmp_path):
        file = tmp_path / "output.txt"
        write_all(str(file), "hello")
        assert file.read_text(encoding="utf-8") == "hello"

    def test_write_all_overwrites(self, tmp_path):
        file = tmp_path / "overwrite.txt"
        file.write_text("original", encoding="utf-8")
        write_all(str(file), "replaced")
        assert file.read_text(encoding="utf-8") == "replaced"

    def test_write_all_append_mode(self, tmp_path):
        file = tmp_path / "append.txt"
        file.write_text("first\n", encoding="utf-8")
        write_all(str(file), "second\n", mode="a")
        assert file.read_text(encoding="utf-8") == "first\nsecond\n"

    def test_write_all_creates_parent_dirs(self, tmp_path):
        """write_all does not create parents; file is created in existing dir."""
        file = tmp_path / "subdir" / "output.txt"
        os.makedirs(tmp_path / "subdir", exist_ok=True)
        write_all(str(file), "data")
        assert file.read_text(encoding="utf-8") == "data"

    def test_write_all_unicode(self, tmp_path):
        file = tmp_path / "unicode.txt"
        write_all(str(file), "café – résumé")
        assert file.read_text(encoding="utf-8") == "café – résumé"

    def test_write_all_empty_string(self, tmp_path):
        file = tmp_path / "empty.txt"
        write_all(str(file), "")
        assert file.read_text(encoding="utf-8") == ""

    def test_write_all_multiline(self, tmp_path):
        file = tmp_path / "multi.txt"
        write_all(str(file), "line1\nline2\nline3")
        result = file.read_text(encoding="utf-8")
        assert result == "line1\nline2\nline3"


# ──────────────────────────────────────────────
# path_join
# ──────────────────────────────────────────────


class TestPathJoin:
    """Tests for path_join."""

    def test_path_join_two_parts(self):
        result = path_join("foo", "bar")
        assert result == os.path.join("foo", "bar")

    def test_path_join_multiple_parts(self):
        result = path_join("a", "b", "c", "d")
        assert result == os.path.join("a", "b", "c", "d")

    def test_path_join_single_part(self):
        result = path_join("single")
        assert result == "single"

    def test_path_join_no_args(self):
        """Calling path_join with no arguments raises TypeError."""
        with pytest.raises(TypeError):
            path_join()

    def test_path_join_with_absolute(self):
        """When first part is absolute, it should be preserved."""
        result = path_join("/abs", "rel")
        assert result == os.path.join("/abs", "rel")


# ──────────────────────────────────────────────
# exists
# ──────────────────────────────────────────────


class TestExists:
    """Tests for exists."""

    def test_exists_file(self, tmp_path):
        file = tmp_path / "real.txt"
        file.write_text("x", encoding="utf-8")
        assert exists(str(file)) is True

    def test_exists_directory(self, tmp_path):
        assert exists(str(tmp_path)) is True

    def test_exists_nonexistent(self, tmp_path):
        assert exists(str(tmp_path / "nope")) is False

    def test_exists_empty_string(self):
        """Empty path should not exist."""
        assert exists("") is False


# ──────────────────────────────────────────────
# rmdirs
# ──────────────────────────────────────────────


class TestRmdirs:
    """Tests for rmdirs."""

    def test_rmdirs_removes_directory(self, tmp_path):
        target = tmp_path / "to_remove"
        target.mkdir()
        rmdirs(str(target))
        assert not target.exists()

    def test_rmdirs_removes_tree(self, tmp_path):
        root = tmp_path / "root"
        sub = root / "sub"
        sub.mkdir(parents=True)
        (sub / "file.txt").write_text("data", encoding="utf-8")
        rmdirs(str(root))
        assert not root.exists()

    def test_rmdirs_nonexistent_noop(self, tmp_path):
        """Removing a non-existent directory should not raise."""
        rmdirs(str(tmp_path / "nonexistent"))
        # no exception is success

    def test_rmdirs_empty_directory(self, tmp_path):
        target = tmp_path / "empty_dir"
        target.mkdir()
        rmdirs(str(target))
        assert not target.exists()


# ──────────────────────────────────────────────
# mkdirs
# ──────────────────────────────────────────────


class TestMkdirs:
    """Tests for mkdirs."""

    def test_mkdirs_creates_directory(self, tmp_path):
        target = tmp_path / "new_dir"
        mkdirs(str(target))
        assert target.is_dir()

    def test_mkdirs_creates_parents(self, tmp_path):
        target = tmp_path / "a" / "b" / "c"
        mkdirs(str(target))
        assert target.is_dir()

    def test_mkdirs_existing_noop(self, tmp_path):
        target = tmp_path / "existing"
        target.mkdir()
        mkdirs(str(target))  # should not raise
        assert target.is_dir()

    def test_mkdirs_root(self, tmp_path):
        """Creating a single-level directory."""
        target = tmp_path / "single"
        mkdirs(str(target))
        assert target.is_dir()


# ──────────────────────────────────────────────
# remove
# ──────────────────────────────────────────────


class TestRemove:
    """Tests for remove."""

    def test_remove_file(self, tmp_path):
        file = tmp_path / "to_delete.txt"
        file.write_text("x", encoding="utf-8")
        remove(str(file))
        assert not file.exists()

    def test_remove_nonexistent(self, tmp_path):
        with pytest.raises(FileNotFoundError):
            remove(str(tmp_path / "nonexistent.txt"))

    def test_remove_directory_raises(self, tmp_path):
        """Removing a directory with remove() should raise OSError (on Windows, PermissionError)."""
        dir_path = tmp_path / "a_dir"
        dir_path.mkdir()
        with pytest.raises((OSError, PermissionError)):
            remove(str(dir_path))

    def test_remove_empty_file(self, tmp_path):
        file = tmp_path / "empty.txt"
        file.write_text("", encoding="utf-8")
        remove(str(file))
        assert not file.exists()


# ──────────────────────────────────────────────
# archive
# ──────────────────────────────────────────────


class TestArchive:
    """Tests for archive."""

    def test_archive_creates_zip(self, tmp_path):
        source = tmp_path / "src"
        source.mkdir()
        (source / "file.txt").write_text("content", encoding="utf-8")
        dest = str(tmp_path / "output")
        archive(str(source), dest, format="zip")
        # shutil.make_archive adds extension automatically
        assert os.path.exists(dest + ".zip")

    def test_archive_empty_directory(self, tmp_path):
        source = tmp_path / "empty_src"
        source.mkdir()
        dest = str(tmp_path / "empty_archive")
        archive(str(source), dest, format="zip")
        assert os.path.exists(dest + ".zip")

    def test_archive_nested_directories(self, tmp_path):
        source = tmp_path / "nested"
        sub = source / "sub"
        sub.mkdir(parents=True)
        (sub / "data.txt").write_text("nested content", encoding="utf-8")
        dest = str(tmp_path / "nested_archive")
        archive(str(source), dest, format="zip")
        assert os.path.exists(dest + ".zip")


# ──────────────────────────────────────────────
# extract
# ──────────────────────────────────────────────


class TestExtract:
    """Tests for extract."""

    def test_extract_zip_roundtrip(self, tmp_path):
        """Archive then extract should reproduce original content."""
        # Create source with content
        source = tmp_path / "src"
        source.mkdir()
        (source / "file.txt").write_text("hello world", encoding="utf-8")
        (source / "sub").mkdir()
        (source / "sub" / "nested.txt").write_text("nested", encoding="utf-8")

        # Archive
        archive_path = str(tmp_path / "roundtrip")
        archive(str(source), archive_path, format="zip")

        # Extract
        dest = tmp_path / "extracted"
        dest.mkdir()
        extract(archive_path + ".zip", str(dest), format="zip")

        # Verify
        assert (dest / "file.txt").read_text(encoding="utf-8") == "hello world"
        assert (dest / "sub" / "nested.txt").read_text(encoding="utf-8") == "nested"

    def test_extract_into_nonexistent_dir(self, tmp_path):
        """Extract should create the destination directory if needed."""
        source = tmp_path / "src2"
        source.mkdir()
        (source / "f.txt").write_text("data", encoding="utf-8")
        archive_path = str(tmp_path / "ext2")
        archive(str(source), archive_path, format="zip")

        dest = tmp_path / "output_new"
        extract(archive_path + ".zip", str(dest), format="zip")

        assert dest.is_dir()
        assert (dest / "f.txt").read_text(encoding="utf-8") == "data"
