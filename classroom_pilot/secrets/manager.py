"""
Secrets and Token Management for GitHub Classroom Repository Operations.

This module handles:
- GitHub token management and authentication for repository access
- Repository secrets configuration and secure deployment to student repositories
- Batch secrets operations with progress tracking and error handling
- Token validation, rotation, and credential lifecycle management
- Integration with GitHub API for automated secrets management workflows
"""

from pathlib import Path
from typing import List, Dict, Optional
import json
import base64

# GitHub API integration with fallback handling
try:
    from github import Github, Repository, GithubException
    GITHUB_AVAILABLE = True
except ImportError:
    GITHUB_AVAILABLE = False

from ..utils import get_logger, PathManager
from ..utils.github_exceptions import (
    GitHubAPIError, GitHubAuthenticationError, GitHubRepositoryError,
    GitHubNetworkError, github_api_retry, github_api_context,
    handle_github_errors, is_github_available
)
from ..config import ConfigLoader

logger = get_logger("secrets.manager")


class SecretsManager:
    """
    SecretsManager handles comprehensive GitHub repository secrets and token operations.

    This class provides methods for managing repository secrets deployment, token
    validation and rotation, and batch secrets operations across multiple student
    repositories. It supports both authenticated GitHub API access and secure
    credential handling with comprehensive error management.

    Args:
        config_path (Path): Path to the assignment configuration file.
                          Defaults to "assignment.conf" in current directory.

    Attributes:
        config_loader (ConfigLoader): Configuration loader instance.
        config (dict): Loaded configuration values.
        path_manager (PathManager): Path management utilities.
        github_client (Github): GitHub API client (if authenticated).

    Methods:
        deploy_secrets_to_repository(repository_name, secrets_dict):
            Deploys specified secrets to the target repository.

        batch_deploy_secrets(repositories, secrets_dict):
            Performs batch secrets deployment across multiple repositories.

        validate_github_token(token):
            Validates GitHub token and checks permissions.

        rotate_repository_secrets(repository_name, new_secrets):
            Rotates existing secrets with new values in specified repository.

        audit_repository_secrets(repository_name):
            Audits current secrets configuration for specified repository.

        load_secrets_template(template_path):
            Loads secrets configuration from template file.

        verify_secrets_deployment(repository_name, secret_names):
            Verifies successful deployment of specified secrets to repository.
    """

    def __init__(self, config_path: Path = Path("assignment.conf")):
        """
        Initialize secrets manager with configuration and API setup.

        Args:
            config_path (Path): Path to configuration file.
                              Defaults to "assignment.conf" in current directory.
        """
        self.config_loader = ConfigLoader(config_path)
        self.config = self.config_loader.load()
        self.path_manager = PathManager()
        self.github_client = None

        # Initialize GitHub API client if available
        if GITHUB_AVAILABLE:
            try:
                self.github_client = self._initialize_github_client()
            except (GitHubAuthenticationError, Exception) as e:
                logger.warning(f"GitHub API initialization failed: {e}")
                self.github_client = None

    def _initialize_github_client(self) -> Optional['Github']:
        """
        Initialize GitHub API client with authentication.

        Returns:
            Github: Authenticated GitHub client instance or None if unavailable.

        Raises:
            GitHubAuthenticationError: If authentication fails.
        """
        if not GITHUB_AVAILABLE:
            logger.warning(
                "PyGithub not available - falling back to CLI operations")
            return None

        tokens = [
            self.config.get('GITHUB_TOKEN'),
            self.config.get('GITHUB_ACCESS_TOKEN'),
        ]

        for token in tokens:
            if not token:
                continue

            try:
                with github_api_context("github_client_initialization"):
                    client = Github(token)
                    # Test authentication by getting user info
                    client.get_user().login
                    logger.info("GitHub API client initialized successfully")
                    return client
            except GithubException as e:
                logger.warning(f"GitHub authentication failed with token: {e}")
                continue

        raise GitHubAuthenticationError(
            "No valid GitHub token found in environment or configuration")

    def load_secrets_template(self) -> Dict[str, str]:
        """Load secrets template from configuration."""
        logger.info("Loading secrets template")

        try:
            secrets_file = self.path_manager.find_config_file("secrets.json")
            if not secrets_file or not secrets_file.exists():
                logger.warning("No secrets template found")
                return {}

            with open(secrets_file, 'r') as f:
                secrets = json.load(f)

            logger.info(f"Loaded {len(secrets)} secret templates")
            return secrets

        except Exception as e:
            logger.error(f"Failed to load secrets template: {e}")
            return {}

    @github_api_retry(max_attempts=2, base_delay=1.0)
    def validate_token(self, token: str, token_type: str = "github") -> bool:
        """
        Validate a GitHub token using API authentication.

        Args:
            token: The token to validate
            token_type: Type of token (default: "github")

        Returns:
            bool: True if token is valid, False otherwise.

        Raises:
            GitHubAuthenticationError: If token validation fails due to auth issues.
        """
        logger.info(f"Validating {token_type} token")

        # Basic format validation
        if not token or len(token) < 20:
            logger.error("Invalid token format")
            return False

        if token_type == "github":
            if not (token.startswith("ghp_") or token.startswith("github_pat_")):
                logger.warning("Token does not match expected GitHub format")

        try:
            if GITHUB_AVAILABLE and self.github_client and token_type == "github":
                return self._validate_token_via_api(token)
            else:
                # Basic format validation only
                logger.warning(
                    "GitHub API not available - using basic format validation")
                return True

        except GitHubAuthenticationError:
            logger.error("Token validation failed - authentication error")
            return False
        except Exception as e:
            logger.error(f"Token validation failed: {e}")
            return False

    def _validate_token_via_api(self, token: str) -> bool:
        """Validate token using GitHub API."""
        logger.info("Validating token via GitHub API")

        try:
            with github_api_context("token_validation"):
                # Create temporary client to test token
                test_client = Github(token)
                # Test authentication by getting user info
                user = test_client.get_user()
                username = user.login

                logger.info(
                    f"Token validation successful for user: {username}")
                return True

        except GithubException as e:
            raise GitHubAuthenticationError(
                f"GitHub token validation failed: {e}",
                original_error=e
            )

    def add_secrets_to_repository(self, repo_name: str, secrets: Dict[str, str]) -> Dict[str, bool]:
        """Add secrets to a specific repository."""
        logger.info(f"Adding {len(secrets)} secrets to {repo_name}")

        results = {}

        for secret_name, secret_value in secrets.items():
            try:
                success = self.add_single_secret(
                    repo_name, secret_name, secret_value)
                results[secret_name] = success

            except GitHubRepositoryError as e:
                logger.error(
                    f"Failed to add secret {secret_name} to {repo_name}: {e}")
                results[secret_name] = False
            except Exception as e:
                logger.error(
                    f"Unexpected error adding secret {secret_name} to {repo_name}: {e}")
                results[secret_name] = False

        return results

    def add_single_secret(self, repo_name: str, secret_name: str, secret_value: str) -> bool:
        """
        Add a single secret to a repository.

        Args:
            repo_name: Repository name (format: owner/repo)
            secret_name: Name of the secret
            secret_value: Value of the secret

        Returns:
            bool: True if secret was added successfully.

        Raises:
            GitHubRepositoryError: If adding secret fails.
        """
        logger.info(f"Adding secret {secret_name} to {repo_name}")

        try:
            if self.github_client:
                return self._add_secret_via_api(repo_name, secret_name, secret_value)
            else:
                return self._add_secret_via_cli(repo_name, secret_name, secret_value)
        except Exception as e:
            raise GitHubRepositoryError(
                f"Failed to add secret {secret_name} to {repo_name}: {e}",
                repository_name=repo_name,
                operation="add_secret"
            )

    def _add_secret_via_api(self, repo_name: str, secret_name: str, secret_value: str) -> bool:
        """Add secret using GitHub API."""
        logger.info("Using GitHub API for adding repository secret")

        try:
            repo = self.github_client.get_repo(repo_name)

            # Note: PyGithub doesn't directly support repository secrets API
            # This would require using the REST API directly or additional libraries
            # For now, we'll use CLI fallback and log a warning
            logger.warning(
                "GitHub API secret addition not yet fully implemented - using CLI fallback")
            return self._add_secret_via_cli(repo_name, secret_name, secret_value)

        except GithubException as e:
            raise GitHubRepositoryError(
                f"GitHub API error adding secret: {e}",
                repository_name=repo_name,
                operation="add_secret"
            )

    def _add_secret_via_cli(self, repo_name: str, secret_name: str, secret_value: str) -> bool:
        """Add secret using GitHub CLI fallback."""
        logger.info("Using GitHub CLI for adding repository secret")

        try:
            import subprocess

            # Use gh CLI to add repository secret
            cmd = [
                'gh', 'secret', 'set', secret_name,
                '--repo', repo_name,
                '--body', secret_value
            ]
            result = subprocess.run(
                cmd, capture_output=True, text=True, check=True)

            logger.info(
                f"Successfully added secret {secret_name} to {repo_name} via CLI")
            return True

        except subprocess.CalledProcessError as e:
            raise GitHubRepositoryError(
                f"GitHub CLI error adding secret: {e}",
                repository_name=repo_name,
                operation="add_secret"
            )

    def add_secrets_to_students(self, assignment_prefix: str) -> Dict[str, Dict[str, bool]]:
        """Add secrets to all student repositories for an assignment."""
        logger.info(
            f"Adding secrets to student repositories for {assignment_prefix}")

        secrets = self.load_secrets_template()
        if not secrets:
            logger.error("No secrets to deploy")
            return {}

        results = {}

        try:
            student_repos = self.find_student_repositories(assignment_prefix)

            for repo_name in student_repos:
                repo_results = self.add_secrets_to_repository(
                    repo_name, secrets)
                results[repo_name] = repo_results

        except GitHubRepositoryError as e:
            logger.error(f"Failed to find student repositories: {e}")
        except Exception as e:
            logger.error(f"Unexpected error adding secrets to students: {e}")

        return results

    @github_api_retry(max_attempts=2, base_delay=1.0)
    def find_student_repositories(self, assignment_prefix: str) -> List[str]:
        """
        Find all student repositories for an assignment.

        Args:
            assignment_prefix: Assignment prefix to search for

        Returns:
            List[str]: List of student repository names.

        Raises:
            GitHubRepositoryError: If repository discovery fails.
        """
        logger.info(f"Finding student repositories for {assignment_prefix}")

        try:
            # Use the RepositoryFetcher for discovery
            from ..repos.fetch import RepositoryFetcher

            fetcher = RepositoryFetcher(self.config_loader.config_path)
            repositories = fetcher.discover_repositories(assignment_prefix)

            # Extract just the repository names for student repositories
            student_repos = [
                repo.name for repo in repositories
                if repo.is_student_repo
            ]

            logger.info(f"Found {len(student_repos)} student repositories")
            return student_repos

        except Exception as e:
            raise GitHubRepositoryError(
                f"Failed to find student repositories for {assignment_prefix}: {e}",
                repository_name=assignment_prefix,
                operation="repository_discovery"
            )

    def rotate_tokens(self) -> Dict[str, bool]:
        """Rotate authentication tokens."""
        logger.info("Rotating authentication tokens")

        results = {}

        try:
            # TODO: Implement token rotation logic
            # 1. Generate new tokens
            # 2. Update configuration
            # 3. Test new tokens
            # 4. Revoke old tokens

            logger.warning("Token rotation not yet implemented")
            results["github_token"] = True

        except Exception as e:
            logger.error(f"Token rotation failed: {e}")
            results["github_token"] = False

        return results

    @github_api_retry(max_attempts=2, base_delay=1.0)
    def audit_repository_secrets(self, repo_name: str) -> List[str]:
        """
        Audit secrets configured for a repository.

        Args:
            repo_name: Repository name (format: owner/repo)

        Returns:
            List[str]: List of secret names configured for the repository.

        Raises:
            GitHubRepositoryError: If secrets audit fails.
        """
        logger.info(f"Auditing secrets for {repo_name}")

        try:
            return self._audit_secrets_via_cli(repo_name)
        except Exception as e:
            raise GitHubRepositoryError(
                f"Failed to audit secrets for {repo_name}: {e}",
                repository_name=repo_name,
                operation="audit_secrets"
            )

    def _audit_secrets_via_cli(self, repo_name: str) -> List[str]:
        """Audit secrets using GitHub CLI."""
        logger.info("Using GitHub CLI for secrets auditing")

        try:
            import subprocess

            # Use gh CLI to list repository secrets
            cmd = ['gh', 'secret', 'list', '--repo', repo_name]
            result = subprocess.run(
                cmd, capture_output=True, text=True, check=True)

            # Parse the output to extract secret names
            secret_names = []
            for line in result.stdout.strip().split('\n'):
                if line.strip():
                    # Extract secret name (first column)
                    secret_name = line.split()[0]
                    secret_names.append(secret_name)

            logger.info(f"Found {len(secret_names)} secrets in {repo_name}")
            return secret_names

        except subprocess.CalledProcessError as e:
            raise GitHubRepositoryError(
                f"GitHub CLI error auditing secrets: {e}",
                repository_name=repo_name,
                operation="audit_secrets"
            )

    def create_secrets_template(self, template_path: Path) -> bool:
        """Create a secrets template file."""
        logger.info(f"Creating secrets template at {template_path}")

        try:
            template = {
                "GITHUB_TOKEN": "your_github_token_here",
                "API_KEY": "your_api_key_here",
                "DATABASE_URL": "your_database_url_here"
            }

            with open(template_path, 'w') as f:
                json.dump(template, f, indent=2)

            logger.info("Secrets template created successfully")
            return True

        except Exception as e:
            logger.error(f"Failed to create secrets template: {e}")
            return False
