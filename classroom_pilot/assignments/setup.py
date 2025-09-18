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
    """
    AssignmentSetup provides an interactive wizard for configuring GitHub Classroom assignments.

    This class guides the user through the process of setting up assignment configuration, including:
    - Collecting assignment and repository information.
    - Gathering assignment-specific details such as assignment name and main file.
    - Configuring secret management for instructor-only tests.
    - Creating necessary configuration and token files.
    - Handling user input, validation, and error management throughout the setup process.

    Attributes:
        path_manager (PathManager): Handles workspace and path management.
        repo_root (Path): The root directory of the repository.
        config_file (Path): Path to the assignment configuration file.
        input_handler (InputHandler): Manages user input and prompts.
        validators (Validators): Provides input validation methods.
        url_parser (URLParser): Extracts information from GitHub Classroom URLs.
        config_generator (ConfigGenerator): Generates configuration files.
        file_manager (FileManager): Manages file creation and updates.
        config_values (dict): Stores collected configuration values.
        token_files (dict): Maps token names to their respective file paths.
        token_validation (dict): Stores token validation preferences.

    Methods:
        run_wizard():
            Runs the interactive setup wizard, orchestrating the full configuration process.
        _collect_assignment_info():
            Prompts for and validates the GitHub Classroom assignment URL.
        _collect_repository_info():
            Extracts and collects repository-related information, including organization and template repo URL.
        _collect_assignment_details():
            Gathers assignment-specific details such as assignment name and main file.
        _configure_secret_management():
            Configures secret management options for instructor-only tests.
        _configure_tokens():
            Prompts for and stores GitHub personal access tokens for instructor test repositories.
        _create_files():
            Creates configuration and token files, and updates .gitignore as needed.
    """

    def __init__(self):
        """
        Initializes the class by setting up path management, configuration file location, input handling, validation, URL parsing, configuration generation, and file management. 
        Also initializes dictionaries for storing configuration values, token files, and token validation results.
        """
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
        """
        Runs the complete setup wizard for assignment configuration.

        This method orchestrates the interactive setup process, including:
        - Displaying a welcome screen.
        - Collecting basic assignment and repository information.
        - Gathering assignment-specific details.
        - Configuring secret management.
        - Creating necessary configuration files.
        - Displaying a completion message upon success.

        Handles user cancellation (KeyboardInterrupt) and unexpected errors gracefully,
        logging relevant information and exiting with appropriate status codes.
        """
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
        """
        Collects basic assignment information from the user.

        Prompts the user to enter the GitHub Classroom assignment URL, validates the input,
        and stores it in the configuration values under the key 'CLASSROOM_URL'.

        Returns:
            None
        """
        logger.debug("Collecting assignment information")

        classroom_url = self.input_handler.prompt_input(
            "GitHub Classroom assignment URL",
            "",
            self.validators.validate_url,
            "Find this in GitHub Classroom when managing your assignment. Example: https://classroom.github.com/classrooms/12345/assignments/assignment-name"
        )
        self.config_values['CLASSROOM_URL'] = classroom_url

    def _collect_repository_info(self):
        """
        Collects and prompts for repository-related configuration values required for assignment setup.

        This method performs the following steps:
        1. Extracts the GitHub organization and assignment name from the provided classroom URL.
        2. Prompts the user to confirm or edit the GitHub organization name, validating the input.
        3. Prompts the user for the template repository URL, suggesting a default based on the organization and assignment name, and validates the input.
        4. Stores the collected values in the configuration dictionary.
        5. Exits the program with an error message if the template repository URL is not provided.

        Raises:
            SystemExit: If the template repository URL is not provided by the user.
        """
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
        """
        Collects assignment-specific details from the user and updates the configuration values.

        This method prompts the user to provide the assignment name and the main assignment file.
        If the assignment name is not provided, it can be auto-extracted from the template URL.
        The main assignment file is the primary file students will work on (e.g., assignment.ipynb, main.py, homework.cpp).
        Both inputs are validated using the appropriate validators before being stored in the configuration.

        Raises:
            ValidationError: If the provided assignment name or file path does not pass validation.
        """
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
        """
        Configure secret management settings for assignment tests.

        This method prompts the user to specify the location of assignment tests:
        either within the template repository (simpler setup) or in a separate
        private instructor repository (more secure). Based on the user's choice,
        it enables or disables secret management for accessing the instructor test
        repository and updates the configuration accordingly.
        """
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
        """
        Configure and prompt for GitHub personal access tokens and related secrets.

        This method guides the user through the process of obtaining and securely storing a GitHub personal access token
        with the required permissions ('repo' and 'admin:repo_hook'). It prompts the user for the token, stores it in the
        configuration, and asks whether the token should be validated (e.g., checking if it starts with 'ghp_'). The method
        also manages the mapping of token validation and storage file locations.
        """
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
        """
        Creates all necessary configuration and token files for the application.

        This method performs the following actions:
        1. Generates the main configuration file using the provided configuration values, token files, and token validation settings.
        2. If secrets are enabled (i.e., 'USE_SECRETS' is set to 'true' in the configuration values), it creates the required token files.
        3. Updates the .gitignore file to ensure sensitive files are excluded from version control.
        """
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
    """
    Initializes and runs the assignment setup wizard.

    This function creates an instance of the AssignmentSetup class and starts
    the interactive setup process for configuring an assignment.

    Returns:
        None
    """
    setup = AssignmentSetup()
    setup.run_wizard()


if __name__ == "__main__":
    setup_assignment()
