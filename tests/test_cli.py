"""
Test module for CLI functionality.

Tests all CLI commands and their behavior.
"""

import shlex
import subprocess
import sys
from pathlib import Path


def run_cli_command(cmd: str, cwd: Path | None = None) -> tuple[bool, str, str]:
    """Helper function to run CLI commands."""
    try:
        # Split command and use list form for better cross-platform compatibility
        if isinstance(cmd, str):
            import shlex
            cmd_list = shlex.split(cmd)
        else:
            cmd_list = cmd

        # Use current environment but ensure Python path is available
        import os
        env = os.environ.copy()

        result = subprocess.run(
            cmd_list,
            capture_output=True,
            text=True,
            cwd=cwd or Path.cwd(),
            timeout=30,
            env=env
        )
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "Command timed out"
    except Exception as e:
        return False, "", str(e)


class TestBasicCLI:
    """Test basic CLI functionality."""

    def test_help_command(self):
        """Test the main help command."""
        success, stdout, stderr = run_cli_command(
            "python -m classroom_pilot --help")

        # Enhanced error reporting for debugging CI issues
        if not success:
            print(f"\n=== DEBUG INFO ===")
            print(f"Command: python -m classroom_pilot --help")
            print(f"Return code: NON-ZERO")
            print(f"STDERR:\n{stderr}")
            print(f"STDOUT:\n{stdout}")
            print(f"Working directory: {Path.cwd()}")
            print(f"Python executable: {sys.executable}")
            print(f"=== END DEBUG ===\n")

        assert success, f"Help command failed: {stderr}"

        # More flexible assertions to handle potential formatting differences
        stdout_lower = stdout.lower()
        assert "usage:" in stdout_lower or "usage" in stdout_lower, f"'Usage:' not found in stdout: {stdout}"
        assert "classroom pilot" in stdout_lower or "classroom-pilot" in stdout_lower, f"'Classroom Pilot' not found in stdout: {stdout}"

    def test_version_command(self):
        """Test the version command."""
        success, stdout, stderr = run_cli_command(
            "python -m classroom_pilot version")
        assert success, f"Version command failed: {stderr}"
        assert "v" in stdout.lower() or "version" in stdout.lower()

    def test_help_without_config(self):
        """Test help works without configuration file."""
        success, stdout, stderr = run_cli_command(
            "python -m classroom_pilot --help")

        # Enhanced error reporting for debugging CI issues
        if not success:
            print(f"\n=== DEBUG INFO ===")
            print(f"Command: python -m classroom_pilot --help")
            print(f"Return code: NON-ZERO")
            print(f"STDERR:\n{stderr}")
            print(f"STDOUT:\n{stdout}")
            print(f"Working directory: {Path.cwd()}")
            print(f"Python executable: {sys.executable}")
            print(f"=== END DEBUG ===\n")

        assert success, f"Help without config failed: {stderr}"

        # More flexible assertion
        stdout_lower = stdout.lower()
        assert "usage:" in stdout_lower or "usage" in stdout_lower, f"'Usage:' not found in stdout: {stdout}"


class TestWorkflowCommands:
    """Test main workflow commands with dry-run."""

    def test_run_command_dry_run(self):
        """Test the run command in dry-run mode."""
        success, stdout, stderr = run_cli_command(
            "python -m classroom_pilot --dry-run --verbose run")
        assert success, f"Run command failed: {stderr}"
        assert "DRY RUN" in stdout
        assert "completed successfully" in stdout

    def test_sync_command_dry_run(self):
        """Test the sync command in dry-run mode."""
        success, stdout, stderr = run_cli_command(
            "python -m classroom_pilot --dry-run --verbose sync")
        assert success, f"Sync command failed: {stderr}"
        assert "DRY RUN" in stdout

    def test_discover_command_dry_run(self):
        """Test the discover command in dry-run mode."""
        success, stdout, stderr = run_cli_command(
            "python -m classroom_pilot --dry-run --verbose discover")
        assert success, f"Discover command failed: {stderr}"
        assert "DRY RUN" in stdout

    def test_secrets_command_dry_run(self):
        """Test the secrets command in dry-run mode."""
        success, stdout, stderr = run_cli_command(
            "python -m classroom_pilot --dry-run --verbose secrets")
        assert success, f"Secrets command failed: {stderr}"
        assert "DRY RUN" in stdout

    def test_assist_command_dry_run(self):
        """Test the assist command in dry-run mode."""
        success, stdout, stderr = run_cli_command(
            "python -m classroom_pilot --dry-run --verbose assist")
        assert success, f"Assist command failed: {stderr}"
        assert "DRY RUN" in stdout


class TestManagementCommands:
    """Test assignment management commands."""

    def test_setup_command_dry_run(self):
        """Test the setup command in dry-run mode."""
        success, stdout, stderr = run_cli_command(
            "python -m classroom_pilot --dry-run --verbose setup")
        assert success, f"Setup command failed: {stderr}"
        assert "DRY RUN" in stdout

    def test_update_command_dry_run(self):
        """Test the update command in dry-run mode."""
        success, stdout, stderr = run_cli_command(
            "python -m classroom_pilot --dry-run --verbose update")
        assert success, f"Update command failed: {stderr}"
        assert "DRY RUN" in stdout

    def test_cron_status_dry_run(self):
        """Test the cron status command in dry-run mode."""
        success, stdout, stderr = run_cli_command(
            "python -m classroom_pilot --dry-run --verbose cron status")
        assert success, f"Cron status command failed: {stderr}"
        assert "DRY RUN" in stdout

    def test_cron_sync_dry_run(self):
        """Test the cron-sync command in dry-run mode."""
        success, stdout, stderr = run_cli_command(
            "python -m classroom_pilot --dry-run --verbose cron-sync")
        assert success, f"Cron-sync command failed: {stderr}"
        assert "DRY RUN" in stdout


class TestCycleCommands:
    """Test collaborator cycling commands."""

    def test_cycle_list_mode(self):
        """Test cycle command in list mode."""
        success, stdout, stderr = run_cli_command(
            "python -m classroom_pilot --dry-run cycle --list lab01")
        assert success, f"Cycle list command failed: {stderr}"
        assert "DRY RUN" in stdout

    def test_cycle_force_mode(self):
        """Test cycle command in force mode with user arguments."""
        cmd = "python -m classroom_pilot --dry-run cycle --force homework01 student123 cs101"
        success, stdout, stderr = run_cli_command(cmd)
        assert success, f"Cycle force command failed: {stderr}"
        assert "DRY RUN" in stdout

    def test_cycle_repo_urls_mode(self):
        """Test cycle command with repo-urls flag."""
        success, stdout, stderr = run_cli_command(
            "python -m classroom_pilot --dry-run cycle --repo-urls")
        assert success, f"Cycle repo-urls command failed: {stderr}"
        assert "DRY RUN" in stdout
