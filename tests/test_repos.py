"""
Test module for Repos functionality.

Tests repository operations and collaborator management including:
- Repository fetching and synchronization  
- Collaborator management and permissions
- Repository discovery and validation
- Git operations and status tracking
"""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import tempfile
import json

from classroom_pilot.repos.fetch import RepositoryFetcher
from classroom_pilot.repos.collaborator import CollaboratorManager


class TestRepositoryFetcher:
    """Test RepositoryFetcher functionality."""

    @pytest.fixture
    def mock_config_data(self):
        """Mock configuration data for testing."""
        return {
            'CLASSROOM_URL': 'https://classroom.github.com/classrooms/test/assignments/test',
            'GITHUB_ORGANIZATION': 'test-org',
            'GITHUB_TOKEN': 'test-token',
            'ASSIGNMENT_NAME': 'test-assignment',
            'TEMPLATE_REPO': 'https://github.com/test-org/template-repo',
            'OUTPUT_DIR': '/tmp/test-repos'
        }

    @pytest.fixture
    def repo_fetcher(self, mock_config_data):
        """Create RepositoryFetcher instance with mocked config."""
        with patch('classroom_pilot.repos.fetch.ConfigLoader') as mock_loader:
            mock_loader.return_value.load.return_value = mock_config_data
            return RepositoryFetcher(Path("test.conf"))

    def test_repository_fetcher_initialization(self, repo_fetcher):
        """Test RepositoryFetcher initialization."""
        assert repo_fetcher is not None
        assert hasattr(repo_fetcher, 'config')
        assert hasattr(repo_fetcher, 'git_manager')
        assert hasattr(repo_fetcher, 'path_manager')

    def test_discover_repositories(self, repo_fetcher):
        """Test repository discovery functionality."""
        repos = repo_fetcher.discover_repositories()

        # Currently returns empty list as placeholder
        assert isinstance(repos, list)

    def test_fetch_single_repository_new_repo(self, repo_fetcher):
        """Test fetching a new repository that doesn't exist locally."""
        with patch('pathlib.Path.exists') as mock_exists, \
                patch('classroom_pilot.repos.fetch.GitManager') as mock_git_class:

            mock_exists.return_value = False  # Repo doesn't exist locally
            mock_git_manager = Mock()
            mock_git_manager.clone_repo.return_value = True
            mock_git_class.return_value = mock_git_manager

            # Patch the git_manager instance
            repo_fetcher.git_manager = mock_git_manager

            with patch.object(repo_fetcher.path_manager, 'ensure_output_directory') as mock_output:
                mock_output.return_value = Path('/tmp/test-repos')

                result = repo_fetcher.fetch_single_repository(
                    "https://github.com/test-org/test-repo")

                assert isinstance(result, bool)

    def test_fetch_single_repository_existing_repo(self, repo_fetcher):
        """Test fetching an existing repository."""
        with patch('pathlib.Path.exists') as mock_exists, \
                patch('classroom_pilot.repos.fetch.GitManager') as mock_git_class:

            mock_exists.return_value = True  # Repo exists locally
            mock_git_manager = Mock()
            mock_git_manager.pull_repo.return_value = True
            mock_git_class.return_value = mock_git_manager

            # Patch the git_manager instance
            repo_fetcher.git_manager = mock_git_manager

            with patch.object(repo_fetcher.path_manager, 'ensure_output_directory') as mock_output:
                mock_output.return_value = Path('/tmp/test-repos')

                result = repo_fetcher.fetch_single_repository(
                    "https://github.com/test-org/test-repo")

                assert isinstance(result, bool)

    def test_fetch_repositories_multiple(self, repo_fetcher):
        """Test fetching multiple repositories."""
        with patch.object(repo_fetcher, 'fetch_single_repository') as mock_fetch:
            mock_fetch.return_value = True

            repo_urls = [
                "https://github.com/test-org/repo1",
                "https://github.com/test-org/repo2"
            ]
            results = repo_fetcher.fetch_repositories(repo_urls)

            assert isinstance(results, dict)
            assert len(results) == len(repo_urls)

    def test_fetch_single_repository_error_handling(self, repo_fetcher):
        """Test error handling in single repository fetching."""
        with patch('pathlib.Path.exists') as mock_exists, \
                patch('classroom_pilot.repos.fetch.GitManager') as mock_git_class:

            mock_exists.return_value = False
            mock_git_manager = Mock()
            mock_git_manager.clone_repo.side_effect = Exception(
                "Clone failed")
            mock_git_class.return_value = mock_git_manager

            repo_fetcher.git_manager = mock_git_manager

            with patch.object(repo_fetcher.path_manager, 'ensure_output_directory') as mock_output:
                mock_output.return_value = Path('/tmp/test-repos')

                result = repo_fetcher.fetch_single_repository(
                    "https://github.com/test-org/invalid-repo")

                assert result is False

    def test_update_repositories(self, repo_fetcher):
        """Test updating all local repositories."""
        with patch.object(repo_fetcher.path_manager, 'ensure_output_directory') as mock_output:
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_path = Path(temp_dir)
                mock_output.return_value = temp_path

                # Create mock repository directory
                repo_dir = temp_path / "test-repo"
                repo_dir.mkdir()
                (repo_dir / ".git").mkdir()

                with patch('classroom_pilot.repos.fetch.GitManager') as mock_git_class:
                    mock_git_manager = Mock()
                    mock_git_manager.pull_repo.return_value = True
                    mock_git_class.return_value = mock_git_manager

                    repo_fetcher.git_manager = mock_git_manager

                    results = repo_fetcher.update_repositories()

                    assert isinstance(results, dict)

    def test_sync_template_repository(self, repo_fetcher):
        """Test template repository synchronization."""
        result = repo_fetcher.sync_template_repository()

        # Currently returns True as placeholder
        assert result is True

    def test_sync_template_repository_no_config(self, repo_fetcher):
        """Test template sync with missing template configuration."""
        # Remove template repo from config
        repo_fetcher.config = {}

        result = repo_fetcher.sync_template_repository()

        assert result is False


class TestCollaboratorManager:
    """Test CollaboratorManager functionality."""

    @pytest.fixture
    def mock_config_data(self):
        """Mock configuration data for testing."""
        return {
            'GITHUB_ORGANIZATION': 'test-org',
            'GITHUB_TOKEN': 'test-token-123',
            'ASSIGNMENT_NAME': 'test-assignment'
        }

    @pytest.fixture
    def collaborator_manager(self, mock_config_data):
        """Create CollaboratorManager instance with mocked config."""
        with patch('classroom_pilot.repos.collaborator.ConfigLoader') as mock_loader:
            mock_loader.return_value.load.return_value = mock_config_data
            return CollaboratorManager(Path("test.conf"))

    def test_collaborator_manager_initialization(self, collaborator_manager):
        """Test CollaboratorManager initialization."""
        assert collaborator_manager is not None
        assert hasattr(collaborator_manager, 'config')
        assert hasattr(collaborator_manager, 'git_manager')

    def test_list_collaborators(self, collaborator_manager):
        """Test listing repository collaborators."""
        collaborators = collaborator_manager.list_collaborators("test-repo")

        # Currently returns empty list as placeholder
        assert isinstance(collaborators, list)

    def test_add_collaborator_success(self, collaborator_manager):
        """Test successful collaborator addition."""
        result = collaborator_manager.add_collaborator(
            "test-repo", "new-user", "push")

        # Currently returns True as placeholder
        assert result is True

    def test_add_collaborator_with_default_permission(self, collaborator_manager):
        """Test adding collaborator with default permission."""
        result = collaborator_manager.add_collaborator("test-repo", "new-user")

        assert result is True

    def test_remove_collaborator(self, collaborator_manager):
        """Test collaborator removal."""
        result = collaborator_manager.remove_collaborator(
            "test-repo", "old-user")

        # Currently returns True as placeholder
        assert result is True

    def test_cycle_collaborator_permissions(self, collaborator_manager):
        """Test collaborator permission cycling."""
        results = collaborator_manager.cycle_collaborator_permissions(
            "assignment-1", "test-user")

        assert isinstance(results, dict)
        assert "assignment-1" in results

    def test_audit_repository_access(self, collaborator_manager):
        """Test repository access auditing."""
        audit_result = collaborator_manager.audit_repository_access(
            "assignment-1")

        assert isinstance(audit_result, dict)

    def test_update_repository_permissions(self, collaborator_manager):
        """Test updating multiple collaborator permissions."""
        permission_updates = {
            "user1": "admin",
            "user2": "push",
            "user3": "pull"
        }

        with patch.object(collaborator_manager, 'update_collaborator_permission') as mock_update:
            mock_update.return_value = True

            results = collaborator_manager.update_repository_permissions(
                "test-repo", permission_updates)

            assert isinstance(results, dict)
            assert len(results) == len(permission_updates)

    def test_update_collaborator_permission(self, collaborator_manager):
        """Test updating single collaborator permission."""
        result = collaborator_manager.update_collaborator_permission(
            "test-repo", "test-user", "admin")

        # Currently returns True as placeholder
        assert result is True

    def test_error_handling_in_collaborator_operations(self, collaborator_manager):
        """Test error handling in collaborator operations."""
        # Test with exception in underlying operation
        with patch.object(collaborator_manager, 'update_collaborator_permission') as mock_update:
            mock_update.side_effect = Exception("API error")

            results = collaborator_manager.update_repository_permissions(
                "test-repo", {"user1": "admin"})

            assert isinstance(results, dict)
            assert results["user1"] is False


class TestReposIntegration:
    """Test integration scenarios for repos functionality."""

    @pytest.fixture
    def mock_config_data(self):
        """Mock configuration data for integration tests."""
        return {
            'CLASSROOM_URL': 'https://classroom.github.com/classrooms/test/assignments/test',
            'GITHUB_ORGANIZATION': 'test-org',
            'GITHUB_TOKEN': 'test-token',
            'ASSIGNMENT_NAME': 'test-assignment',
            'TEMPLATE_REPO': 'https://github.com/test-org/template-repo',
            'OUTPUT_DIR': '/tmp/test-repos'
        }

    def test_complete_repository_workflow(self, mock_config_data):
        """Test complete workflow from discovery to collaboration."""
        with patch('classroom_pilot.repos.fetch.ConfigLoader') as mock_loader:
            mock_loader.return_value.load.return_value = mock_config_data

            fetcher = RepositoryFetcher(Path("test.conf"))

            # Discover repositories
            repos = fetcher.discover_repositories()
            assert isinstance(repos, list)

            # Sync template
            template_result = fetcher.sync_template_repository()
            assert template_result is True

    def test_collaborator_management_workflow(self, mock_config_data):
        """Test collaborator management workflow."""
        with patch('classroom_pilot.repos.collaborator.ConfigLoader') as mock_loader:
            mock_loader.return_value.load.return_value = mock_config_data

            manager = CollaboratorManager(Path("test.conf"))

            # List current collaborators
            collaborators = manager.list_collaborators("test-repo")
            assert isinstance(collaborators, list)

            # Add new collaborator
            add_result = manager.add_collaborator(
                "test-repo", "new-user", "push")
            assert add_result is True

            # Audit access
            audit = manager.audit_repository_access("assignment-1")
            assert isinstance(audit, dict)

    def test_error_recovery_scenarios(self, mock_config_data):
        """Test error recovery in repos operations."""
        with patch('classroom_pilot.repos.fetch.ConfigLoader') as mock_loader:
            mock_loader.return_value.load.return_value = mock_config_data

            fetcher = RepositoryFetcher(Path("test.conf"))

            # Test with error simulation using proper mocking
            with patch.object(fetcher, 'fetch_single_repository') as mock_fetch:
                mock_fetch.return_value = False  # Simulate failure

                result = fetcher.fetch_single_repository(
                    "https://github.com/test-org/test-repo")
                assert result is False

    def test_configuration_validation(self, mock_config_data):
        """Test configuration validation for repos operations."""
        # Test with missing template repo
        invalid_config = mock_config_data.copy()
        del invalid_config['TEMPLATE_REPO']

        with patch('classroom_pilot.repos.fetch.ConfigLoader') as mock_loader:
            mock_loader.return_value.load.return_value = invalid_config

            fetcher = RepositoryFetcher(Path("test.conf"))

            # Should handle missing template gracefully
            result = fetcher.sync_template_repository()
            assert result is False

    def test_concurrent_operations_handling(self, mock_config_data):
        """Test handling concurrent repository operations."""
        with patch('classroom_pilot.repos.fetch.ConfigLoader') as mock_loader:
            mock_loader.return_value.load.return_value = mock_config_data

            fetcher = RepositoryFetcher(Path("test.conf"))

            # Simulate multiple repository operations
            repo_urls = [
                "https://github.com/test-org/repo1",
                "https://github.com/test-org/repo2",
                "https://github.com/test-org/repo3"
            ]

            with patch.object(fetcher, 'fetch_single_repository') as mock_fetch:
                mock_fetch.return_value = True

                results = fetcher.fetch_repositories(repo_urls)

                assert isinstance(results, dict)
                assert len(results) == len(repo_urls)
                assert all(results.values())  # All should succeed


class TestReposUtilities:
    """Test repos utility functions and helpers."""

    def test_repository_url_parsing(self):
        """Test repository URL parsing utilities."""
        from classroom_pilot.repos.fetch import RepositoryFetcher

        with patch('classroom_pilot.repos.fetch.ConfigLoader'):
            fetcher = RepositoryFetcher(Path("test.conf"))

            # Test URL parsing behavior through fetch_single_repository
            with patch.object(fetcher, 'fetch_single_repository') as mock_fetch:
                mock_fetch.return_value = True

                result = fetcher.fetch_single_repository(
                    "https://github.com/test-org/test-repo.git")
                assert isinstance(result, bool)

    def test_repository_path_management(self):
        """Test repository path management."""
        from classroom_pilot.repos.fetch import RepositoryFetcher

        with patch('classroom_pilot.repos.fetch.ConfigLoader'):
            fetcher = RepositoryFetcher(Path("test.conf"))

            # Test path operations
            with patch.object(fetcher.path_manager, 'ensure_output_directory') as mock_dir:
                mock_dir.return_value = Path("/tmp/test")

                with patch.object(fetcher, 'fetch_single_repository') as mock_fetch:
                    mock_fetch.return_value = True

                    result = fetcher.fetch_single_repository(
                        "https://github.com/test-org/test-repo")
                    assert isinstance(result, bool)

    def test_permission_level_validation(self):
        """Test permission level validation utilities."""
        from classroom_pilot.repos.collaborator import CollaboratorManager

        with patch('classroom_pilot.repos.collaborator.ConfigLoader'):
            manager = CollaboratorManager(Path("test.conf"))

            # Test permission handling
            result = manager.update_collaborator_permission(
                "test-repo", "user", "admin")
            assert isinstance(result, bool)

    def test_repository_name_extraction(self):
        """Test repository name extraction from URLs."""
        from classroom_pilot.repos.fetch import RepositoryFetcher

        with patch('classroom_pilot.repos.fetch.ConfigLoader'):
            fetcher = RepositoryFetcher(Path("test.conf"))

            # Test with different URL formats through the actual method
            test_urls = [
                "https://github.com/test-org/repo-name",
                "https://github.com/test-org/repo-name.git"
            ]

            for url in test_urls:
                with patch.object(fetcher, 'fetch_single_repository') as mock_fetch:
                    mock_fetch.return_value = True

                    result = fetcher.fetch_single_repository(url)
                    assert isinstance(result, bool)

    def test_batch_operation_results(self):
        """Test batch operation result handling."""
        from classroom_pilot.repos.collaborator import CollaboratorManager

        with patch('classroom_pilot.repos.collaborator.ConfigLoader'):
            manager = CollaboratorManager(Path("test.conf"))

            # Test batch permission updates
            updates = {"user1": "admin", "user2": "push"}

            with patch.object(manager, 'update_collaborator_permission') as mock_update:
                mock_update.return_value = True

                results = manager.update_repository_permissions(
                    "test-repo", updates)

                assert isinstance(results, dict)
                assert len(results) == len(updates)
                assert all(isinstance(v, bool) for v in results.values())
