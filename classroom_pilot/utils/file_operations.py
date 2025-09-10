"""
File Operations for the GitHub Classroom Setup Wizard.

This module handles file creation, token file management, and .gitignore updates.
"""

import os
import stat
import subprocess
from pathlib import Path
from typing import Dict

from .ui_components import print_header, print_success, print_status, print_error, print_warning, Colors, print_colored


class FileManager:
    """Manage file operations for the setup wizard."""

    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.gitignore_file = repo_root / ".gitignore"

    def create_token_files(self, config_values: Dict[str, str], token_files: Dict[str, str]) -> None:
        """Create token files with secure permissions."""
        print_header("Creating Token Files")

        for secret_name, token_file in token_files.items():
            token_path = self.repo_root / token_file
            token_value = config_values.get(f'{secret_name}_VALUE', '')

            # Write token file
            with open(token_path, 'w') as f:
                f.write(token_value)

            # Set secure permissions (owner read/write only)
            os.chmod(token_path, stat.S_IRUSR | stat.S_IWUSR)

            print_success(f"Created secure token file: {token_file}")

    def update_gitignore(self) -> None:
        """Update .gitignore with instructor files."""
        print_header("Updating .gitignore")

        # Read existing .gitignore if it exists
        gitignore_content = ""
        if self.gitignore_file.exists():
            with open(self.gitignore_file, 'r') as f:
                gitignore_content = f.read()
        else:
            print_status("Created new .gitignore file")

        # Check if instructor files section already exists
        if "# Instructor-only files" not in gitignore_content:
            gitignore_addition = """
# =============================================================================
# Instructor-only files (GitHub Classroom automation)
# =============================================================================
# Token files for GitHub API access
*token*.txt
instructor_token.txt
api_token.txt

# Assignment configuration (contains sensitive paths)
assignment.conf

# Generated batch files
tools/generated/
*.batch

# Temporary files from automation scripts
.temp_*
temp_*

# IDE and editor files
.vscode/settings.json
.idea/
*.swp
*.swo
*~

"""

            # Append to .gitignore
            with open(self.gitignore_file, 'a') as f:
                f.write(gitignore_addition)

            print_success("Added instructor files to .gitignore")
        else:
            print_status(
                ".gitignore already contains instructor file patterns")


class GitHubValidator:
    """Validate GitHub CLI access and permissions."""

    def __init__(self, config_values: Dict[str, str]):
        self.config_values = config_values

    def validate_github_access(self) -> None:
        """Validate GitHub CLI access."""
        print_header("Validating GitHub Access")

        # Check if GitHub CLI is installed
        try:
            subprocess.run(['gh', '--version'],
                           capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print_error("GitHub CLI (gh) is not installed")
            print_colored(
                "Please install GitHub CLI from: https://cli.github.com/", Colors.YELLOW)
            return

        # Check if GitHub CLI is authenticated
        try:
            subprocess.run(['gh', 'auth', 'status'],
                           capture_output=True, check=True)
        except subprocess.CalledProcessError:
            print_error("GitHub CLI is not authenticated")
            print_colored("Please run: gh auth login", Colors.YELLOW)
            return

        # Test access to organization
        org = self.config_values.get('GITHUB_ORGANIZATION', '')
        try:
            subprocess.run(
                ['gh', 'api', f'orgs/{org}'], capture_output=True, check=True)
            print_success(
                "GitHub CLI authenticated and organization access confirmed")
        except subprocess.CalledProcessError:
            print_warning(
                f"Cannot access organization '{org}'. You may need additional permissions.")
            print_colored(
                "Please ensure you have access to the GitHub organization", Colors.YELLOW)
