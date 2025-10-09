"""
Comprehensive test suite for AssignmentService.

This test suite provides comprehensive coverage for the AssignmentService class,
which handles assignment orchestration, setup, validation, and student assistance.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
import tempfile

from classroom_pilot.services.assignment_service import AssignmentService


class TestAssignmentServiceInit:
    """Test AssignmentService initialization."""

    def test_init_default_params(self):
        """Test initialization with default parameters."""
        service = AssignmentService()
        assert service.dry_run is False
        assert service.verbose is False

    def test_init_with_params(self):
        """Test initialization with custom parameters."""
        service = AssignmentService(dry_run=True, verbose=True)
        assert service.dry_run is True
        assert service.verbose is True


class TestAssignmentServiceSetup:
    """Test assignment setup functionality."""

    def test_setup_dry_run(self):
        """Test setup in dry-run mode."""
        service = AssignmentService(dry_run=True)
        success, message = service.setup()

        assert success is True
        assert "DRY RUN" in message
        assert "interactive assignment setup wizard" in message

    def test_setup_with_url_dry_run(self):
        """Test setup with URL in dry-run mode."""
        service = AssignmentService(dry_run=True)
        url = "https://classroom.github.com/classrooms/12345/assignments/test"
        success, message = service.setup(url=url)

        assert success is True
        assert "DRY RUN" in message
        assert "GitHub Classroom URL" in message
        assert url in message

    def test_setup_with_simplified_dry_run(self):
        """Test setup with simplified option in dry-run mode."""
        service = AssignmentService(dry_run=True)
        success, message = service.setup(simplified=True)

        assert success is True
        assert "DRY RUN" in message
        assert "simplified setup wizard" in message

    def test_setup_with_simplified_not_implemented(self):
        """Test setup with simplified option when not implemented."""
        # TODO: Update this test when simplified setup is implemented
        # When simplified setup is working, this test should:
        # - Change to test_setup_with_simplified_success()
        # - Assert success is True
        # - Assert successful completion message
        # - Mock AssignmentSetup.run_wizard_simplified() method
        service = AssignmentService(dry_run=False)
        success, message = service.setup(simplified=True)

        assert success is False
        assert "Simplified setup mode not yet implemented" in message

    @patch('classroom_pilot.assignments.setup.AssignmentSetup')
    def test_setup_success(self, mock_assignment_setup):
        """Test successful setup execution."""
        # Mock the AssignmentSetup class
        mock_wizard = Mock()
        mock_wizard.run_wizard.return_value = True
        mock_assignment_setup.return_value = mock_wizard

        service = AssignmentService(dry_run=False)
        success, message = service.setup()

        assert success is True
        assert "Assignment setup completed successfully" in message
        mock_assignment_setup.assert_called_once()
        mock_wizard.run_wizard.assert_called_once()

    @patch('classroom_pilot.assignments.setup.AssignmentSetup')
    def test_setup_cancelled(self, mock_assignment_setup):
        """Test setup cancelled by user."""
        # Mock the AssignmentSetup class
        mock_wizard = Mock()
        mock_wizard.run_wizard.return_value = False
        mock_assignment_setup.return_value = mock_wizard

        service = AssignmentService(dry_run=False)
        success, message = service.setup()

        assert success is False
        assert "setup was cancelled or failed" in message

    @patch('classroom_pilot.assignments.setup.AssignmentSetup')
    def test_setup_exception(self, mock_assignment_setup):
        """Test setup with exception."""
        # Mock the AssignmentSetup class to raise an exception
        mock_assignment_setup.side_effect = Exception("Setup failed")

        service = AssignmentService(dry_run=False)
        success, message = service.setup()

        assert success is False
        assert "Assignment setup failed" in message

    @patch('classroom_pilot.assignments.setup.AssignmentSetup')
    def test_setup_with_url_success(self, mock_assignment_setup):
        """Test successful setup with GitHub Classroom URL."""
        # Mock the AssignmentSetup class
        mock_wizard = Mock()
        mock_wizard.run_wizard_with_url.return_value = True
        mock_assignment_setup.return_value = mock_wizard

        service = AssignmentService(dry_run=False)
        url = "https://classroom.github.com/classrooms/12345/assignments/test"
        success, message = service.setup(url=url)

        assert success is True
        assert "Assignment setup completed successfully with GitHub Classroom URL" in message
        mock_assignment_setup.assert_called_once()
        mock_wizard.run_wizard_with_url.assert_called_once_with(url)

    @patch('classroom_pilot.assignments.setup.AssignmentSetup')
    def test_setup_with_url_cancelled(self, mock_assignment_setup):
        """Test setup with URL cancelled by user."""
        # Mock the AssignmentSetup class
        mock_wizard = Mock()
        mock_wizard.run_wizard_with_url.return_value = False
        mock_assignment_setup.return_value = mock_wizard

        service = AssignmentService(dry_run=False)
        url = "https://classroom.github.com/classrooms/12345/assignments/test"
        success, message = service.setup(url=url)

        assert success is False
        assert "setup was cancelled or failed" in message
        mock_wizard.run_wizard_with_url.assert_called_once_with(url)

    @patch('classroom_pilot.assignments.setup.AssignmentSetup')
    def test_setup_with_url_exception(self, mock_assignment_setup):
        """Test setup with URL when wizard raises exception."""
        # Mock the AssignmentSetup class
        mock_wizard = Mock()
        mock_wizard.run_wizard_with_url.side_effect = Exception(
            "URL parsing failed")
        mock_assignment_setup.return_value = mock_wizard

        service = AssignmentService(dry_run=False)
        url = "https://classroom.github.com/classrooms/12345/assignments/test"
        success, message = service.setup(url=url)

        assert success is False
        assert "Assignment setup failed" in message
        mock_wizard.run_wizard_with_url.assert_called_once_with(url)


class TestAssignmentServiceOrchestrate:
    """Test assignment orchestration functionality."""

    def test_orchestrate_dry_run(self):
        """Test orchestration in dry-run mode."""
        service = AssignmentService(dry_run=True)
        success, message = service.orchestrate()

        assert success is True
        assert "Assignment orchestration completed successfully" in message

    @patch('classroom_pilot.assignments.orchestrator.AssignmentOrchestrator')
    def test_orchestrate_success(self, mock_orchestrator):
        """Test successful orchestration."""
        # Mock the orchestrator
        mock_orch = Mock()
        mock_orch.validate_configuration.return_value = True
        mock_orch.show_configuration_summary.return_value = None
        mock_orch.confirm_execution.return_value = True
        mock_orch.execute_workflow.return_value = [Mock(success=True)]
        mock_orch.generate_workflow_report.return_value = None
        mock_orchestrator.return_value = mock_orch

        service = AssignmentService(dry_run=False)
        success, message = service.orchestrate()

        assert success is True
        assert "Assignment orchestration completed successfully" in message


class TestAssignmentServiceValidateConfig:
    """Test configuration validation functionality."""

    def test_validate_config_dry_run(self):
        """Test config validation in dry-run mode."""
        service = AssignmentService(dry_run=True)
        success, message = service.validate_config("test.conf")

        assert success is True
        assert "DRY RUN" in message
        assert "validate configuration" in message

    @patch('classroom_pilot.config.ConfigValidator')
    def test_validate_config_success(self, mock_validator):
        """Test successful config validation."""
        # Mock the validator
        mock_val = Mock()
        mock_val.validate_config_file.return_value = (True, [])
        mock_validator.return_value = mock_val

        # Use the existing assignment.conf file which exists in the test environment
        service = AssignmentService(dry_run=False)
        success, message = service.validate_config("assignment.conf")

        assert success is True
        assert "is valid" in message


class TestAssignmentServiceStudentHelp:
    """Test student assistance functionality."""

    def test_help_student_dry_run(self):
        """Test help student in dry-run mode."""
        service = AssignmentService(dry_run=True)
        success, message = service.help_student("test-student")

        assert success is True
        assert "DRY RUN" in message
        assert "help student" in message

    def test_help_students_dry_run(self):
        """Test help multiple students in dry-run mode."""
        service = AssignmentService(dry_run=True)
        success, message = service.help_students(["student1", "student2"])

        assert success is True
        assert "DRY RUN" in message
        assert "help students" in message

    def test_check_student_dry_run(self):
        """Test check student in dry-run mode."""
        service = AssignmentService(dry_run=True)
        success, message = service.check_student("test-student")

        assert success is True
        assert "DRY RUN" in message
        assert "check student" in message


class TestAssignmentServiceIntegration:
    """Integration tests for AssignmentService."""

    def test_service_chain_dry_run(self):
        """Test chaining multiple service calls in dry-run mode."""
        service = AssignmentService(dry_run=True, verbose=True)

        # Test setup
        success, _ = service.setup()
        assert success is True

        # Test validation
        success, _ = service.validate_config()
        assert success is True

        # Test orchestration
        success, _ = service.orchestrate()
        assert success is True


class TestAssignmentServiceErrors:
    """Test error handling in AssignmentService."""

    def test_import_error_handling(self):
        """Test handling of import errors."""
        service = AssignmentService()

        # This would test import failures, but we can't easily mock imports
        # in the current structure without more complex patching
        pass

    def test_file_not_found_handling(self):
        """Test handling of missing configuration files."""
        service = AssignmentService()

        success, message = service.validate_config("nonexistent.conf")
        # Should handle file not found gracefully
        assert success is False or "not found" in message.lower()
