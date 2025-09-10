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
        # First, try to verify the module can be imported
        try:
            import classroom_pilot.cli
            module_importable = True
        except ImportError as e:
            module_importable = False
            print(f"Module import failed: {e}")

        assert module_importable, "classroom_pilot.cli module could not be imported"

        # Use sys.executable to ensure we're using the same Python interpreter
        cmd = f"{sys.executable} -m classroom_pilot --help"
        success, stdout, stderr = run_cli_command(cmd)

        # Enhanced error reporting for debugging CI issues
        if not success:
            print(f"\n=== DEBUG INFO ===")
            print(f"Command: {cmd}")
            print(f"Return code: NON-ZERO")
            print(f"STDERR:\n{stderr}")
            print(f"STDOUT:\n{stdout}")
            print(f"Working directory: {Path.cwd()}")
            print(f"Python executable: {sys.executable}")

            # Try alternative execution methods
            try:
                import classroom_pilot.__main__
                print("__main__ module exists")
            except Exception as e:
                print(f"__main__ import failed: {e}")

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
        # First, try to verify the module can be imported
        try:
            import classroom_pilot.cli
            module_importable = True
        except ImportError as e:
            module_importable = False
            print(f"Module import failed: {e}")

        assert module_importable, "classroom_pilot.cli module could not be imported"

        # Use sys.executable to ensure we're using the same Python interpreter
        cmd = f"{sys.executable} -m classroom_pilot --help"
        success, stdout, stderr = run_cli_command(cmd)

        # Enhanced error reporting for debugging CI issues
        if not success:
            print(f"\n=== DEBUG INFO ===")
            print(f"Command: {cmd}")
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
            "python -m classroom_pilot run --dry-run --verbose")
        assert success, f"Run command failed: {stderr}"
        # Dry run message appears in stderr from logger
        assert "[DRY RUN]" in stderr

    def test_sync_command_dry_run(self):
        """Test the repo push command (sync equivalent) in dry-run mode."""
        success, stdout, stderr = run_cli_command(
            "python -m classroom_pilot repos push --dry-run --verbose")
        assert success, f"Repo push command failed: {stderr}"
        # Dry run message appears in stderr from logger
        assert "[DRY RUN]" in stderr

    def test_discover_command_dry_run(self):
        """Test the repo fetch command (discover equivalent) in dry-run mode."""
        success, stdout, stderr = run_cli_command(
            "python -m classroom_pilot repos fetch --dry-run --verbose")
        assert success, f"Repo fetch command failed: {stderr}"
        # Dry run message appears in stderr from logger
        assert "[DRY RUN]" in stderr

    def test_secrets_command_dry_run(self):
        """Test the secrets add command in dry-run mode."""
        success, stdout, stderr = run_cli_command(
            "python -m classroom_pilot secrets add --dry-run --verbose")
        assert success, f"Secrets add command failed: {stderr}"
        # Dry run message appears in stderr from logger
        assert "[DRY RUN]" in stderr

    def test_assist_command_dry_run(self):
        """Test the assignment orchestrate command (full workflow) in dry-run mode."""
        success, stdout, stderr = run_cli_command(
            "python -m classroom_pilot assignments orchestrate --dry-run --verbose")
        assert success, f"Assignment orchestrate command failed: {stderr}"
        # Dry run message appears in stderr from logger
        assert "[DRY RUN]" in stderr


class TestManagementCommands:
    """Test assignment management commands."""

    def test_setup_command_help(self):
        """Test the new Python setup command help."""
        success, stdout, stderr = run_cli_command(
            "python -m classroom_pilot setup --help")
        assert success, f"Setup help command failed: {stderr}"
        assert "Interactive Python wizard" in stdout

    def test_assignment_setup_command_help(self):
        """Test the assignment setup command help."""
        success, stdout, stderr = run_cli_command(
            "python -m classroom_pilot assignments setup --help")
        assert success, f"Assignment setup help command failed: {stderr}"
        assert "Interactive Python wizard" in stdout

    def test_update_command_dry_run(self):
        """Test the repos update command in dry-run mode."""
        success, stdout, stderr = run_cli_command(
            "python -m classroom_pilot repos update --dry-run --verbose")
        assert success, f"Update command failed: {stderr}"
        # Dry run message appears in stderr from logger
        assert "[DRY RUN]" in stderr

    def test_cron_status_dry_run(self):
        """Test the cron status command in dry-run mode."""
        success, stdout, stderr = run_cli_command(
            "python -m classroom_pilot automation cron --dry-run --verbose --action status")
        assert success, f"Cron status command failed: {stderr}"
        # Dry run message appears in stderr from logger
        assert "[DRY RUN]" in stderr

    def test_cron_sync_dry_run(self):
        """Test the automation sync command in dry-run mode."""
        success, stdout, stderr = run_cli_command(
            "python -m classroom_pilot automation sync --dry-run --verbose")
        assert success, f"Automation sync command failed: {stderr}"
        # Dry run message appears in stderr from logger
        assert "[DRY RUN]" in stderr


class TestCycleCommands:
    """Test collaborator cycling commands."""

    def test_cycle_list_mode(self):
        """Test cycle-collaborator command in dry-run mode."""
        success, stdout, stderr = run_cli_command(
            "python -m classroom_pilot repos cycle-collaborator --dry-run --verbose")
        assert success, f"Cycle collaborator command failed: {stderr}"
        # Dry run message appears in stderr from logger
        assert "[DRY RUN]" in stderr

    def test_cycle_force_mode(self):
        """Test cycle-collaborator command help."""
        success, stdout, stderr = run_cli_command(
            "python -m classroom_pilot repos cycle-collaborator --help")
        assert success, f"Cycle collaborator help command failed: {stderr}"
        assert "Cycle repository collaborator" in stdout

    def test_cycle_repo_urls_mode(self):
        """Test cycle-collaborator with verbose dry-run mode."""
        success, stdout, stderr = run_cli_command(
            "python -m classroom_pilot repos cycle-collaborator --dry-run --verbose")
        assert success, f"Cycle collaborator verbose command failed: {stderr}"
        # Dry run message appears in stderr from logger
        assert "[DRY RUN]" in stderr
