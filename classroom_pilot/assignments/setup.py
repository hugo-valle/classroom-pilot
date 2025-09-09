"""
Assignment setup and configuration wizard.

This module provides the interactive setup wizard for creating new assignment configurations.
"""

import argparse
import re
import sys
from pathlib import Path
from typing import Dict

from ..config import ConfigLoader, ConfigValidator
from ..config.generator import ConfigGenerator
from ..utils import get_logger, PathManager
from ..utils.ui_components import (
    Colors, print_colored, print_error, print_success,
    show_welcome, show_completion
)
from ..utils.input_handlers import InputHandler, Validators, URLParser
from ..utils.file_operations import FileManager

logger = get_logger("assignments.setup")


class AssignmentSetup:
    """Interactive assignment setup wizard."""

    def __init__(self):
        self.path_manager = PathManager()
        self.repo_root = self.path_manager.get_workspace_root()
        self.config_file = self.repo_root / "assignment.conf"

        # Initialize handlers
        self.input_handler = InputHandler()
        self.validators = Validators()
        self.url_parser = URLParser()
        self.config_generator = ConfigGenerator(self.config_file)
        self.file_manager = FileManager(self.repo_root)

        # Data storage
        self.config_values = {}
        self.token_files = {}
        self.token_validation = {}

    def run_wizard(self):
        """Run the complete setup wizard."""
        try:
            logger.info("Starting assignment setup wizard")

            # Show welcome screen
            show_welcome()

            # Collect basic assignment information
            self._collect_assignment_info()

            # Collect repository information
            self._collect_repository_info()

            # Collect assignment details
            self._collect_assignment_details()

            # Configure secret management
            self._configure_secret_management()

            # Create configuration files
            self._create_files()

            # Show completion
            show_completion(self.config_values, self.token_files)

            print_success("Assignment setup completed successfully!")
            logger.info("Assignment setup wizard completed")

        except KeyboardInterrupt:
            print_colored("Setup cancelled by user.", Colors.YELLOW)
            logger.info("Setup wizard cancelled by user")
            sys.exit(1)
        except Exception as e:
            print_error(f"Setup failed: {e}")
            logger.error(f"Setup wizard failed: {e}")
            sys.exit(1)

    def _collect_assignment_info(self):
        """Collect basic assignment information."""
        logger.debug("Collecting assignment information")

        classroom_url = self.input_handler.prompt_input(
            "GitHub Classroom assignment URL",
            "",
            self.validators.validate_url,
            "Find this in GitHub Classroom when managing your assignment. Example: https://classroom.github.com/classrooms/12345/assignments/assignment-name"
        )
        self.config_values['CLASSROOM_URL'] = classroom_url

    def _collect_repository_info(self):
        """Collect repository information."""
        logger.debug("Collecting repository information")

        # Extract organization and assignment name from URL
        extracted_org = self.url_parser.extract_org_from_url(
            self.config_values['CLASSROOM_URL'])
        extracted_assignment = self.url_parser.extract_assignment_from_url(
            self.config_values['CLASSROOM_URL'])

        github_org = self.input_handler.prompt_input(
            "GitHub organization name",
            extracted_org,
            self.validators.validate_organization,
            "The GitHub organization that contains your assignment repositories"
        )
        self.config_values['GITHUB_ORGANIZATION'] = github_org

        template_url = self.input_handler.prompt_input(
            "Template repository URL",
            f"https://github.com/{github_org}/{extracted_assignment}-template.git",
            self.validators.validate_url,
            "The TEMPLATE repository that students fork from (contains starter code/files). Usually has '-template' suffix."
        )

        if not template_url:
            print_error(
                "The Template repository URL is required for assignment setup.")
            sys.exit(1)

        self.config_values['TEMPLATE_REPO_URL'] = template_url

    def _collect_assignment_details(self):
        """Collect assignment-specific details."""
        logger.debug("Collecting assignment details")

        extracted_assignment = self.url_parser.extract_assignment_from_url(
            self.config_values['CLASSROOM_URL'])

        assignment_name = self.input_handler.prompt_input(
            "Assignment name (optional)",
            extracted_assignment,
            self.validators.validate_assignment_name,
            "Leave empty to auto-extract from template URL"
        )
        self.config_values['ASSIGNMENT_NAME'] = assignment_name

        main_file = self.input_handler.prompt_input(
            "Main assignment file",
            "assignment.ipynb",
            self.validators.validate_file_path,
            "The primary file students work on (e.g., assignment.ipynb, main.py, homework.cpp)"
        )
        self.config_values['MAIN_ASSIGNMENT_FILE'] = main_file

    def _configure_secret_management(self):
        """Configure secret management settings."""
        logger.debug("Configuring secret management")

        print_colored("Where are your assignment tests located?", Colors.BLUE)
        print_colored(
            "   Option 1: Tests are included in the template repository (simpler setup)", Colors.CYAN)
        print_colored(
            "   Option 2: Tests are in a separate private instructor repository (more secure)", Colors.CYAN)

        use_secrets = self.input_handler.prompt_yes_no(
            "Do you have tests in a separate private instructor repository?",
            False
        )

        if use_secrets:
            self.config_values['USE_SECRETS'] = 'true'
            print_success(
                "✓ Secret management will be enabled for accessing instructor test repository")
            self._configure_tokens()
        else:
            self.config_values['USE_SECRETS'] = 'false'
            print_success(
                "✓ Secret management will be disabled (tests in template repository)")

    def _configure_tokens(self):
        """Configure GitHub tokens and secrets."""
        logger.debug("Configuring tokens")

        print_colored(
            "💡 You need a GitHub personal access token with 'repo' and 'admin:repo_hook' permissions", Colors.BLUE)
        print_colored(
            "Create one at: https://github.com/settings/tokens", Colors.YELLOW)

        # Get main instructor token
        token_value = self.input_handler.prompt_secure(
            "GitHub personal access token",
            "This token will be securely stored in instructor_token.txt"
        )
        self.config_values['INSTRUCTOR_TESTS_TOKEN_VALUE'] = token_value

        # Ask about token validation
        validate_instructor = self.input_handler.prompt_yes_no(
            "Should this token be validated as a GitHub token (starts with 'ghp_')?",
            True
        )
        self.token_validation['INSTRUCTOR_TESTS_TOKEN'] = validate_instructor
        self.token_files['INSTRUCTOR_TESTS_TOKEN'] = 'instructor_token.txt'

    def _create_files(self):
        """Create all configuration and token files."""
        logger.debug("Creating configuration files")

        # Create configuration file
        self.config_generator.create_config_file(
            self.config_values,
            self.token_files,
            self.token_validation
        )

        # Create token files if secrets are enabled
        if self.config_values.get('USE_SECRETS') == 'true':
            self.file_manager.create_token_files(
                self.config_values, self.token_files)

        # Update .gitignore
        self.file_manager.update_gitignore()


def setup_assignment():
    """Main entry point for assignment setup."""
    setup = AssignmentSetup()
    setup.run_wizard()


if __name__ == "__main__":
    setup_assignment()
