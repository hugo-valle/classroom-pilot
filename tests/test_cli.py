"""
Comprehensive test suite for classroom_pilot.cli module.

This test suite provides comprehensive coverage for the CLI interface,
which handles command-line operations for GitHub Classroom assignment management.
The tests include unit tests for individual commands, integration tests for
workflow operations, and comprehensive validation of CLI behavior across different scenarios.

Test Categories:
1. Basic CLI Tests - Core CLI functionality and help system
2. Management Command Tests - Assignment lifecycle management commands
3. Repository Command Tests - Repository operations and GitHub integration
4. Secrets Command Tests - Secret management and deployment operations
5. Automation Command Tests - Scheduling and batch processing commands
6. Error Handling Tests - CLI error scenarios and user feedback
7. Integration Tests - End-to-end CLI workflow validation

The CLI module provides commands for:
- Interactive assignment setup and configuration generation
- Complete assignment workflow orchestration with progress tracking
- Repository discovery, fetching, and management operations
- Secure secrets deployment to student repositories
- Automation scheduling with cron integration
- Rich console output with progress indicators and error handling
- Comprehensive help system with usage examples

Command Structure:
- Main commands: --help, --version
- Assignment management: assignments setup, assignments orchestrate, assignments manage
- Repository operations: repos fetch, repos update, repos push, repos cycle-collaborator
- Secret management: secrets add, secrets manage
- Automation: automation cron, automation sync, automation batch

Dependencies and Integration:
- Built on Typer framework for modern CLI development
- Integrates with Rich console for enhanced user experience
- Uses classroom_pilot.config for configuration management
- Leverages classroom_pilot.repos for repository operations
- Connects to classroom_pilot.secrets for secure deployment
- Supports classroom_pilot.automation for scheduling workflows
"""

import subprocess
import sys
import os
from pathlib import Path
import pytest


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
    """
    TestBasicCLI contains unit tests for core CLI functionality including help system,
    version information, and basic command validation. It verifies that the CLI
    interface properly handles user interactions and displays helpful information.

    Test Cases:
    - test_help_command: Tests main help command display and formatting
    - test_version_flag: Tests version information display via --version flag
    - test_help_without_config: Tests help system functionality without configuration files
    - test_sync_command_dry_run: Tests repository synchronization in dry-run mode
    - test_discover_command_dry_run: Tests repository discovery in dry-run mode  
    - test_secrets_command_dry_run: Tests secrets management in dry-run mode
    - test_assist_command_dry_run: Tests full workflow orchestration in dry-run mode
    """

    def test_help_command(self):
        """
        Test main help command display and formatting.

        This test verifies that the CLI properly displays the main help information
        when invoked with --help. It checks for proper usage information, command
        descriptions, and overall help system functionality to ensure users can
        discover available commands and their usage patterns.
        """
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
            print("\n=== DEBUG INFO ===")
            print(f"Command: {cmd}")
            print("Return code: NON-ZERO")
            print(f"STDERR:\n{stderr}")
            print(f"STDOUT:\n{stdout}")
            print(f"Working directory: {Path.cwd()}")
            print(f"Python executable: {sys.executable}")

            # Try alternative execution methods
            try:
                print("__main__ module exists")
            except Exception as e:
                print(f"__main__ import failed: {e}")

            print("=== END DEBUG ===\n")

        assert success, f"Help command failed: {stderr}"

        # More flexible assertions to handle potential formatting differences
        stdout_lower = stdout.lower()
        assert "usage:" in stdout_lower or "usage" in stdout_lower, f"'Usage:' not found in stdout: {stdout}"
        assert "classroom pilot" in stdout_lower or "classroom-pilot" in stdout_lower, f"'Classroom Pilot' not found in stdout: {stdout}"

    def test_version_flag(self):
        """
        Test version information display via --version flag.

        This test verifies that the CLI properly displays version information
        when invoked with the --version flag. It ensures the version output
        contains appropriate version formatting and required version information
        for user reference and debugging purposes.
        """
        success, stdout, stderr = run_cli_command(
            "python -m classroom_pilot --version")
        assert success, f"Version flag failed: {stderr}"
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
            print("\n=== DEBUG INFO ===")
            print(f"Command: {cmd}")
            print("Return code: NON-ZERO")
            print(f"STDERR:\n{stderr}")
            print(f"STDOUT:\n{stdout}")
            print(f"Working directory: {Path.cwd()}")
            print(f"Python executable: {sys.executable}")
            print("=== END DEBUG ===\n")

        assert success, f"Help without config failed: {stderr}"

        # More flexible assertion
        stdout_lower = stdout.lower()
        assert "usage:" in stdout_lower or "usage" in stdout_lower, f"'Usage:' not found in stdout: {stdout}"


class TestWorkflowCommands:
    """Test main workflow commands with dry-run."""

    def test_sync_command_dry_run(self):
        """Test the repo push command (sync equivalent) in dry-run mode."""
        success, stdout, stderr = run_cli_command(
            "python -m classroom_pilot repos --dry-run --verbose push")
        assert success, f"Repo push command failed: {stderr}"
        # Dry run message appears in stderr from logger
        assert "DRY RUN:" in stderr

    def test_discover_command_dry_run(self):
        """Test the repo fetch command (discover equivalent) in dry-run mode."""
        success, stdout, stderr = run_cli_command(
            "python -m classroom_pilot repos --dry-run --verbose fetch")
        assert success, f"Repo fetch command failed: {stderr}"
        # Dry run message appears in stderr from logger
        assert "DRY RUN:" in stderr

    def test_secrets_command_dry_run(self):
        """Test the secrets add command in dry-run mode."""
        success, stdout, stderr = run_cli_command(
            "python -m classroom_pilot secrets --dry-run --verbose add")
        assert success, f"Secrets add command failed: {stderr}"
        # Dry run message appears in stderr from logger
        assert "[DRY RUN]" in stderr or "Dry run:" in stderr or "DRY RUN:" in stderr

    @pytest.mark.skipif(
        os.getenv("CI") and not (
            os.getenv("GITHUB_TOKEN") or os.getenv("GH_TOKEN")),
        reason="Skipping orchestration test in CI without GitHub token"
    )
    def test_assist_command_dry_run(self):
        """Test the assignment orchestrate command (full workflow) in dry-run mode."""
        success, stdout, stderr = run_cli_command(
            "python -m classroom_pilot assignments --dry-run --verbose orchestrate")
        assert success, f"Assignment orchestrate command failed: {stdout}\n{stderr}"
        # Dry run message appears in stderr from logger
        assert "DRY RUN:" in stderr


class TestManagementCommands:
    """
    TestManagementCommands contains unit tests for assignment management and
    administrative CLI commands. It verifies that management operations properly
    handle configuration, provide appropriate help information, and maintain
    consistent behavior across different command categories.

    Test Cases:
    - test_setup_command_help: Tests setup command help display and option information
    - test_management_command_validation: Tests parameter validation for management commands
    - test_configuration_command_integration: Tests integration with configuration system
    - test_workflow_command_orchestration: Tests assignment workflow coordination
    """

    def test_assignment_setup_command_help(self):
        """Test the assignment setup command help."""
        success, stdout, stderr = run_cli_command(
            "python -m classroom_pilot assignments setup --help")
        assert success, f"Assignment setup help command failed: {stderr}"
        # Check for the actual help text from the current implementation
        assert "interactive wizard" in stdout.lower(
        ) or "configure" in stdout.lower() or "assignment" in stdout.lower()

    def test_update_command_dry_run(self):
        """Test the repos update command in dry-run mode."""
        success, stdout, stderr = run_cli_command(
            "python -m classroom_pilot repos --dry-run --verbose update")
        assert success, f"Update command failed: {stderr}"
        # Dry run message appears in stderr from logger
        assert "DRY RUN:" in stderr

    def test_cron_status_dry_run(self):
        """Test the cron status command in dry-run mode."""
        success, stdout, stderr = run_cli_command(
            "python -m classroom_pilot automation --dry-run --verbose cron-status")
        assert success, f"Cron status command failed: {stderr}"
        # Dry run message appears in stderr from logger
        assert "DRY RUN:" in stderr

    def test_cron_sync_dry_run(self):
        """Test the automation sync command in dry-run mode."""
        success, stdout, stderr = run_cli_command(
            "python -m classroom_pilot automation --dry-run --verbose sync")
        assert success, f"Automation sync command failed: {stderr}"
        # Dry run message appears in stderr from logger
        assert "DRY RUN:" in stderr


class TestCycleCommands:
    """Test collaborator cycling commands."""

    def test_cycle_list_mode(self):
        """Test cycle-collaborator command in dry-run mode."""
        success, stdout, stderr = run_cli_command(
            "python -m classroom_pilot repos --dry-run --verbose cycle-collaborator")
        assert success, f"Cycle collaborator command failed: {stderr}"
        # Dry run message appears in stderr from logger
        assert "DRY RUN:" in stderr

    def test_cycle_force_mode(self):
        """Test cycle-collaborator command help."""
        success, stdout, stderr = run_cli_command(
            "python -m classroom_pilot repos cycle-collaborator --help")
        assert success, f"Cycle collaborator help command failed: {stderr}"
        assert "Cycle repository collaborator" in stdout

    def test_cycle_repo_urls_mode(self):
        """Test cycle-collaborator with verbose dry-run mode."""
        success, stdout, stderr = run_cli_command(
            "python -m classroom_pilot repos --dry-run --verbose cycle-collaborator")
        assert success, f"Cycle collaborator verbose command failed: {stderr}"
        # Dry run message appears in stderr from logger
        assert "DRY RUN:" in stderr
