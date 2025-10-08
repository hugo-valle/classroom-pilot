"""
Assignment orchestration service for comprehensive workflow management.

This service handles the complete assignment workflow including repository
synchronization, student repository discovery, secrets deployment, and
assistance operations.
"""

from ..assignments.orchestrator import (
    AssignmentOrchestrator, WorkflowConfig, WorkflowStep, StepResult
)
from pathlib import Path
from typing import Optional, Set, List, Tuple
import typer

from ..utils.logger import get_logger

logger = get_logger("services.assignment")


class AssignmentService:
    """Service for assignment orchestration and workflow management."""

    def __init__(self, dry_run: bool = False, verbose: bool = False):
        """
        Initialize assignment service.

        Args:
            dry_run: If True, show what would be done without executing
            verbose: Enable verbose logging
        """
        self.dry_run = dry_run
        self.verbose = verbose
        self.orchestrator = None

    def orchestrate(
        self,
        config_file: str = "assignment.conf",
        force_yes: bool = False,
        step: Optional[str] = None,
        skip_steps: Optional[str] = None
    ) -> Tuple[bool, str]:
        """
        Execute complete assignment workflow with comprehensive orchestration.

        Args:
            config_file: Path to assignment configuration file
            force_yes: Skip confirmation prompts and proceed automatically
            step: Execute only the specified workflow step
            skip_steps: Comma-separated list of steps to skip

        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            from ..assignments.orchestrator import (
                AssignmentOrchestrator, WorkflowConfig, WorkflowStep
            )

            # Initialize orchestrator with configuration
            config_path = Path(config_file) if config_file else None
            self.orchestrator = AssignmentOrchestrator(config_path)

            # Validate configuration
            if not self.orchestrator.validate_configuration():
                return False, "Configuration validation failed"

            # Show configuration summary
            self.orchestrator.show_configuration_summary()

            # Parse workflow configuration
            enabled_steps = set(WorkflowStep)
            skip_step_set = set()
            step_override = None

            # Handle step override
            if step:
                try:
                    step_override = WorkflowStep(step.lower())
                    logger.info(
                        f"Executing single step: {step_override.value}")
                except ValueError:
                    valid_steps = [s.value for s in WorkflowStep]
                    return False, f"Invalid step '{step}'. Valid steps: {', '.join(valid_steps)}"

            # Handle skip steps
            if skip_steps:
                for skip_step in skip_steps.split(','):
                    try:
                        skip_step_set.add(WorkflowStep(
                            skip_step.strip().lower()))
                    except ValueError:
                        valid_steps = [s.value for s in WorkflowStep]
                        return False, f"Invalid skip step '{skip_step}'. Valid steps: {', '.join(valid_steps)}"

            # Create workflow configuration
            workflow_config = WorkflowConfig(
                enabled_steps=enabled_steps,
                dry_run=self.dry_run,
                verbose=self.verbose,
                force_yes=force_yes,
                step_override=step_override,
                skip_steps=skip_step_set
            )

            # Confirm execution (skip confirmation in dry-run mode)
            if not self.dry_run and not self.orchestrator.confirm_execution(workflow_config):
                return True, "Orchestration cancelled by user"

            # Execute workflow
            results = self.orchestrator.execute_workflow(workflow_config)

            # Generate and display report
            self.orchestrator.generate_workflow_report()

            # Check for failures
            failed_steps = [r for r in results if not r.success]
            if failed_steps:
                return False, f"Orchestration completed with {len(failed_steps)} failed steps"

            return True, "Assignment orchestration completed successfully"

        except ImportError as e:
            return False, f"Failed to import orchestrator components: {e}"
        except Exception as e:
            return False, f"Assignment orchestration failed: {e}"

    def setup(self) -> Tuple[bool, str]:
        """
        Run interactive assignment setup wizard.

        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            from ..assignments.setup import AssignmentSetup

            setup_wizard = AssignmentSetup()

            if self.dry_run:
                return True, "DRY RUN: Would run interactive assignment setup wizard"

            # Run the setup wizard
            success = setup_wizard.run_setup()

            if success:
                return True, "Assignment setup completed successfully"
            else:
                return False, "Assignment setup was cancelled or failed"

        except ImportError as e:
            return False, f"Failed to import setup wizard: {e}"
        except Exception as e:
            return False, f"Assignment setup failed: {e}"

    def validate_config(self, config_file: str = "assignment.conf") -> Tuple[bool, str]:
        """
        Validate assignment configuration.

        Args:
            config_file: Path to configuration file to validate

        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            from ..config import ConfigValidator

            validator = ConfigValidator()
            config_path = Path(config_file)

            if not config_path.exists():
                return False, f"Configuration file not found: {config_file}"

            # Validate the configuration
            is_valid, errors = validator.validate_config_file(config_path)

            if is_valid:
                return True, f"Configuration file '{config_file}' is valid"
            else:
                error_msg = f"Configuration validation failed:\n" + \
                    "\n".join(errors)
                return False, error_msg

        except ImportError as e:
            return False, f"Failed to import config validator: {e}"
        except Exception as e:
            return False, f"Configuration validation failed: {e}"

    def help_student(
        self,
        repo_url: str,
        one_student: bool = False,
        auto_confirm: bool = False,
        config_file: str = "assignment.conf"
    ) -> Tuple[bool, str]:
        """
        Help a specific student with repository updates.

        Args:
            repo_url: URL of the student repository to help
            one_student: Use template repository directly instead of classroom
            auto_confirm: Skip confirmation prompts
            config_file: Path to configuration file

        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            from ..assignments.student_helper import StudentUpdateHelper, OperationResult

            # Initialize helper
            config_path = Path(config_file) if config_file else None
            helper = StudentUpdateHelper(
                config_path, auto_confirm=auto_confirm)

            # Validate configuration
            if not helper.validate_configuration():
                return False, "Configuration validation failed"

            if self.dry_run:
                mode = "Template direct" if one_student else "Classroom"
                return True, f"DRY RUN: Would help student {repo_url} (Mode: {mode})"

            # Help the student
            result = helper.help_single_student(
                repo_url, use_template_direct=one_student)

            # Handle result
            if result.result == OperationResult.SUCCESS:
                return True, f"Successfully helped student: {result.message}"
            elif result.result == OperationResult.UP_TO_DATE:
                return True, f"Student already up to date: {result.message}"
            else:
                return False, f"Failed to help student: {result.message}"

        except ImportError as e:
            return False, f"Failed to import student helper: {e}"
        except Exception as e:
            return False, f"Student assistance failed: {e}"

    def help_students(
        self,
        repo_file: str,
        auto_confirm: bool = False,
        config_file: str = "assignment.conf"
    ) -> Tuple[bool, str]:
        """
        Help multiple students with repository updates (batch processing).

        Args:
            repo_file: Path to file containing student repository URLs
            auto_confirm: Skip all confirmation prompts
            config_file: Path to configuration file

        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            from ..assignments.student_helper import StudentUpdateHelper

            # Initialize helper
            config_path = Path(config_file) if config_file else None
            helper = StudentUpdateHelper(
                config_path, auto_confirm=auto_confirm)

            # Validate configuration
            if not helper.validate_configuration():
                return False, "Configuration validation failed"

            if self.dry_run:
                return True, f"DRY RUN: Would help students from file: {repo_file}"

            # Process students
            repo_file_path = Path(repo_file)
            if not repo_file_path.exists():
                return False, f"Repository file not found: {repo_file}"

            summary = helper.batch_help_students(repo_file_path)

            # Display summary
            helper.display_batch_summary(summary)

            if summary.errors > 0:
                return False, f"Completed with {summary.errors} errors"
            else:
                return True, "Batch student assistance completed successfully"

        except ImportError as e:
            return False, f"Failed to import student helper: {e}"
        except Exception as e:
            return False, f"Batch student assistance failed: {e}"

    def check_student(
        self,
        repo_url: str,
        config_file: str = "assignment.conf"
    ) -> Tuple[bool, str]:
        """
        Check the status of a student repository.

        Args:
            repo_url: URL of the student repository to check
            config_file: Path to configuration file

        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            from ..assignments.student_helper import StudentUpdateHelper

            # Initialize helper
            config_path = Path(config_file) if config_file else None
            helper = StudentUpdateHelper(config_path)

            # Validate configuration
            if not helper.validate_configuration():
                return False, "Configuration validation failed"

            if self.dry_run:
                return True, f"DRY RUN: Would check student repository: {repo_url}"

            # Check student status
            status = helper.check_student_status(repo_url)

            # Display status
            helper.display_student_status(status)

            # Return appropriate status
            if not status.accessible:
                return False, "Student repository is not accessible"
            elif status.needs_update:
                return True, "Student needs updates"
            else:
                return True, "Student is up to date"

        except ImportError as e:
            return False, f"Failed to import student helper: {e}"
        except Exception as e:
            return False, f"Student status check failed: {e}"


logger = get_logger("services.assignment")


class AssignmentService:
    """Service for assignment orchestration and workflow management."""

    def __init__(self, dry_run: bool = False, verbose: bool = False):
        """
        Initialize assignment service.

        Args:
            dry_run: If True, show what would be done without executing
            verbose: Enable verbose logging
        """
        self.dry_run = dry_run
        self.verbose = verbose
        self.orchestrator = None

    def orchestrate(
        self,
        config_file: str = "assignment.conf",
        force_yes: bool = False,
        step: Optional[str] = None,
        skip_steps: Optional[str] = None
    ) -> Tuple[bool, str]:
        """
        Execute complete assignment workflow with comprehensive orchestration.

        Args:
            config_file: Path to assignment configuration file
            force_yes: Skip confirmation prompts and proceed automatically
            step: Execute only the specified workflow step
            skip_steps: Comma-separated list of steps to skip

        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            # Initialize orchestrator with configuration
            config_path = Path(config_file) if config_file else None
            self.orchestrator = AssignmentOrchestrator(config_path)

            # Validate configuration
            if not self.orchestrator.validate_configuration():
                return False, "Configuration validation failed"

            # Show configuration summary
            self.orchestrator.show_configuration_summary()

            # Parse workflow configuration
            enabled_steps = set(WorkflowStep)
            skip_step_set = set()
            step_override = None

            # Handle step override
            if step:
                try:
                    step_override = WorkflowStep(step.lower())
                    logger.info(
                        f"Executing single step: {step_override.value}")
                except ValueError:
                    valid_steps = [s.value for s in WorkflowStep]
                    return False, f"Invalid step '{step}'. Valid steps: {', '.join(valid_steps)}"

            # Handle skip steps
            if skip_steps:
                for skip_step in skip_steps.split(','):
                    try:
                        skip_step_set.add(WorkflowStep(
                            skip_step.strip().lower()))
                    except ValueError:
                        valid_steps = [s.value for s in WorkflowStep]
                        return False, f"Invalid skip step '{skip_step}'. Valid steps: {', '.join(valid_steps)}"

            # Create workflow configuration
            workflow_config = WorkflowConfig(
                enabled_steps=enabled_steps,
                dry_run=self.dry_run,
                verbose=self.verbose,
                force_yes=force_yes,
                step_override=step_override,
                skip_steps=skip_step_set
            )

            # Confirm execution (skip confirmation in dry-run mode)
            if not self.dry_run and not self.orchestrator.confirm_execution(workflow_config):
                return True, "Orchestration cancelled by user"

            # Execute workflow
            results = self.orchestrator.execute_workflow(workflow_config)

            # Generate and display report
            self.orchestrator.generate_workflow_report()

            # Check for failures
            failed_steps = [r for r in results if not r.success]
            if failed_steps:
                return False, f"Orchestration completed with {len(failed_steps)} failed steps"

            return True, "Assignment orchestration completed successfully"

        except ImportError as e:
            return False, f"Failed to import orchestrator components: {e}"
        except Exception as e:
            return False, f"Assignment orchestration failed: {e}"

    def setup(self) -> Tuple[bool, str]:
        """
        Run interactive assignment setup wizard.

        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            from ..assignments.setup import AssignmentSetup

            setup_wizard = AssignmentSetup()

            if self.dry_run:
                return True, "DRY RUN: Would run interactive assignment setup wizard"

            # Run the setup wizard
            success = setup_wizard.run_setup()

            if success:
                return True, "Assignment setup completed successfully"
            else:
                return False, "Assignment setup was cancelled or failed"

        except ImportError as e:
            return False, f"Failed to import setup wizard: {e}"
        except Exception as e:
            return False, f"Assignment setup failed: {e}"

    def validate_config(self, config_file: str = "assignment.conf") -> Tuple[bool, str]:
        """
        Validate assignment configuration.

        Args:
            config_file: Path to configuration file to validate

        Returns:
            Tuple of (success: bool, message: str)
        """
        try:
            from ..config import ConfigValidator

            validator = ConfigValidator()
            config_path = Path(config_file)

            if not config_path.exists():
                return False, f"Configuration file not found: {config_file}"

            # Validate the configuration
            is_valid, errors = validator.validate_config_file(config_path)

            if is_valid:
                return True, f"Configuration file '{config_file}' is valid"
            else:
                error_msg = f"Configuration validation failed:\n" + \
                    "\n".join(errors)
                return False, error_msg

        except ImportError as e:
            return False, f"Failed to import config validator: {e}"
        except Exception as e:
            return False, f"Configuration validation failed: {e}"
