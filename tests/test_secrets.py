"""
Test suite for the secrets management package.
"""

import pytest
from unittest.mock import Mock, patch, mock_open
from pathlib import Path
import json
import tempfile

from classroom_pilot.secrets.manager import SecretsManager


class TestSecretsManager:
    """Test the SecretsManager class."""

    @pytest.fixture
    def secrets_manager(self):
        """Create a SecretsManager instance for testing."""
        with patch('classroom_pilot.secrets.manager.ConfigLoader'):
            return SecretsManager(Path("test.conf"))

    def test_load_secrets_template_success(self, secrets_manager):
        """Test loading secrets template from configuration."""
        mock_secrets = {"GITHUB_TOKEN": "test-token",
                        "API_KEY": "test-api-key"}

        with patch.object(secrets_manager.path_manager, 'find_config_file') as mock_find:
            mock_file = Mock()
            mock_file.exists.return_value = True
            mock_find.return_value = mock_file

            with patch('builtins.open', mock_open(read_data=json.dumps(mock_secrets))):
                with patch('json.load', return_value=mock_secrets):
                    result = secrets_manager.load_secrets_template()
                    assert result == mock_secrets

    def test_validate_token_valid(self, secrets_manager):
        """Test validating a valid GitHub token."""
        valid_token = "ghp_1234567890abcdef1234567890abcdef12345678"
        result = secrets_manager.validate_token(valid_token, "github")
        assert result is True

    def test_validate_token_empty(self, secrets_manager):
        """Test validating an empty token."""
        result = secrets_manager.validate_token("", "github")
        assert result is False

    def test_add_single_secret(self, secrets_manager):
        """Test adding a single secret to a repository."""
        result = secrets_manager.add_single_secret(
            "test-repo", "SECRET_NAME", "secret_value")
        assert result is True

    def test_create_secrets_template(self, secrets_manager):
        """Test creating a secrets template file."""
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            template_path = Path(tmp_file.name)

        try:
            result = secrets_manager.create_secrets_template(template_path)
            assert result is True
            assert template_path.exists()
        finally:
            if template_path.exists():
                template_path.unlink()
