"""Tests for the process management utilities module."""

import time
from unittest.mock import patch, MagicMock, call

import pytest
import psutil

from wolth.util.processes import kill, kill_process_tree


# ──────────────────────────────────────────────
# kill_process_tree
# ──────────────────────────────────────────────


class TestKillProcessTree:
    """Tests for kill_process_tree."""

    def _make_parent_mock(self, children=None):
        """Helper to create a parent mock with child mocks."""
        parent = MagicMock()
        parent.children.return_value = children or []
        return parent

    @patch("wolth.util.processes.psutil.Process")
    def test_kill_process_tree_force(self, mock_process_class):
        """Force kill terminates children then parent."""
        child1 = MagicMock()
        child2 = MagicMock()
        parent = self._make_parent_mock([child1, child2])
        mock_process_class.return_value = parent

        with patch("wolth.util.processes.psutil.wait_procs", return_value=([], [])):
            kill_process_tree(1234, force=True)

        parent.children.assert_called_once_with(recursive=True)
        child1.kill.assert_called_once()
        child2.kill.assert_called_once()
        parent.kill.assert_called_once()

    @patch("wolth.util.processes.psutil.Process")
    def test_kill_process_tree_graceful(self, mock_process_class):
        """Graceful kill terminates children then parent."""
        child = MagicMock()
        parent = self._make_parent_mock([child])
        mock_process_class.return_value = parent

        with patch("wolth.util.processes.psutil.wait_procs", return_value=([child], [])):
            kill_process_tree(1234, force=False)

        child.terminate.assert_called_once()
        parent.terminate.assert_called_once()

    @patch("wolth.util.processes.psutil.Process")
    def test_kill_process_tree_no_such_process(self, mock_process_class):
        """Should silently return if the process doesn't exist."""
        mock_process_class.side_effect = psutil.NoSuchProcess(9999)
        # Should not raise
        kill_process_tree(9999)

    @patch("wolth.util.processes.psutil.Process")
    def test_kill_process_tree_child_already_gone(self, mock_process_class):
        """Should handle children that disappear during iteration."""
        child = MagicMock()
        child.kill.side_effect = psutil.NoSuchProcess(1111)
        parent = self._make_parent_mock([child])
        mock_process_class.return_value = parent

        with patch("wolth.util.processes.psutil.wait_procs", return_value=([], [])):
            kill_process_tree(1234, force=True)

        child.kill.assert_called_once()  # should not raise

    @patch("wolth.util.processes.psutil.Process")
    def test_kill_process_tree_force_kill_alive_children(self, mock_process_class):
        """Children that don't exit in 3s should be force-killed."""
        child = MagicMock()
        parent = self._make_parent_mock([child])
        mock_process_class.return_value = parent

        with patch("wolth.util.processes.psutil.wait_procs", return_value=([], [child])):
            kill_process_tree(1234, force=False)

        # child was terminated but didn't exit, so force-killed
        child.terminate.assert_called_once()
        child.kill.assert_called_once()

    @patch("wolth.util.processes.psutil.Process")
    def test_kill_process_tree_parent_timeout_then_force(self, mock_process_class):
        """If parent.wait() times out, it should be force-killed."""
        parent = self._make_parent_mock([])
        parent.wait.side_effect = psutil.TimeoutExpired(seconds=3, pid=1234)
        mock_process_class.return_value = parent

        with patch("wolth.util.processes.psutil.wait_procs", return_value=([], [])):
            kill_process_tree(1234, force=False)

        parent.terminate.assert_called_once()
        parent.kill.assert_called_once()


# ──────────────────────────────────────────────
# kill
# ──────────────────────────────────────────────


class TestKill:
    """Tests for kill."""

    @patch("wolth.util.processes.kill_process_tree")
    @patch("wolth.util.processes.psutil.pid_exists")
    def test_kill_process_exits_in_time(self, mock_pid_exists, mock_kill_tree):
        """Process exits before timeout, no force needed."""
        mock_pid_exists.side_effect = [True, False]  # exists then gone

        kill(1234, timeout=5)

        mock_kill_tree.assert_has_calls([call(1234, force=False)])
        assert mock_kill_tree.call_count == 1

    @patch("wolth.util.processes.kill_process_tree")
    @patch("wolth.util.processes.psutil.pid_exists")
    def test_kill_process_timed_out(self, mock_pid_exists, mock_kill_tree):
        """Process doesn't exit in time, so force kill is used."""
        mock_pid_exists.side_effect = [True, True, True, True, True, False]
        # The loop checks pid_exists repeatedly. We need enough True values
        # to simulate the timeout being exceeded.

        def fake_kill_tree(pid, force=False):
            if force:
                # After force kill, pid_exists returns False
                pass

        mock_kill_tree.side_effect = fake_kill_tree

        kill(1234, timeout=0)  # timeout = 0 means immediate force

        # First graceful, then forceful
        mock_kill_tree.assert_has_calls([
            call(1234, force=False),
            call(1234, force=True),
        ])

    @patch("wolth.util.processes.kill_process_tree")
    @patch("wolth.util.processes.psutil.pid_exists")
    def test_kill_with_custom_timeout(self, mock_pid_exists, mock_kill_tree):
        """Custom timeout value is respected."""
        mock_pid_exists.side_effect = [True, True, True, False]

        with patch("wolth.util.processes.time.time") as mock_time:
            mock_time.side_effect = [0, 0.5, 1.0, 1.5]  # within 2s timeout
            kill(1234, timeout=2)

        # Only graceful kill should have been attempted
        mock_kill_tree.assert_called_once_with(1234, force=False)

    @patch("wolth.util.processes.kill_process_tree")
    @patch("wolth.util.processes.psutil.pid_exists")
    def test_kill_pid_as_string(self, mock_pid_exists, mock_kill_tree):
        """PID provided as string should still work."""
        mock_pid_exists.side_effect = [True, False]

        kill("1234", timeout=5)

        mock_kill_tree.assert_called_once_with(1234, force=False)
