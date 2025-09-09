"""
Test module for BashWrapper functionality.

Tests the BashWrapper class and its integration with bash scripts.
"""

import pytest
from pathlib import Path

from classroom_pilot.bash_wrapper import BashWrapper


class TestBashWrapperInitialization:
    """Test BashWrapper initialization."""

    def test_init_with_config(self, test_config):
        """Test BashWrapper initialization with config."""
        wrapper = BashWrapper(test_config)
        assert wrapper.config == test_config
        assert wrapper.dry_run is False
        assert wrapper.verbose is False
        assert wrapper.auto_yes is False

    def test_init_with_flags(self, test_config):
        """Test BashWrapper initialization with flags."""
        wrapper = BashWrapper(
            config=test_config,
            dry_run=True,
            verbose=True,
            auto_yes=True
        )
        assert wrapper.config == test_config
        assert wrapper.dry_run is True
        assert wrapper.verbose is True
        assert wrapper.auto_yes is True


class TestScriptPathResolution:
    """Test script path resolution functionality."""

    def test_get_script_path_existing(self, test_wrapper):
        """Test getting path for existing script."""
        script_path = test_wrapper._get_script_path(
            "assignment-orchestrator.sh")
        assert script_path.exists()
        assert script_path.name == "assignment-orchestrator.sh"

    def test_get_script_path_nonexistent(self, test_wrapper):
        """Test getting path for non-existent script."""
        with pytest.raises(FileNotFoundError):
            test_wrapper._get_script_path("nonexistent-script.sh")


class TestEnvironmentPreparation:
    """Test environment variable preparation."""

    def test_prepare_environment_basic(self, test_wrapper):
        """Test basic environment preparation."""
        env = test_wrapper._prepare_environment()

        # Check wrapper-specific variables
        assert env.get('DRY_RUN') == 'true'
        assert env.get('VERBOSE') == 'true'
        assert env.get('AUTO_YES') == 'true'

        # Check config variables are present
        assert 'CLASSROOM_URL' in env
        assert 'GITHUB_ORGANIZATION' in env

    def test_prepare_environment_no_flags(self, test_config):
        """Test environment preparation without flags."""
        wrapper = BashWrapper(test_config, dry_run=False,
                              verbose=False, auto_yes=False)
        env = wrapper._prepare_environment()

        # These should not be set
        assert 'DRY_RUN' not in env
        assert 'VERBOSE' not in env
        assert 'AUTO_YES' not in env


class TestWorkflowMethods:
    """Test main workflow methods."""

    def test_assignment_orchestrator(self, test_wrapper):
        """Test assignment orchestrator method."""
        result = test_wrapper.assignment_orchestrator("run")
        assert result is True  # Should succeed in dry-run mode

    def test_push_to_classroom(self, test_wrapper):
        """Test push to classroom method."""
        result = test_wrapper.push_to_classroom()
        assert result is True

    def test_fetch_student_repos(self, test_wrapper):
        """Test fetch student repos method."""
        result = test_wrapper.fetch_student_repos()
        assert result is True

    def test_add_secrets_to_students(self, test_wrapper):
        """Test add secrets to students method."""
        result = test_wrapper.add_secrets_to_students()
        assert result is True

    def test_student_update_helper(self, test_wrapper):
        """Test student update helper method."""
        result = test_wrapper.student_update_helper()
        assert result is True


class TestManagementMethods:
    """Test assignment management methods."""

    def test_setup_assignment(self, test_wrapper):
        """Test setup assignment method."""
        result = test_wrapper.setup_assignment()
        assert result is True

    def test_update_assignment(self, test_wrapper):
        """Test update assignment method."""
        result = test_wrapper.update_assignment()
        assert result is True

    def test_manage_cron(self, test_wrapper):
        """Test manage cron method."""
        result = test_wrapper.manage_cron("status")
        assert result is True

    def test_cron_sync(self, test_wrapper):
        """Test cron sync method."""
        result = test_wrapper.cron_sync()
        assert result is True


class TestCycleCollaborator:
    """Test cycle collaborator functionality."""

    def test_cycle_collaborator_list_mode(self, test_wrapper):
        """Test cycle collaborator in list mode."""
        result = test_wrapper.cycle_collaborator(
            assignment_prefix="test-assignment",
            list_mode=True
        )
        assert result is True

    def test_cycle_collaborator_single_user(self, test_wrapper):
        """Test cycle collaborator for single user."""
        result = test_wrapper.cycle_collaborator(
            assignment_prefix="homework01",
            username="student123",
            organization="cs101",
            force_cycle=True
        )
        assert result is True

    def test_cycle_collaborator_batch_mode(self, test_wrapper):
        """Test cycle collaborator in batch mode."""
        result = test_wrapper.cycle_collaborator(
            batch_file="/tmp/batch.txt",
            repo_url_mode=True
        )
        assert result is True

    def test_cycle_collaborator_minimal_args(self, test_wrapper):
        """Test cycle collaborator with minimal arguments."""
        result = test_wrapper.cycle_collaborator(repo_url_mode=True)
        assert result is True
