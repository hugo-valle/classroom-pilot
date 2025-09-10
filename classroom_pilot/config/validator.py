"""
Configuration validation for Classroom Pilot.

This module provides validation for configuration values and settings.
"""

import re
from typing import Dict, Any, List, Tuple
from ..utils import get_logger

logger = get_logger("config.validator")


class ConfigValidator:
    """Validate configuration values and settings."""

    @staticmethod
    def validate_github_url(url: str) -> Tuple[bool, str]:
        """
        Validate GitHub URL format.

        Args:
            url: URL to validate

        Returns:
            Tuple of (is_valid, error_message)
        """
        if not url:
            return False, "URL cannot be empty"

        github_pattern = r'^https://github\.com/.+/.+$'
        classroom_pattern = r'^https://classroom\.github\.com/classrooms/.+/assignments/.+$'

        if re.match(github_pattern, url) or re.match(classroom_pattern, url):
            return True, ""
        else:
            return False, "Must be a valid GitHub or GitHub Classroom URL"

    @staticmethod
    def validate_organization(org: str) -> Tuple[bool, str]:
        """
        Validate GitHub organization name.

        Args:
            org: Organization name to validate

        Returns:
            Tuple of (is_valid, error_message)
        """
        if not org:
            return False, "Organization name cannot be empty"

        if re.match(r'^[a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?$', org):
            return True, ""
        else:
            return False, "Organization name must contain only letters, numbers, and hyphens"

    @staticmethod
    def validate_assignment_name(name: str) -> Tuple[bool, str]:
        """
        Validate assignment name.

        Args:
            name: Assignment name to validate

        Returns:
            Tuple of (is_valid, error_message)
        """
        if not name:
            return True, ""  # Allow empty assignment names

        if re.match(r'^[a-zA-Z0-9]([a-zA-Z0-9_-]*[a-zA-Z0-9])?$', name):
            return True, ""
        else:
            return False, "Assignment name must contain only letters, numbers, hyphens, and underscores"

    @staticmethod
    def validate_file_path(file_path: str) -> Tuple[bool, str]:
        """
        Validate file path has proper extension.

        Args:
            file_path: File path to validate

        Returns:
            Tuple of (is_valid, error_message)
        """
        if not file_path:
            return False, "File path cannot be empty"

        valid_extensions = {'.ipynb', '.py', '.cpp', '.sql', '.md',
                            '.html', '.js', '.ts', '.java', '.c', '.h', '.hpp', '.txt'}

        if any(file_path.endswith(ext) for ext in valid_extensions):
            return True, ""
        else:
            return False, f"File must have a valid extension: {', '.join(sorted(valid_extensions))}"

    @staticmethod
    def validate_required_fields(config: Dict[str, Any]) -> List[str]:
        """
        Validate that all required configuration fields are present.

        Args:
            config: Configuration dictionary to validate

        Returns:
            List of missing required fields
        """
        required_fields = [
            'CLASSROOM_URL',
            'TEMPLATE_REPO_URL',
            'GITHUB_ORGANIZATION',
            'ASSIGNMENT_FILE'
        ]

        missing_fields = []
        for field in required_fields:
            if field not in config or not config[field]:
                missing_fields.append(field)

        return missing_fields

    @staticmethod
    def validate_full_config(config: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Perform full configuration validation.

        Args:
            config: Configuration dictionary to validate

        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []

        # Check required fields
        missing = ConfigValidator.validate_required_fields(config)
        if missing:
            errors.extend(
                [f"Missing required field: {field}" for field in missing])

        # Validate specific fields if present
        if config.get('CLASSROOM_URL'):
            valid, error = ConfigValidator.validate_github_url(
                config['CLASSROOM_URL'])
            if not valid:
                errors.append(f"CLASSROOM_URL: {error}")

        if config.get('TEMPLATE_REPO_URL'):
            valid, error = ConfigValidator.validate_github_url(
                config['TEMPLATE_REPO_URL'])
            if not valid:
                errors.append(f"TEMPLATE_REPO_URL: {error}")

        if config.get('GITHUB_ORGANIZATION'):
            valid, error = ConfigValidator.validate_organization(
                config['GITHUB_ORGANIZATION'])
            if not valid:
                errors.append(f"GITHUB_ORGANIZATION: {error}")

        if config.get('ASSIGNMENT_NAME'):
            valid, error = ConfigValidator.validate_assignment_name(
                config['ASSIGNMENT_NAME'])
            if not valid:
                errors.append(f"ASSIGNMENT_NAME: {error}")

        if config.get('ASSIGNMENT_FILE'):
            valid, error = ConfigValidator.validate_file_path(
                config['ASSIGNMENT_FILE'])
            if not valid:
                errors.append(f"ASSIGNMENT_FILE: {error}")

        return len(errors) == 0, errors
