"""
Repository operations and management module.

This module handles:
- Student repository discovery and fetching
- Repository cloning and synchronization
- Template repository management
- Git operations and status tracking
"""

from pathlib import Path
from typing import List, Dict, Optional
import subprocess

from ..utils import get_logger, GitManager, PathManager
from ..config import ConfigLoader

logger = get_logger("repos.fetch")


class RepositoryFetcher:
    """Handles fetching and managing student repositories."""

    def __init__(self, config_path: Path = Path("assignment.conf")):
        """Initialize repository fetcher with configuration."""
        self.config_loader = ConfigLoader(config_path)
        self.config = self.config_loader.load()
        self.git_manager = GitManager()
        self.path_manager = PathManager()

    def discover_repositories(self) -> List[str]:
        """Discover student repositories from GitHub Classroom."""
        logger.info("Discovering student repositories")

        # TODO: Implement GitHub API integration for repository discovery
        logger.warning(
            "Repository discovery not yet implemented - using bash wrapper")
        return []

    def fetch_repositories(self, repo_urls: List[str]) -> Dict[str, bool]:
        """Fetch multiple repositories."""
        logger.info(f"Fetching {len(repo_urls)} repositories")

        results = {}
        for repo_url in repo_urls:
            try:
                success = self.fetch_single_repository(repo_url)
                results[repo_url] = success
            except Exception as e:
                logger.error(f"Failed to fetch {repo_url}: {e}")
                results[repo_url] = False

        return results

    def fetch_single_repository(self, repo_url: str) -> bool:
        """Fetch a single repository."""
        logger.info(f"Fetching repository: {repo_url}")

        try:
            # Extract repository name from URL
            repo_name = repo_url.split("/")[-1].replace(".git", "")
            local_path = self.path_manager.ensure_output_directory(
                "student-repos") / repo_name

            if local_path.exists():
                # Repository exists, pull latest changes
                return self.git_manager.pull_repo()
            else:
                # Clone repository
                return self.git_manager.clone_repo(repo_url, local_path)

        except Exception as e:
            logger.error(f"Error fetching repository {repo_url}: {e}")
            return False

    def sync_template_repository(self) -> bool:
        """Synchronize changes from template repository."""
        logger.info("Synchronizing template repository")

        try:
            template_repo = self.config.get("TEMPLATE_REPO")
            if not template_repo:
                logger.error("No template repository configured")
                return False

            # TODO: Implement template synchronization logic
            logger.warning(
                "Template sync not yet implemented - using bash wrapper")
            return True

        except Exception as e:
            logger.error(f"Template sync failed: {e}")
            return False

    def update_repositories(self) -> Dict[str, bool]:
        """Update all local repositories."""
        logger.info("Updating all repositories")

        results = {}
        repo_dir = self.path_manager.ensure_output_directory("student-repos")

        if not repo_dir.exists():
            logger.warning("No repository directory found")
            return results

        for repo_path in repo_dir.iterdir():
            if repo_path.is_dir() and (repo_path / ".git").exists():
                try:
                    # Create a GitManager instance for this repo directory
                    git_manager = GitManager(repo_path)
                    success = git_manager.pull_repo()
                    results[repo_path.name] = success
                except Exception as e:
                    logger.error(f"Failed to update {repo_path.name}: {e}")
                    results[repo_path.name] = False

        return results
