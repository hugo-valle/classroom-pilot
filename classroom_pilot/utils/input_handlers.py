"""
Input Handlers and Validation for the GitHub Classroom Setup Wizard.

This module provides input prompting, validation functions, and URL parsing utilities.
"""

import re
import sys
from getpass import getpass
from typing import Optional, Callable

from .ui_components import print_error, print_colored, Colors


class InputHandler:
    """Handle user input with validation and prompting."""

    @staticmethod
    def prompt_input(
        prompt: str,
        default: str = "",
        validator: Optional[Callable] = None,
        help_text: str = ""
    ) -> str:
        """Prompt for input with validation."""
        while True:
            if help_text:
                print_colored(f"💡 {help_text}", Colors.BLUE)

            if default:
                display_prompt = f"{prompt} [{default}]: "
            else:
                display_prompt = f"{prompt}: "

            print_colored(display_prompt, Colors.GREEN, end="")

            try:
                # Handle interactive vs non-interactive mode
                if sys.stdin.isatty():
                    value = input()
                else:
                    value = input() if sys.stdin.readable() else default
            except (EOFError, KeyboardInterrupt):
                value = default

            # Use default if empty
            if not value and default:
                value = default

            # Validate input if validator provided
            if validator:
                try:
                    if validator(value):
                        return value
                    else:
                        print_error("Invalid input. Please try again.")
                        continue
                except Exception as e:
                    print_error(f"Validation error: {e}")
                    continue
            else:
                return value

    @staticmethod
    def prompt_secure(prompt: str, help_text: str = "") -> str:
        """Prompt for secure input (passwords/tokens)."""
        if help_text:
            print_colored(f"💡 {help_text}", Colors.BLUE)

        print_colored(f"{prompt}: ", Colors.GREEN, end="")

        try:
            if sys.stdin.isatty():
                value = getpass("")
            else:
                value = input()  # Fallback for non-interactive mode
        except (EOFError, KeyboardInterrupt):
            value = ""

        return value

    @staticmethod
    def prompt_yes_no(prompt: str, default: bool = False) -> bool:
        """Prompt for yes/no input."""
        default_text = "Y/n" if default else "y/N"
        response = InputHandler.prompt_input(f"{prompt} ({default_text})")

        if not response:
            return default

        return response.lower().startswith('y')


class Validators:
    """Collection of input validation functions."""

    @staticmethod
    def validate_url(url: str) -> bool:
        """Validate GitHub or GitHub Classroom URL."""
        github_pattern = r'^https://github\.com/.+/.+$'
        classroom_pattern = r'^https://classroom\.github\.com/classrooms/.+/assignments/.+$'

        if re.match(github_pattern, url) or re.match(classroom_pattern, url):
            return True
        else:
            print_error("Please enter a valid GitHub or GitHub Classroom URL")
            return False

    @staticmethod
    def validate_organization(org: str) -> bool:
        """Validate GitHub organization name."""
        if re.match(r'^[a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?$', org):
            return True
        else:
            print_error(
                "Organization name must contain only letters, numbers, and hyphens")
            return False

    @staticmethod
    def validate_assignment_name(name: str) -> bool:
        """Validate assignment name."""
        if not name:  # Allow empty names
            return True
        if re.match(r'^[a-zA-Z0-9]([a-zA-Z0-9_-]*[a-zA-Z0-9])?$', name):
            return True
        else:
            print_error(
                "Assignment name must contain only letters, numbers, hyphens, and underscores")
            return False

    @staticmethod
    def validate_file_path(file_path: str) -> bool:
        """Validate file path has proper extension."""
        valid_extensions = {'.ipynb', '.py', '.cpp', '.sql', '.md',
                            '.html', '.js', '.ts', '.java', '.c', '.h', '.hpp', '.txt'}

        if any(file_path.endswith(ext) for ext in valid_extensions):
            return True
        else:
            print_error(
                "Please specify a valid file extension (.ipynb, .py, .cpp, .sql, .md, etc.)")
            return False

    @staticmethod
    def validate_non_empty(value: str) -> bool:
        """Validate that value is not empty."""
        if value.strip():
            return True
        else:
            print_error("This field cannot be empty")
            return False


class URLParser:
    """Utility functions for parsing URLs and extracting information."""

    @staticmethod
    def extract_assignment_from_url(url: str) -> str:
        """Extract assignment name from URL."""
        match = re.search(r'/([^/]+)/?$', url)
        return match.group(1) if match else ""

    @staticmethod
    def extract_org_from_url(url: str) -> str:
        """Extract organization from GitHub URL."""
        match = re.search(r'github\.com/([^/]+)/', url)
        return match.group(1) if match else ""
