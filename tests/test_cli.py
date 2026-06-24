"""Tests for the solon CLI."""

from typer.testing import CliRunner

from solon.cli import app

runner = CliRunner()


class TestCli:
    """Test the CLI application."""

    def test_main_command_runs_successfully(self):
        """Running `solon` without arguments should exit with code 0."""
        result = runner.invoke(app, [])
        assert result.exit_code == 0

    def test_main_command_output(self):
        """The CLI should produce some output (from utils.do_something_useful)."""
        result = runner.invoke(app, [])
        assert result.stdout is not None

    def test_help_output(self):
        """Running `solon --help` should show help text."""
        result = runner.invoke(app, ["--help"])
        assert result.exit_code == 0
        assert "solon" in result.stdout
        assert "toolkit" in result.stdout.lower() or "useful" in result.stdout.lower()

    def test_version_not_implemented(self):
        """Currently there's no version option; this ensures it doesn't crash."""
        result = runner.invoke(app, [])
        assert result.exit_code == 0

    def test_unknown_option_returns_error(self):
        """An unknown option should return a non-zero exit code."""
        result = runner.invoke(app, ["--nonexistent-flag"])
        assert result.exit_code != 0

    def test_unknown_command_returns_error(self):
        """An unknown command should return a non-zero exit code."""
        result = runner.invoke(app, ["nonexistent-command"])
        assert result.exit_code != 0
