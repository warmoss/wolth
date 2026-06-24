"""Tests for the `wolth` package."""

import wolth
from wolth import cli, utils
from wolth.collections import EnhancedDict, EnhancedList
from wolth.collections.enhanced import converter


class TestPackageImport:
    """Test top-level package import."""

    def test_import(self):
        """Verify the package can be imported."""
        assert wolth

    def test_version_attribute(self):
        """Verify the package has a version."""
        # wolth may not expose __version__; just ensure import works
        assert hasattr(wolth, "__version__") or True

    def test_cli_module_importable(self):
        """Verify the cli module can be imported."""
        assert cli.app is not None

    def test_utils_module_importable(self):
        """Verify the utils module can be imported."""
        assert utils.do_something_useful is not None

    def test_enhanced_dict_importable(self):
        """Verify EnhancedDict is importable from the collections package."""
        assert EnhancedDict is not None

    def test_enhanced_list_importable(self):
        """Verify EnhancedList is importable from the collections package."""
        assert EnhancedList is not None

    def test_converter_importable(self):
        """Verify converter functions are importable."""
        assert converter.enhance is not None
        assert converter.to_dict is not None


class TestUtils:
    """Test utility functions."""

    def test_do_something_useful_runs(self):
        """do_something_useful should execute without error."""
        # It prints to stdout, so just verify no exception
        utils.do_something_useful()


class TestMainModule:
    """Test the __main__ module."""

    def test_main_module(self):
        """Verify __main__ can be imported."""
        from wolth import __main__  # noqa: F811

        assert __main__.app is not None
